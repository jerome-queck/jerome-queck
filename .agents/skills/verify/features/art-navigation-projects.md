# Art, navigation and projects

## Sub-features

Native GitHub profile avatar, original cover and illustrated project exhibits; three numbered chapter buttons; native Mathematics, Software and Public work headings; five mathematics destinations; four software projects; website, LinkedIn and design provenance links. Source is `README.md`, `data/projects.json`, `scripts/render_interface.py` and `docs/design/circuit-atlas.md`.

## How to get to it (user POV)

Open the public profile or the repository README. Click each illustrated chapter button. Explore all five mathematics destinations and inspect their source disclosure. Read all four software descriptions and open repository links. Follow the footer's design provenance.

## Driving it with Playwright

Run both `drive.cjs` commands in the skill. The driver uses `article.markdown-body`, image links whose observed href names each chapter, and native `details > summary` clicks. It saves target geometry after chapter clicks and navigates actual source anchors to every selected public repository. Inspect before/expanded, native profile avatar and destination screenshots. Avatar metadata and element screenshots are captured only on the actual profile. Compare the visible avatar against the approved artwork; README images cannot establish that the account avatar changed. Manually open each non-GitHub project URL and website/LinkedIn/provenance link if the change touches its destination; capture actual navigation and final page. A source repository response does not prove its deployed site.

## Gotchas

GitHub rewrites heading IDs to `user-content-*`; href changes alone do not prove a chapter scrolled into view. Image decoding does not establish artistic quality. Calculator requires sign-in for notebook execution; public landing navigation is reachable, authenticated notebook behavior is a distinct `verified-unreachable` boundary without authorized credentials. Syrax and Emmy graphics are illustrative, not screenshots or execution proof.
