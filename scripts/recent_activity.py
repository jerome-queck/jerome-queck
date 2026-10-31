"""Public event links, including GitHub's compact pull-request payloads."""

import html
import json
import subprocess
import textwrap


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
            if len(activity) == 2:
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
        y = 80 + index * 132
        title = textwrap.shorten(item["title"], width=76, placeholder="…")
        for line, value in enumerate(textwrap.wrap(title, width=40)):
            rows.append(
                f'<text x="28" y="{y + line * 28}" fill="#e2e8f0" font-size="24">{html.escape(value)}</text>'
            )
        repository = f"{item['repo']}#{item['number']}"
        repository = repository if len(repository) <= 48 else repository[:45] + "…"
        rows.append(
            f'<text x="28" y="{y + 62}" fill="#b9cbd5" font-size="20">{html.escape(repository)}</text>'
        )
        rows.append(
            f'<text x="28" y="{y + 88}" fill="#b9cbd5" font-size="20">{html.escape(item["action"])} · {item["date"]}</text>'
        )
    height = 68 + max(len(activity), 1) * 132
    if not rows:
        rows.append(
            '<text x="28" y="80" fill="#b9cbd5" font-size="24">No matching recent events</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}" role="img">
    <title>Two recent public pull request and issue events. Full titles and links in the snapshot README.</title>
    <rect width="640" height="{height}" rx="18" fill="#0d1422"/>
    <g font-family="Segoe UI,Arial,sans-serif">
    <text x="28" y="36" fill="#8be9ee" font-size="25">Recent public work</text>
    {"".join(rows)}</g></svg>'''
