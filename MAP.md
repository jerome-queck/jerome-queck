# Repository map

Jerome Queck's personal GitHub profile and its public-data pipeline.

- `README.md` is the profile, with nine selected projects and graphical navigation.
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/agents/` carry contributor rules; `CONTEXT.md` carries vocabulary.
- `data/projects.json` is the authored nine-project catalogue, separate from fetched facts.
- `assets/` contains original artwork and authored interface/diagram assets; provenance is in `assets/README.md`.
- `scripts/render_readme_world.py` composes native linked workshop views; `scripts/readme_world.py` composes the snapshot data ledger. Older interface studies remain documented prototypes.
- `scripts/profile_data.py` collects the complete snapshot; `scripts/upstream_prs.py` owns the scoped upstream search; `scripts/profile_style.py` owns measured outlined type.
- `scripts/repo_pulse.py`, `public_calendar.py`, `recent_activity.py` own selected repo facts, public calendar and the minimal feed; `source_lines.py` counts pinned public source archives.
- `.github/workflows/` runs CI and daily collection/publication; `tests/` exercises metrics, boundaries and remote Git publication.
- `assets/type/` contains pinned OFL fonts and their manifest; `requirements.txt` pins shaping dependencies.
- `.agents/skills/verify/` owns the actual GitHub browser driver, feature maps and maintenance procedure.
- `.agents/skills/profile-publication/` and `formal/` own the bounded publication model, real Git mutation checks and source-drift alarm.
- `docs/design/data-graphics.md` records public graphic definitions and regeneration; `docs/design/decisions.md` retains the decision history.
- `docs/research/` records primary evidence; `docs/adr/` records architectural tradeoffs.
- Exploratory designs remain on `prototype/` branches and do not merge into `main`.
