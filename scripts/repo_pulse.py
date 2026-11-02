import datetime as dt
import json
import re
from pathlib import Path
from urllib.parse import urlparse

QUERY = """query($owner:String!, $name:String!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    nameWithOwner url visibility isPrivate isEmpty
    languages(first:100, orderBy:{field:SIZE, direction:DESC}) { totalSize totalCount edges { size node { name } } pageInfo { hasNextPage } }
    defaultBranchRef { name target { __typename ... on Commit { oid committedDate url } } }
    releases(first:100, after:$cursor) {
      nodes { isDraft isPrerelease publishedAt tagName url }
      pageInfo { hasNextPage endCursor }
    }
  }
}"""


def load_projects(path: Path) -> tuple[dict, ...]:
    projects = json.loads(path.read_text())
    if not isinstance(projects, list) or len(projects) != 9:
        raise ValueError("Expected nine selected projects")
    seen = set()
    for project in projects:
        if not isinstance(project, dict) or set(project) != {
            "repo",
            "name",
            "group",
            "url",
            "summary",
        }:
            raise ValueError("Invalid selected project")
        if not all(
            isinstance(value, str) and value.strip() for value in project.values()
        ):
            raise ValueError("Invalid selected project")
        repo = project["repo"]
        if not re.fullmatch(
            r"(?:Jerome-Group|jerome-queck)/[A-Za-z0-9_.-]+", repo, re.IGNORECASE
        ):
            raise ValueError("Invalid selected repository")
        key = repo.casefold()
        if key in seen or repo.split("/")[1].casefold() in {
            "clarifold",
            "doomsday-protocol",
        }:
            raise ValueError("Duplicate or excluded repository")
        if (
            project["group"] not in {"mathematics", "software"}
            or urlparse(project["url"]).scheme != "https"
            or not urlparse(project["url"]).netloc
        ):
            raise ValueError("Invalid selected project")
        seen.add(key)
    return tuple(projects)


def _date(value):
    if not isinstance(value, str):
        raise TypeError("Invalid GitHub date")
    try:
        parsed = dt.datetime.fromisoformat(value)
        if parsed.tzinfo is None:
            raise ValueError
        return parsed
    except ValueError:
        raise ValueError("Invalid GitHub date") from None


def _required_text(value):
    if not isinstance(value, str) or not value:
        raise ValueError("Incomplete public repository data")
    return value


def fetch_repo_pulse(graphql, project: dict) -> dict:
    owner, name = project["repo"].split("/")
    cursor = None
    seen = set()
    selected = None
    identity = None
    head = None
    branch_name = None
    for _ in range(1000):
        variables = {"owner": owner, "name": name}
        if cursor is not None:
            variables["cursor"] = cursor
        response = graphql(QUERY, **variables)
        repo = response.get("repository") if isinstance(response, dict) else None
        if (
            not isinstance(repo, dict)
            or repo.get("visibility") != "PUBLIC"
            or repo.get("isPrivate") is not False
            or not isinstance(repo.get("nameWithOwner"), str)
            or repo["nameWithOwner"].casefold() != project["repo"].casefold()
        ):
            raise ValueError("Selected public repository unavailable")
        current_url = _required_text(repo.get("url"))
        if identity is None:
            languages = language_bytes(repo.get("languages"))
            identity = current_url
            branch = repo.get("defaultBranchRef")
            if branch is None:
                if repo.get("isEmpty") is not True:
                    raise ValueError("Incomplete public repository data")
            else:
                if not isinstance(branch, dict) or repo.get("isEmpty") is not False:
                    raise ValueError("Incomplete public repository data")
                branch_name = _required_text(branch.get("name"))
                target = branch.get("target")
                if not isinstance(target, dict) or target.get("__typename") != "Commit":
                    raise ValueError("Incomplete public repository data")
                committed = _required_text(target.get("committedDate"))
                _date(committed)
                head = {
                    "oid": _required_text(target.get("oid")),
                    "committed_at": committed,
                    "url": _required_text(target.get("url")),
                }
        elif current_url != identity:
            raise ValueError("Selected public repository changed during collection")
        releases = repo.get("releases")
        if (
            not isinstance(releases, dict)
            or not isinstance(releases.get("nodes"), list)
            or not isinstance(releases.get("pageInfo"), dict)
        ):
            raise TypeError("Incomplete public repository data")
        for release in releases["nodes"]:
            if (
                not isinstance(release, dict)
                or not isinstance(release.get("isDraft"), bool)
                or not isinstance(release.get("isPrerelease"), bool)
            ):
                raise TypeError("Incomplete public repository data")
            if release["isDraft"] or release.get("publishedAt") is None:
                continue
            published = _required_text(release["publishedAt"])
            instant = _date(published)
            record = {
                "tag": _required_text(release.get("tagName")),
                "published_at": published,
                "url": _required_text(release.get("url")),
                "prerelease": release["isPrerelease"],
            }
            if selected is None or (instant, record["url"]) > (
                selected[0],
                selected[1]["url"],
            ):
                selected = (instant, record)
        page = releases["pageInfo"]
        if page.get("hasNextPage") is False:
            return {
                **project,
                "repository_url": identity,
                "default_branch": branch_name,
                "head": head,
                "release": selected[1] if selected else None,
                "language_bytes": languages,
            }
        next_cursor = page.get("endCursor")
        if (
            page.get("hasNextPage") is not True
            or not isinstance(next_cursor, str)
            or not next_cursor
            or next_cursor in seen
        ):
            raise ValueError("Incomplete release pagination")
        seen.add(next_cursor)
        cursor = next_cursor
    raise ValueError("Incomplete release pagination")


def language_bytes(connection):
    if (
        not isinstance(connection, dict)
        or connection.get("pageInfo", {}).get("hasNextPage") is not False
        or not isinstance(connection.get("edges"), list)
    ):
        raise ValueError("Incomplete selected repository languages")
    result = {}
    for edge in connection["edges"]:
        name, size = edge.get("node", {}).get("name"), edge.get("size")
        if (
            not isinstance(name, str)
            or not name
            or type(size) is not int
            or size < 0
            or name in result
        ):
            raise ValueError("Invalid selected repository language bytes")
        result[name] = size
    if (
        type(connection.get("totalSize")) is not int
        or type(connection.get("totalCount")) is not int
        or connection["totalSize"] != sum(result.values())
        or connection["totalCount"] != len(result)
    ):
        raise ValueError("Incomplete selected repository language totals")
    return dict(sorted(result.items(), key=lambda item: (-item[1], item[0])))


def render_pulse(projects, updated, mobile=False):
    from scripts.profile_style import BLUE, CITRON, COBALT, INK, RULE, rule, svg, text

    width = 480 if mobile else 900
    has_releases = any(project["release"] for project in projects)
    row_height = (160 if has_releases else 117) if mobile else 112
    totals = {}
    for project in projects:
        for name, size in project["language_bytes"].items():
            totals[name] = totals.get(name, 0) + size
    languages = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    chart = languages[:4]
    if len(languages) > 4:
        chart.append(("Other", sum(size for _, size in languages[4:])))
    height = (
        475
        + len(projects) * row_height
        + (len(chart) * 42 if mobile else ((len(chart) + 1) // 2) * 40)
    )
    parts = [
        text("REPOSITORY NOTEBOOK", 28, 47, 32, "display"),
        text("Default-branch tips / any author", 28, 87, 25, color=BLUE),
        text(updated, 28, 124, 20, "mono", BLUE),
    ]
    for index, project in enumerate(projects):
        y = 163 + index * row_height
        parts += [
            rule(28, y, width - 28, y),
            text(f"{index + 1:02d}", 28, y + 41, 20, "mono", COBALT),
            text(project["name"], 79, y + 43, 35, "display", max_width=width - 107),
        ]
        head, release = project["head"], project["release"]
        commit = (
            f"{head['committed_at'][:10]} / {head['oid'][:7]}"
            if head
            else "No default-branch commit"
        )
        parts.append(text(commit, 79, y + 82, 23, "mono", BLUE, max_width=width - 107))
        if release:
            release_text = (
                "Prerelease " if release["prerelease"] else "Release "
            ) + release["published_at"][:10]
            parts.append(
                text(
                    release_text,
                    79 if mobile else 514,
                    y + 120 if mobile else y + 82,
                    24,
                    max_width=width - 107 if mobile else 358,
                )
            )
    y = 195 + len(projects) * row_height
    if not has_releases:
        parts.append(
            text(
                "No published releases in this selection.",
                28,
                y,
                24,
                color=BLUE,
                max_width=width - 56,
            )
        )
    parts.append(
        text(
            "Source links + release records in snapshot.",
            28,
            y + 36,
            23,
            color=BLUE,
            max_width=width - 56,
        )
    )
    y += 105
    parts += [
        text("GitHub language bytes", 28, y, 34, "display", max_width=width - 56),
        text("Nine selected repos / not expertise", 28, y + 40, 24, color=BLUE),
    ]
    colors = [COBALT, BLUE, INK, CITRON, RULE]
    total = sum(totals.values())
    x = 28
    for index, (name, size) in enumerate(chart):
        bar = size / total * (width - 56) if total else 0
        color = colors[index]
        parts.append(
            f'<rect x="{x:.3f}" y="{y + 63}" width="{bar:.3f}" height="24" fill="{color}" stroke="{INK}" stroke-width="0.5"><title>{name}: {size} bytes</title></rect>'
        )
        x += bar
        column, row = (0, index) if mobile else (index % 2, index // 2)
        label_x, label_y = 28 + column * 430, y + 126 + row * 42
        parts.append(
            f'<rect x="{label_x}" y="{label_y - 20}" width="18" height="18" fill="{color}" stroke="{INK}" stroke-width="0.5"/>'
        )
        parts.append(
            text(
                f"{name}: {size:,} / {size / total:.1%}" if total else f"{name}: 0",
                label_x + 30,
                label_y,
                23,
                max_width=394 if mobile else 390,
            )
        )
    if not languages:
        parts.append(
            text(
                "No language bytes in this selection.",
                28,
                y + 118,
                24,
                max_width=width - 56,
            )
        )
    return svg(
        width,
        height,
        "".join(parts),
        "Selected repository pulse. Default-branch tips by any author and latest published release dates. Exact tags and source links in native snapshot. GitHub language bytes aggregate nine selected repositories, not expertise. Top four languages plus Other, with exact full bytes in native snapshot.",
    )


def markdown_pulse(projects: tuple[dict, ...]) -> str:
    def escape(value):
        return re.sub(r"([\\`*_{}\[\]<>|])", r"\\\1", str(value)).replace("\n", " ")

    lines = []
    for project in projects:
        head, release = project["head"], project["release"]
        lines.append(
            f"- **{escape(project['name'])}** ([repository]({project['repository_url']}))"
        )
        lines.append(
            f"  - Default-branch tip commit: [{escape(project['default_branch'])} · {escape(head['committed_at'])}]({head['url']})"
            if head
            else "  - No default-branch commit"
        )
        lines.append(
            f"  - Latest published GitHub release: [{escape(release['tag'])}]({release['url']}) · {escape(release['published_at'])}"
            + (" · prerelease" if release["prerelease"] else "")
            if release
            else "  - No published GitHub release"
        )
        languages = project["language_bytes"]
        lines.append(
            "  - GitHub language bytes: "
            + (
                ", ".join(
                    f"{escape(name)} {size:,}" for name, size in languages.items()
                )
                or "none"
            )
        )
    return "\n".join(lines) + "\n"
