"""Public contribution counters; fail closed before publishing generated assets."""

import datetime as dt
import html
import json
import subprocess
import sys
from pathlib import Path


def graphql(query, **variables):
    command = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        command += ["-f", f"{key}={value}"]
    result = json.loads(subprocess.check_output(command, text=True))
    if result.get("errors"):
        raise RuntimeError("GitHub query failed; retaining published data")
    return result["data"]


def public_calendar_check(collection):
    if (
        collection["restrictedContributionsCount"]
        or collection["hasAnyRestrictedContributions"]
    ):
        raise ValueError("Calendar contains private counts; retaining published data")


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
    data = graphql("""query { user(login:"jerome-queck") {
      contributionsCollection { restrictedContributionsCount hasAnyRestrictedContributions }
    }
    opened: search(query:"is:public author:jerome-queck is:pr", type:ISSUE) { issueCount }
    merged: search(query:"is:public author:jerome-queck is:pr is:merged", type:ISSUE) { issueCount }
    }""")
    public_calendar_check(data["user"]["contributionsCollection"])
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


def render_counters(counts, updated):
    labels = ["PRs opened", "PRs merged", "Linked issues resolved"]
    colors = ["#a78bfa", "#2dd4bf", "#fbbf24"]
    cards = []
    for index, (count, label, color) in enumerate(zip(counts, labels, colors)):
        x = 28 + index * 260
        cards.append(f'''<rect x="{x}" y="66" width="244" height="104" rx="12" fill="#172033"/>
        <text x="{x + 18}" y="112" fill="{color}" font-size="34" font-weight="700">{count:,}</text>
        <text x="{x + 18}" y="144" fill="#dbe4f0" font-size="15">{label}</text>''')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="820" height="220" viewBox="0 0 820 220" role="img">
    <title>Public contributions: {counts[0]} PRs opened, {counts[1]} merged, {counts[2]} linked issues resolved</title>
    <rect width="820" height="220" rx="18" fill="#0d1422"/>
    <g font-family="Segoe UI,Arial,sans-serif">
    <text x="28" y="39" fill="#f1f5f9" font-size="20" font-weight="600">Building in public</text>
    <text x="790" y="38" fill="#94a3b8" font-size="12" text-anchor="end">ALL TIME · PUBLIC</text>
    {"".join(cards)}
    <text x="28" y="199" fill="#94a3b8" font-size="12">Updated {html.escape(updated)} · Issues linked to authored merged PRs</text>
    </g></svg>"""


def main():
    counts = fetch_counters()
    events = json.loads(
        subprocess.check_output(
            [
                "gh",
                "api",
                "--paginate",
                "--slurp",
                "users/jerome-queck/events/public?per_page=100",
            ],
            text=True,
        )
    )
    activity = []
    for page in events[:3]:
        for event in page:
            repo = event["repo"]["name"]
            if not event.get("public") or any(
                word in repo.lower() for word in ("clarifold", "doomsday")
            ):
                continue
            if event["type"] not in ("IssuesEvent", "PullRequestEvent"):
                continue
            item = event["payload"].get("issue") or event["payload"].get("pull_request")
            if not item:
                continue
            url = item["html_url"]
            if not url.startswith("https://github.com/"):
                raise ValueError("Unexpected activity URL")
            label = (
                html.escape(item["title"]).replace("[", "&#91;").replace("]", "&#93;")
            )
            activity.append(
                f"- {event['created_at'][:10]} · [{repo}#{item['number']}: {label}]({url})"
            )
    activity = activity[:8]
    updated = dt.datetime.now(dt.timezone.utc).strftime("%d %b %Y %H:%M UTC")
    output = Path(sys.argv[1])
    output.mkdir(parents=True, exist_ok=True)
    (output / "counters.svg").write_text(render_counters(counts, updated))
    (output / "README.md").write_text(
        f"# Public contribution snapshot\n\nUpdated {updated}.\n\n"
        f"- Authored PRs opened, all time: {counts[0]}\n"
        f"- Authored PRs merged, all time: {counts[1]}\n"
        f"- Distinct closed issues linked to those merged PRs: {counts[2]}\n\n"
        "Linked issues must close at or after the PR merge. This measures linked resolution, "
        "not who clicked Close; GitHub can change links retrospectively.\n\n"
        "Calendar: last year. Recent activity: public issue and PR events among the "
        "latest 300 GitHub events; this is a bounded feed, not a complete history.\n\n"
        "[Browse PRs](https://github.com/pulls?q=is%3Apr+author%3Ajerome-queck+is%3Apublic) · "
        "[Browse issues](https://github.com/issues?q=is%3Aissue+author%3Ajerome-queck+is%3Apublic)\n"
    )
    with (output / "README.md").open("a") as summary:
        summary.write(
            "\n## Recent issue and PR events\n\n" + "\n".join(activity) + "\n"
        )


if __name__ == "__main__":
    main()
