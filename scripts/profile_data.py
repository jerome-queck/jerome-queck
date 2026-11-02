import datetime as dt
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

from scripts.profile_style import BLUE, COBALT, rule, svg, text
from scripts.public_calendar import fetch_calendar, render_calendar, weekday_totals
from scripts.recent_activity import fetch_activity, markdown_activity, render_activity
from scripts.repo_pulse import (
    fetch_repo_pulse,
    load_projects,
    markdown_pulse,
    render_pulse,
)
from scripts.upstream_prs import (
    fetch_upstream,
    markdown_upstream,
    upstream_by_repo,
    upstream_totals,
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
    start = dt.date(2026, 7, 1)
    if today < start:
        raise ValueError("Graph window begins 1 July 2026")
    last = today.year * 12 + today.month - 1
    months = {
        f"{index // 12:04}-{index % 12 + 1:02}": 0
        for index in range(start.year * 12 + start.month - 1, last + 1)
    }
    for date, count in merged_dates.items():
        if date[:7] in months and dt.date.fromisoformat(date) <= today:
            months[date[:7]] += count
    return months


def render_counters(counts, updated, mobile=False, upstream=()):
    width, height = (480, 795) if mobile else (900, 500)
    labels = ["PRs opened", "PRs merged", "Linked closed issues"]
    parts = [
        text("Public work", 28, 65, 51, "display"),
        text("AUTHORED PUBLIC PRS / ALL TIME", 28, 108, 20, "mono", BLUE),
    ]
    for index, (count, label) in enumerate(zip(counts, labels)):
        x, y = (28, 191 + index * 111) if mobile else (28 + index * 296, 219)
        parts.append(text(f"{count:,}", x, y, 78, "display", COBALT, max_width=265))
        parts.append(text(label, x, y + 38, 27, max_width=424 if mobile else 270))
    y = 565 if mobile else 324
    parts += [
        rule(28, y - 39, width - 28, y - 39, COBALT, 2),
        text("OPEN-SOURCE CONTRIBUTIONS", 28, y, 19, "mono", BLUE),
    ]
    for index, (count, label) in enumerate(
        zip(
            upstream_totals(upstream),
            ["Merged PRs", "Open PRs", "Open-source projects"],
        )
    ):
        x = 28 + index * (142 if mobile else 296)
        parts += [
            text(str(count), x, y + 63, 55, "display", COBALT),
            text("Open-source" if mobile and index == 2 else label, x, y + 98, 24),
        ]
    if mobile:
        parts.append(text("projects", 312, y + 128, 24))
    parts.append(text(updated, 28, height - 24, 20, "mono", BLUE, max_width=width - 56))
    return svg(
        width,
        height,
        "".join(parts),
        f"All-time authored public contributions: {counts[0]:,} PRs opened, {counts[1]:,} merged, {counts[2]:,} distinct linked closed issues. Upstream means outside jerome-queck and Jerome-Group owned repositories. Collection {updated}.",
    )


def render_cadence(months, updated, mobile=False, upstream=()):
    repos = upstream_by_repo(upstream)
    status_y = 188 + len(months) * 48 if mobile else 408
    width, height = (
        (480, status_y + 205 + len(repos) * 104)
        if mobile
        else (900, 560 + len(repos) * 63)
    )
    maximum = max(months.values(), default=0) or 1
    upstream_months = Counter(
        item["merged_at"][:7] for item in upstream if item["merged_at"]
    )
    parts = [
        text("A year of merges", 28, 61, 45, "display"),
        text("Authored public PRs / UTC months", 28, 103, 25, color=BLUE),
    ]
    for index, (month, count) in enumerate(months.items()):
        if mobile:
            y = 165 + index * 48
            parts += [
                text(month, 28, y, 24, "mono"),
                f'<rect x="159" y="{y - 23}" width="{max(2, count / maximum * 198):.2f}" height="27" fill="{COBALT if month == next(reversed(months)) else BLUE}"/>',
                text(str(count), 452, y, 25, "mono", anchor="end"),
            ]
            if upstream_months[month]:
                parts.append(
                    text(
                        f"+{upstream_months[month]}",
                        385,
                        y,
                        20,
                        "mono",
                        COBALT,
                        anchor="end",
                    )
                )
        else:
            slot = 828 / len(months)
            x = 36 + index * slot
            bar = count / maximum * 153
            parts += [
                f'<rect x="{x}" y="{291 - bar:.2f}" width="{slot * 0.61:.2f}" height="{max(2, bar):.2f}" fill="{COBALT if month == next(reversed(months)) else BLUE}"/>',
                text(
                    str(count), x + slot * 0.305, 278 - bar, 22, "mono", anchor="middle"
                ),
                text(month[5:], x + slot * 0.305, 325, 21, "mono", anchor="middle"),
            ]
            if upstream_months[month]:
                parts.append(
                    text(
                        f"+{upstream_months[month]}",
                        x + slot * 0.305,
                        361,
                        21,
                        "mono",
                        COBALT,
                        anchor="middle",
                    )
                )
    y = status_y
    parts += [
        text("+n = external project merges", 28, y, 24, color=COBALT),
        text("OPEN-SOURCE PR STATUS", 28, y + 47, 20, "mono", BLUE),
    ]
    for index, (repo, states) in enumerate(repos.items()):
        top = y + 91 + index * (104 if mobile else 63)
        parts.append(text(repo, 28, top, 26, max_width=424 if mobile else 400))
        summary = f"{states['MERGED']} merged / {states['OPEN']} open / {states['CLOSED']} closed"
        parts.append(
            text(
                summary,
                28 if mobile else 462,
                top + 37 if mobile else top,
                22,
                "mono",
                COBALT,
                max_width=424 if mobile else 410,
            )
        )
    parts.append(
        text(
            f"{next(iter(months))} to {next(reversed(months))} / current month partial",
            28,
            height - 63,
            22,
            color=BLUE,
            max_width=width - 56,
        )
    )
    parts.append(text(updated, 28, height - 24, 20, "mono", BLUE, max_width=width - 56))
    return svg(
        width,
        height,
        "".join(parts),
        f"Authored public PRs merged by UTC calendar month: {dict(months)}. Cobalt annotations count upstream merges within those totals. Upstream status by repository, closed means not merged. {updated}",
    )


def collect_snapshot():
    started = dt.datetime.now(dt.timezone.utc)
    today = started.date()
    contributions = fetch_contributions()
    start, days = fetch_calendar(graphql, today)
    activity = fetch_activity()
    catalogue = load_projects(Path(__file__).parents[1] / "data/projects.json")
    projects = [fetch_repo_pulse(graphql, project) for project in catalogue]
    upstream = fetch_upstream(graphql)
    completed = dt.datetime.now(dt.timezone.utc)
    return {
        "schema_version": 2,
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
        "upstream_prs": upstream,
    }


def render_snapshot(snapshot):
    if snapshot.get("schema_version") != 2:
        raise ValueError("Rendering requires a complete schema-v2 public snapshot")
    counts, updated = snapshot["counts"], snapshot["updated"]
    upstream = snapshot["upstream_prs"]
    start = dt.date.fromisoformat(snapshot["calendar_start"])
    today = dt.date.fromisoformat(snapshot["calendar_end"])
    days, months = snapshot["calendar_days"], snapshot["merge_months"]
    files = {
        "snapshot.json": json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n",
        "activity.svg": render_activity(snapshot["recent_events"]),
    }
    for mobile in (False, True):
        suffix = "-mobile" if mobile else ""
        files[f"counters{suffix}.svg"] = render_counters(
            counts, updated, mobile, upstream
        )
        files[f"calendar{suffix}.svg"] = render_calendar(
            start, today, days, mobile, updated
        )
        files[f"cadence{suffix}.svg"] = render_cadence(
            months, updated, mobile, upstream
        )
        files[f"pulse{suffix}.svg"] = render_pulse(
            snapshot["projects"], updated, mobile
        )
    upstream_months = Counter(
        item["merged_at"][:7] for item in upstream if item["merged_at"]
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
        + "\n".join(
            f"- {month}: {count}, including {upstream_months[month]} upstream"
            for month, count in months.items()
        )
        + "\n\n## Upstream PR records\n\n"
        + markdown_upstream(upstream, snapshot["observed_to"])
        + "\n\n## Selected repository pulse\n\n"
        "Nine authored selections. Default-branch tip commit and its Git committer date, by any author. "
        "Latest published GitHub release includes prereleases, explicitly labelled. "
        "Commits and releases do not establish deployment status or Jerome's personal contribution. "
        "No published release is a valid empty state, not a failed request. "
        "GitHub language bytes cover these nine repositories only, including any author and generated or vendored code as classified by GitHub. They are not expertise or a measure of personal work.\n\n"
        + markdown_pulse(snapshot["projects"])
        + f"\n\n## Public contribution calendar\n\n{start} through {today}, reconstructed from public "
        "commit, issue, PR, review and repository contribution records. The displayed window begins 1 July 2026. Count is records, not hours or quality. "
        "Cell levels are zero, then four nonzero levels relative to the largest daily count in this window. "
        "This is not a promise of parity with GitHub's native graph.\n\n"
        + "\n".join(f"- {date}: {count}" for date, count in sorted(days.items()))
        + "\n\n### Weekday frequency\n\n"
        + "Same calendar records grouped by UTC weekday. Counts are frequency, not effort.\n\n"
        + "\n".join(f"- {day}: {count}" for day, count in weekday_totals(days).items())
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
