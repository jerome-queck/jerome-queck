# Profile feature map

All four features are required. Neither a convenient single screenshot nor the collector alone covers the public experience.

| Feature | Source | Required surfaces |
| --- | --- | --- |
| [Art, navigation and projects](art-navigation-projects.md) | `README.md`, `data/projects.json`, `scripts/readme_world.py`, `scripts/render_readme_world.py` | Profile and repository README; continuous canvas, nine image-title destinations and five source buttons |
| [Contribution charts and upstream work](contributions-upstream.md) | `scripts/profile_data.py`, `scripts/public_calendar.py`, `scripts/recent_activity.py`, `scripts/repo_pulse.py`, `scripts/source_lines.py` | Static data ledger, native definitions, six merged upstream PRs, published text |
| [Publication and source](publication-source.md) | `.github/workflows/profile.yml`, `scripts/profile_data.py` | Collector CLI, actual `profile-data` branch, workflow page |
| [Accessibility and responsive layout](accessibility-responsive.md) | `README.md`, `assets/`, SVG renderers | Both GitHub surfaces, desktop/mobile, light/dark, collapsed/expanded |

[Coverage record](../coverage.json) pins the baseline source and honest run status. Maintenance rereads all source entries, checks siblings match this index, then drives every mapped feature. Keep screenshots and run notes outside the repository.
