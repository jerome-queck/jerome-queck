---
name: verify
description: Drive Jerome Queck's actual public GitHub profile and repository README, generated contribution publication, and collector CLI. Use after profile artwork, README, renderer, or data workflow changes.
---

# Verify the public profile

Read [every mapped feature](features/README.md) first. The primary surface is GitHub's rendered profile at `https://github.com/jerome-queck`. The repository README is a second required GitHub surface. The collector CLI is secondary. There is no local app server. Local HTML or SVG previews cannot prove GitHub rendering, sanitization, image proxy behavior, links, or publication.

## Launch

Run from this repository's root. Choose an external evidence parent and runtime directory. These concrete commands use temporary directories; print and retain their resulting paths in the run report.

```sh
PROFILE_EVIDENCE=$(mktemp -d /tmp/profile-evidence.XXXXXX)
PROFILE_RUNTIME=$(mktemp -d /tmp/profile-runtime.XXXXXX)
npm install --prefix "$PROFILE_RUNTIME" --no-audit --no-fund --save-exact playwright@1.62.1 pngjs@7.0.0
export NODE_PATH="$PROFILE_RUNTIME/node_modules"
python3 -m venv "$PROFILE_RUNTIME/python"
PROFILE_PYTHON="$PROFILE_RUNTIME/python/bin/python"
"$PROFILE_PYTHON" -m pip install -r requirements.txt
node -e 'console.log(require("playwright/package.json").version)'
"$PROFILE_PYTHON" .agents/skills/verify/scripts/doctor.py --plan
```

Node 20+ and Python 3.10+ with the pinned requirements suffice. The external virtual environment supplies HarfBuzz, fontTools and Pillow; a bare system Python is insufficient for collection or rendering. `npx` must exist before setup. This reusable Playwright library driver runs a complete browser matrix; it uses no Playwright test fixtures. By default it launches installed Chrome in a separate headless process. If Chrome is absent, install the pinned browser into the external runtime and use `--channel chromium` on each drive.

```sh
export PLAYWRIGHT_BROWSERS_PATH="$PROFILE_RUNTIME/browsers"
node "$PROFILE_RUNTIME/node_modules/playwright/cli.js" install chromium
```

An existing Codex bundled Playwright 1.62.1 may substitute for the install. Resolve its actual Node executable and package directory with `load_workspace_dependencies`; set `NODE_PATH` to that directory. Never commit machine-specific runtime paths. Readiness means doctor sees HTTP 200 and a rendered Markdown article, then the browser sees the article and first decoded image. Browser contexts are anonymous and owned by this invocation; shared MCP sessions are unnecessary.

## Doctor

```sh
"$PROFILE_PYTHON" .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck
"$PROFILE_PYTHON" .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck/jerome-queck/blob/main/README.md
```

Record the source head and dirty state. Doctor performs only GET and Git reads. `--plan` performs no network, starts no service, writes no files, and prints what a later drive would do. On a surprising result, rerun doctor before retrying in a fresh evidence directory. A GitHub 404, authentication wall or unavailable README is a page failure, separately from an undecoded image or failed asset request. Never sign in or substitute a local rendering to clear a failure.

## Drive

```sh
node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck --output "$PROFILE_EVIDENCE/profile" --mode read-only
node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck/jerome-queck/blob/main/README.md --output "$PROFILE_EVIDENCE/repository" --mode read-only
```

For a proposed branch, replace the second URL with its actual GitHub rendered README URL, for example obtain it from the open PR's head branch, then supply it as `--url`. A private/unpushed head cannot be verified anonymously; report that prerequisite. The live profile still proves the deployed main README, never the proposed head. Record both source head and target URL rather than equating them.

The README canvas is one paragraph containing sixteen images. It has one hero, four full-width software title links, five website title/repository pairs (75/25 widths), then the generated data world. Native text-edition disclosure supplies nine descriptions, six merged upstream receipts, separately labelled open proposals and the public-records source. Chapter image buttons were replaced by direct project links. Native section links are optional; every one present must still scroll to its uncovered heading.

The driver checks eleven canvas rows, exact shared tile edges and no vertical gaps within one CSS pixel. It records mobile image-anchor hit areas and requires 44 CSS pixels in both directions. Geometry does not prove readable fonts, visual button boundaries or sufficient contrast. Review screenshots.

Normal contexts capture hero and one interior room at 0, 2.3 and 5 seconds and require visible decorative movement in at least one. The generated data image must retain identical pixels across its three frames. Fresh reduced-motion contexts inspect every picture's selected wide/mobile still file and capture the entire canvas three times with zero decoded pixel changes. SVG inspection distinguishes authored masters from generated data. Masters expose real nonduplicate `<view>` boxes; only decorative circles may animate. Still files contain no style or animation. Generated worlds expose `data-snapshot` and a static `world-data` boundary and need no animation.

Each drive uses desktop 1440×1100 and mobile 390×844, each in light and dark. It checks actual background, meaningful headings, named disclosure controls, profile avatar, decoded images, selected picture files, optional native section navigation, disclosure clicks, overflow, alternatives and actual destination clicks. After outlined typography ships, add `--require-outlines yes` to require paths and prohibit SVG `<text>` in all selected SVG assets. Visual review still checks legibility and opaque coverage.

Browser file selection and SVG fragment selection are separate evidence. Chrome can report the first cached fragment in `img.currentSrc` for later views of the same file. The driver retains unchanged `src`, source declarations and `currentSrc`; file comparison strips only the hash. It separately requires the declared view ID and unique viewBox, and retains each rendered tile screenshot and hash. Review those screenshots for actual distinct crops. Matching file URLs alone never proves the intended fragment rendered.

GitHub profile native anchors have a 64-pixel scroll margin; the repository README SPA currently settles around 125 pixels despite a zero CSS margin. The near-top band accepts both observed behaviors while rejecting a heading merely somewhere in the viewport.

The driver clicks nine project-title images, five secondary source images and all six merged PR anchors, then discovers the actual records-source link by its rendered text. Anonymous website 401/403 responses are retained as `verified-unreachable` with that prerequisite; repository responses must succeed. It follows the source page’s actual snapshot anchor, including preview-hosted data directories. Preview proof never establishes production publication. The driver opens all disclosures before checking their images. It scrolls the page to paint images before full screenshots. It reads the actual browser-selected asset URLs, not guessed source paths. Read JSON and screenshots together; inspect hierarchy, art legibility, clipping, light/dark contrast and statistics wording. A decoded image alone cannot prove its text is readable or accurate. Follow the feature maps for remaining manual review and CLI checks. Exit zero means the scripted checks passed, not that every editorial or data accuracy judgment passed.

Secondary collector verification requires an authenticated `gh` with public GraphQL access. Check `gh auth status` without printing tokens, then explicitly invoke collection into external scratch output. This runs GET-only GitHub API queries and writes local artifacts; it never publishes. There is no collector dry-run flag.

```sh
gh auth status
GH_TOKEN="$(gh auth token)" "$PROFILE_PYTHON" -m scripts.profile_data "$PROFILE_EVIDENCE/collected"
"$PROFILE_PYTHON" -m unittest discover -s tests
```

Verify the emitted fifteen named payloads (the prior eleven plus four static data-world SVGs) against `.github/workflows/profile.yml`, inspect `snapshot.json`, and compare accessible `README.md` with generated SVG counts/dates. Collection failure must leave the published branch unchanged. Successful local generation does not prove the `publish` job, branch protection, CDN convergence or scheduled execution. Those require actual workflow run and publication readback, recorded separately.

## Evidence

The chosen external parent retains `report.json`, timestamp, checkout source head, browser and Playwright versions, original/final URLs, four before/expanded JSON states, full screenshots, action screenshots/states, destination screenshots/text and SVG response bodies. Each image record includes geometry, natural dimensions, alt, currentSrc and matching source media. Report failures by kind. Keep failed iterations too. Never overwrite an earlier output directory. Artifacts can contain the public content visited; no authenticated browser state is used.

Before completion, read every map's proof conditions and identify any condition not exercised. Record product gaps separately from harness drift. Do not change assertions or maps to make a broken product pass. Browser links that return native GitHub 404 are destination failures; image network errors are asset failures. Screenshots of sign-in or error pages prove unreachability only.

## Cleanup

The driver closes its own browser and contexts in `finally`, including failed drives. It owns no persistent profile, server, port or launch service. Do not kill processes by name. If the terminal itself was interrupted, terminate only the process/session this run launched. Evidence survives cleanup.

```sh
test -s "$PROFILE_EVIDENCE/profile/report.json"
test -s "$PROFILE_EVIDENCE/repository/report.json"
```

After checking retained evidence, the optional runtime directory may be deleted using its exact recorded path. Never delete the evidence parent. Keep output paths in the handoff.

## Helpers

- `"$PROFILE_PYTHON" .agents/skills/verify/scripts/doctor.py --plan` prints the read-only local plan.
- `"$PROFILE_PYTHON" .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck` checks source and target readiness.
- `node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck --output "$PROFILE_EVIDENCE/profile" --mode read-only` runs the anonymous browser matrix.
- `node --test .agents/skills/verify/scripts/drive.test.cjs` checks the read-only and external evidence boundary guards.

## Maintenance

Run the installed `maintain-verification-skill` after README destinations, project registry, image payload names, renderers, collector semantics, GitHub DOM, or publication workflow changes. Resolve its current installed `SKILL.md`; plugin versions move. No automation is created. A concrete refresh request is “Maintain `.agents/skills/verify`, compare every feature map with this checkout, drive both actual GitHub surfaces in all four variants, preserve external evidence, and report clean, changed or blocked.”

Maintenance edits only this skill directory. Check index hygiene, obtain per-feature source coverage, reconcile missing surfaces against concrete source, then one coordinator drives all features. Use parallel readers only when authorized; otherwise record sequential source review and its limitation. Recheck doctor after failures, re-drive every harness correction, retain failed evidence, and update [coverage](coverage.json) only with observed source/target facts. Product regressions stay product gaps. Reread source and maps after every source-head change; a stale coverage head proves only its recorded baseline. No schedule, sign-in, publication or repository mutation is implied.
