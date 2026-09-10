"""Calendar reconstructed from public contribution records, never anonymous totals."""

import datetime as dt
from collections import Counter


def add_public_days(days, nodes, resource=None):
    for node in nodes:
        item = node.get(resource) if resource else node
        if node["isRestricted"] or not item:
            continue
        repository = item["repository"]
        if not repository["isPrivate"]:
            days[node["occurredAt"][:10]] += node.get("commitCount", 1)


def fetch_calendar(graphql, today):
    start = today - dt.timedelta(days=364)
    days = Counter()
    window = start
    while window <= today:
        end = min(window + dt.timedelta(days=27), today)
        query = """query($from:DateTime!, $to:DateTime!) { user(login:"jerome-queck") {
          contributionsCollection(from:$from,to:$to) {
            totalRepositoriesWithContributedCommits
            commitContributionsByRepository(maxRepositories:100) {
              contributions(first:100) { pageInfo { hasNextPage }
                nodes { isRestricted occurredAt commitCount repository { isPrivate } }
              }
            }
          }
        }}"""
        collection = graphql(
            query, **{"from": f"{window}T00:00:00Z", "to": f"{end}T23:59:59Z"}
        )["user"]["contributionsCollection"]
        if collection["totalRepositoriesWithContributedCommits"] > 100:
            raise ValueError("Commit repositories truncated")
        for repo in collection["commitContributionsByRepository"]:
            connection = repo["contributions"]
            if connection["pageInfo"]["hasNextPage"]:
                raise ValueError("Commit days truncated")
            add_public_days(days, connection["nodes"])
        window = end + dt.timedelta(days=1)
    for connection, resource in [
        ("issueContributions", "issue"),
        ("pullRequestContributions", "pullRequest"),
        ("pullRequestReviewContributions", None),
        ("repositoryContributions", None),
    ]:
        cursor = None
        resource_field = (
            f"{resource} {{ repository {{ isPrivate }} }}"
            if resource
            else "repository { isPrivate }"
        )
        arguments = (
            ", excludeFirst:false, excludePopular:false"
            if connection in ("issueContributions", "pullRequestContributions")
            else ""
        )
        query = f"""query($from:DateTime!, $to:DateTime!, $cursor:String) {{ user(login:"jerome-queck") {{
          contributionsCollection(from:$from,to:$to) {{
            {connection}(first:100,after:$cursor{arguments}) {{
              pageInfo {{ hasNextPage endCursor }}
              nodes {{ isRestricted occurredAt {resource_field} }}
            }}
          }}
        }} }}"""
        while True:
            variables = {"from": f"{start}T00:00:00Z", "to": f"{today}T23:59:59Z"}
            if cursor:
                variables["cursor"] = cursor
            page = graphql(query, **variables)["user"]["contributionsCollection"][
                connection
            ]
            add_public_days(days, page["nodes"], resource)
            if not page["pageInfo"]["hasNextPage"]:
                break
            cursor = page["pageInfo"]["endCursor"]
    return start, days


def render_calendar(start, today, days):
    sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    palette = ["#202c40", "#255e63", "#268e88", "#2cc5ae", "#8af0cc"]
    maximum = max(days.values(), default=1) or 1
    squares = []
    date = start
    while date <= today:
        offset = (date - sunday).days
        count = days.get(str(date), 0)
        level = min(4, max(1, round(count / maximum * 4))) if count else 0
        squares.append(
            f'<rect x="{28 + offset // 7 * 14}" y="{65 + offset % 7 * 14}" width="11" height="11" rx="2" fill="{palette[level]}"><title>{date}: {count}</title></rect>'
        )
        date += dt.timedelta(days=1)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="205" viewBox="0 0 820 205" role="img">
    <title>Public contribution calendar, {start} to {today}</title>
    <rect width="820" height="205" rx="18" fill="#0d1422"/>
    <g font-family="Segoe UI,Arial,sans-serif" fill="#dbe4f0">
    <text x="28" y="38" font-size="18">A year of public contributions</text>
    <text x="790" y="38" font-size="13" text-anchor="end">{sum(days.values()):,} contributions</text>
    {"".join(squares)}
    <text x="28" y="187" font-size="12" fill="#94a3b8">{start} → {today} · Public commits, issues, PRs, reviews and repositories</text>
    </g></svg>"""
