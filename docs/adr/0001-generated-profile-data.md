# ADR-0001: Generate profile graphics on GitHub Actions

Accepted 2026-09-10; issue #7.

Reuse the maintained GitHub Readme Stats Action for the OpenClaw repository card,
pinning the Action commit and core package version. Standard-library Python supplies
the contribution counters, public calendar and recent issue/PR activity.
GitHub hosts execution and assets; no local service or personal token is required.

Lowlighter was evaluated first. GitHub's native calendar includes restricted counts
under the repository token, and compact PR events omit fields its activity plugin
expects. Replacing those components is smaller than maintaining a patched fork.

Only the publication job gets contents-write permission. Generation publishes an artifact
only after every step succeeds. The publisher replaces five explicitly named files in
`profile-data` in one commit, retaining the prior branch on generation failures.
That generated-only branch is the narrow exception to the authored-file PR rule;
README, source and workflow changes still require PRs. No force pushes.

The calendar reconstructs the last 365 days from public contribution records, filtering
restricted/private nodes. Commits use bounded date windows; other contribution
connections are paginated. Truncation fails the refresh. Recent activity uses the public
events endpoint and hydrates compact PR payloads. Excluded projects stay out of the feed.

The daily schedule and manual dispatch activate only when this workflow reaches `main`.
A temporary prototype push trigger seeded the reviewed preview in run 34430852374.
That trigger is removed after validation; normal publication is restricted to `main`.
GitHub schedules can be delayed or disabled after prolonged repository inactivity.

Sources evaluated:
- https://github.com/stats-organization/github-readme-stats-action
- https://github.com/lowlighter/metrics
