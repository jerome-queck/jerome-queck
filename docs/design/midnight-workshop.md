# Midnight workshop

The profile moves through one cutaway workshop. Each project has a title and short caption. Website titles open their sites, with a separate repository action. Software titles open their repositories. Native text retains all project links and descriptions when images are unavailable.

Wide and narrow SVG masters compose the scene separately. Each master contains named views for the hero and nine rooms. The `full`, `title`, and `source` masters have different intrinsic widths so adjacent native image links meet without a gap on GitHub. A view fragment selects the visible room. Browser verification needs the actual image URL, crop, and rendered pixels. Chrome's `currentSrc` alone did not reliably distinguish fragment views during testing.

Native `<picture>` sources select still masters for reduced motion. Embedded SVG CSS media queries did not honor that preference in the tested GitHub image path. The still and ambient masters share a resting frame. Only small decorative lights animate.

## Artwork provenance

`assets/pixel-world/workshop-original.png` is original artwork generated for this profile with built-in OpenAI ImageGen. Its SHA256 is `9fe259a2184042445935f4dfdf34725e52faebf45d50dc903c248f9915507158`. The environment supplies the pixel artwork. Python composes outlined typography, palette overlays, decorative motion, and view geometry over it. Native README links provide the actual destinations.

`workshop.jpg` is a mechanical 900-pixel, quality-55 JPEG conversion embedded in the SVG masters. It contains no live data. Fonts come from the pinned local OFL sources in `assets/type/manifest.json`, outlined through `scripts/profile_style.py`.

The [poteto process post](https://x.com/poteto/status/2117043478140276847) and [tibo.dog](https://tibo.dog/) informed process and visual research. No game artwork was copied into the profile. External gameplay captures remain research evidence, separate from committed original assets. Earlier avatar candidates remain candidates until a final artwork is selected. No blanket reuse licence has been chosen.

## Catalogue and snapshot boundaries

`data/projects.json` owns selected project names, repository identities, website destinations, and native descriptions. `scripts/render_readme_world.py` owns room order and shorter captions suited to the image layout. Its loader validates the canonical catalogue and requires an exact room match. Four software rooms precede five mathematics rooms.

The root README and workshop masters are authored assets. Scheduled snapshot publication updates the separate `profile-data` branch. A catalogue edit needs regenerated workshop masters and corresponding authored README links. Snapshot refreshes do not rewrite the root README.

The data room uses the same plum, timber, and gold palette with a faint JPEG crop of the cellar. Contribution records and repository measurements come from the completed snapshot. Patch statistics describe entire merged PRs and all their contributors. File changes can repeat. Proposal ages count completed days at snapshot time. Exact records, definitions, and links remain in the native text snapshot. The main profile keeps its open-source receipts compact and leaves extended analytics in that snapshot.

Fifteen required data payloads publish in one Git commit. They comprise nine individual SVGs, four data-room SVGs, `snapshot.json`, and its native `README.md`. Missing payloads prevent publication. Failed collection or rendering retains the prior snapshot and timestamp. Separate CDN caches may refresh at different times. The four data-room variants cover wide and narrow layouts with ambient and still motion.

## Regenerate the authored masters

From the repository root, install `requirements.txt`, then run these commands.

```sh
sips -s format jpeg -s formatOptions 55 --resampleWidth 900 assets/pixel-world/workshop-original.png --out assets/pixel-world/workshop.jpg
python3 -m scripts.render_readme_world
python3 -m unittest tests.test_readme_static tests.test_readme_world
```

The renderer uses repository-relative asset paths. Regenerate the JPEG only when its original source changes. Inspect the SVG diff and verify native links, narrow layout, and reduced-motion selection on GitHub before accepting a visual change. See [data graphic definitions and regeneration](data-graphics.md) for the separate snapshot pipeline.
