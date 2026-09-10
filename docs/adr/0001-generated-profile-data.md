# ADR-0001: Generate profile graphics on GitHub Actions

Accepted 2026-09-10; issue #7.

Reuse Lowlighter Metrics' calendar and recent activity plugins at a fixed commit.
A small standard-library Python supplement supplies the custom linked-resolution metric.
GitHub hosts execution and assets; no local service or personal token is required by our workflow.
The repository token compatibility is verified by the live Actions run, not assumed from upstream examples.

Only the publication job gets contents-write permission. Generation publishes an artifact
only after every step succeeds. The publisher replaces three explicitly named files in
`profile-data` in one commit, retaining the prior branch on generation failures.
That generated-only branch is the narrow exception to the authored-file PR rule;
README, source and workflow changes still require PRs. No force pushes.

Public-only scope is deliberate. The native calendar is rejected when GitHub reports
restricted contributions rather than publishing anonymous private counts. This can stop
refreshes if the owner enables private contribution display; the previous timestamp remains.
Lowlighter receives a repository-scoped token and explicitly public recent events.

The daily schedule and manual dispatch activate only when this workflow reaches `main`.
A prototype-branch push trigger provides an integration test before that merge.
GitHub schedules can be delayed or disabled after prolonged repository inactivity.

Upstream: https://github.com/lowlighter/metrics (MIT; used as an Action, not vendored).
