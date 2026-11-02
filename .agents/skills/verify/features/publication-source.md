# Publication and source

## Sub-features

GET-only authenticated collector; complete saved input; generated SVG and accessible text agreement; fail-before-publish; scheduled/manual collection; main-only publication to `profile-data`. Source is `scripts/profile_data.py`, `.github/workflows/profile.yml`, `tests/test_publication.py` and the other data tests.

## How to get to it (user POV)

Open All public records and definitions from the text edition. Follow Reproducible public input to `snapshot.json`. Open `.github/workflows/profile.yml` on GitHub separately to inspect actual runs. A maintainer explicitly runs the collector into external output.

## Driving it with Playwright and the CLI

The browser matrix clicks the actual records-source and snapshot anchors and saves page states. On `profile-data`, follow `snapshot.json`; save raw JSON and published README with exact branch revision and collection time. Run doctor, `gh auth status`, the skill's explicit collector command, and unit suite. Compare emitted payload names with the fifteen workflow copy paths (including four static data worlds), saved public input with displayed values, and failure behavior with publication tests. For an actual publication change, inspect the real successful run's head, both jobs and resulting branch revision, then rerun the browser matrix after assets settle.

## Gotchas

The CLI has no dry-run mode; do not invent one. Its output directory is positional. Browser checks use no authentication. Collection needs `gh` credentials, never printed or committed. A failed collector must not move publication refs. Local unit or formal proofs cannot establish hosted permissions or a successful deployed refresh. Merely opening Actions does not prove scheduling, successful jobs or delivery. Keep these unproved unless inspected directly.

A proposed README may link an immutable preview data directory instead of `tree/profile-data`. Discover the actual rendered source anchor and record its target; do not hard-code the production branch or infer publication from preview success. Source checkout head and browser target commit must both be recorded. Hosted workflow execution remains separate evidence.
