"""Complete public authored PR search outside the two owned namespaces."""

import datetime as dt
import html
import re
from collections import Counter, defaultdict

SEARCH = "is:public is:pr author:jerome-queck -user:jerome-queck -org:Jerome-Group"
DEFINITION = "Public PRs authored by jerome-queck outside repositories owned by jerome-queck or Jerome-Group."
QUERY = """query($search:String!, $cursor:String) {
  search(query:$search, type:ISSUE, first:100, after:$cursor) {
    issueCount pageInfo { hasNextPage endCursor }
    nodes { ... on PullRequest {
      id number title url state createdAt updatedAt closedAt mergedAt
      author { login }
      repository { nameWithOwner isPrivate visibility owner { login } }
    } }
  }
}"""


def _date(value):
    if not isinstance(value, str):
        raise TypeError("Incomplete upstream PR timestamp")
    try:
        instant = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if instant.tzinfo is None:
            raise ValueError
    except ValueError:
        raise ValueError("Incomplete upstream PR timestamp") from None
    return value


def _record(node):
    repo = node.get("repository") if isinstance(node, dict) else None
    if (
        not isinstance(repo, dict)
        or repo.get("isPrivate") is not False
        or repo.get("visibility") != "PUBLIC"
    ):
        raise ValueError("Upstream public repository unavailable")
    owner = repo.get("owner", {}).get("login")
    name = repo.get("nameWithOwner")
    if (
        not isinstance(owner, str)
        or owner.casefold() in {"jerome-queck", "jerome-group"}
        or not isinstance(name, str)
        or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", name)
        or name.split("/")[0].casefold() != owner.casefold()
    ):
        raise ValueError("Upstream search returned an owned or invalid repository")
    if node.get("author", {}).get("login", "").casefold() != "jerome-queck":
        raise ValueError("Upstream PR author mismatch")
    number = node.get("number")
    if (
        type(number) is not int
        or number <= 0
        or node.get("url") != f"https://github.com/{name}/pull/{number}"
        or not isinstance(node.get("id"), str)
        or not node["id"]
        or not isinstance(node.get("title"), str)
    ):
        raise ValueError("Incomplete upstream PR identity")
    state, merged, closed = (
        node.get("state"),
        node.get("mergedAt"),
        node.get("closedAt"),
    )
    if (
        state not in {"OPEN", "CLOSED", "MERGED"}
        or (state == "MERGED") != (merged is not None)
        or (state == "OPEN") != (closed is None)
    ):
        raise ValueError("Inconsistent upstream PR state")
    return {
        "id": node["id"],
        "repo": name,
        "number": number,
        "title": node["title"],
        "url": node["url"],
        "state": state,
        "created_at": _date(node.get("createdAt")),
        "updated_at": _date(node.get("updatedAt")),
        "merged_at": _date(merged) if merged is not None else None,
        "closed_at": _date(closed) if closed is not None else None,
    }


def fetch_upstream(graphql):
    records, seen_ids, seen_cursors = [], set(), set()
    cursor, expected = None, None
    for _ in range(10):
        variables = {"search": SEARCH}
        if cursor is not None:
            variables["cursor"] = cursor
        response = graphql(QUERY, **variables).get("search")
        if (
            not isinstance(response, dict)
            or type(response.get("issueCount")) is not int
            or not 0 <= response["issueCount"] <= 1000
        ):
            raise ValueError(
                "Upstream search exceeds the complete 1000-result bound or is unavailable"
            )
        count = response["issueCount"]
        if expected is None:
            expected = count
        if expected != count:
            raise ValueError("Upstream search count changed during collection")
        nodes, page = response.get("nodes"), response.get("pageInfo")
        if (
            not isinstance(nodes, list)
            or len(nodes) > 100
            or not isinstance(page, dict)
        ):
            raise ValueError("Incomplete upstream pagination")
        for node in nodes:
            record = _record(node)
            if record["id"] in seen_ids:
                raise ValueError("Duplicate upstream PR during pagination")
            seen_ids.add(record["id"])
            records.append(record)
        if len(records) > expected:
            raise ValueError("Upstream search result count mismatch")
        if page.get("hasNextPage") is False:
            if len(records) != expected:
                raise ValueError("Upstream search result count mismatch")
            return sorted(
                records, key=lambda item: (item["repo"].casefold(), item["number"])
            )
        cursor = page.get("endCursor")
        if (
            page.get("hasNextPage") is not True
            or not nodes
            or not isinstance(cursor, str)
            or not cursor
            or cursor in seen_cursors
        ):
            raise ValueError("Upstream pagination did not advance")
        seen_cursors.add(cursor)
    raise ValueError(
        "Upstream search pagination exceeded the complete 1000-result bound"
    )


def upstream_totals(records):
    states = Counter(item["state"] for item in records)
    return states["MERGED"], states["OPEN"], len({item["repo"] for item in records})


def upstream_by_repo(records):
    repos = defaultdict(Counter)
    for item in records:
        repos[item["repo"]][item["state"]] += 1
    return dict(sorted(repos.items(), key=lambda item: item[0].casefold()))


def markdown_upstream(records, observed):
    def label(value):
        return (
            html.escape(value)
            .replace("[", "&#91;")
            .replace("]", "&#93;")
            .replace("\n", " ")
        )

    lines = [
        f"{DEFINITION} Closed without merge is separate from merged. Open means current state, not an outcome. Observed {observed}. Search is complete within GitHub's 1000-result bound; a larger result aborts refresh.",
        "",
    ]
    merged, opened, repos = upstream_totals(records)
    closed = sum(item["state"] == "CLOSED" for item in records)
    lines.extend(
        [
            f"{merged} merged, {opened} open, {closed} closed without merge, across {repos} repositories with PRs in any state.",
            "",
            "| Repository | Merged | Open | Closed without merge |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for repo, states in upstream_by_repo(records).items():
        lines.append(
            f"| [{repo}](https://github.com/{repo}) | {states['MERGED']} | {states['OPEN']} | {states['CLOSED']} |"
        )
    lines.append("")
    for item in records:
        timing = (
            f"merged {item['merged_at']}"
            if item["merged_at"]
            else f"updated {item['updated_at']}"
        )
        lines.append(
            f"- **{item['state']}** · [{item['repo']}#{item['number']}: {label(item['title'])}]({item['url']}) · {timing}"
        )
    return (
        "\n".join(lines) if records else "\n".join(lines) + "No matching upstream PRs."
    )
