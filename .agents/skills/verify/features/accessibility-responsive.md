# Accessibility and responsive layout

## Sub-features

Native heading hierarchy, descriptive image alternatives, ordinary text descriptions, real links and disclosures; responsive `<picture>` selection; legible light/dark content and no horizontal overflow. Source is `README.md`, `assets/`, `scripts/readme_world.py`, `scripts/render_interface.py` and data SVG renderers.

## How to get to it (user POV)

Open either GitHub surface on desktop or a narrow phone. Change system color scheme. Read and navigate with native headings and links; expand every disclosure. Images retain equivalent plain text destinations and descriptions.

## Driving it with Playwright

The matrix covers 1440×1100 and 390×844 in both schemes. Compare actual page background and browser-selected source URL, not merely requested media. Decode all images after opening disclosures; inspect natural and rendered dimensions. Check saved native heading records, alternatives, article/document geometry and full-page images. Inspect each screenshot at readable scale for thin text, clipping and contrast. After outline typography lands, run `--require-outlines yes` and review retained SVG bodies' path/text counts. Manual keyboard and screen-reader use remains separate unless actually performed and recorded.

## Gotchas

A large raster or SVG may decode while text is unreadable at mobile width. GitHub sanitizes embedded HTML and proxies images; local HTML tests cannot prove this surface. A responsive declaration is insufficient without checking the selected file in `currentSrc`. Strip fragments only for file comparison; retain all original URLs and review separately captured view bitmaps and SVG view declarations. Full-page screenshots require scrolling to paint long offscreen content; the driver does that. Contrast cannot be inferred from the requested scheme alone. Treat visual defects as failures even if scripted geometry passes.

Motion: review all saved actual embedded-image frame comparisons. Hero or an interior room must show decorative motion. Generated data must stay static. Every fresh reduced-motion picture must choose its still source, and the full canvas must stay pixel-identical. Inspect retained source CSS and `world-data` boundary: animation selectors may affect decorative scene elements only. Review opaque coverage and narrow readability manually. With images blocked, native projects, public records, links and disclosure controls remain usable.

The canvas must fill each row without gaps or overflow, including all five 75/25 title/source pairs. Mobile image links need at least 44 CSS pixels in each dimension. Native text-edition fallback retains nine descriptions, PR receipts and actual records-source link. Required headings and disclosure names must be nonempty; no obsolete heading wording or disclosure count is imposed. Geometry cannot establish typography legibility or manual screen-reader behavior.
