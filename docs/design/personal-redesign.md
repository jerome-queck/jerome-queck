> Historical design record. The Owner rejected this direction. [Circuit Atlas](circuit-atlas.md) is the current implementation; earlier prototypes remain separate.

# Editorial personal profile

Owner feedback, 1 November 2026. The old project-tree image repeated the native lists and the
atmospheric banner did not change the composition enough. Organisation work was cancelled.
The personal replacement uses an editorial monograph direction, selected autonomously under
the Owner's full-control instruction.

## What earns its place

The cover establishes identity with large serif typography, pale paper and vermilion geometry.
Native chapter links let a visitor jump directly to mathematics, software, upstream work or
activity. The mathematical plate demonstrates noncommutativity with exact point transforms.
It explains a fact rather than displaying the projects a second time.

The square starts with its top-right corner at (1,1). A quarter-turn anticlockwise maps
(x,y) to (-y,x). Reflection across the horizontal axis maps (x,y) to (x,-y). Rotation then
reflection ends at (-1,-1); the reverse order ends at (1,1). Ringed corners mark the start,
filled red markers the result. Matplotlib generates both layouts, not Image Gen, so coordinates
and labels come from the same explicit transforms. Native alt text explains the full result.

The source-supported software story is course material becoming local sources, Academic OS
checking those sources, and Syrax querying the tools. Emmy remains a separate advisory operating
kit. Availability is not learning, and no unsupported integration is drawn.

Contribution panels use a horizontal desktop composition and a stacked mobile composition from
the same counts and timestamp. Calendar and event data use the same paper/ink palette. The
unrelated upstream repository-stat card and its Action dependency are removed. Existing metric
scopes, source filters, two-event limit and failure preservation remain.

## Asset provenance

Built-in imagegen produced `assets/editorial-cover.jpg`, delivered as a 1600px-wide JPEG using
`sips -s format jpeg -s formatOptions 90 --resampleWidth 1600 INPUT --out OUTPUT`.
No CLI/API fallback, compositing or creative retouching was used. No blanket licence is selected.
The old landscape remains historical; the project-map asset and its generator were removed.

Final cover prompt:

> Use case: logo-brand. Asset type: final typographic cover image for Jerome Queck's GitHub personal README. Wide 3:1 landscape, 1800x600 intended. Produce ONLY the cover, no screenshot, no browser, no page mock. Design a striking editorial mathematical monograph masthead. Warm very pale ivory paper #f6f1e9, rich near-black ink. On left two thirds, enormous elegant high-contrast serif typography, impeccably typeset, two lines. Exact text only: "JEROME" on first line, "QUECK" on second. The title must dominate, no cramped small labels. At the right, one spare original black-ink square construction, four tiny red corner marks and two restrained vermilion directional arcs suggest rotation and reflection; this is a decorative construction, no equations or factual labels. Use generous geometric negative space and one razor-thin red editorial rule across the lower edge. Print-like precision, minimal subtle paper grain, no fake wear. No other words, dates, metrics, edition numbers, logos, brands, people, fantasy landscape, dashboard or drop shadows. This must feel intentionally composed, distinctive and legible at 308px total display width. Preserve exact spelling J-E-R-O-M-E Q-U-E-C-K. No signature or watermark.

## Regenerate

```sh
uv run --with-requirements docs/design/graphics-requirements.txt python -B scripts/render_math_plate.py
python3 -B -m scripts.profile_data generated
python3 -B -m unittest discover -s tests
```

Matplotlib is optional authoring tooling, pinned in graphics-requirements.txt. It is not imported
by the daily data workflow. Exact-transform tests run without it. Commit updated mathematical
PNGs with any source change. Authored art stays on main; data stays on profile-data.

GitHub picture/source selects layouts below 600px. Native image descriptions, project links,
case notes and the generated text snapshot retain meaning without graphics. Do not claim mobile,
theme or actual-profile verification from the mockups, file metadata or Markdown API alone.
