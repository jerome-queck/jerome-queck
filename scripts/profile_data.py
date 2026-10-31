import datetime as dt
import html
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from scripts.public_calendar import fetch_calendar, render_calendar
from scripts.recent_activity import fetch_activity, markdown_activity, render_activity
from scripts.repo_pulse import (
    fetch_repo_pulse,
    load_projects,
    markdown_pulse,
    render_pulse,
)


def graphql(query, **variables):
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        command += ["-f", f"{key}={value}"]
    result = json.loads(subprocess.check_output(command, text=True))
    if result.get("errors"):
        raise RuntimeError("GitHub query failed; retaining published data")
    return result["data"]


def resolved_issues(pull_requests):
    resolved = set()
    for pr in pull_requests:
        if pr["repository"]["isPrivate"]:
            continue
        references = pr["closingIssuesReferences"]
        if references["pageInfo"]["hasNextPage"]:
            raise ValueError("Closing issue references truncated")
        for issue in references["nodes"]:
            if (
                not issue["repository"]["isPrivate"]
                and issue["closed"]
                and issue["closedAt"] >= pr["mergedAt"]
            ):
                resolved.add(issue["id"])
    return resolved


def fetch_contributions():
    totals = graphql("""query {
    opened: search(query:"is:public author:jerome-queck is:pr", type:ISSUE) { issueCount }
    merged: search(query:"is:public author:jerome-queck is:pr is:merged", type:ISSUE) { issueCount }
    }""")
    resolved, merged_dates = set(), Counter()
    cursor, seen = None, set()
    while True:
        query = """query($cursor:String) { user(login:"jerome-queck") {
          pullRequests(first:100, after:$cursor, states:MERGED) {
            pageInfo { hasNextPage endCursor }
            nodes { mergedAt repository { isPrivate }
              closingIssuesReferences(first:100) {
                pageInfo { hasNextPage }
                nodes { id closed closedAt repository { isPrivate } }
              }
            }
          }
        }}"""
        page = graphql(query, **({"cursor": cursor} if cursor else {}))["user"][
            "pullRequests"
        ]
        resolved |= resolved_issues(page["nodes"])
        for pr in page["nodes"]:
            if not pr["repository"]["isPrivate"]:
                date = dt.datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))
                merged_dates[str(date.astimezone(dt.timezone.utc).date())] += 1
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
        if not cursor or cursor in seen:
            raise ValueError("Merged PR pagination did not advance")
        seen.add(cursor)
    return {
        "counts": [
            totals["opened"]["issueCount"],
            totals["merged"]["issueCount"],
            len(resolved),
        ],
        "merged_dates": dict(merged_dates),
    }


def merge_months(merged_dates, today):
    last = today.year * 12 + today.month - 1
    months = {
        f"{index // 12:04}-{index % 12 + 1:02}": 0
        for index in range(last - 11, last + 1)
    }
    for date, count in merged_dates.items():
        if date[:7] in months and dt.date.fromisoformat(date) <= today:
            months[date[:7]] += count
    return months


def render_counters(counts, updated, mobile=False):
    labels = ["PRs opened", "PRs merged", "Linked issues resolved"]
    width, height = (480, 380) if mobile else (900, 240)
    body = []
    for index, (count, label) in enumerate(zip(counts, labels)):
        x, y = (28, 105 + index * 83) if mobile else (30 + index * 300, 119)
        if mobile:
            body.append(
                f'<text x="452" y="{y}" text-anchor="end" fill="#dfff00" font-size="43" font-weight="900">{count:,}</text>'
            )
            body.append(
                f'<text x="{x}" y="{y}" fill="#f4f1e9" font-size="23">{label}</text>'
            )
            body.append(f'<path d="M28 {y + 23}H452" stroke="#484848"/>')
        else:
            body.append(
                f'<text x="{x}" y="{y}" fill="#dfff00" font-size="64" font-weight="900">{count:,}</text>'
            )
            body.append(
                f'<text x="{x}" y="{y + 42}" fill="#f4f1e9" font-size="23">{label}</text>'
            )
            if index:
                body.append(f'<path d="M{x - 20} 68V171" stroke="#484848"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <title>All-time authored public contributions: {counts[0]} PRs opened, {counts[1]} merged, {counts[2]} distinct linked issues resolved</title>
    <rect width="{width}" height="{height}" fill="#101010"/>
    <path d="M0 0H{width}" stroke="#f04416" stroke-width="10"/>
    <g font-family="Arial,sans-serif">
    <text x="28" y="40" fill="#f04416" font-size="23" font-weight="700">PUBLIC WORK / ALL TIME</text>
    {"".join(body)}
    <text x="28" y="{height - 20}" fill="#c7c3bb" font-size="21">{html.escape(updated)}</text>
    </g></svg>'''


def render_cadence(months, updated, mobile=False):
    width, height = (480, 780) if mobile else (900, 380)
    maximum = max(months.values(), default=0) or 1
    parts = []
    for index, (month, count) in enumerate(months.items()):
        if mobile:
            y = 124 + index * 48
            parts.extend(
                [
                    f'<text x="28" y="{y}" font-size="23">{month}</text>',
                    f'<rect x="151" y="{y - 20}" width="{max(2, count / maximum * 220):.1f}" height="24" fill="#f04416"/>',
                    f'<text x="452" y="{y}" text-anchor="end" font-size="23">{count}</text>',
                ]
            )
        else:
            x = 40 + index * 72
            bar = count / maximum * 158
            parts.extend(
                [
                    f'<rect x="{x}" y="{260 - bar:.1f}" width="43" height="{max(2, bar):.1f}" fill="#f04416"/>',
                    f'<text x="{x + 21}" y="{248 - bar:.1f}" text-anchor="middle" font-size="23">{count}</text>',
                    f'<text x="{x + 21}" y="289" text-anchor="middle" font-size="20">{month[5:]}</text>',
                ]
            )
    last = next(reversed(months))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <title>Authored public PRs merged by UTC calendar month. {html.escape(str(months))}</title>
    <rect width="{width}" height="{height}" fill="#f4f1e9"/>
    <g font-family="Arial,sans-serif" fill="#101010">
    <text x="28" y="40" font-size="25" font-weight="900">MERGE CADENCE</text>
    <text x="28" y="76" font-size="21">Authored public PRs / {sum(months.values()):,} merged</text>
    {"".join(parts)}
    <text x="28" y="{height - 58}" font-size="21">{next(iter(months))} to {last} / last month partial</text>
    <text x="28" y="{height - 24}" font-size="21">{html.escape(updated)}</text>
    </g></svg>'''


def collect_snapshot():
    started = dt.datetime.now(dt.timezone.utc)
    today = started.date()
    contributions = fetch_contributions()
    start, days = fetch_calendar(graphql, today)
    activity = fetch_activity()
    catalogue = load_projects(Path(__file__).parents[1] / "data/projects.json")
    projects = [fetch_repo_pulse(graphql, project) for project in catalogue]
    completed = dt.datetime.now(dt.timezone.utc)
    return {
        "schema_version": 1,
        "observed_from": started.isoformat(),
        "observed_to": completed.isoformat(),
        "updated": completed.strftime("%d %b %Y %H:%M UTC"),
        "counts": contributions["counts"],
        "calendar_start": str(start),
        "calendar_end": str(today),
        "calendar_days": dict(days),
        "merge_months": merge_months(contributions["merged_dates"], today),
        "projects": projects,
        "recent_events": activity,
    }


def render_snapshot(snapshot):
    counts, updated = snapshot["counts"], snapshot["updated"]
    start = dt.date.fromisoformat(snapshot["calendar_start"])
    today = dt.date.fromisoformat(snapshot["calendar_end"])
    days, months = snapshot["calendar_days"], snapshot["merge_months"]
    files = {
        "snapshot.json": json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        "activity.svg": render_activity(snapshot["recent_events"]),
    }
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        files[f"counters{suffix}.svg"] = render_counters(counts, updated, mobile)
        files[f"calendar{suffix}.svg"] = render_calendar(
            start, today, days, mobile, updated
        )
        files[f"cadence{suffix}.svg"] = render_cadence(months, updated, mobile)
        files[f"pulse{suffix}.svg"] = render_pulse(
            snapshot["projects"], updated, mobile
        )
    files["README.md"] = (
        f"# Public work snapshot\n\nCollected {updated}.\n\n"
        f"Observation interval: {snapshot['observed_from']} to {snapshot['observed_to']}. "
        "GitHub queries are separate observations, not a transaction at one instant. "
        "[Reproducible public input](snapshot.json).\n\n"
        f"- Authored public PRs opened, all time: {counts[0]}\n"
        f"- Authored public PRs merged, all time: {counts[1]}\n"
        f"- Distinct currently closed public issues linked to those merged PRs: {counts[2]}\n\n"
        "Linked issues must close at or after the PR merge. This measures linked resolution, "
        "not who clicked Close or proof that a PR alone caused closure; GitHub can change links retrospectively.\n\n"
        f"## Merge cadence\n\nAuthored public PRs merged by UTC calendar month, {next(iter(months))} "
        f"through {next(reversed(months))}. Current month is partial through {today}. "
        "Across all public repositories, not just the selected projects.\n\n"
        + "\n".join(f"- {month}: {count}" for month, count in months.items())
        + "\n\n## Selected repository pulse\n\n"
        "Nine authored selections. Default-branch tip commit and its Git committer date, by any author. "
        "Latest published GitHub release includes prereleases, explicitly labelled. "
        "Commits and releases do not establish deployment status or Jerome's personal contribution. "
        "No published release is a valid empty state, not a failed request.\n\n"
        + markdown_pulse(snapshot["projects"])
        + f"\n\n## Public contribution calendar\n\n{start} through {today}, reconstructed from public "
        "commit, issue, PR, review and repository contribution records. Count is records, not hours or quality. "
        "Cell levels are zero, then four nonzero levels relative to the largest daily count in this window. "
        "This is not a promise of parity with GitHub's native graph.\n\n"
        + "\n".join(f"- {date}: {count}" for date, count in sorted(days.items()))
        + "\n\n## Recent issue and PR events\n\n"
        + markdown_activity(snapshot["recent_events"])
        + "\n\nThe profile shows two matching issue/PR events sampled from the latest 300 public GitHub events. "
        "GitHub retains at most 30 days of public events. This is not a complete history. "
        "Aggregate counts and the calendar include all public projects. Featured exclusions apply to selected projects and the feed. "
        "Every source must succeed before publication. Failed refreshes retain the previous published snapshot and timestamp. "
        "Scheduled runs can be delayed or disabled by GitHub. One Git commit publishes the payload; CDN caches can refresh separately.\n\n"
        "[Browse authored public PRs](https://github.com/pulls?q=is%3Apr+author%3Ajerome-queck+is%3Apublic).\n"
    )
    return files


def main():
    files = render_snapshot(collect_snapshot())
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        (output / name).write_text(content)


if __name__ == "__main__":
    main()
