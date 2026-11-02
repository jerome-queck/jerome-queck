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
npm install --prefix "$PROFILE_RUNTIME" --no-audit --no-fund --save-exact playwright@1.62.1
export NODE_PATH="$PROFILE_RUNTIME/node_modules"
node -e 'console.log(require("playwright/package.json").version)'
python3 .agents/skills/verify/scripts/doctor.py --plan
```

Node 20+ and Python 3.10+ suffice. `npx` must exist before setup. This reusable Playwright library driver runs a complete browser matrix; it uses no Playwright test fixtures. By default it launches installed Chrome in a separate headless process. If Chrome is absent, install the pinned browser into the external runtime and use `--channel chromium` on each drive.

```sh
export PLAYWRIGHT_BROWSERS_PATH="$PROFILE_RUNTIME/browsers"
node "$PROFILE_RUNTIME/node_modules/playwright/cli.js" install chromium
```

An existing Codex bundled Playwright 1.62.1 may substitute for the install. Resolve its actual Node executable and package directory with `load_workspace_dependencies`; set `NODE_PATH` to that directory. Never commit machine-specific runtime paths. Readiness means doctor sees HTTP 200 and a rendered Markdown article, then the browser sees the article and first decoded image. Browser contexts are anonymous and owned by this invocation; shared MCP sessions are unnecessary.

## Doctor

```sh
python3 .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck
python3 .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck/jerome-queck/blob/main/README.md
```

Record the source head and dirty state. Doctor performs only GET and Git reads. `--plan` performs no network, starts no service, writes no files, and prints what a later drive would do. On a surprising result, rerun doctor before retrying in a fresh evidence directory. A GitHub 404, authentication wall or unavailable README is a page failure, separately from an undecoded image or failed asset request. Never sign in or substitute a local rendering to clear a failure.

## Drive

```sh
node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck --output "$PROFILE_EVIDENCE/profile" --mode read-only
node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck/jerome-queck/blob/main/README.md --output "$PROFILE_EVIDENCE/repository" --mode read-only
```

For a proposed branch, replace the second URL with its actual GitHub rendered README URL, for example obtain it from the open PR's head branch, then supply it as `--url`. A private/unpushed head cannot be verified anonymously; report that prerequisite. The live profile still proves the deployed main README, never the proposed head. Record both source head and target URL rather than equating them.

Each drive uses desktop 1440×1100 and mobile 390×844, each in light and dark. It checks actual background color, native headings, the actual account avatar on the profile, decoded nonzero images, chosen picture source, chapter link clicks and heading arrival in the top 160 pixels (or the larger CSS scroll margin), with an uncovered heading, disclosure clicks, overflow, text alternatives, and GET destination navigation through actual rendered links. It records SVG path/text counts without assuming a font or palette. After outlined typography ships, add `--require-outlines yes` to require paths and prohibit SVG `<text>` in authored navigation assets. This optional requirement does not claim that all illustrated data must be outlines.

GitHub profile native anchors have a 64-pixel scroll margin; the repository README SPA currently settles around 125 pixels despite a zero CSS margin. The near-top band accepts both observed behaviors while rejecting a heading merely somewhere in the viewport.

The driver opens all disclosures before checking their images. It scrolls the page to paint images before full screenshots. It reads the actual browser-selected asset URLs, not guessed source paths. Read JSON and screenshots together; inspect hierarchy, art legibility, clipping, light/dark contrast and statistics wording. A decoded image alone cannot prove its text is readable or accurate. Follow the feature maps for remaining manual review and CLI checks. Exit zero means the scripted checks passed, not that every editorial or data accuracy judgment passed.

Secondary collector verification requires an authenticated `gh` with public GraphQL access. Check `gh auth status` without printing tokens, then explicitly invoke collection into external scratch output. This runs GET-only GitHub API queries and writes local artifacts; it never publishes. There is no collector dry-run flag.

```sh
gh auth status
GH_TOKEN="$(gh auth token)" python3 -m scripts.profile_data "$PROFILE_EVIDENCE/collected"
python3 -m unittest discover -s tests
```

Verify the emitted eleven named payloads against `.github/workflows/profile.yml`, inspect `snapshot.json`, and compare accessible `README.md` with generated SVG counts/dates. Collection failure must leave the published branch unchanged. Successful local generation does not prove the `publish` job, branch protection, CDN convergence or scheduled execution. Those require actual workflow run and publication readback, recorded separately.

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

- `python3 .agents/skills/verify/scripts/doctor.py --plan` prints the read-only local plan.
- `python3 .agents/skills/verify/scripts/doctor.py --url https://github.com/jerome-queck` checks source and target readiness.
- `node .agents/skills/verify/scripts/drive.cjs --url https://github.com/jerome-queck --output "$PROFILE_EVIDENCE/profile" --mode read-only` runs the anonymous browser matrix.
- `node --test .agents/skills/verify/scripts/drive.test.cjs` checks the read-only and external evidence boundary guards.

## Maintenance

Run the installed `maintain-verification-skill` after README destinations, project registry, image payload names, renderers, collector semantics, GitHub DOM, or publication workflow changes. Resolve its current installed `SKILL.md`; plugin versions move. No automation is created. A concrete refresh request is “Maintain `.agents/skills/verify`, compare every feature map with this checkout, drive both actual GitHub surfaces in all four variants, preserve external evidence, and report clean, changed or blocked.”

Maintenance edits only this skill directory. Check index hygiene, obtain per-feature source coverage, reconcile missing surfaces against concrete source, then one coordinator drives all features. Use parallel readers only when authorized; otherwise record sequential source review and its limitation. Recheck doctor after failures, re-drive every harness correction, retain failed evidence, and update [coverage](coverage.json) only with observed source/target facts. Product regressions stay product gaps. Reread source and maps after every source-head change; a stale coverage head proves only its recorded baseline. No schedule, sign-in, publication or repository mutation is implied.
