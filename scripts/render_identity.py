import html
from pathlib import Path

PROJECTS = {
    "name": "Jerome Queck",
    "subtitle": "Mathematics studied. Software built.",
    "Mathematics": [
        "Calculator",
        "Probability",
        "Number theory",
        "Algebra",
        "Calculus",
    ],
    "Software": ["Academic OS", "NTULearn Sync", "Syrax", "Emmy"],
    "footer": "Upstream · OpenClaw + freeCodeCamp",
}


def render():
    def label(x, y, value, size=26, color="#e8e2d3", anchor="start"):
        return (
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" fill="{color}" '
            f'font-size="{size}">{html.escape(value)}</text>'
        )

    body = label(320, 48, PROJECTS["name"], 34, anchor="middle")
    body += label(320, 82, PROJECTS["subtitle"], 20, "#b9cbd5", "middle")
    body += '<path d="M320 100V118M160 118H480M160 118V145M480 118V145" fill="none" stroke="#8be9ee" stroke-width="2"/>'
    for x, category in ((24, "Mathematics"), (344, "Software")):
        body += f'<rect x="{x}" y="146" width="272" height="275" rx="10" fill="#162936" stroke="#344b5c"/>'
        body += label(x + 20, 184, category, 28, "#8be9ee")
        for index, project in enumerate(PROJECTS[category]):
            body += label(x + 20, 228 + index * 40, project, 24)
    body += label(320, 458, PROJECTS["footer"], 22, "#efb48b", "middle")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="640" height="484" viewBox="0 0 640 484" role="img">'
        f"<title>{html.escape(PROJECTS['name'])} project map</title>"
        "<desc>Editorial groupings, not technical dependencies. Project links and descriptions follow in the README.</desc>"
        '<rect width="640" height="484" rx="12" fill="#0b1c28"/>'
        f'<g font-family="Segoe UI,Arial,sans-serif">{body}</g></svg>\n'
    )


if __name__ == "__main__":
    Path(Path(__file__).parents[1] / "assets/project-map.svg").write_text(
        render(), encoding="utf-8"
    )
