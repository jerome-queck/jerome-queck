# Accessibility and responsive layout

## Sub-features

Native heading hierarchy, descriptive image alternatives, empty alternatives for decorative folios, ordinary text descriptions, real links and disclosures; responsive `<picture>` selection; legible light/dark content and no horizontal overflow. Source is `README.md`, `assets/`, `scripts/render_interface.py` and data SVG renderers.

## How to get to it (user POV)

Open either GitHub surface on desktop or a narrow phone. Change system color scheme. Read and navigate with native headings and links; expand every disclosure. Images retain equivalent plain text destinations and descriptions.

## Driving it with Playwright

The matrix covers 1440×1100 and 390×844 in both schemes. Compare actual page background and browser-selected source URL, not merely requested media. Decode all images after opening disclosures; inspect natural and rendered dimensions. Check saved native heading records, alternatives, article/document geometry and full-page images. Inspect each screenshot at readable scale for thin text, clipping and contrast. After outline typography lands, run `--require-outlines yes` and review retained SVG bodies' path/text counts. Manual keyboard and screen-reader use remains separate unless actually performed and recorded.

## Gotchas

A large raster or SVG may decode while text is unreadable at mobile width. GitHub sanitizes embedded HTML and proxies images; local HTML tests cannot prove this surface. A responsive source declaration is insufficient without checking `currentSrc`. Full-page screenshots require scrolling to paint long offscreen content; the driver does that. Contrast cannot be inferred from the requested scheme alone. Treat visual defects as failures even if scripted geometry passes.
