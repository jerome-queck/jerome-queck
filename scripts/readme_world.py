"""One opaque, locally outlined workshop and its observed public records."""

import base64
import datetime as dt
import html
import math
import xml.etree.ElementTree as ET

from scripts.profile_style import svg, text

COBALT = "#efad62"
BLUE = "#c9b2a6"
RULE = "#795451"
from collections import Counter
from pathlib import Path
from textwrap import wrap

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
        f'<path d="M0 {y}H{width}v12H0z" fill="#422d34"/>'
        f'<path d="M0 {y + 2}H{width}M0 {y + 10}H{width}" stroke="#a8785e" stroke-width="2"/>'
        f'<path d="M12 {y + 12}v19m{width - 24} 0v-19" stroke="#795451" stroke-width="5"/>'
    )


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
    return "".join(parts), y + 195


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
    columns = min(len(months), 4 if mobile else 8) or 1
    pitch = (width - 56) / columns
    rows = max(1, math.ceil(len(months) / columns))
    row_height = 204
    for index, (month, count) in enumerate(months.items()):
        row, column = divmod(index, columns)
        x = 28 + column * pitch
        baseline = y + 245 + row * row_height
        height = count / maximum * 110
        parts += [
            (
                f'<rect x="{x}" y="{baseline - height}" width="{pitch * 0.62}" height="{height}" fill="{COBALT}"/>'
                if count
                else ""
            ),
            text(count, x, baseline - 15 - height, 20, "mono", max_width=pitch - 12),
            text(month, x, baseline + 30, 18, "mono", max_width=pitch - 12),
        ]
    footer = y + 313 + (rows - 1) * row_height
    parts += [
        text(
            f"2026-07-01 to {snapshot['calendar_end']}",
            28,
            footer,
            20,
            "mono",
            BLUE,
            max_width=width - 56,
        ),
        text(
            "Current month partial; all public repositories.",
            28,
            footer + 31,
            20,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    return "".join(parts), footer + 64


def _activity_mix(snapshot, width, y):
    kinds = snapshot["calendar_kinds"]
    labels = (
        ("commits", "Commits"),
        ("issues", "Issues opened"),
        ("pull_requests", "PRs opened"),
        ("reviews", "Reviews"),
        ("repositories", "Repos created"),
    )
    colors = ("#eeb36e", "#b77b70", "#82a8b1", "#c1a57b", "#806d8a")
    total = sum(kinds.values())
    cx, cy, radius = 105, y + 198, 67
    parts = [
        text("Activity mix", 28, y + 54, 36, "display"),
        text("Public contributions since 1 July 2026", 28, y + 87, 20, color=BLUE),
    ]
    if total:
        angle = -math.pi / 2
        for (key, _), color in zip(labels, colors):
            value = kinds[key]
            if not value:
                continue
            span = 2 * math.pi * value / total
            if value == total:
                parts.append(
                    f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{color}" stroke-width="26"/>'
                )
            else:
                end = angle + span
                x1, y1 = cx + radius * math.cos(angle), cy + radius * math.sin(angle)
                x2, y2 = cx + radius * math.cos(end), cy + radius * math.sin(end)
                parts.append(
                    f'<path d="M{x1:.2f} {y1:.2f} A{radius} {radius} 0 {int(span > math.pi)} 1 {x2:.2f} {y2:.2f}" fill="none" stroke="{color}" stroke-width="26"/>'
                )
                angle = end
        parts.append(text("100%", cx, cy + 7, 22, "mono", anchor="middle"))
    else:
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{RULE}" stroke-width="3"/>'
        )
        parts.append(text("No records", cx, cy + 7, 18, anchor="middle"))
    for i, ((key, label), color) in enumerate(zip(labels, colors)):
        row = y + 129 + i * 43
        parts.append(
            f'<rect x="202" y="{row - 13}" width="11" height="11" fill="{color}"/>'
        )
        parts.append(text(label, 220, row, 18, max_width=125))
        value = kinds[key]
        percent = value / total * 100 if total else 0
        percentage = "<0.1" if 0 < percent < 0.05 else f"{percent:.1f}"
        number = f"{value:,}" + (f" ({percentage}%)" if total else "")
        parts.append(text(number, width - 28, row + 20, 17, "mono", anchor="end"))
    return "".join(parts), y + 375


def _footprint(snapshot, width, y):
    from scripts.upstream_prs import change_footprint

    values = change_footprint(snapshot["upstream_prs"])
    parts = [
        text("Merged patch footprint", 28, y + 54, 35, "display", max_width=width - 56),
        text(f"{values['prs']} upstream PRs / all time", 28, y + 88, 20, color=BLUE),
    ]
    rows = (
        ("additions", "Lines added"),
        ("deletions", "Lines deleted"),
        ("file_changes", "File-change entries"),
    )
    line_max = max(values["additions"], values["deletions"]) or 1
    for i, (key, label) in enumerate(rows):
        row = y + 132 + i * 45
        parts += [
            text(label, 28, row, 20),
            text(f"{values[key]:,}", width - 28, row, 20, "mono", anchor="end"),
        ]
        if key != "file_changes" and values[key]:
            length = (width - 355) * values[key] / line_max
            parts.append(
                f'<rect x="170" y="{row - 14}" width="{length:.2f}" height="13" fill="{COBALT if key == "additions" else BLUE}"/>'
            )
    parts += [
        text(
            "Whole PR patches include every coauthor.",
            28,
            y + 282,
            19,
            color=BLUE,
            max_width=width - 56,
        ),
        text(
            "File changes can repeat across PRs.",
            28,
            y + 308,
            19,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    return "".join(parts), y + 340


def _proposal_ages(snapshot, width, y):
    from scripts.upstream_prs import open_pr_ages

    ages = open_pr_ages(snapshot["upstream_prs"], snapshot["observed_to"])
    bins = Counter(item["days"] for item in ages)
    days = sorted({0, 1, 2} | set(bins))
    parts = [
        text("Open proposal ages", 28, y + 54, 35, "display", max_width=width - 56),
        text(
            "Completed days at collection; one dot per PR",
            28,
            y + 87,
            19,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    cursor = y + 128
    for day in days:
        count = bins[day]
        parts.append(text(str(day) + " d", 28, cursor, 19, "mono"))
        for i in range(count):
            parts.append(
                f'<circle cx="{104 + (i % 20) * 15}" cy="{cursor - 6 + (i // 20) * 18}" r="4" fill="{COBALT}"/>'
            )
        parts.append(text(str(count), width - 28, cursor, 19, "mono", anchor="end"))
        cursor += 44 + max(0, (count - 1) // 20) * 18
    return "".join(parts), cursor + 12


def _languages(snapshot, width, y):
    source = snapshot["source_lines"]
    rows = sorted(
        source["by_language"].items(), key=lambda item: (-item[1]["code"], item[0])
    )
    shown = rows[:10]
    maximum = max((row["code"] for _, row in shown), default=0) or 1
    parts = [
        text("Languages / code lines", 28, y + 48, 32, "display", max_width=width - 56),
        text(
            "9 public projects / all authors / cloc 2.10",
            28,
            y + 80,
            18,
            color=BLUE,
            max_width=width - 56,
        ),
    ]
    cursor = y + 122
    for name, row in shown:
        parts += [
            text(name, 28, cursor, 20, max_width=width - 185),
            text(f"{row['code']:,}", width - 28, cursor, 19, "mono", anchor="end"),
            f'<rect x="28" y="{cursor + 10}" width="{(width - 56) * row["code"] / maximum:.3f}" height="5" fill="{COBALT}"/>',
        ]
        cursor += 43
    if not rows:
        parts.append(text("No classified code lines", 28, cursor, 20))
        cursor += 40
    other = sum(row["code"] for _, row in rows[10:])
    if len(rows) > 10:
        parts.append(
            text(
                f"Other: {other:,} code lines",
                28,
                cursor,
                18,
                color=BLUE,
                max_width=width - 56,
            )
        )
        cursor += 31
    total = source["totals"]
    for label in (
        f"{total['code']:,} code / {total['files']:,} classified files",
        f"{total['comment']:,} comments / {total['blank']:,} blank lines",
        "Contents, not personal authorship. Scope in snapshot.",
    ):
        parts.append(text(label, 28, cursor, 17, color=BLUE, max_width=width - 56))
        cursor += 28
    return "".join(parts), cursor + 16


def _calendar(snapshot, width, y, mobile):
    days = snapshot["calendar_days"]
    start = dt.date.fromisoformat(snapshot["calendar_start"])
    end = dt.date.fromisoformat(snapshot["calendar_end"])
    sunday = start - dt.timedelta(days=(start.weekday() + 1) % 7)
    maximum = max(days.values(), default=0)
    palette = ("#302a3a", "#61454e", "#99705d", "#c69060", "#f2b768")
    columns = 18 if mobile else 36
    cell = 19 if mobile else 21
    pitch = 23
    weeks = (end - sunday).days // 7 + 1
    panels = (weeks + columns - 1) // columns
    parts = [
        text(
            "Public contribution calendar",
            28,
            y + 54,
            33,
            "display",
            max_width=width - 56,
        ),
        text(f"{start} to {end}", 28, y + 86, 20, "mono", color=BLUE),
    ]
    last_panel_weeks = weeks - (panels - 1) * columns
    last_rows = 7 if last_panel_weeks > 1 else (end.weekday() + 1) % 7 + 1
    for panel in range(panels):
        for label, row in (("M", 1), ("W", 3), ("F", 5)):
            if panel == panels - 1 and row >= last_rows:
                continue
            parts.append(
                text(label, 18, y + 130 + panel * 205 + row * pitch, 14, "mono", BLUE)
            )
    marker = start.replace(day=1)
    while marker <= end:
        visible = max(marker, start)
        week = (visible - sunday).days // 7
        panel, col = divmod(week, columns)
        parts.append(
            text(
                f"{marker:%b}",
                32 + col * pitch,
                y + 108 + panel * 205,
                15,
                "mono",
                BLUE,
            )
        )
        marker = (marker.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    date = start
    while date <= end:
        week = (date - sunday).days // 7
        panel, col = divmod(week, columns)
        row = (date.weekday() + 1) % 7
        x, yy = 32 + col * pitch, y + 115 + panel * 205 + row * pitch
        count = days.get(str(date), 0)
        level = 0 if count == 0 else min(4, 1 + (count - 1) * 4 // maximum)
        parts.append(
            f'<rect x="{x}" y="{yy}" width="{cell}" height="{cell}" fill="{palette[level]}"><title>{date}: {count} records</title></rect>'
        )
        date += dt.timedelta(days=1)
    legend_y = y + 115 + (panels - 1) * 205 + last_rows * pitch + 20
    parts.append(text("0 to daily peak", 28, legend_y + 17, 19, color=BLUE))
    for i, color in enumerate(palette):
        parts.append(
            f'<rect x="{190 + i * 26}" y="{legend_y}" width="20" height="20" fill="{color}"/>'
        )
    return "".join(parts), legend_y + 50


def render_world(snapshot, panels, mobile=False, motion="ambient"):
    from scripts.pixel_world import SCENE_SIZE

    width, _ = SCENE_SIZE["mobile" if mobile else "wide"]
    parts = [_beam(width, 0)]
    y = 8
    count_art, y = _counts(snapshot, width, y, mobile)
    parts.append(count_art)
    cadence_art, y = _cadence(snapshot, width, y + 8, mobile)
    parts.append(cadence_art)
    activity_art, y = _activity_mix(snapshot, width, y + 8)
    parts.append(activity_art)
    calendar_art, y = _calendar(snapshot, width, y + 8, mobile)
    parts.append(calendar_art)
    parts.append(_beam(width, y))
    languages, y = _languages(snapshot, width, y + 8)
    parts.append(languages)
    parts.append(_beam(width, y))
    footprint, y = _footprint(snapshot, width, y + 8)
    parts.append(footprint)
    ages, y = _proposal_ages(snapshot, width, y)
    parts.append(ages)
    parts.append(
        text(
            "Collected " + snapshot["updated"],
            28,
            y + 30,
            19,
            "mono",
            BLUE,
            max_width=width - 56,
        )
    )
    y += 50
    parts.append(_beam(width, y))
    merged, opened, _ = upstream_totals(snapshot["upstream_prs"])
    parts += [
        text(
            "Open-source contributions", 28, y + 39, 30, "display", max_width=width - 56
        ),
        text(f"{merged} merged / {opened} open", 28, y + 64, 18, "mono", BLUE),
    ]
    y += 70
    merged_by_repo = {}
    for item in snapshot["upstream_prs"]:
        if item["state"] == "MERGED":
            merged_by_repo.setdefault(item["repo"], []).append(item["number"])
    if not merged_by_repo:
        parts.append(text("No merged upstream PRs", 28, y + 20, 19, color=BLUE))
        y += 23
    aliases = {
        "openclaw/openclaw": "OpenClaw",
        "freecodecamp/freecodecamp": "freeCodeCamp",
    }
    for repo, numbers in sorted(
        merged_by_repo.items(), key=lambda item: item[0].casefold()
    ):
        name = aliases.get(repo.casefold(), repo)
        label = name + "  " + ", ".join("#" + str(number) for number in sorted(numbers))
        for line in wrap(label, 35 if mobile else 75):
            parts.append(text(line, 28, y + 20, 18, "mono", max_width=width - 56))
            y += 23
    y += 8
    texture = base64.b64encode(
        (
            Path(__file__).resolve().parents[1]
            / "assets/pixel-world/ledger-texture.jpg"
        ).read_bytes()
    ).decode("ascii")
    world = svg(
        width,
        y + 20,
        f'<defs><pattern id="ledger-texture" width="160" height="192" patternUnits="userSpaceOnUse"><image width="160" height="192" href="data:image/jpeg;base64,{texture}"/></pattern></defs>'
        f'<rect width="{width}" height="{y + 20}" fill="url(#ledger-texture)" opacity=".08"/>'
        f'<path d="M0 0h18v{y + 20}H0zM{width - 18} 0h18v{y + 20}h-18z" fill="#392833"/>'
        f'<path d="M16 0v{y + 20}M{width - 16} 0v{y + 20}" stroke="#805750" stroke-width="3"/>'
        + '<g id="world-data" aria-label="Observed public GitHub records">'
        + "".join(parts)
        + "</g>",
        "Public GitHub records for Jerome Queck. " + snapshot["updated"],
        background="#211b29",
    )
    return world.replace(
        "<svg ",
        '<svg data-snapshot="'
        + html.escape(snapshot["observed_to"], quote=True)
        + '" ',
        1,
    )
