---
name: profile-publication
description: Check complete, failure-retaining profile-data publication after changes to collection, rendering, workflow publication, or its tests.
---

A partial refresh can show contradictory public facts. The checked promise is that an existing profile-data ref contains one complete generation after a successful push; failure before push leaves the ref untouched, and a stale non-force push cannot overwrite a newer commit.

Run `python3 formal/check.py`. It checks source hashes and the payload mapping, executes the real workflow's bare-Git fixture, requires a scratch omitted-copy workflow to expose a mixed snapshot, and runs the passing model plus two missing-copy mutants using TLC 2.19 from the SHA-256-pinned TLA+ tools 1.7.4. Java is required. Set `JAVA` to its executable and optionally `TLA2TOOLS` to the pinned jar; otherwise the checker downloads it to the user cache. The hashes are drift alarms, not evidence of semantic equivalence.

The source mapping was reviewed through `a968bf7`. It covers the generate and publish workflow, the CI invocation, `scripts/profile_data.py`, its imported local collection and rendering helpers, requirements, the project catalogue and both publication fixtures. Helper internals are outside the proof. The separately authored static-art renderer `scripts/render_readme_world.py` is not called by this workflow and is outside coverage. See [maintenance](../../../formal/maintenance.md) for the mapping, bounds and evidence.

The model starts with either the exact 11-file legacy snapshot or a complete 15-file snapshot. Two publishers attempt once each; their interleavings are adversarial although hosted workflow concurrency serializes runs. Collect/render success maps to Ready, copies to Copy, pre-push failure to Fail, and Git's atomic non-force update to Push. Numbered copy order is abstract except copy 6, cadence-mobile.svg, which is the mutant site. Generation, artifact upload and a complete payload are assumed before Ready. Bare-Git fixtures exercise both initial snapshots, each missing file, complete publication and stale push. Equality of generation represents ancestry only within this bound.

The check does not prove fetcher or renderer internals, GitHub API truth, font layout, scheduler behavior, cache visibility, first publication to an absent ref, or arbitrary writers. It does not execute the hosted runner. Model checking explores a bounded abstraction, not Python or shell semantics.

[One-publisher lifecycle](../../../formal/chart.mmd) illustrates both initial states. It hides copy-stage failure arrows and is not the two-publisher proof. To regenerate it, resolve the installed pstack Statechart script and run from the repository root with Java and the pinned jar available:

```sh
statechart=$(find "$HOME/.codex/plugins/cache/pstack-claude/pstack" -path '*/skills/statechart/scripts/statechart' -print | head -n 1)
"$statechart" formal/Publication.tla --config formal/chart.cfg --view formal/view.mjs --out /tmp/profile-publication-chart
```

On drift, read the diff from the sync commit, including moved writers and callers. Decide whether it changes an atomic boundary, failure path, payload list or promise. Update the model and fixture from actual code, never weaken a property to obtain a pass. Replay counterexamples against the real workflow. Confirm the original passes and both mutations fail for the stated reasons before updating the sync commit and hashes. For accumulated changes use `/maintain-formal-verification-skill`. CI invokes the check; also run it manually whenever covered code changes.
