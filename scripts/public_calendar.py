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
        cursor, seen = None, set()
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
            if not cursor or cursor in seen:
                raise ValueError("Contribution pagination did not advance")
            seen.add(cursor)
    return start, days


def render_calendar(start, today, days, mobile=False, updated=""):
    sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    palette = ["#303030", "#81452b", "#b34e23", "#f04416", "#dfff00"]
    maximum = max(days.values(), default=1) or 1
    width, height = (480, 790) if mobile else (900, 350)
    squares = []
    date = start
    while date <= today:
        offset = (date - sunday).days
        week, weekday = offset // 7, offset % 7
        count = days.get(str(date), 0)
        level = min(4, max(1, round(count / maximum * 4))) if count else 0
        if mobile:
            panel, column = divmod(week, 18)
            x, y, size = 78 + column * 20, 140 + panel * 185 + weekday * 19, 15
        else:
            x, y, size = 52 + week * 15, 120 + weekday * 17, 12
        squares.append(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{palette[level]}"><title>{date}: {count}</title></rect>'
        )
        date += dt.timedelta(days=1)
    labels = []
    for panel in range(3 if mobile else 1):
        origin = 140 + panel * 185 if mobile else 120
        for label, day in [("M", 1), ("W", 3), ("F", 5)]:
            labels.append(
                f'<text x="28" y="{origin + day * (19 if mobile else 17) + 13}" font-size="21">{label}</text>'
            )
        if mobile:
            beginning = max(start, sunday + dt.timedelta(weeks=panel * 18))
            labels.append(
                f'<text x="78" y="{origin - 18}" font-size="22">{beginning:%d %b %Y}</text>'
            )
        else:
            for week in range(0, 53, 8):
                marker = sunday + dt.timedelta(weeks=week)
                labels.append(
                    f'<text x="{52 + week * 15}" y="102" font-size="21">{marker:%b %y}</text>'
                )
    legend_y = height - 92
    legend = "".join(
        f'<rect x="{167 + n * 31}" y="{legend_y - 18}" width="23" height="23" fill="{color}"/>'
        for n, color in enumerate(palette)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <title>Public contribution records, {start} to {today}; {sum(days.values())} records. Zero to four nonzero levels relative to daily maximum {maximum}.</title>
    <rect width="{width}" height="{height}" fill="#101010"/>
    <g font-family="Arial,sans-serif" fill="#f4f1e9">
    <text x="28" y="40" font-size="25" font-weight="900">PUBLIC CONTRIBUTION RHYTHM</text>
    <text x="28" y="76" font-size="22">365 days / {sum(days.values()):,} records</text>
    {"".join(labels)}{"".join(squares)}
    <text x="28" y="{legend_y}" font-size="21">0 → peak</text>{legend}
    <text x="28" y="{height - 56}" font-size="20">{start} to {today}</text>
    <text x="28" y="{height - 23}" fill="#c7c3bb" font-size="20">{updated}</text>
    </g></svg>"""
