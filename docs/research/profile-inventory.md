# Profile inventory . 2026-10-31

Evidence: GitHub API and direct HTTP reads on 2026-10-31. Status is time-sensitive. Personal checkout's origin is `https://github.com/jerome-queck/jerome-queck.git`; authenticated `gh api user` reports `jerome-queck`. The [personal profile source](https://github.com/jerome-queck/jerome-queck/blob/main/README.md) and [organisation profile source](https://github.com/Jerome-Group/.github/blob/main/profile/README.md) were read via GitHub API.

## Mathematics

| Project | Site | Public source / owner | Evidence and boundary |
|---|---|---|---|
| Calculator | [calculator.jeromegroup.org](https://calculator.jeromegroup.org) | [Jerome-Group/calculator](https://github.com/Jerome-Group/calculator) | Symbolic computation, notebook and graphs. Unauthenticated HTTP redirected to OpenAI sign-in; final response 403 in this environment. Do not claim an authenticated journey was verified. |
| Probability | [probability.jeromegroup.org](https://probability.jeromegroup.org) | [jerome-queck/probability](https://github.com/jerome-queck/probability) | Public personal repository, not org-owned. Site returned HTTP 200; README describes a first course and public reading. |
| Number theory | [numbertheory.jeromegroup.org](https://numbertheory.jeromegroup.org) | [Jerome-Group/numbertheory](https://github.com/Jerome-Group/numbertheory) | HTTP 200. Repository describes an interactive elementary number theory atlas; publication is separate from source. |
| Algebra | [algebra.jeromegroup.org](https://algebra.jeromegroup.org) | [Jerome-Group/algebra](https://github.com/Jerome-Group/algebra) | HTTP 200. Groups, rings, fields, representations, interactive visual labs. |
| Calculus | [calculus.jeromegroup.org](https://calculus.jeromegroup.org) | [Jerome-Group/calculus](https://github.com/Jerome-Group/calculus) | HTTP 200. Undergraduate calculus with diagrams and interactive explorations. |

HTTP status establishes reachability only; it does not establish current deployed content, sign-in, or functionality. The source READMEs above support descriptions and are not proof that each live deployment matches current source.

## Contributions

- [freeCodeCamp #71474](https://github.com/freeCodeCamp/freeCodeCamp/pull/71474): authored by `jerome-queck`, **merged** 2026-10-31 11:09 UTC. Corrected callback review definitions to account for synchronous callbacks.
- [freeCodeCamp #71484](https://github.com/freeCodeCamp/freeCodeCamp/pull/71484): authored by `jerome-queck`, **open** at readback; handles weather data edge cases.
- [freeCodeCamp #71496](https://github.com/freeCodeCamp/freeCodeCamp/pull/71496): authored by `jerome-queck`, **open** at readback; accepts valid enums in digital pet game tests. Open PRs must not be described as merged.
- [OpenClaw #130275](https://github.com/openclaw/openclaw/pull/130275): authored by `jerome-queck`, merged 2026-08-28 20:49 UTC. Existing profile summary describes oversized Groq requests being misclassified as retryable rate limits.

## Useful existing material and ownership

- [Emmy](https://github.com/jerome-queck/emmy) is a **public personal repository**, owned by `jerome-queck`, not Jerome-Group. Its README calls it a chief-of-staff operating kit for Jerome's ChatGPT Dot; it provides local context, evidence checks, and advisory routing. It explicitly says native products own execution, permissions, schedules and delivery. Relevant to a personal software profile; avoid implying native autonomous delivery or org ownership.
- Organisation's existing software: [Academic OS](https://github.com/Jerome-Group/academic-os), [NTULearn](https://github.com/Jerome-Group/ntulearn), [Syrax](https://github.com/Jerome-Group/syrax), and [F1 Analytics](https://github.com/Jerome-Group/f1-analytics), all confirmed public org repositories. Their existing summaries and organisation policies are useful starting points.
- Personal profile currently retains linked website, LinkedIn and org, contribution counters, calendar, recent activity, algebra, calculus, academic software and an OpenClaw contribution card. Organisation profile retains community policy links, work practices, public activity graphics, declared-assistance graphic with qualification, algebra, calculus and software list.
- Generated profile assets are published on [`profile-data`](https://github.com/jerome-queck/jerome-queck/tree/profile-data); [design notes](https://github.com/jerome-queck/jerome-queck/blob/main/docs/design/contribution-dashboard.md) document daily refresh, public-only metrics, latest-300-event activity boundary and exclusions. [Organisation profile-data](https://github.com/Jerome-Group/.github/tree/profile-data) supplies corresponding graphics and definitions. Preserve meaningful metric and scope qualifications.
- Exclude Clarifold from featured content as requested. Personal design notes also exclude Doomsday from featured activity, while aggregate public counts still span public repositories. Preserve this existing distinction; do not promise exclusion from all aggregates.
