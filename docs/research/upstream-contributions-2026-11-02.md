# Public upstream contribution evidence

Observed 2026-11-02 12:48 UTC via connected GitHub search_prs, get_pr_info, fetch_pr, list_pr_changed_filenames and fetch_pr_file_patch. Exact PR author verified as `jerome-queck` for every row. Public-only search returned 18 PRs outside Jerome-Group and personal repositories. Recent updated-since-2026-10-30 search returned 17. A merged-only search returned six, including the two already featured. No Clarifold or Doomsday material included. Read-only research; no tests rerun here.

Direct PR links below identify the reviewed primary records. The implementation session also collected the complete public scoped search at 2026-11-02 13:03 UTC, with 18 PRs, six merged, eleven open and one closed without merge across three repositories. The external session evidence retains raw metadata and reviewed patches. Status is a snapshot. GitHub metadata's `merge_commit_sha` can exist on open PRs; only `merged: true` plus `merged_at` establishes merging.

## Strongest new additions

| PR | Status / merged UTC | Safe profile wording | Implementation evidence reviewed |
| --- | --- | --- | --- |
| [OpenClaw #189784](https://github.com/openclaw/openclaw/pull/189784) | Merged 2026-10-31 23:38:15 | YAML alias traversal and cycle-safe search | Actual diff adds YAML alias dereferencing in resolver/finder, maintains document context, guards active recursive alias cycles, and extends existing tests. Alias-slot replacement supported; write-through remains refused; YAML merge keys excluded. |
| [OpenClaw #189855](https://github.com/openclaw/openclaw/pull/189855) | Merged 2026-11-01 00:42:44 | JSON edits that target the effective duplicate key | Actual diff changes named reads/searches to last duplicate, edits effective source node with jsonc-parser, retains earlier shadowed values and formatting, refuses ambiguous insertion. Covers JSON, JSONC and JSONL. |
| [OpenClaw #189960](https://github.com/openclaw/openclaw/pull/189960) | Merged 2026-11-01 02:54:39 | Recursive JSONL search with reusable line addresses | Actual diff moves consumed value keys out of JSONL's physical-line address slot and extends recursive finder regressions. Addresses round-trip; no new syntax. |
| [OpenClaw #189993](https://github.com/openclaw/openclaw/pull/189993) | Merged 2026-11-02 02:37:00 | Actionable errors for invalid CLI input | Actual diff classifies existing numeric validation as ExpectedCliError, moves class/helper to dependency-light owner and migrates callers. Includes yxshee's diagnostic-only pairing contribution with attribution; do not imply sole authorship of pairing work. |
| [freeCodeCamp #71484](https://github.com/freeCodeCamp/freeCodeCamp/pull/71484) | Open; not merged | Proposed weather-lab fixes for async errors and zero measurements | Two weather-lab Markdown files; reviewed actual v1 patch awaits missing-data operations, restores replacements in finally, preserves display on failure, differentiates zero/undefined, exercises Paris button, repairs supplied solution. PR body reports Node/jsdom checks; explicitly not a browser-suite pass. |
| [freeCodeCamp #71496](https://github.com/freeCodeCamp/freeCodeCamp/pull/71496) | Open; not merged | Proposed curriculum tests that accept valid TypeScript enums | Reviewed actual Digital Pet Game patch strips JS comments, replaces restrictive character class, accepts enum initializers/spacing, relaxes Record type spacing, aligns uppercase names and hint text. |
| [OpenClaw #190799](https://github.com/openclaw/openclaw/pull/190799) | Open; not merged | Proposed Teams broadcast repair that preserves group-chat session identity | Reviewed actual handler patch publishes routePeer only for group chats. File list includes config-doctor migration, inbound regression suite and broadcast docs. PR body updates limit migration to group-chat keys, retain DM/channel identities, make collisions/idempotency explicit. Body contains superseded earlier claims; use the later scoped update. Loopback Bot Framework QA evidence is not a live Teams tenant. |
| [Vorssaint #3734](https://github.com/vorssaint/vorssaint-utils/pull/3734) | Open; not merged | Proposed daylight-saving correction for hourly usage charts | Actual Swift patch constructs hour starts until next local midnight, replacing fixed 24 buckets; tests file changed. PR explicitly says macOS build/tests and visual inspection were not run locally. Optional breadth item; weaker validation than selected OpenClaw fixes. |

Recommendation for a concise README: group #189784/#189855/#189960 into one merged `Structured-file tooling` item with three PR links, then #189993 as a second merged item. Retain existing Groq and callback items. If showing pending work, add one separate clearly labelled `Open PRs` line for the two freeCodeCamp changes and Teams session identity repair. Omit Vorssaint if space is tight. Avoid mixing open work into a list labelled merged or shipped.

## Existing items rechecked

- [OpenClaw #130275](https://github.com/openclaw/openclaw/pull/130275), author jerome-queck, merged 2026-08-28 20:49:11 UTC. Stops futile retries/compaction for Groq per-request token ceilings and shows reset guidance; configured transport-owned fallback remains supported. Still strongest older technical item. Metadata/body refreshed; no new independent replay.
- [freeCodeCamp #71474](https://github.com/freeCodeCamp/freeCodeCamp/pull/71474), author jerome-queck, merged 2026-10-31 11:09:15 UTC. Corrects synchronous/asynchronous callback definitions in two reviews. Already featured; useful to retain as concise educational contribution.

## Remaining recent work

All author jerome-queck, checked against direct PR metadata.

| PR | State | Selection reason |
| --- | --- | --- |
| [OpenClaw #190257](https://github.com/openclaw/openclaw/pull/190257) | Open | Async persisted-auth probing removes misleading Matrix SDK warnings in status/channels/doctor. Strong alternate pending item; body reports real built CLI and red/green proof. |
| [OpenClaw #190269](https://github.com/openclaw/openclaw/pull/190269) | Open | Doctor advisory for bare empty tool allow lists. Companion credits original Navras98 patch; avoid sole-original-fix claim. |
| [OpenClaw #190299](https://github.com/openclaw/openclaw/pull/190299) | Open | Useful unknown-device diagnostics, narrower than merged #189993. |
| [OpenClaw #190282](https://github.com/openclaw/openclaw/pull/190282) | Open | Gateway lock errors identify lock path. Companion preserves carlosjarenom authorship; lower priority for personal profile. |
| [OpenClaw #189880](https://github.com/openclaw/openclaw/pull/189880) | Open | Sandbox explain bundled-channel repair, companion work. |
| [OpenClaw #189881](https://github.com/openclaw/openclaw/pull/189881) | Open | Doctor warns on undeliverable cron alerts, companion work. |
| [OpenClaw #189499](https://github.com/openclaw/openclaw/pull/189499) | Closed, not merged; merged_at null | Do not describe as landed. macOS dns-sd TXT parsing proposal. |
| [Vorssaint #3737](https://github.com/vorssaint/vorssaint-utils/pull/3737) | Open | Focus-follows-mouse fallback proposal; macOS verification absent per PR. Prefer DST item if including one Vorssaint example. |

