# Publication proof maintenance

The source mapping is synchronized to `a968bf7`. The follow-up to `db91bb7` removes narration and sizes cadence columns from measured labels, allowing the current five-month mobile view to occupy one row. These changes do not move collection, rendering, writing or push boundaries. A layout failure still occurs before the completed mapping is returned. The unchanged checker rejected the changed helper hash before the mapping was refreshed. The prior synchronized base was `92b883461dbd1031a74d0730f40f83c891e6ce8b`; the unchanged check refused the workflow hash before this review. That was verification drift, not a demonstrated product bug. The covered diff includes e064c03's upstream inputs and font rendering, 865a4ed's four world outputs, 503c463's schema-v3 metrics, f22f6b3's source-line collection, 884d95d's calendar changes, and db91bb7's cadence layout. CI invokes the checker since ece575f.

`collect_snapshot` collects each required source, including source lines. `render_snapshot` validates schema 4 and builds the entire 15-file mapping. `main` writes only after both return. A generation failure or partial output write prevents the dependent publish job from receiving a successful artifact. The publish shell checks out the existing ref, copies and stages every payload, removes the obsolete card, and commits and pushes once if changed. An unchanged output is a no-op. The model abstracts collection, rendering, writes, artifact transfer and failed copies as pre-push failure. It treats unchanged successful publication as a complete generation; it does not distinguish the no-op branch. The source mapping covers the workflow, CI, collection and rendering entry points, their imported local helper modules, requirements, project catalogue and both Git fixtures. Their hashes are review alarms, not proof of their semantics. `scripts/render_readme_world.py` authors separate static artwork; the publication workflow does not call it and it is outside this proof.

The model starts from either the 11-file legacy snapshot with four absent world files or a complete 15-file snapshot. Two publishers attempt once each, capture a base, copy the 15 payloads and attempt an atomic non-force update. The numbered copies abstract their order except copy 6, which the guard maps to the actual cadence-mobile copy. Git ancestry is represented by generation equality only within this bound. Hosted workflow concurrency serializes runs; the model explores overlapping attempts. First publication to an absent ref, retries, arbitrary writers, liveness, hosted execution, API truth, font layout, pixel scene quality, randomness, animation and CDN consistency are excluded. Rendering is assumed successful before Ready; fixture execution supplies evidence for shell and Git correspondence, not a proof of their semantics.

TLC 2.19 with pinned TLA+ tools 1.7.4 explores 2,431 distinct states and 4,742 generated states to depth 35. `CompleteSnapshot` and `StaleRejected` hold. Omitting the existing cadence-mobile copy breaks completeness in 17 transitions, including from the legacy state. The scratch workflow reproduces the mixed snapshot with old cadence-mobile content; the restored fixture passes both initial states, all 15 missing payloads, complete one-commit updates, unrelated-file preservation and stale-parent rejection. Omitting a new world file is not modeled as a successful push: staging the absent path fails. Structural guard mutations for the bound, legacy slots, copy, staging and CI invocation were rejected. Detailed run output is retained as external evidence.

[One-publisher lifecycle](chart.mmd) is an illustration of both initial states, not the two-publisher proof. Its view hides 32 copy-stage failure steps; each retains its initial snapshot. The two-publisher passing run exceeds Statechart's 500-state drawing budget. The legacy-only mutant path and full passing report were generated separately.

## One-publisher lifecycle

This is the exact Statechart output from `chart.cfg`. It illustrates the checked lifecycle for one publisher, with both starting snapshots. The full two-publisher proof is reported above. Thirty-two copy-stage failure transitions are hidden; each leaves its initial complete or legacy snapshot intact.

```mermaid
---
title: "One publisher. Legacy upgrade and steady refresh."
---
stateDiagram-v2
  s0: Complete snapshot, 15 files
  s1: Legacy snapshot, 11 files
  s2: Copied 0 of 15 payloads
  s3: Complete snapshot retained
  s4: Legacy snapshot retained
  s5: Copied 1 of 15 payloads
  s6: Copied 2 of 15 payloads
  s7: Copied 3 of 15 payloads
  s8: Copied 4 of 15 payloads
  s9: Copied 5 of 15 payloads
  s10: Copied 6 of 15 payloads
  s11: Copied 7 of 15 payloads
  s12: Copied 8 of 15 payloads
  s13: Copied 9 of 15 payloads
  s14: Copied 10 of 15 payloads
  s15: Copied 11 of 15 payloads
  s16: Copied 12 of 15 payloads
  s17: Copied 13 of 15 payloads
  s18: Copied 14 of 15 payloads
  s19: Copied 15 of 15 payloads
  s20: Snapshot published
  [*] --> s0
  [*] --> s1
  s0 --> s2: Collect and render
  s0 --> s3: Refresh fails
  s1 --> s2: Collect and render
  s1 --> s4: Refresh fails
  s2 --> s5: Copy next payload
  s5 --> s6: Copy next payload
  s6 --> s7: Copy next payload
  s7 --> s8: Copy next payload
  s8 --> s9: Copy next payload
  s9 --> s10: Copy next payload
  s10 --> s11: Copy next payload
  s11 --> s12: Copy next payload
  s12 --> s13: Copy next payload
  s13 --> s14: Copy next payload
  s14 --> s15: Copy next payload
  s15 --> s16: Copy next payload
  s16 --> s17: Copy next payload
  s17 --> s18: Copy next payload
  s18 --> s19: Copy next payload
  s19 --> s20: Push snapshot
```
