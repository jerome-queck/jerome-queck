![Jerome Queck. Mathematics × software. Original Circuit Atlas artwork.](assets/circuit-atlas-hero.jpg)

# Mathematics & software

I study mathematics and build tools for learning, research and organising my work.

<p>
<a href="#mathematics"><img src="assets/nav-explore.svg" width="32%" alt="01. Explore mathematics"></a>
<a href="#software"><img src="assets/nav-build.svg" width="32%" alt="02. Software I build"></a>
<a href="#public-work"><img src="assets/nav-contribute.svg" width="32%" alt="03. Public contributions and repository data"></a>
</p>

[Website](https://jeromegroup.org) · [LinkedIn](https://www.linkedin.com/in/jeromequeck/) · [Jerome-Group](https://github.com/Jerome-Group)

<a name="mathematics"></a>

## <img src="assets/chapter-math.svg" width="64" alt=""> Mathematics

Notes websites and tools for exploring ideas. A small example from algebra follows. **The order of two operations can change their result.**

<a href="https://algebra.jeromegroup.org">
<picture>
  <source media="(min-width: 601px)" srcset="assets/order-matters.png">
  <img alt="Start at (1,1). Rotate a square a quarter-turn anticlockwise, then reflect across the horizontal axis, to end at (-1,-1). Reverse those operations to end at (1,1). The same moves give different results." src="assets/order-matters-mobile.png" width="100%">
</picture>
</a>

<p>
<a href="https://algebra.jeromegroup.org"><img src="assets/enter-algebra.svg" width="49%" alt="Explore Algebra. Structure and symmetry."></a>
<a href="https://calculus.jeromegroup.org"><img src="assets/enter-calculus.svg" width="49%" alt="Explore Calculus. Change and geometry."></a>
</p>
<p>
<a href="https://probability.jeromegroup.org"><img src="assets/enter-probability.svg" width="49%" alt="Explore Probability. Reasoning about uncertainty."></a>
<a href="https://numbertheory.jeromegroup.org"><img src="assets/enter-numbertheory.svg" width="49%" alt="Explore Number theory. Patterns in the integers."></a>
</p>

**Algebra** explores structure and symmetry; **Calculus** explores change and geometry. **Probability** develops reasoning about uncertainty; **Number theory** explores patterns in the integers.

[![Open Calculator. Mathematical notebooks. Sign-in required.](assets/enter-calculator.svg)](https://calculator.jeromegroup.org)

**Calculator** provides mathematical notebooks with exact computation, graphs and reusable definitions. **Sign-in required.**

<details>
<summary>Five mathematics destinations, descriptions and source</summary>

- **[Algebra](https://algebra.jeromegroup.org)**. Groups, rings, fields and representations, with visual laboratories and proof writing. [Source](https://github.com/Jerome-Group/algebra).
- **[Calculus](https://calculus.jeromegroup.org)**. One-variable and multivariable calculus through arguments, examples and interactive geometry. [Source](https://github.com/Jerome-Group/calculus).
- **[Probability](https://probability.jeromegroup.org)**. A first course with worked examples, practice and experiments. [Source](https://github.com/jerome-queck/probability).
- **[Number theory](https://numbertheory.jeromegroup.org)**. Proofs, practice and exact computational experiments in elementary number theory. [Source](https://github.com/Jerome-Group/numbertheory).
- **[Calculator](https://calculator.jeromegroup.org)**. Mathematical notebooks with exact computation, graphs and reusable definitions. Sign-in required. [Source](https://github.com/Jerome-Group/calculator).

</details>

<a name="software"></a>

## <img src="assets/chapter-software.svg" width="64" alt=""> Software

**Course material becomes a local working desk.** These connections describe actual interfaces between the projects.

<picture>
  <source media="(min-width: 601px)" srcset="assets/software-circuit.jpg">
  <img alt="NTULearn Sync writes course pages, announcements and original attachments into local module folders. Academic OS checks source structure and freshness alongside tasks and calendars. Syrax's academic desk can query both tools. Files on disk are not evidence of learning. Emmy has a separate role in ChatGPT Dot." src="assets/software-circuit-mobile.jpg" width="100%">
</picture>

**[NTULearn Sync](https://github.com/Jerome-Group/ntulearn)** saves pages and announcements as Markdown and attachments in their original formats. **[Academic OS](https://github.com/Jerome-Group/academic-os)** works with those module folders, tasks and calendars, checking source structure, freshness and missing material.

[![Syrax. Telegram academic desk. File search and tool queries. Original illustrative exhibit.](assets/syrax-exhibit.jpg)](https://github.com/Jerome-Group/syrax)

**[Syrax](https://github.com/Jerome-Group/syrax)** is my Telegram assistant, built on OpenClaw, with file search and an academic desk that can query NTULearn Sync and Academic OS.

[![Emmy. Operating kit for ChatGPT Dot. Context and current evidence. Original illustrative exhibit.](assets/emmy-exhibit.jpg)](https://github.com/jerome-queck/emmy)

**[Emmy](https://github.com/jerome-queck/emmy)** provides responsibility context and current evidence checks for ChatGPT Dot. Native products own execution, permissions, schedules and delivery.

<a name="public-work"></a>

## <img src="assets/chapter-public-work.svg" width="64" alt=""> Public work

<a href="https://github.com/jerome-queck/jerome-queck/tree/profile-data">
<picture>
  <source media="(min-width: 601px)" srcset="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/counters.svg">
  <img alt="All-time public PRs authored by me, opened and merged, plus distinct currently closed public issues linked to my merged PRs. Open the text snapshot for current values and collection time." src="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/counters-mobile.svg" width="100%">
</picture>
</a>

<a href="https://github.com/jerome-queck/jerome-queck/tree/profile-data#merge-cadence">
<picture>
  <source media="(min-width: 601px)" srcset="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/cadence.svg">
  <img alt="Authored public PRs merged per UTC calendar month over twelve months. The current month is partial. All values are available in the text snapshot." src="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/cadence-mobile.svg" width="100%">
</picture>
</a>

<a href="https://github.com/jerome-queck/jerome-queck/tree/profile-data#public-contribution-calendar">
<picture>
  <source media="(min-width: 601px)" srcset="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/calendar.svg">
  <img alt="365 days reconstructed from public commit, issue, PR, review and repository contribution records. Zero to peak cell colors indicate daily frequency; dates and exact values are in the text snapshot." src="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/calendar-mobile.svg" width="100%">
</picture>
</a>

### Selected upstream fixes

**[OpenClaw #130275](https://github.com/openclaw/openclaw/pull/130275), merged 28 August 2026.** Oversized Groq requests were repeatedly retried as recoverable rate limits, leaving sessions stuck. The fix stops futile retries, returns clear `/reset` or `/new` guidance, and preserves configured fallback.

**[freeCodeCamp #71474](https://github.com/freeCodeCamp/freeCodeCamp/pull/71474), merged 31 October 2026.** The callback review definitions excluded synchronous callbacks. The correction covers both synchronous and asynchronous use.

### The repositories behind the work

The nine selected projects, refreshed from their public repositories. Default-branch commit dates cover **any author**. Releases mean published GitHub Releases, including labelled prereleases. Neither establishes deployment status.

<details>
<summary>Inspect all nine repository tips and published-release records</summary>

<a href="https://github.com/jerome-queck/jerome-queck/tree/profile-data#selected-repository-pulse">
<picture>
  <source media="(min-width: 601px)" srcset="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/pulse.svg">
  <img alt="Selected repository pulse. Current default-branch commit dates and latest published GitHub releases for all five mathematics and four software projects. Open the text snapshot for exact records and source links." src="https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/pulse-mobile.svg" width="100%">
</picture>
</a>

</details>

[Last successful collection, definitions and exact values](https://github.com/jerome-queck/jerome-queck/tree/profile-data) · [Daily refresh workflow](https://github.com/jerome-queck/jerome-queck/actions/workflows/profile.yml).

<details>
<summary>Two recent events and how to read the numbers</summary>

[![Two recent public issue and PR events, with full titles and links in the text snapshot.](https://raw.githubusercontent.com/jerome-queck/jerome-queck/profile-data/activity.svg)](https://github.com/jerome-queck/jerome-queck/tree/profile-data#recent-issue-and-pr-events)

Counters cover all-time public PRs authored by me. Linked resolutions count distinct currently closed public issues linked to those merged PRs, closed at or after the merge. This does not measure who clicked Close or prove a PR alone caused closure. Records can change retrospectively.

Merge cadence, calendar and aggregate counts span all public projects. The repository pulse covers only the nine authored selections above. The feed samples the latest 300 public GitHub events, subject to GitHub's 30-day retention. These numbers measure records, not effort, learning or quality.

Every source must succeed before a new publication. Failed refreshes retain the previous snapshot and timestamp. GitHub can delay scheduled runs. Collection spans a recorded interval; GitHub queries are not a transaction at one instant. Published images and accessible text derive from the same saved public input; CDN caches can refresh at different times.

</details>

[![Jerome Queck. Explore the website.](assets/exit.svg)](https://jeromegroup.org)

**[Explore the website ↗](https://jeromegroup.org)** · [LinkedIn](https://www.linkedin.com/in/jeromequeck/) · [How this profile is made](docs/design/circuit-atlas.md)
