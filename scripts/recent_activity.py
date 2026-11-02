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
    from scripts.profile_style import BLUE, COBALT, rule, svg, text

    parts = [
        text("Recent public work", 28, 52, 38, "display"),
        text("Full titles + links in native snapshot", 28, 91, 23, color=BLUE),
    ]
    for index, item in enumerate(activity):
        y = 139 + index * 121
        parts += [
            rule(28, y - 22, 612, y - 22),
            text(
                f"{item['repo']}#{item['number']}",
                28,
                y + 16,
                27,
                "mono",
                COBALT,
                max_width=584,
                minimum=12,
            ),
            text(f"{item['action']} / {item['date']}", 28, y + 57, 25),
        ]
    if not activity:
        parts.append(text("No matching recent events", 28, 155, 28))
    return svg(
        640,
        156 + max(len(activity), 1) * 121,
        "".join(parts),
        "Two recent public issue and pull request events. Graphics show repository, number, action and date. Full original Unicode titles and links are in the native snapshot README.",
    )
