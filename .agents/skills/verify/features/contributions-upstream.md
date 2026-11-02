# Contribution charts and upstream work

## Sub-features

Counters, merge cadence and public contribution calendar beginning 1 July 2026 (current month partial), selected repository pulse, recent public issue/PR events, six merged upstream contributions with open proposals labelled separately and exact text definitions. Source is `README.md` and `scripts/profile_data.py`, `scripts/public_calendar.py`, `scripts/repo_pulse.py`, `scripts/recent_activity.py`.

## How to get to it (user POV)

Click Public records. Read visible charts; open repository pulse and recent-events disclosures. Click each chart to the exact published text snapshot. Read Selected upstream fixes and open each cited pull request.

## Driving it with Playwright

Run the matrix. Inspect `*-expanded.json` selected sources and decoded dimensions for every chart. Destination captures include the published snapshot links actually present in the article. Match charts' definitions, dates and values to the saved public snapshot and collector output. Open every selected upstream PR from its actual rendered anchor, check merged status/date and diff description, retain destination evidence. Upstream claims must remain consistent with the actual PR, not just an image label.

## Gotchas

GitHub Camo and raw CDNs can cache different generations. Keep collection interval and published timestamp; never call a chart fresh from screenshot appearance. The baseline counts all public PRs and linked currently closed issues; changing those meanings requires rereading collector source and updating this map. Public contribution frequency measures records, not effort, learning or quality. Selected repository commit dates can include any author; releases do not prove deployments. Private contributions are excluded. Open PRs, closures and merge links may change retrospectively.
