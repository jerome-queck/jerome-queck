# Circuit Atlas

Personal profile only. The Owner rejected the initial project-name tree and the later editorial layout. The new composition uses an original cinematic masthead, graphic chapter navigation, a precise mathematical exhibit, a verified software circuit and prominent automatically generated data. Mathematics and software remain equally important.

The full-page concept is a visual target, not a screenshot or factual source. Its fabricated model captions and illustrative plots are not published. An independent design review chose Circuit Atlas but rejected its repetitive card rows. The implementation varies a panorama, linked destination bands, an exact diagram, an illustrated flow and data panels. [Primary design research](../research/heavily-designed-readmes.md).

## Authored assets

- `assets/circuit-atlas-hero.jpg` is original built-in ImageGen artwork, compressed to JPEG with `sips`. Its chrome loop is an illustration, not a claim about a particular mathematical surface.
- `assets/software-circuit.jpg` and its separately recomposed portrait `assets/software-circuit-mobile.jpg` are original built-in ImageGen artwork. The source integration evidence is recorded in [personal-redesign-evidence.md](../research/personal-redesign-evidence.md). A targeted edit removed two incorrect lower arrowheads. Remaining lower routes point from Syrax toward the two queried tools. This is an illustration of interfaces, not a product screenshot or formal proof.
- Decorative chapter folios, navigation, destination links and the closing strip come from `python3 -m scripts.render_interface`. They contain authored interface text and diagram structure, no live metrics.
- Exact square rotation/reflection figures come from `scripts/render_math_plate.py`, with pinned optional dependencies in `graphics-requirements.txt`. Run `uv run --with-requirements docs/design/graphics-requirements.txt python -m scripts.render_math_plate`. The point transforms are tested independently.
- `assets/syrax-exhibit.jpg` and `assets/emmy-exhibit.jpg` are separately linked original built-in ImageGen illustrations. They depict a signal/search tool and a context/evidence dossier. They are not screenshots or new feature claims. The Emmy exhibit deliberately inverts the surface to ivory.
- `assets/exit.svg` is the designed closing link to the website.
- Earlier covers and project captures remain historical evidence. No blanket artwork licence is selected.

The five ImageGen assets are stable authored files. They do not regenerate daily and a repeated prompt will not reproduce identical pixels. Update artwork and its native alternatives together when the depicted interfaces change.

## Final hero prompt

Built-in ImageGen, referenced the selected full-page Circuit Atlas concept.

> Make the FINAL production hero image asset only for Jerome Queck's personal GitHub README. Target 2400 x 800, wide 3:1 banner. Reference image is the selected Circuit Atlas full-page visual target, use only its TOP masthead art direction; do not output the full page, project tiles, navigation, metrics, quotations, dates or any lower sections. Recompose a new extremely polished oversized typographic panorama rather than crop the reference. Black subtle textured background, sharp orange-red and warm ivory text, original sculptural chrome twisted mathematical loop dramatically lit orange at the right, very large forward-leaning condensed technical sans-serif typography occupying left two-thirds. Exact text only JEROME on top line and QUECK beneath, and small subtitle MATHEMATICS × SOFTWARE below. Spelling J E R O M E / Q U E C K. Add restrained precise thin technical linework and small corner ticks, no tiny pseudo-text, no quotes or invented slogans. Clear generous edges, full name readable on mobile. No logos, protected brand shapes, checkered flags, cars, people, signatures, ratings, project names, extra glyphs or watermark. Keep the original high-energy motorsport/cinema-inspired design character without copying any brand. Final self-contained banner on opaque near-black background, not screenshot or UI mockup.

## Software illustration prompt

Built-in ImageGen, referenced the final masthead for palette and materials.

> FINAL production illustrated software relationship diagram for a personal GitHub README, 2400x1200 wide landscape. Same near-black field, chrome and orange-red materials, warm ivory typography, tiny acid-yellow accents, precise industrial linework. Create three very large physical 3D illustrated modules horizontally with clear directional arrows left to right. Left a stack of original documents inside a translucent orange inbox, labelled exactly NTULEARN SYNC. Centre organized local folders in a mechanical file tray, labelled exactly LOCAL MODULE FOLDERS. Right a chrome checklist mechanism with a small orange verification lens, labelled exactly ACADEMIC OS. The left-to-centre arrow means saves material, centre-to-right arrow means reads sources; put these exact short labels above respective arrows. Below the three, one smaller connected chrome sphere labelled exactly SYRAX with subtitle queries both tools. Two thin orange arrows originate from SYRAX and point upward to NTULEARN SYNC and ACADEMIC OS, respectively. No connection from Syrax to the folders. Do not use bidirectional arrows. No Emmy in this diagram, it is a separate tool outside this connected pipeline. No fake UI screenshot, terminal text, invented product screens, metrics, external logos or protected brand shapes. Header exact text FROM COURSE MATERIAL TO A LOCAL DESK. Footer exact text Files on disk are not evidence of learning. All labels should be large, immaculate and fully readable at 900px display width. Distinctive cinematic diagram with beautifully rendered subject-specific objects, not plain rectangles. Graphic clarity and accurate arrow endpoints matter more than ornament. No extra text, no pseudo-text, no date or watermark.

Targeted edit prompt:

> Preserve ALL imagery, composition, dimensions, type, labels, colors, modules, text and upper left-to-right arrows exactly. Change ONLY the two small lower horizontal arrowheads next to the SYRAX sphere: REMOVE the small right-facing arrowhead immediately to the left of the sphere, and REMOVE the small left-facing arrowhead immediately to the right of the sphere. Keep those horizontal orange lines as plain continuous lines. The only arrowheads on the lower two orange routes should be the UPWARD arrowheads pointing at NTULEARN SYNC and ACADEMIC OS. Routes must therefore originate at Syrax and point only upward at each tool. No other modifications.

## Generated data

`data/projects.json` is the authored selection and description catalogue. `python3 -m scripts.profile_data <empty-output-directory>` reads public GitHub sources through `gh`, collects every source before rendering, and produces eleven payloads. `snapshot.json` preserves the minimal public input for deterministic image and text regeneration with `render_snapshot(snapshot)`.

The workflow runs daily and manually. A read-only collection job uploads the complete output; a separate main-only job copies and stages an explicit eleven-file allowlist and pushes one non-force Git commit to `profile-data`. No additional token or scheduler is introduced. Missing inputs, API failures and missing publication payloads prevent a new remote snapshot. The previous successful timestamp remains. API calls are separate observations during a recorded interval, not an atomic GitHub read. CDN cache timing remains independent.

Repository pulse reads only nine explicitly selected public identities. It fully enumerates releases, includes labelled prereleases and distinguishes no release from request failure. Default-branch tip dates are Git committer dates, by any author. The twelve-month merge chart reuses the complete authored-merged-PR traversal, excludes private records, includes zero months and marks the current month partial. The 365-day calendar has native exact daily values and an explicit relative color scale. Failed refreshes do not conceal errors with zeroes.

## Verification boundary

Tests exercise privacy, release pagination/selection, merge-date windows, escaped/bounded text, reproducible rendering and whole-publication failure behavior. Inspect the actual generated images, not just test status. Inspect actual GitHub desktop/mobile light/dark rendering before publication. Source inspection, Markdown sanitization and local SVG rendering do not establish assembled behavior. Verify chapter buttons against the generated heading IDs, responsive image selection, loaded images and expanded details.

[Bounded publication lifecycle and its limits](publication-lifecycle.md) records the statechart and deliberate mixed-generation mutation. It describes refresh publication, not the broader project identity.


## Assistant exhibit prompts

Built-in ImageGen. Each used the final masthead as a palette/material reference. No data values were generated in these assets.

Syrax prompt:

> FINAL original graphical project exhibit for a personal GitHub README, 2400x800 wide 3:1. Project SYRAX, a Telegram assistant built on OpenClaw with file search and an academic desk that can query NTULearn Sync and Academic OS. This is illustrative art, no product screenshot. Carry reference masthead's chrome, near-black, orange-red and ivory high-energy design. Distinct asymmetrical composition with huge italic condensed word SYRAX at left, subtitle exactly TELEGRAM ACADEMIC DESK and small line FILE SEARCH + TOOL QUERIES. At right, original polished chrome signal orb with a few precise orange routes to a document stack, a magnifying lens and an abstract pair of terminal-like physical ports, all sculptural not UI screenshots. These objects symbolize the verified features, no extra claims or invented project names. Large clean text readable at 900px; no small pseudo-text, no logos, no robot face, no fantasy scene, no other names, metrics, statuses, dates, app controls, trademark imagery or watermark. This is a substantial visual exhibit with three-dimensional material detail, not a black rounded card or a text-only banner. Keep plenty of clean room around the typography.

Emmy prompt:

> Final original project exhibit for a personal GitHub README. 2400x800 wide 3:1 composition. Project EMMY, an operating kit for ChatGPT Dot that provides responsibility context and current evidence checks, not an autonomous robot or its own execution engine. Use the reference's original orange-red, ivory, chrome, sharp condensed typography and precise industrial linework, but deliberately INVERT the surface to warm ivory with charcoal and orange typography so this exhibit contrasts with the dark Syrax panel. Huge exact text EMMY at left, subtitle OPERATING KIT FOR CHATGPT DOT. Smaller exact line CONTEXT + CURRENT EVIDENCE. Right third has a sophisticated physical ivory folded field dossier with chrome edges, orange translucent evidence tabs and one precise orange lens resting on top; sculptural still life, not a fake software screenshot, not a product mockup with imaginary controls or labels. Native products own execution and permissions, so no workflow arrows, no agent controlling other projects, no invented project names, metrics or powers. No robot, face, logos, extra tiny text, protected branding or watermark. Readable at GitHub's 900px content width and on mobile. Polished abundant material detail but uncluttered, a distinct visual exhibit rather than an equal text-only card.


## Mobile software illustration prompt

Built-in ImageGen, referenced the final desktop software illustration.

> Recompose this verified software relationship illustration as a FINAL portrait MOBILE asset, target 960x1600, no device bezel or browser. Preserve the chrome/orange/near-black material style and exactly the same three software relationships. Do not squash or crop the wide artwork. Use original physically rendered document inbox at TOP labelled exactly NTULEARN SYNC; organized local folder tray at MIDDLE labelled exactly LOCAL MODULE FOLDERS; checklist with verification lens BELOW labelled exactly ACADEMIC OS. Large orange DOWN arrows connect inbox to folders then folders to checklist. Below those three, a smaller chrome SYRAX signal sphere has TWO separate thin orange routes that go up the RIGHT outside edge and point LEFT into NTULEARN SYNC and ACADEMIC OS respectively. They originate from Syrax; there must be NO arrowheads at Syrax and no connection to the folders. A large bottom caption exactly SYRAX QUERIES BOTH TOOLS can clarify those two routes. Use large perfectly readable high-contrast lettering, with the long LOCAL MODULE FOLDERS label broken over two lines if needed. At top a compact headline exactly COURSE MATERIAL → LOCAL DESK. No formats/subtitles, metrics, extra labels, Emmy, product screenshots or invented features. Avoid small pseudo-text on documents; use plain abstract lines on paper. The three large objects should occupy most of the portrait frame, with orderly spacious separation. This needs to remain handsome and readable at 308px display width. No protected branding, logos, decorative card rectangles, watermark or extra text.


Actual GitHub browser inspection found that image-only chapter headings were unnamed in the accessibility snapshot. GitHub also strips a custom heading aria-label. Plain native text now names each H2. A small decorative number folio with an empty alternative sits outside the heading; including it inside changed GitHub’s generated permalink and broke the chapter buttons. This preserves chapter navigation and permits meaningful heading navigation without repeating a giant title graphic.
