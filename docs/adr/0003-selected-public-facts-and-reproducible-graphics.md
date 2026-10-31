# ADR-0003. Selected public facts and reproducible graphics

Status: accepted for implementation, 1 November 2026. Extends ADR-0002.

The Owner requests useful repository and contribution automation alongside the graphical redesign. Broad repository discovery would feature excluded or unrelated work. Independent widget refreshes would mix provenance and dates.

Keep the existing scoped contribution collectors and add a small selected-repository collector, driven by nine authored identities in `data/projects.json`. Reject unavailable, transferred or non-public identities. Enumerate published releases fully, label prereleases, and treat an empty release history as a valid result. Read the default branch's actual Commit target rather than repository update time. Its date is not Jerome's authorship or deployment evidence.

Persist minimal normalized public facts in `snapshot.json`. All data graphics and accessible text derive from that saved input. Reuse the existing merged PR traversal for twelve UTC calendar-month buckets, with the current month explicitly partial. Capture collection start and completion. GitHub offers no transaction across these source reads, so the publication states an observation interval.

Retain the existing generate/publish job separation, daily cadence, explicit payload allowlist, main-only publication and non-force push. All eleven required payloads advance in one Git commit. An absent current payload or failed source prevents publication. This protects the previous complete snapshot; it does not synchronize raw-image CDN caches, prove source correctness, or retract previously public history after a visibility change. A privacy change needs deliberate removal of already-published historical data outside this ordinary refresh.

A general API client, renderer registry and separate scheduler add no useful boundary here. One composition root and specialized collectors/renderers keep the implementation small. This choice extends the public data payload beyond ADR-0002's five files; that earlier migration remains historical.
