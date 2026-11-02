"""Compose native linked views of the midnight workshop."""

import base64
from pathlib import Path
from textwrap import wrap

from scripts.profile_style import svg, text

OUT = Path(__file__).resolve().parents[1] / "assets/pixel-world"
PROJECTS = [
    (
        "ntulearn",
        "NTULearn Sync",
        "Course pages and attachments, gathered for study.",
        "https://github.com/Jerome-Group/ntulearn",
        None,
    ),
    (
        "algebra",
        "Algebra",
        "Structure, symmetry and proofs.",
        "https://github.com/Jerome-Group/algebra",
        "https://algebra.jeromegroup.org",
    ),
    (
        "academic-os",
        "Academic OS",
        "A study desk for sources, tasks and freshness.",
        "https://github.com/Jerome-Group/academic-os",
        None,
    ),
    (
        "calculus",
        "Calculus",
        "Change, geometry and arguments.",
        "https://github.com/Jerome-Group/calculus",
        "https://calculus.jeromegroup.org",
    ),
    (
        "syrax",
        "Syrax",
        "A Telegram assistant with an academic desk.",
        "https://github.com/Jerome-Group/syrax",
        None,
    ),
    (
        "probability",
        "Probability",
        "Uncertainty, examples and experiments.",
        "https://github.com/jerome-queck/probability",
        "https://probability.jeromegroup.org",
    ),
    (
        "emmy",
        "Emmy",
        "An operating kit for ChatGPT Dot.",
        "https://github.com/jerome-queck/emmy",
        None,
    ),
    (
        "numbertheory",
        "Number theory",
        "Proofs and exact computational experiments.",
        "https://github.com/Jerome-Group/numbertheory",
        "https://numbertheory.jeromegroup.org",
    ),
    (
        "calculator",
        "Calculator",
        "Exact computation and notebooks. Sign-in required.",
        "https://github.com/Jerome-Group/calculator",
        "https://calculator.jeromegroup.org",
    ),
]

PROJECT_ORDER = (
    "ntulearn",
    "academic-os",
    "syrax",
    "emmy",
    "algebra",
    "calculus",
    "probability",
    "numbertheory",
    "calculator",
)
PROJECTS.sort(key=lambda item: PROJECT_ORDER.index(item[0]))


def master(mobile, role, motion):
    width, height = (480, 190) if mobile else (900, 220)
    title_width, button_width = width * 3 // 4, width // 4
    button = role == "source"
    view_width = {"full": width, "title": title_width, "source": button_width}[role]
    image = base64.b64encode((OUT / "workshop.jpg").read_bytes()).decode("ascii")
    # Project rooms reveal consecutive portions of the cutaway at a constant scale.
    art_height = (len(PROJECTS) + 1) * height
    art_width = art_height * 2 / 3
    art_x = width * 0.65 - art_width * 420 / 1024
    art = f'<defs><image id="scene-art" width="900" height="1350" href="data:image/jpeg;base64,{image}"/></defs>'
    art += f'<use href="#scene-art" transform="translate({art_x} 0) scale({art_width / 900})"/>'
    body = [art]
    views = [f'<view id="hero" viewBox="0 0 {view_width} {height}"/>']
    if not button:
        body += [
            f'<path d="M12 14h{width * 0.56}v{height - 28}H12z" fill="#1b1725" fill-opacity=".78"/>',
            text(
                "Jerome Queck",
                25,
                69 if mobile else 96,
                44 if mobile else 62,
                "display",
                max_width=width * 0.54,
            ),
            text(
                "Things I make",
                27,
                138 if mobile else 192,
                23 if mobile else 32,
                "display",
            ),
        ]
        for first, count, x in (
            (1, 2, 12),
            (3, 2, width * 0.05),
            (5, 3, 12),
            (8, 2, width * 0.05),
        ):
            body.append(
                f'<path d="M{x} {first * height + 5}h{width * 0.56}v{height * count - 10}H{x}z" fill="#1c1722" fill-opacity=".82"/>'
            )
    for i, (slug, name, desc, _, _) in enumerate(PROJECTS):
        y = (i + 1) * height
        x0 = title_width if button else 0
        views.append(f'<view id="{slug}" viewBox="{x0} {y} {view_width} {height}"/>')
        if button:
            body += [
                f'<path d="M{x0 + 8} {y + height - 56}h{button_width - 16}v43H{x0 + 8}z" fill="#211925" fill-opacity=".80"/>',
                text(
                    "REPO  >",
                    x0 + button_width / 2,
                    y + height - 28,
                    20 if mobile else 22,
                    "mono",
                    anchor="middle",
                    max_width=button_width - 20,
                ),
            ]
        else:
            panel_width = width * 0.56
            label_x = (12 if i < 2 or 4 <= i < 7 else width * 0.05) + 13
            lines = wrap(desc, 23 if mobile else 35)
            body.append(
                text(
                    name,
                    label_x,
                    y + (53 if mobile else 70),
                    31 if mobile else 42,
                    "display",
                    max_width=panel_width - 26,
                )
            )
            for n, line in enumerate(lines):
                body.append(
                    text(
                        line,
                        label_x,
                        y + (83 if mobile else 110) + n * (26 if mobile else 29),
                        22 if mobile else 25,
                        "body",
                        max_width=panel_width - 26,
                        minimum=15,
                    )
                )
            if PROJECTS[i][4]:
                body.append(
                    text(
                        "WEBSITE  >",
                        label_x,
                        y + height - 13,
                        19,
                        "mono",
                        color="#eab878",
                    )
                )
    if motion == "ambient":
        body.append(
            "<style>@keyframes glow{0%,100%{opacity:.15}50%{opacity:.8}}.glow{animation:glow 4s ease-in-out infinite}</style>"
        )
    for lantern_x, lantern_y in ((420, 300), (380, 515), (745, 1110), (287, 1020)):
        x = art_x + art_width * lantern_x / 1024
        y = art_height * lantern_y / 1536
        body.append(
            f'<circle class="glow" cx="{x:.2f}" cy="{y:.2f}" r="{5 if mobile else 8}" opacity=".15" fill="#ffe9a8"/>'
        )
    document = svg(
        view_width,
        height,
        "".join(body),
        "Jerome Queck’s midnight workshop",
        background="#211b29",
    )
    return document.replace("<defs>", "".join(views) + "<defs>", 1)


def generate():
    for mobile, suffix in ((False, "wide"), (True, "mobile")):
        for role in ("full", "title", "source"):
            for motion in ("ambient", "still"):
                (OUT / f"{role}-{suffix}-{motion}.svg").write_text(
                    master(mobile, role, motion)
                )


if __name__ == "__main__":
    generate()
