# ADR-0004. Outlined typography and complete upstream input

Accepted 2 November 2026.

## Context

The public data graphics need the same Fraunces, Source Sans 3 and IBM Plex Mono in local previews and GitHub's image renderer. Native Markdown cannot set custom fonts. External font loads inside images are unreliable, while arbitrary PR titles and release tags can contain Unicode beyond the three fonts. New upstream and language charts must share the existing all-or-nothing refresh.

## Decision

Bundle pinned OFL font sources and licenses. Use pinned fontTools and uharfbuzz with an explicit HarfBuzz version. One small typography module owns palette, font roles, shaping, measured bounds, outlines and missing-glyph failure. Existing renderers keep their composition. Reuse local glyph definitions within each SVG. Native Markdown retains full Unicode titles, exact release tags, values and links. Graphic text uses compact authored labels or public repository identities. Unsupported glyphs and overflow abort rendering.

Extend the public snapshot to schema 2. Require complete scoped upstream records and selected-repository language byte maps; do not interpret absent fields as empty. The upstream collector validates public visibility, author, owned-namespace exclusions, explicit merged state and timestamps. Search pagination must produce its exact reported count, with advancing cursors, no duplicate records and at most 1000 results. Repository language connections must fit the 100-language request and match their reported totals. A failure in either new source aborts the complete refresh before writing.

Keep ADR-0003's nine selections, existing aggregate scope, timestamp interval, saved input and eleven publication payload names. The displayed cadence and calendar begin on 1 July 2026. All-time counters retain their scope. The charts add upstream merges and repository states, language bytes, and weekday frequency inside the existing SVGs. These are records, not expertise, effort, impact or deployment evidence.

## Consequences

Graphic text renders without installed browser fonts. Font and shaping updates require pinned dependencies, hash readback, regeneration and visual review. Local paths enlarge assets, so definitions are shared within each image and byte sizes are checked. The font licenses travel with the font files, without changing the repository's undecided blanket license.

New source errors preserve the previous complete publication. A search above 1000 results requires a future partitioned collector. This version fails honestly at that boundary. Schema 1 remains historical and cannot silently acquire zero-valued new charts.
