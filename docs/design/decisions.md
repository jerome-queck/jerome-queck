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

## Accepted reporting and automation

The reporting choices above are now settled: all-time public PR counters, linked
issue resolutions, last-year calendar, recent public issue/PR activity, daily refresh.
Reuse Lowlighter's established plugins with a small custom metric supplement.
See `contribution-dashboard.md` and ADR-0001. Visual acceptance remains with the owner.

Implementation evaluation: use GitHub Readme Stats for the OpenClaw card. Native
calendar privacy and compact PR events made Lowlighter unsuitable without a fork;
small tested Python panels handle the custom public contribution requirements.

## Published profile simplification — 2026-09-10

Owner removed the Algebra and Calculus screenshots as unnecessary. Keep their native
project descriptions and links. Contribution graphics remain. Historical captures stay
in `assets/` as design evidence; they are no longer embedded in the profile.

## Graphical refresh, 31 October 2026

The Owner now explicitly requests new generated assets and a prominent project map. Use one
original, restrained mathematical-world banner, a deterministic map and native project links.
This replaces the earlier general rejection of generated artwork for this refresh. It does
not restore the removed project screenshots. Preserve separate Mathematics and Software
sections, featured-project exclusions and the precise public-only aggregate metric scope.

Add verified Calculator, Probability and Number theory sites. Add personally owned Emmy to
Software. Feature the merged freeCodeCamp callback correction alongside OpenClaw. Do not
describe open contributions as merged or imply that upstream repository statistics measure
personal work. Put the retained calendar, two-event feed and repository card in details.

See [research](../research/profile-refresh.md), [inventory](../research/profile-inventory.md)
and [asset prompts and maintenance](profile-refresh.md).

## Owner rejection and editorial replacement, 1 November 2026

The Owner rejected the project-tree diagram as a repetition of the native project lists,
and the initial visual treatment as insufficient design. The Owner grants full creative
control for the replacement and cancelled organisation work.

Choose the first of three generated composition studies, an editorial monograph. Remove
the project map and the landscape from the active README. The new figure demonstrates
noncommutativity of a square's rotation and reflection. It teaches an actual mathematical
relationship instead of classifying projects. A typographic cover, compact horizontal
counters, readable mobile variant and native chapter navigation set the new hierarchy.

The five mathematics sites, four software projects, two selected merged upstream fixes,
featured-project exclusions and aggregate scopes remain. Stop showing upstream repository
statistics, which do not measure personal contribution. Preserve the useful authored
contribution records, calendar and two-event feed. See personal-redesign.md.

## Research-led graphical interface, 1 November 2026

The Owner also rejected the editorial replacement as insufficiently different, requesting a wildly different layout, many more design elements and useful repository/contribution automation. Research heavily designed READMEs before choosing another composition. The earlier editorial target is superseded, retained on `prototype/personal-editorial`.

Primary source and asset research now covers collectioneur's whole-profile custom graphics, andyruwruw's subject-specific interfaces, BrunnerLivio's complete themed page and other references. The next three generated full-page studies vary the entire composition. Independent review selects Circuit Atlas, while challenging its repetitive card rows. Use varied exhibits and a meaningful software relationship graphic instead. These generated studies are visual targets; their model-invented captions and illustrative plots do not become content.

Original chrome/orange/ivory artwork, separately linked navigation, a precise math experiment, illustrated software flow and substantial contribution/repo displays carry one visual identity. Native text and independently usable links remain. Show twelve-month authored public merge cadence and the nine selected repositories' actual default-branch tips/published releases. Keep the two-event feed minimal. Source facts, scope, timestamps and failure behavior remain explicit. See [Circuit Atlas](circuit-atlas.md), [research](../research/heavily-designed-readmes.md) and ADR-0003. Actual GitHub visual acceptance remains unverified while browser access is unavailable. All organisation work remains cancelled.
