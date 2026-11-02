"""Calendar reconstructed from public contribution records, never anonymous totals."""

import datetime as dt
from collections import Counter
from dataclasses import dataclass

KINDS = ("commits", "issues", "pull_requests", "reviews", "repositories")


@dataclass(frozen=True)
class PublicCalendar:
    start: dt.date
    days: dict
    kinds: dict


def add_public_days(days, nodes, resource=None):
    for node in nodes:
        item = node.get(resource) if resource else node
        if node["isRestricted"] or not item:
            continue
        repository = item["repository"]
        if not repository["isPrivate"]:
            days[node["occurredAt"][:10]] += node.get("commitCount", 1)


def _date_windows(start, end, days):
    while start <= end:
        stop = min(start + dt.timedelta(days=days - 1), end)
        yield start, stop
        start = stop + dt.timedelta(days=1)


def fetch_calendar(graphql, today, start=dt.date(2026, 7, 1)):
    if start > today:
        raise ValueError("Calendar window begins after its end")
    days = Counter()
    kinds = dict.fromkeys(KINDS, 0)
    seen_records = set()

    def add(kind, nodes, resource=None):
        public = []
        for node in nodes:
            item = node.get(resource) if resource else node
            if node["isRestricted"] or not item or item["repository"]["isPrivate"]:
                continue
            if resource:
                record_id = item["id"]
            elif kind == "reviews":
                record_id = node["pullRequestReview"]["id"]
            else:
                record_id = item["repository"]["id"]
            identity = (
                kind,
                record_id,
                node["occurredAt"] if kind == "commits" else "",
            )
            if identity in seen_records:
                raise ValueError("Duplicate public contribution record")
            seen_records.add(identity)
            date = dt.date.fromisoformat(node["occurredAt"][:10])
            count = node["commitCount"] if kind == "commits" else 1
            if not start <= date <= today or type(count) is not int or count < 0:
                raise ValueError("Invalid public contribution date or count")
            public.append(node)
            kinds[kind] += count
        add_public_days(days, public, resource)

    for window, end in _date_windows(start, today, 28):
        query = """query($from:DateTime!, $to:DateTime!) { user(login:"jerome-queck") {
          contributionsCollection(from:$from,to:$to) {
            totalRepositoriesWithContributedCommits
            commitContributionsByRepository(maxRepositories:100) {
              contributions(first:100) { pageInfo { hasNextPage }
                nodes { isRestricted occurredAt commitCount repository { id isPrivate } }
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
            if connection["pageInfo"]["hasNextPage"] is not False:
                raise ValueError("Commit days truncated")
            add("commits", connection["nodes"])
    for kind, connection, resource in [
        ("issues", "issueContributions", "issue"),
        ("pull_requests", "pullRequestContributions", "pullRequest"),
        ("reviews", "pullRequestReviewContributions", None),
        ("repositories", "repositoryContributions", None),
    ]:
        resource_field = (
            f"{resource} {{ id repository {{ id isPrivate }} }}"
            if resource
            else "repository { id isPrivate }"
        )
        if kind == "reviews":
            resource_field += " pullRequestReview { id }"
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
        for window, end in _date_windows(start, today, 365):
            cursor, seen = None, set()
            while True:
                variables = {"from": f"{window}T00:00:00Z", "to": f"{end}T23:59:59Z"}
                if cursor:
                    variables["cursor"] = cursor
                page = graphql(query, **variables)["user"]["contributionsCollection"][
                    connection
                ]
                add(kind, page["nodes"], resource)
                if page["pageInfo"]["hasNextPage"] is False:
                    break
                if page["pageInfo"]["hasNextPage"] is not True:
                    raise ValueError("Incomplete contribution pagination")
                cursor = page["pageInfo"]["endCursor"]
                if not cursor or cursor in seen:
                    raise ValueError("Contribution pagination did not advance")
                seen.add(cursor)
    return PublicCalendar(start, dict(days), kinds)


def weekday_totals(days):
    totals = dict.fromkeys(("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), 0)
    for date, count in days.items():
        totals[dt.date.fromisoformat(date).strftime("%a")] += count
    return totals


def render_calendar(start, today, days, mobile=False, updated=""):
    from scripts.profile_style import BLUE, CITRON, COBALT, INK, RULE, svg, text

    sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    palette = [RULE, CITRON, BLUE, COBALT, INK]
    maximum = max(days.values(), default=1) or 1
    weeks = (today - sunday).days // 7 + 1
    panels = (weeks + 17) // 18 if mobile else 1
    column_pitch = min(42, 790 / max(1, weeks - 1))
    row_pitch = 22 if weeks <= 30 else 17
    cell_size = min(row_pitch - 4, column_pitch - 3)
    legend_y = (
        163 + (panels - 1) * 185 + 170
        if mobile
        else 158 + 6 * row_pitch + cell_size + 35
    )
    frequency_y = legend_y + 98
    width, height = (480, frequency_y + 325) if mobile else (900, frequency_y + 270)
    parts = [
        text("Public records", 28, 59, 46, "display"),
        text(
            f"{(today - start).days + 1} days / {sum(days.values()):,} public records",
            28,
            101,
            26,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    date = start
    while date <= today:
        offset = (date - sunday).days
        week, weekday = offset // 7, offset % 7
        count = days.get(str(date), 0)
        level = min(4, max(1, round(count / maximum * 4))) if count else 0
        if mobile:
            panel, column = divmod(week, 18)
            x, y, size = 78 + column * 20, 163 + panel * 185 + weekday * 19, 15
        else:
            x, y, size = (
                52 + week * column_pitch,
                158 + weekday * row_pitch,
                cell_size,
            )
        parts.append(
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" fill="{palette[level]}"><title>{date}: {count}</title></rect>'
        )
        date += dt.timedelta(days=1)
    for panel in range(panels):
        origin = 163 + panel * 185 if mobile else 158
        for label, day in [("M", 1), ("W", 3), ("F", 5)]:
            parts.append(
                text(
                    label,
                    28,
                    origin + day * (19 if mobile else row_pitch) + 13,
                    20,
                    "mono",
                    BLUE,
                )
            )
        if mobile:
            beginning = max(start, sunday + dt.timedelta(weeks=panel * 18))
            parts.append(
                text(f"{beginning:%d %b %Y}", 78, origin - 18, 22, "mono", BLUE)
            )
        else:
            marker = start
            while marker <= today:
                week = (marker - sunday).days // 7
                parts.append(
                    text(
                        f"{marker:%b}", 52 + week * column_pitch, 138, 20, "mono", BLUE
                    )
                )
                marker = (marker.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    parts.append(text("0 → peak", 28, legend_y + 18, 22, color=BLUE))
    for index, color in enumerate(palette):
        parts.append(
            f'<rect x="{171 + index * 31}" y="{legend_y}" width="23" height="23" fill="{color}"/>'
        )
    parts.append(text("Public records by weekday", 28, frequency_y - 32, 27, "display"))
    totals = weekday_totals(days)
    peak = max(totals.values()) or 1
    for index, (day, count) in enumerate(totals.items()):
        x = 28 + index * (61 if mobile else 121)
        bar = count / peak * (88 if mobile else 83)
        parts += [
            f'<rect x="{x}" y="{frequency_y + 100 - bar:.2f}" width="{39 if mobile else 74}" height="{max(2, bar):.2f}" fill="{COBALT}"/>',
            text(day, x, frequency_y + 135, 19 if mobile else 22, "mono"),
            text(
                str(count),
                x,
                frequency_y + 166,
                20,
                "mono",
                BLUE,
                max_width=56 if mobile else 114,
            ),
        ]
    parts.append(
        text(
            f"{start} to {today}",
            28,
            height - 61,
            21,
            "mono",
            BLUE,
            max_width=width - 56,
        )
    )
    parts.append(text(updated, 28, height - 24, 20, "mono", BLUE, max_width=width - 56))
    return svg(
        width,
        height,
        "".join(parts),
        f"Public contribution records, {start} to {today}; {sum(days.values())} records. Zero to four nonzero levels relative to daily maximum {maximum}. Same records grouped by UTC weekday: {totals}. {updated}",
    )
