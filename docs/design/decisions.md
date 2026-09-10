# Profile design decisions

Recorded 2026-09-10. Reversible editorial choices live here; ADRs are reserved for significant architectural trade-offs.

## Settled

- Remote: `jerome-queck/jerome-queck`; local folder is already the repository root.
- Mathematics and software receive equal emphasis.
- Algebra and Calculus feature prominently as mathematical notes websites.
- Clarifold and Doomsday Protocol are excluded until the owner explicitly changes that decision.
- Prototype in GitHub itself before choosing the final design.
- Use authentic Algebra and Calculus screenshots, with native text and links outside images.
- Rejected A/B/C image-generated mockups: too artificial, overdecorated and poorly matched to GitHub. Do not continue that aesthetic.
- Scaffold without another setup approval: GitHub Issues, five canonical triage labels, a single domain context.
- Retain template agent guidance, adapting personal-repository assumptions. Do not install organisation automation or claim Terraform ownership.
- Omit a blanket licence for now. Artwork and code licensing can be decided separately before distributing reusable final assets.

## Open

- Select the contribution dashboard presentation and reporting window.
- Define the issue metric: closure actor versus authored closed issues versus issues resolved by merged PRs.
- Confirm public-only metrics or anonymous private contribution counts.
- Any graphic must be assessed in an actual GitHub render; keep project descriptions as text.

## Prototype

[Current GitHub-native prototype](https://github.com/jerome-queck/jerome-queck/tree/prototype/profile-directions) live on a separate prototype branch.
The setup branch carries durable instructions and decisions only. No final visual design is selected.

The rejected generated board is retained only in git history.

## Revision

The owner accepted the recommendation to use authentic project screenshots with native Markdown. Two live screenshots now illustrate Algebra and Calculus. No decorative curve is included in the profile. The screenshot draft remains on the prototype branch for review.

## Contribution-focused direction

- Swiss Grid is rejected as too boring. DenverCoder1 is a mechanism reference, not a layout to copy.
- Give graphical contribution activity a prominent section that updates automatically.
- Keep Mathematics and Software as separate project sections.
- Add a separate Upstream contributions section, initially featuring OpenClaw only.
- Verified: authored PR [openclaw/openclaw#130275](https://github.com/openclaw/openclaw/pull/130275) merged 2026-08-28T20:49:11Z. It fixes oversized Groq requests being treated as retryable rate limits, which stalled sessions.
- Its linked issue [#130096](https://github.com/openclaw/openclaw/issues/130096) was closed by maintainer `obviyus`; do not label it as an issue personally closed by the author.

Proposed dashboard: contribution calendar, PRs opened, PRs merged, and a precisely defined issue metric, followed by a short linked activity list. Proposed cadence: daily, plus manual refresh, with the last successful update shown. These reporting choices remain open; automatic updates are not implemented yet.
