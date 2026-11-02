# Midnight workshop

One opaque SVG spans each viewport. The original workshop artwork and observed public data share the same canvas and collection timestamp. Mobile art is composed for 480 units, desktop for 900; GitHub selects the image with a native `picture` element. SVG animation affects scenery only. Browser-native reduced-motion picture sources select separately rendered static worlds: embedded SVG media queries did not reliably stop animation in the observed Chrome image context. Static worlds contain no animation CSS. No controls imply unsupported interaction, and direct destinations remain native links beneath the world.

The sky continues into a workshop cutaway: authored project shelves, all-time counters, a monthly merge clock and the public-record calendar. Shelf bars show repository language bytes; tip dates include any author. Full language names, exact bytes, release records and source URLs remain in the accessible text snapshot. These graphics do not establish expertise or deployment.

Artwork is original, authored in `scripts/pixel_world.py`. Typography uses pinned local OFL sources listed in `assets/type/manifest.json`; all visible lettering becomes local SVG paths. Artwork attribution and retained reference provenance accompany the artist module. Existing upstream contribution authorship remains attached to the original PRs.

`render_world(snapshot, panels, mobile=False)` consumes the same completed schema-2 public input as the other data graphics. Inline scene and calendar IDs receive distinct namespaces. No external images, font requests or scripts execute inside the world. The native snapshot preserves arbitrary Unicode titles and full source records.

Fifteen required payloads publish in a single ordinary Git commit: nine individual SVGs, four world SVGs, `snapshot.json` and its native `README.md`. Any missing payload prevents the remote ref from moving. Failed collection or rendering retains the prior publication and its timestamp. Separate CDN caches may refresh at different times.
