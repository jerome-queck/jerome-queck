# Screenshot provenance

Captured directly from the live public sites on 2026-09-10 using the in-app browser. No image generation, compositing, or retouching. The captures contain rendered site content, not course PDFs or private account pages.

- `algebra.jpg`: [Four cube actions](https://algebra.jeromegroup.org/#cube-four-actions), Understand tab; four diagonal action, full group, identity transformation.
- `calculus.jpg`: [The gradient points uphill and across contours](https://calculus.jeromegroup.org/#gradient-normals-and-steepest-ascent), default gradient experiment after resetting the camera. The live course overview also shows Calculus I, II and III.

Both captures use the same desktop viewport. The README links each screenshot to the depicted lesson; descriptions remain ordinary text. Screenshots are snapshots, not a claim that the live interface stays unchanged. No blanket reuse licence is selected.

## Superseded profile assets, 31 October 2026

`control-room.jpg` is original generated artwork. The removed `project-map.svg` came from the former authored
registry in `scripts/render_identity.py`. Both survive in Git history. See [prompts and maintenance](../docs/design/profile-refresh.md).
The historical project screenshots above are retained as evidence and are not embedded.

## Editorial redesign, 1 November 2026

The active cover is `editorial-cover.jpg`. The exact mathematical figures are
`order-matters.png` and `order-matters-mobile.png`, generated with Matplotlib from
quarter-turn and reflection transforms. The project-tree graphic and its generator
were removed. The earlier atmospheric banner is historical and no longer embedded.
See [current design and provenance](../docs/design/personal-redesign.md).

## Circuit Atlas, 1 November 2026

The editorial cover above is superseded and retained historically. Active artwork is
`circuit-atlas-hero.jpg`, `software-circuit.jpg`, `software-circuit-mobile.jpg`, `syrax-exhibit.jpg` and `emmy-exhibit.jpg`, produced with built-in ImageGen.
The software image depicts verified interfaces, not a screenshot. Exact prompts and a
corrective arrow edit are recorded in [Circuit Atlas](../docs/design/circuit-atlas.md).
Decorative numbered `chapter-*.svg` folios, `nav-*.svg`, `enter-*.svg` and `exit.svg` come from
`scripts/render_interface.py`; the square-transform figures retain their exact mathematics
with the new palette. Generated live data remains on `profile-data`, separate from authored art.

## Typography data core and avatar candidate, 2 November 2026

The field-journal composition was a rejected prototype. Its proposed masthead and diagram assets are not embedded or committed here. Existing Circuit Atlas assets above remain historical source material for the next composition review. The new data charts use locally outlined Fraunces, Source Sans 3 and IBM Plex Mono through `scripts/profile_style.py`.

`type/manifest.json` records font sources pinned to exact Google Fonts commits, SHA256 hashes, axes and OFL licenses. The actual font files and licenses are local. Graphic letters are shaped with uharfbuzz 0.43.0 and HarfBuzz 10.1.0, then outlined with fontTools 4.55.3. Individual glyph paths are reused inside each SVG. No font loads from a CDN at runtime. Native Markdown retains descriptions, exact dynamic text and individually usable links. See [data graphic definitions and regeneration](../docs/design/data-graphics.md).

`avatar-jq.jpg` is a separate built-in ImageGen candidate generated on 2 November 2026 for review before manual profile upload. The source PNG is external session evidence; JPEG conversion changes the encoding, not the artwork. The brief was a bold JQ typographic monogram using warm ivory, dark aubergine and cobalt. The generator's exact prompt remains in the task's tool history. No claim of a public reuse license accompanies it.

## Midnight workshop, 2 November 2026

`pixel-world/workshop-original.png` is the original built-in OpenAI ImageGen environment for the active cutaway workshop. Its SHA256 is `9fe259a2184042445935f4dfdf34725e52faebf45d50dc903c248f9915507158`. `pixel-world/workshop.jpg` is its mechanical 900-pixel, quality-55 JPEG conversion.

`scripts/render_readme_world.py` embeds that JPEG in twelve SVG masters. Wide and narrow layouts each have full, title, and source views in ambient and still variants. Code supplies outlined typography, overlays, light animation, and view geometry. The root README supplies native image links. The environment's pixels come from ImageGen.

The [poteto process post](https://x.com/poteto/status/2117043478140276847) and [tibo.dog](https://tibo.dog/) were research references. Their artwork is not included in these assets. See [workshop provenance and regeneration](../docs/design/midnight-workshop.md). Historical assets above are retained separately from the active workshop. No blanket reuse licence has been selected.
