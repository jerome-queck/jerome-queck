import datetime as dt
import html
import json
import re
from pathlib import Path
from urllib.parse import urlparse

QUERY = """query($owner:String!, $name:String!, $cursor:String) {
  repository(owner:$owner, name:$name) {
    nameWithOwner url visibility isPrivate isEmpty
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


def _short(value, limit):
    return value if len(value) <= limit else value[: limit - 1] + "…"


def render_pulse(projects: tuple[dict, ...], updated: str, mobile=False) -> str:
    width = 480 if mobile else 900
    has_releases = any(project["release"] for project in projects)
    row_height = (142 if mobile else 96) if has_releases else (92 if mobile else 76)
    height = 200 + len(projects) * row_height
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">',
        '<rect width="100%" height="100%" fill="#101010"/>',
    ]

    def text(x, y, value, size=22, color="#f4f1e9", limit=None, title=None):
        full = html.escape(str(title if title is not None else value))
        display = html.escape(_short(str(value), limit) if limit else str(value))
        length = min(width - x - 28, len(html.unescape(display)) * size * 0.56)
        parts.append(
            f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" textLength="{length:.1f}" lengthAdjust="spacingAndGlyphs"><title>{full}</title>{display}</text>'
        )

    text(28, 48, "SELECTED REPOSITORY PULSE", 26, "#dfff00", 27 if mobile else None)
    text(
        28,
        83,
        "Default-branch commit · any author",
        22,
        limit=36 if mobile else None,
    )
    text(28, 115, updated, 22, "#f4f1e9", 34 if mobile else 75)
    for i, project in enumerate(projects):
        y = 145 + i * row_height
        parts.append(
            f'<path d="M28 {y} H{width - 28}" stroke="#f04416" stroke-width="2"/>'
        )
        text(
            28,
            y + 32,
            f"{i + 1:02d}  {project['name']}",
            24,
            "#dfff00",
            28 if mobile else 30,
        )
        head = project["head"]
        commit = (
            f"{head['committed_at'][:10]} · {project['default_branch']}"
            if head
            else "No default-branch commit"
        )
        release = project["release"]
        release_text = (
            f"{_short(release['tag'], 12)} · {release['published_at'][:10]}"
            + (" · prerelease" if release["prerelease"] else "")
            if release
            else "No published GitHub release"
        )
        if mobile:
            text(28, y + 65, f"Commit: {commit}", 22, limit=35)
            if not has_releases:
                continue
            text(28, y + 98, "Latest published GitHub release:", 22)
            text(
                28,
                y + 128,
                release_text,
                22,
                limit=34,
                title=release["tag"] if release else None,
            )
        else:
            text(350, y + 32, f"Commit: {commit}", 22, limit=43)
            if not has_releases:
                continue
            text(
                350,
                y + 68,
                f"Release: {release_text}",
                22,
                limit=43,
                title=release["tag"] if release else None,
            )
    if not has_releases:
        if mobile:
            text(28, height - 55, "No published GitHub releases", 22)
            text(28, height - 24, "in this selection.", 22)
        else:
            text(28, height - 24, "No published GitHub releases in this selection.", 22)
    parts.append("</svg>")
    return "\n".join(parts)


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
    return "\n".join(lines) + "\n"
