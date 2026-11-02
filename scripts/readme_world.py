"""One opaque, locally outlined workshop and its observed public records."""

import html
import xml.etree.ElementTree as ET

from scripts.profile_style import BLUE, COBALT, INK, RULE, svg, text
from scripts.upstream_prs import upstream_totals


def embed(document, prefix, x=0, y=0):
    root = ET.fromstring(document)
    content = document
    for identifier in sorted(
        (node.attrib["id"] for node in root.iter() if "id" in node.attrib),
        key=len,
        reverse=True,
    ):
        content = content.replace(f'id="{identifier}"', f'id="{prefix}-{identifier}"')
        content = content.replace(f'#{identifier}"', f'#{prefix}-{identifier}"')
        content = content.replace(f"#{identifier})", f"#{prefix}-{identifier})")
    return f'<g transform="translate({x} {y})">{content}</g>'


def _beam(width, y):
    return (
        f'<path d="M20 {y}H{width - 20}v8H20z" fill="{RULE}"/>'
        f'<path d="M28 {y + 8}v20m{width - 56} 0v-20" stroke="{BLUE}" stroke-width="4"/>'
    )


PROJECT_LINES = {
    "Algebra": "Structure / symmetry / proof",
    "Calculus": "Change / geometry / argument",
    "Probability": "Uncertainty / experiments",
    "Number theory": "Patterns / exact experiments",
    "Calculator": "Exact notebooks / sign-in required",
    "NTULearn Sync": "Course pages / original attachments",
    "Academic OS": "Freshness / sources / study desk",
    "Syrax": "Telegram assistant / OpenClaw",
    "Emmy": "Operating kit for ChatGPT Dot",
}


def _projects(projects, width, y, mobile):
    parts = [text("Things I make", 28, y + 52, 42, "display")]
    columns = 1 if mobile else 2
    pitch = (width - 56) // columns
    for index, project in enumerate(projects):
        x = 28 + (index % columns) * pitch
        top = y + 100 + (index // columns) * 154
        parts += [
            f'<path d="M{x} {top + 105}h{pitch - 20}v7H{x}z" fill="{RULE}"/>',
            f'<path d="M{x} {top + 102}v-88h7v88m7 0v-98h7v98" fill="{BLUE}"/>',
            text(project["name"], x + 39, top, 29, "display", max_width=pitch - 53),
            text(
                PROJECT_LINES[project["name"]],
                x + 39,
                top + 28,
                21,
                "body",
                BLUE,
                max_width=pitch - 53,
            ),
        ]
        tip = project["head"]["committed_at"][:10] if project["head"] else "unavailable"
        parts.append(
            text(f"repo tip {tip}", x + 39, top + 53, 20, "mono", max_width=pitch - 53)
        )
        release = project["release"]
        release_label = (
            ("prerelease " if release["prerelease"] else "release ")
            + release["published_at"][:10]
            if release
            else "no published release"
        )
        parts.append(
            text(
                release_label,
                x + 39,
                top + 77,
                20,
                "mono",
                color=BLUE,
                max_width=pitch - 53,
            )
        )
        languages = sorted(
            project["language_bytes"].items(), key=lambda item: (-item[1], item[0])
        )
        total = sum(value for _, value in languages)
        cursor = x + 39
        for language_index, (language, value) in enumerate(languages):
            length = (pitch - 60) * value / total
            parts.append(
                f'<rect x="{cursor}" y="{top + 90}" width="{length}" height="6" fill="{(COBALT, BLUE, INK, RULE)[language_index % 4]}"><title>{html.escape(language)}: {value} bytes</title></rect>'
            )
            cursor += length
    return "".join(parts), y + 105 + ((len(projects) + columns - 1) // columns) * 154


def _counts(snapshot, width, y, mobile):
    parts = [text("Public work / all time", 28, y + 55, 35, "display")]
    labels = ("PRs opened", "PRs merged", "Linked closed issues")
    pitch = (width - 56) / 3
    for index, (count, label) in enumerate(zip(snapshot["counts"], labels)):
        x = 28 if mobile else 28 + pitch * index
        baseline = y + 130 + (index * 92 if mobile else 0)
        parts += [
            text(
                f"{count:,}",
                x,
                baseline,
                53,
                "display",
                COBALT,
                max_width=140 if mobile else pitch - 12,
            ),
            text(
                label,
                185 if mobile else x,
                baseline - 8 if mobile else baseline + 33,
                23 if mobile else 22,
                max_width=267 if mobile else pitch - 12,
            ),
        ]
    if mobile:
        y += 185
    merged, opened, repos = upstream_totals(snapshot["upstream_prs"])
    parts += [
        text(
            f"UPSTREAM  {merged} merged / {opened} open",
            28,
            y + 215,
            21,
            "mono",
            BLUE,
            max_width=width - 56,
        ),
        text(
            f"{repos} external repositories / open is not merged",
            28,
            y + 247,
            19,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    return "".join(parts), y + 285


def _cadence(snapshot, width, y, mobile):
    months = snapshot["merge_months"]
    maximum = max(months.values(), default=0) or 1
    parts = [
        text("The merge clock", 28, y + 53, 37, "display"),
        text(
            "Authored public PR merges / UTC months",
            28,
            y + 89,
            22,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    pitch = (width - 56) / len(months)
    for index, (month, count) in enumerate(months.items()):
        x = 28 + index * pitch
        height = count / maximum * 110
        parts += [
            f'<rect x="{x}" y="{y + 245 - height}" width="{pitch * 0.62}" height="{max(2, height)}" fill="{COBALT}"/>',
            text(count, x, y + 230 - height, 20, "mono"),
            text(month[5:], x, y + 275, 20, "mono"),
        ]
    parts += [
        text(
            f"2026-07-01 to {snapshot['calendar_end']}",
            28,
            y + 313,
            20,
            "mono",
            BLUE,
            max_width=width - 56,
        ),
        text(
            "Current month partial; all public repositories.",
            28,
            y + 344,
            20,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    return "".join(parts), y + 377


def render_world(snapshot, panels, mobile=False, motion="ambient"):
    from scripts.pixel_world import PALETTE, SCENE_SIZE, render_scene

    width, scene_height = SCENE_SIZE["mobile" if mobile else "wide"]
    scene = embed(render_scene(mobile=mobile, motion=motion), "scene")
    # The title lives in the quiet sky; records remain outside every animated group.
    heading = [
        text("Jerome Queck", 28, 65, 43 if mobile else 56, "display", INK),
        text("MATHEMATICS × SOFTWARE", 28, 103, 20, "mono", BLUE),
    ]
    parts = []
    y = scene_height
    merged_repos = {
        record["repo"].casefold()
        for record in snapshot["upstream_prs"]
        if record["state"] == "MERGED"
    }
    if {"openclaw/openclaw", "freecodecamp/freecodecamp"} <= merged_repos:
        parts += [
            text(
                "Contributions merged into",
                28,
                y + 42,
                30,
                "display",
                max_width=width - 56,
            ),
            text(
                "OpenClaw + freeCodeCamp",
                28,
                y + 84,
                32,
                "display",
                COBALT,
                max_width=width - 56,
            ),
        ]
        y += 115
    parts.append(_beam(width, y))
    project_art, y = _projects(snapshot["projects"], width, y + 16, mobile)
    parts.append(project_art)
    parts.append(_beam(width, y))
    count_art, y = _counts(snapshot, width, y + 8, mobile)
    parts.append(count_art)
    parts.append(_beam(width, y))
    cadence_art, y = _cadence(snapshot, width, y + 8, mobile)
    parts.append(cadence_art)
    suffix = "-mobile" if mobile else ""
    calendar = panels[f"calendar{suffix}.svg"]
    parts.append(_beam(width, y))
    parts.append(embed(calendar, "calendar", 0, y + 24))
    y += 24 + float(ET.fromstring(calendar).get("height"))
    parts += [
        text(
            "Collected " + snapshot["updated"],
            28,
            y + 31,
            19,
            "mono",
            BLUE,
            max_width=width - 56,
        ),
        text("Exact records + project links below.", 28, y + 65, 22, color=BLUE),
    ]
    world = svg(
        width,
        y + 100,
        scene
        + "".join(heading)
        + '<g id="world-data" aria-label="Observed public GitHub records">'
        + "".join(parts)
        + "</g>",
        "Jerome Queck. Mathematics and software. A midnight workshop with nine projects and public GitHub records. "
        + snapshot["updated"],
        background=PALETTE["sky"],
    )
    # Namespace nested IDs before the outer outline deduplicator adds its glyphs.
    return world.replace(
        "<svg ",
        '<svg data-snapshot="'
        + html.escape(snapshot["observed_to"], quote=True)
        + '" ',
        1,
    )
