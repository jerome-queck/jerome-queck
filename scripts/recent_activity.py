"""Public event links, including GitHub's compact pull-request payloads."""

import html
import json
import subprocess


def rest(endpoint):
    return json.loads(subprocess.check_output(["gh", "api", endpoint], text=True))


def select_activity(pages, fetch=rest):
    activity = []
    for page in pages:
        for event in page:
            repo = event["repo"]["name"]
            if not event.get("public") or any(
                word in repo.lower() for word in ("clarifold", "doomsday")
            ):
                continue
            if event["type"] not in ("IssuesEvent", "PullRequestEvent") or event[
                "payload"
            ]["action"] not in ("opened", "closed", "reopened"):
                continue
            item = event["payload"].get("issue") or event["payload"].get("pull_request")
            if not item:
                continue
            number = item["number"]
            if "title" not in item:
                item = fetch(f"repos/{repo}/pulls/{number}")
            kind = "pull" if event["type"] == "PullRequestEvent" else "issues"
            activity.append(
                {
                    "url": f"https://github.com/{repo}/{kind}/{number}",
                    "title": item["title"],
                    "repo": repo,
                    "number": number,
                    "date": event["created_at"][:10],
                    "action": event["payload"]["action"],
                }
            )
            if len(activity) == 8:
                return activity
    return activity


def fetch_activity():
    return select_activity(
        [
            rest(f"users/jerome-queck/events/public?per_page=100&page={page}")
            for page in range(1, 4)
        ]
    )


def markdown_activity(activity):
    lines = []
    for item in activity:
        title = (
            html.escape(item["title"])
            .replace("[", "&#91;")
            .replace("]", "&#93;")
            .replace("\n", " ")
        )
        lines.append(
            f"- {item['date']} · {item['action']} · [{item['repo']}#{item['number']}: {title}]({item['url']})"
        )
    return "\n".join(lines) or "No matching events in the latest 300 public events."


def render_activity(activity):
    rows = []
    for index, item in enumerate(activity):
        y = 76 + index * 65
        title = item["title"]
        title = title if len(title) <= 83 else title[:80] + "…"
        rows.append(f'''<circle cx="34" cy="{y - 5}" r="5" fill="#a78bfa"/>
        <text x="52" y="{y}" fill="#e2e8f0" font-size="15">{html.escape(title)}</text>
        <text x="52" y="{y + 23}" fill="#94a3b8" font-size="12">{html.escape(item["repo"])}#{item["number"]} · {item["action"]} · {item["date"]}</text>''')
    height = 80 + max(len(activity), 1) * 65
    if not rows:
        rows.append(
            '<text x="28" y="80" fill="#94a3b8">No matching recent events</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="820" height="{height}" viewBox="0 0 820 {height}" role="img">
    <title>Recent public pull request and issue activity</title>
    <rect width="820" height="{height}" rx="18" fill="#0d1422"/>
    <g font-family="Segoe UI,Arial,sans-serif">
    <text x="28" y="36" fill="#e2e8f0" font-size="20">Recent contributions</text>
    {"".join(rows)}</g></svg>'''
