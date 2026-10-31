# Repository map

Jerome Queck's personal GitHub profile and its public-data pipeline.

- `README.md` is the profile, with nine selected projects and graphical navigation.
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/agents/` carry contributor rules; `CONTEXT.md` carries vocabulary.
- `data/projects.json` is the authored nine-project catalogue, separate from fetched facts.
- `assets/` contains original artwork and authored interface/diagram assets; provenance is in `assets/README.md`.
- `scripts/render_interface.py` authors static chapter navigation, project links and the closing strip; `scripts/render_math_plate.py` plots exact square transforms.
- `scripts/profile_data.py` collects the complete snapshot and renders counters, merge cadence and accessible text.
- `scripts/repo_pulse.py`, `public_calendar.py`, `recent_activity.py` own selected repo facts, public calendar and the two-event feed.
- `.github/workflows/` runs CI and daily collection/publication; `tests/` exercises metrics, boundaries and remote Git publication.
- `docs/design/circuit-atlas.md` records the current design, prompts and regeneration; `docs/design/decisions.md` retains the decision history.
- `docs/research/` records primary evidence; `docs/adr/` records architectural tradeoffs.
- Exploratory designs remain on `prototype/` branches and do not merge into `main`.
