# Useful relationships and native copy

Checked via authenticated `gh` against public GitHub main/PR data at 2026-10-31T20:42Z, 1 November in Singapore. No repository or remote writes. Primary source links below identify the evidence. Raw API captures are retained in the task audit folder.

## Recommendation

A complete ecosystem diagram does not earn profile space. Emmy has no verified integration with these projects. The five mathematics sites are separate applications. Drawing all nine as a connected system would invent relationships or reproduce the rejected taxonomy.

One defensible compact diagram can explain a real boundary in the academic workflow. Use it only if the composition needs this explanatory story, not as decoration.

**Course material becomes a local source, not evidence of learning.**

`NTULearn course → NTULearn Sync → Module's NTULearn folder → Academic OS checks freshness and missing material`

Use the source-to-local-material arrows solid. Put the Academic OS step below as an inspection arrow, not a transformation that implies it automatically teaches, completes work, grades, or moves every imported file. Native caption can say “Course pages and attachments become local sources. Academic OS checks their structure and freshness; availability does not establish mastery.” This explains what the software accomplishes and its limit, beyond project membership.

Sources:

- [NTULearn README](https://github.com/Jerome-Group/ntulearn/blob/main/README.md) says pages/announcements become Markdown; attachments retain their formats; chosen course destinations hold the files. Assessments remain online-only cards. Questions, submissions, grades and discussion posts stay in NTULearn.
- [Academic OS README](https://github.com/Jerome-Group/academic-os/blob/main/README.md) explicitly says NTULearn already writes current module material into contract-declared importer roots. `imports status` reads receipts. `learning materials` checks referenced files. It explicitly says file availability never implies progress or mastery.
- [Module folder contract](https://github.com/Jerome-Group/academic-os/blob/main/docs/module-folder-contract.md) defines the `NTULearn/` importer root beside learning and administrative controls. These private folders are outside the public source repository.

Syrax can truthfully join a separate, more technical diagram. Its academic desk calls the products' CLIs, reads the calendar mirror and NTULearn digest, and posts a composed Telegram brief. Sync and calendar Promotion require explicit confirmation. It does not hold those products' credentials. This is more complicated than a profile needs, and the Syrax README explicitly retains a fresh end-to-end acceptance run as outstanding. Do not present deployment health as established.

Sources:

- [Syrax README](https://github.com/Jerome-Group/syrax/blob/main/README.md).
- [Academic desk ADR](https://github.com/Jerome-Group/syrax/blob/main/docs/adr/0030-the-academic-desk-composes-the-brief-and-the-writes-wait-for-a-tap.md).
- [System overview](https://github.com/Jerome-Group/syrax/blob/main/docs/system-overview.md).

A mathematical alternative that actually teaches something is a labelled square demonstrating noncommutativity. “Rotate then reflect” and “reflect then rotate” have different labelled outputs. This could be an attractive linked invitation to Algebra rather than a claim that all the sites integrate. Set the convention explicitly. Let R(x,y)=(-y,x), S(x,y)=(x,-y). For the marked point (1,1), R then S gives (-1,-1); S then R gives (1,1). Show all four vertex labels to avoid the trap that an unlabelled square looks unchanged. Caption “Order matters. Try square symmetries in Algebra.”

This is supported as a project topic by Algebra's square and symmetry laboratory entries in the [generated feature map](https://github.com/Jerome-Group/algebra/blob/main/lib/algebra/feature-map.json), plus the [source coverage ledger](https://github.com/Jerome-Group/algebra/blob/main/docs/source-coverage.md). The arithmetic above is directly checked by substitution. Link the verified site root, https://algebra.jeromegroup.org, unless the designer separately verifies the current live lesson/lab URL. The coverage ledger warns some local teaching additions are not yet published to the older Site. Do not claim the graphic reproduces an observed live screen. This option teaches a small mathematical fact and is preferable to a nine-project connection graph.

## Native project descriptions

Use these as short native links next to any graphical treatment. They describe source-supported capabilities, not current deployment verification. Avoid exact lesson counts in a long-lived profile.

| Project | Concise native copy | Verified source |
| --- | --- | --- |
| Calculator | Mathematical notebooks with exact computation, graphs and reusable definitions. Sign-in required. | https://github.com/Jerome-Group/calculator/blob/main/README.md |
| Probability | A first course in probability, with worked examples, practice and experiments. | https://github.com/jerome-queck/probability/blob/main/README.md |
| Number theory | Proofs, practice and exact computational experiments in elementary number theory. | https://github.com/Jerome-Group/numbertheory/blob/main/README.md |
| Algebra | Groups, rings, fields and representations, with visual laboratories and proof writing. | https://github.com/Jerome-Group/algebra/blob/main/README.md |
| Calculus | One-variable and multivariable calculus through arguments, examples and interactive geometry. | https://github.com/Jerome-Group/calculus/blob/main/README.md |
| Academic OS | Folder contracts, tasks, calendars and source checks for my degree and research. | https://github.com/Jerome-Group/academic-os/blob/main/README.md |
| NTULearn Sync | Course pages, announcements and attachments copied into local course folders. | https://github.com/Jerome-Group/ntulearn/blob/main/README.md |
| Syrax | My Telegram assistant, with an OpenClaw adapter, file search and an academic desk. | https://github.com/Jerome-Group/syrax/blob/main/README.md |
| Emmy | My operating kit for ChatGPT Dot, retaining responsibility context and checking current evidence. | https://github.com/jerome-queck/emmy/blob/main/README.md |

For Emmy, native products own execution, permissions, schedules and delivery. Its CLI checks or proposes native work. It is not an independently executing replacement for Dot. Do not draw Emmy supervising Syrax, NTULearn or Academic OS without separate current evidence.

Site entrypoints preserved in current personal README and matching source project descriptions:

- https://calculator.jeromegroup.org
- https://probability.jeromegroup.org
- https://numbertheory.jeromegroup.org
- https://algebra.jeromegroup.org
- https://calculus.jeromegroup.org

These URLs were verified as current repository/profile links. This research did not perform current browser interaction or establish production feature parity.

## Upstream curation

| PR | Fresh state | Native description |
| --- | --- | --- |
| [freeCodeCamp #71474](https://github.com/freeCodeCamp/freeCodeCamp/pull/71474) | MERGED 2026-10-31 11:09:15Z | Corrected callback definitions to include synchronous callbacks. |
| [freeCodeCamp #71484](https://github.com/freeCodeCamp/freeCodeCamp/pull/71484) | OPEN; updated 2026-10-31 14:24:16Z | Strengthens weather-app tests around rejected promises, missing data and valid zero readings. |
| [freeCodeCamp #71496](https://github.com/freeCodeCamp/freeCodeCamp/pull/71496) | OPEN; updated 2026-10-31 14:59:32Z | Accepts valid TypeScript enum syntax in digital-pet tests. |
| [OpenClaw #130275](https://github.com/openclaw/openclaw/pull/130275) | MERGED 2026-08-28 20:49:11Z | Stops oversized Groq requests being retried as recoverable rate limits. |

The three freeCodeCamp readbacks identify author `jerome-queck`; OpenClaw merge and title were freshly read separately. #71484 and #71496 are newer contributions, not newer merged contributions. For strongest concise curation retain OpenClaw as the substantial merged runtime repair, then one merged freeCodeCamp correction. Optionally add one visibly labelled “Open PR” for weather edge cases. Do not describe #71484 or #71496 as shipped or merged.
