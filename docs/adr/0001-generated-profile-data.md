# ADR-0001: Generate profile graphics on GitHub Actions

Accepted 2026-09-10; issue #7.

Reuse Lowlighter Metrics' recent activity plugin at a fixed commit.
A small standard-library Python supplement supplies the custom linked-resolution metric and public-only calendar.
GitHub hosts execution and assets; no local service or personal token is required by our workflow.
The repository token compatibility is verified by the live Actions run, not assumed from upstream examples.

Only the publication job gets contents-write permission. Generation publishes an artifact
only after every step succeeds. The publisher replaces four explicitly named files in
`profile-data` in one commit, retaining the prior branch on generation failures.
That generated-only branch is the narrow exception to the authored-file PR rule;
README, source and workflow changes still require PRs. No force pushes.

Public-only scope is deliberate. The live integration test showed that GitHub's native
calendar includes restricted counts under the repository token. We therefore reconstruct
the last 365 days from public contribution records, filtering restricted/private nodes.
Commits use bounded date windows; all other contribution connections are paginated.
Truncation fails the refresh. Lowlighter receives a repository-scoped token and explicitly
public recent events. Its documented personal-token recommendation is tested here with
the narrower repository token before acceptance.

The daily schedule and manual dispatch activate only when this workflow reaches `main`.
A prototype-branch push trigger provides an integration test before that merge.
GitHub schedules can be delayed or disabled after prolonged repository inactivity.

Upstream: https://github.com/lowlighter/metrics (MIT; used as an Action, not vendored).
