# Contribution dashboard — design in progress

## Accepted intent

Prominent graphical GitHub activity that updates automatically. Preserve distinct Mathematics, Software and Upstream contributions sections. OpenClaw is the initial curated upstream project.

## Proposed layout

1. Personal masthead with a stronger identity than Swiss Grid.
2. Contribution dashboard: calendar + PR and issue counters + last successful refresh.
3. Mathematics: Algebra and Calculus.
4. Software: Academic OS, NTULearn Sync and Syrax.
5. Upstream contributions: verified OpenClaw contribution, with its merged PR link.

## Definitions to settle

- Calendar: the ordinary last-year contribution heatmap is the proposed default.
- Counters: last 12 months versus all time; label the interval explicitly.
- PRs opened and PRs merged: authored by `jerome-queck`; exclude PRs merely reviewed or merged for someone else.
- Issues: “closed by me” requires closure-event actor evidence. “My closed issues” means authored issues now closed. “Issues resolved” requires a linked merged contribution; these sets are not interchangeable.
- Scope: public activity proposed by default. Private details must never enter generated public files; anonymous private totals require a separate choice and verification of GitHub’s visible-count semantics.

## Refresh approach to evaluate

Generate small SVG assets and a linked activity summary from GitHub data on a daily GitHub Actions schedule. Keep the last successful output on fetch failures, display its timestamp, and never replace missing data with zero. Curate the upstream-project allowlist rather than automatically featuring every repository interaction.

No workflow is installed by this design record. A scheduled workflow must reach the default branch to run. Schedules may be delayed and public-repository schedules can disable after 60 days without activity. Resolve how generated files are published without bypassing this repo’s PR rules before activating updates.

The ordinary contribution calendar does not count closing issues as a separate category. It includes qualifying issue openings, PRs, reviews and commits, among other activity. Counts on this dashboard must not be presented as GitHub’s calendar total unless obtained using the same semantics.

## Evidence

- [GitHub contribution rules](https://docs.github.com/en/account-and-profile/reference/profile-contributions-reference)
- [GitHub scheduled workflow behaviour](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Lowlighter metrics](https://github.com/lowlighter/metrics): useful SVG dashboard mechanism reference; final generator not selected.
- [OpenClaw PR #130275](https://github.com/openclaw/openclaw/pull/130275): GitHub API confirms author and merge timestamp.
- [OpenClaw issue #130096](https://github.com/openclaw/openclaw/issues/130096): closure timeline actor is `obviyus`, not `jerome-queck`.
