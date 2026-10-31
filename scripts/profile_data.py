"""Public contribution counters; fail closed before publishing generated assets."""

import datetime as dt
import html
import json
import subprocess
import sys
from pathlib import Path

from scripts.public_calendar import fetch_calendar, render_calendar
from scripts.recent_activity import fetch_activity, markdown_activity, render_activity


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


def fetch_counters():
    data = graphql("""query {
    opened: search(query:"is:public author:jerome-queck is:pr", type:ISSUE) { issueCount }
    merged: search(query:"is:public author:jerome-queck is:pr is:merged", type:ISSUE) { issueCount }
    }""")
    resolved = set()
    cursor = None
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
        if not page["pageInfo"]["hasNextPage"]:
            break
        cursor = page["pageInfo"]["endCursor"]
    return data["opened"]["issueCount"], data["merged"]["issueCount"], len(resolved)


def render_counters(counts, updated, mobile=False):
    labels = ["PRs opened", "PRs merged", "Linked issues resolved"]
    width, height = (480, 306) if mobile else (900, 200)
    body = []
    for index, (count, label) in enumerate(zip(counts, labels)):
        x, y = (28, 83 + index * 66) if mobile else (30 + index * 300, 104)
        if mobile:
            body.append(
                f'<text x="{width - 28}" y="{y}" text-anchor="end" fill="#b73524" font-size="37">{count:,}</text>'
            )
            body.append(
                f'<text x="{x}" y="{y}" fill="#1b1b18" font-size="23">{label}</text>'
            )
            body.append(f'<path d="M28 {y + 20}H{width - 28}" stroke="#d8ccbc"/>')
        else:
            body.append(
                f'<text x="{x}" y="{y}" fill="#b73524" font-size="58" font-family="Georgia,serif">{count:,}</text>'
            )
            body.append(
                f'<text x="{x}" y="{y + 36}" fill="#1b1b18" font-size="23">{label}</text>'
            )
            if index:
                body.append(f'<path d="M{x - 20} 60V146" stroke="#d8ccbc"/>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img">
    <title>All-time authored public contributions: {counts[0]} PRs opened, {counts[1]} merged, {counts[2]} distinct linked issues resolved</title>
    <rect width="{width}" height="{height}" fill="#f6f1e9"/>
    <g font-family="Segoe UI,Arial,sans-serif">
    <text x="28" y="32" fill="#6b6256" font-size="19">PUBLIC WORK · ALL TIME</text>
    {"".join(body)}
    <text x="28" y="{height - 18}" fill="#6b6256" font-size="19">Updated {html.escape(updated)}</text>
    </g></svg>'''


def main():
    counts = fetch_counters()
    today = dt.datetime.now(dt.timezone.utc).date()
    start, days = fetch_calendar(graphql, today)
    activity = fetch_activity()
    updated = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y %H:%M UTC")
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=True)
    (output / "activity.svg").write_text(render_activity(activity))
    (output / "calendar.svg").write_text(render_calendar(start, today, days))
    (output / "counters.svg").write_text(render_counters(counts, updated))
    (output / "counters-mobile.svg").write_text(
        render_counters(counts, updated, mobile=True)
    )
    (output / "README.md").write_text(
        f"# Public contribution snapshot\n\nUpdated {updated}.\n\n"
        f"- Authored PRs opened, all time: {counts[0]}\n"
        f"- Authored PRs merged, all time: {counts[1]}\n"
        f"- Distinct closed issues linked to those merged PRs: {counts[2]}\n\n"
        "Linked issues must close at or after the PR merge. This measures linked resolution, "
        "not who clicked Close; GitHub can change links retrospectively.\n\n"
        "Calendar: last 365 days, reconstructed from public contribution records. Recent activity: public issue and PR events among the "
        "latest 300 GitHub events; this is a bounded feed, not a complete history.\n\n"
        "The profile shows two recent events. Aggregate public counts and the calendar include all public projects. "
        "Failed refreshes retain the previous published data and timestamp. Scheduled runs may be delayed or disabled by GitHub.\n\n"
        "[Browse PRs](https://github.com/pulls?q=is%3Apr+author%3Ajerome-queck+is%3Apublic) · "
        "[Browse issues](https://github.com/issues?q=is%3Aissue+author%3Ajerome-queck+is%3Apublic)\n"
    )
    with (output / "README.md").open("a") as summary:
        summary.write(
            "\n## Recent issue and PR events\n\n" + markdown_activity(activity) + "\n"
        )


if __name__ == "__main__":
    main()
