![Jerome Queck. Original editorial cover with a geometric construction.](assets/editorial-cover.jpg)

# Mathematics & software

I study mathematics and build tools for learning, research and organising my work.

[Mathematics](#mathematics) · [Software](#software) · [Upstream work](#upstream-work) · [Activity](#public-work)

[Website](https://jeromegroup.org) · [LinkedIn](https://www.linkedin.com/in/jeromequeck/) · [Jerome-Group](https://github.com/Jerome-Group)

<a href="https://github.com/jerome-queck/jerome-queck/tree/prototype/personal-editorial/_preview">
<picture>
  <source media="(max-width: 600px)" srcset="https://raw.githubusercontent.com/jerome-queck/jerome-queck/prototype/personal-editorial/_preview/counters-mobile.svg">
  <img alt="All-time authored public PRs opened, PRs merged and distinct linked issues resolved. Open the timestamped text snapshot for current numbers." src="https://raw.githubusercontent.com/jerome-queck/jerome-queck/prototype/personal-editorial/_preview/counters.svg" width="100%">
</picture>
</a>

Public authored work, across public repositories. [Definitions and last successful refresh](https://github.com/jerome-queck/jerome-queck/tree/prototype/personal-editorial/_preview). These counts measure records and linked resolutions, not effort.

<a name="mathematics"></a>

## 01 · Mathematics

Notes and tools that make an idea easier to explore.

<a href="https://algebra.jeromegroup.org">
<picture>
  <source media="(max-width: 600px)" srcset="assets/order-matters-mobile.png">
  <img alt="Order matters. Start at the ringed corner (1,1). A quarter-turn anticlockwise followed by reflection across the horizontal axis ends at (-1,-1). Reflecting first, then rotating, ends at (1,1). The same operations give different results." src="assets/order-matters.png" width="100%">
</picture>
</a>

A small example of a bigger idea. Rotate a square, then reflect it. Reverse those moves and the marked corner lands somewhere else. [Explore groups and actions in Algebra](https://algebra.jeromegroup.org).

<table>
<tr>
<td width="50%" valign="top">
<h3><a href="https://algebra.jeromegroup.org">Algebra ↗</a></h3>
<p>Structure and symmetry.</p>
<p>Groups, rings, fields and representations, with visual laboratories and proof writing.</p>
<a href="https://github.com/Jerome-Group/algebra">Source</a>
</td>
<td width="50%" valign="top">
<h3><a href="https://calculus.jeromegroup.org">Calculus ↗</a></h3>
<p>Change and geometry.</p>
<p>One-variable and multivariable calculus through arguments, examples and interactive geometry.</p>
<a href="https://github.com/Jerome-Group/calculus">Source</a>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3><a href="https://probability.jeromegroup.org">Probability ↗</a></h3>
<p>Reasoning about uncertainty.</p>
<p>A first course with worked examples, practice and experiments.</p>
<a href="https://github.com/jerome-queck/probability">Source</a>
</td>
<td width="50%" valign="top">
<h3><a href="https://numbertheory.jeromegroup.org">Number theory ↗</a></h3>
<p>Patterns in the integers.</p>
<p>Proofs, practice and exact computational experiments in elementary number theory.</p>
<a href="https://github.com/Jerome-Group/numbertheory">Source</a>
</td>
</tr>
</table>

### Work it out

**[Open Calculator ↗](https://calculator.jeromegroup.org)** for mathematical notebooks with exact computation, graphs and reusable definitions. Sign-in required. [Source](https://github.com/Jerome-Group/calculator).

<a name="software"></a>

## 02 · Software

Systems I use for my own degree and research.

### Course material, made local

[NTULearn Sync](https://github.com/Jerome-Group/ntulearn) turns course pages and announcements into Markdown and saves attachments in their original formats. It writes those sources into local module folders.

[Academic OS](https://github.com/Jerome-Group/academic-os) works with those folders, alongside tasks and calendars. It checks source structure, freshness and missing material. Having a file is not evidence of learning it.

### Two assistants, different jobs

<table>
<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Jerome-Group/syrax">Syrax ↗</a></h3>
<p>My Telegram assistant, built on OpenClaw.</p>
<p>Its academic desk can query NTULearn Sync and Academic OS, alongside file search and other tools.</p>
</td>
<td width="50%" valign="top">
<h3><a href="https://github.com/jerome-queck/emmy">Emmy ↗</a></h3>
<p>My operating kit for ChatGPT Dot.</p>
<p>Responsibility context and current evidence checks. Native products own execution, permissions, schedules and delivery.</p>
</td>
</tr>
</table>

<a name="upstream-work"></a>

## 03 · Upstream work

Selected fixes, with the actual pull requests.

### OpenClaw · runtime failure

Oversized Groq requests were repeatedly retried as recoverable rate limits, leaving sessions stuck. The fix stops futile retries, returns clear `/reset` or `/new` guidance, and preserves configured fallback.

[PR #130275](https://github.com/openclaw/openclaw/pull/130275) · **Merged 28 August 2026**.

### freeCodeCamp · callback definitions

The callback review definitions excluded synchronous callbacks. The correction makes the definition cover both synchronous and asynchronous use.

[PR #71474](https://github.com/freeCodeCamp/freeCodeCamp/pull/71474) · **Merged 31 October 2026**.

## Public work

[Daily refresh workflow](https://github.com/jerome-queck/jerome-queck/actions/workflows/profile.yml) · [Current numbers and records](https://github.com/jerome-queck/jerome-queck/tree/prototype/personal-editorial/_preview).

<details>
<summary>Calendar, two recent events and metric definitions</summary>

[![365 days reconstructed from public contribution records. Definitions and textual records are linked.](https://raw.githubusercontent.com/jerome-queck/jerome-queck/prototype/personal-editorial/_preview/calendar.svg)](https://github.com/jerome-queck/jerome-queck/tree/prototype/personal-editorial/_preview)

[![Two recent public issue and PR events, with full titles and links in the text snapshot.](https://raw.githubusercontent.com/jerome-queck/jerome-queck/prototype/personal-editorial/_preview/activity.svg)](https://github.com/jerome-queck/jerome-queck/tree/prototype/personal-editorial/_preview#recent-issue-and-pr-events)

Counters cover all-time public PRs authored by me. Linked resolutions count distinct currently closed public issues linked to those merged PRs, closed at or after the merge. This does not measure who clicked Close or establish that a PR alone caused the resolution.

The calendar and aggregate counts span all public projects. The recent feed samples the latest 300 public GitHub events. Failed refreshes retain the previous published data and timestamp. GitHub can delay scheduled runs.

</details>
