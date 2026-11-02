"""Local, measured type. Unsupported glyphs fail before publication."""

import hashlib
import html
import json
import re
from functools import lru_cache
from pathlib import Path

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

PAPER = "#F3EEDC"
INK = "#30243B"
COBALT = "#4055B5"
BLUE = "#345C6A"
CITRON = "#D7D99D"
RULE = "#C9C5BB"
FONT_ROOT = Path(__file__).resolve().parents[1] / "assets/type"


@lru_cache(maxsize=3)
def face(role):
    if hb.version_string() != "10.1.0":
        raise RuntimeError("Expected the pinned HarfBuzz 10.1.0 shaping engine")
    record = next(
        item
        for item in json.loads((FONT_ROOT / "manifest.json").read_text())
        if item["role"] == role
    )
    source = (FONT_ROOT / record["file"]).read_bytes()
    if hashlib.sha256(source).hexdigest() != record["sha256"]:
        raise ValueError(f"Font checksum mismatch: {role}")
    font = TTFont(FONT_ROOT / record["file"])
    if record["axes"]:
        font = instantiateVariableFont(font, record["axes"], inplace=True)
    shaping = hb.Font(hb.Face(source))
    shaping.set_variations(record["axes"])
    return font, shaping


@lru_cache(maxsize=8192)
def shaped(value, role):
    font, shaping = face(role)
    if not value:
        return (), 0, (0, 0, 0, 0), font["head"].unitsPerEm
    buffer = hb.Buffer()
    buffer.add_str(value)
    buffer.guess_segment_properties()
    hb.shape(shaping, buffer)
    glyphs, cursor, bounds = [], 0, None
    glyphset = font.getGlyphSet()
    for info, position in zip(buffer.glyph_infos, buffer.glyph_positions):
        if info.codepoint == 0:
            points = " ".join(f"U+{ord(char):04X}" for char in value)
            raise ValueError(f"Unsupported glyph in {role}: {points}")
        name = font.getGlyphName(info.codepoint)
        glyph = glyphset[name]
        pen = SVGPathPen(glyphset)
        glyph.draw(pen)
        box = BoundsPen(glyphset)
        glyph.draw(box)
        x, y = cursor + position.x_offset, position.y_offset
        if box.bounds:
            left, bottom, right, top = box.bounds
            current = (x + left, y + bottom, x + right, y + top)
            bounds = (
                current
                if bounds is None
                else (
                    min(bounds[0], current[0]),
                    min(bounds[1], current[1]),
                    max(bounds[2], current[2]),
                    max(bounds[3], current[3]),
                )
            )
        glyphs.append((pen.getCommands(), x, y))
        cursor += position.x_advance
    return tuple(glyphs), cursor, bounds or (0, 0, 0, 0), font["head"].unitsPerEm


def measure(value, size, role="body"):
    _, advance, bounds, units = shaped(str(value), role)
    return max(advance, bounds[2]) * size / units - min(0, bounds[0]) * size / units


def text(
    value,
    x,
    y,
    size=24,
    role="body",
    color=INK,
    max_width=None,
    anchor="start",
    minimum=None,
):
    value = str(value)
    glyphs, advance, bounds, units = shaped(value, role)
    width = max(advance, bounds[2]) - min(0, bounds[0])
    if max_width is not None and width * size / units > max_width:
        fitted = max_width * units / width
        if fitted < (minimum if minimum is not None else size * 0.72):
            raise ValueError(f"Text does not fit {role} field: {value!r}")
        size = fitted
    scale = size / units
    x -= {"start": 0, "middle": advance * scale / 2, "end": advance * scale}[anchor]
    paths = "".join(
        f'<path d="{path}" transform="translate({dx} {dy})"/>'
        for path, dx, dy in glyphs
        if path
    )
    ink_bounds = (
        x + bounds[0] * scale,
        y - bounds[3] * scale,
        x + bounds[2] * scale,
        y - bounds[1] * scale,
    )
    box = " ".join(f"{edge:.4f}" for edge in ink_bounds)
    return f'<g fill="{color}" data-bounds="{box}" aria-label="{html.escape(value, quote=True)}"><title>{html.escape(value)}</title><g transform="translate({x:.4f} {y:.4f}) scale({scale:.8f} {-scale:.8f})">{paths}</g></g>'


def svg(width, height, body, title, background=PAPER):
    definitions = {}

    def reference(match):
        path, transform = match.groups()
        if path not in definitions:
            definitions[path] = f"glyph-{len(definitions)}"
        return f'<use href="#{definitions[path]}" transform="{transform}"/>'

    body = re.sub(r'<path d="([^"]+)" transform="([^"]+)"/>', reference, body)
    glyphs = "".join(
        f'<path id="{identifier}" d="{path}"/>'
        for path, identifier in definitions.items()
    )
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img"><title>{html.escape(title)}</title><defs>{glyphs}</defs><rect width="{width}" height="{height}" fill="{background}"/>{body}</svg>'


def rule(x1, y1, x2, y2, color=RULE, width=1):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>'
