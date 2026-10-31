# Profile artwork and maps

Generated 31 October 2026 with the built-in imagegen tool. The artwork illustrates identity;
it does not represent real dependencies, mathematical results or measurements. Native text
and the separate project map carry factual content. No blanket artwork licence is selected.

The shared direction uses midnight blue, cyan, ivory and small warm accents. The original
prompts ask for a cinematic mathematical control room, an original exploration-game map and
motorsport precision, without protected logos or branding. Existing project screenshots stay
unfeatured. Both banners have their own opaque canvas for consistent light/dark appearance.

## Prompts

### Personal

Use case: stylized-concept
Asset type: original wide banner for a mathematician and software builder's GitHub profile README.
Primary request: a restrained cinematic mathematical control room, drawn as a precise isometric cutaway on deep midnight blue. One continuous luminous cyan trajectory runs through a wireframe saddle surface and a tiny amber computation instrument, then turns like a racing line around a sculptural curve. A few subtle film-frame perforation marks at the edges suggest cinema. The composition should feel like a thoughtful indie video game's navigation map, not corporate clip art. Sparse, highly deliberate, generous negative space, tactile paper grain and fine technical engraving. Wide 3:1 landscape composition, no lettering whatsoever. Palette midnight navy, ice cyan, warm ivory, small vermilion accents. No logos, no people, no protected game or racing branding, no trophy, no dashboard cards, no neon city, no text, no watermark. Keep all salient details visible when scaled to 720 pixels wide. This is an atmospheric artwork; it must not pretend to display real project architecture or data.

### Organisation

Use case: stylized-concept
Asset type: original wide banner for Jerome-Group's GitHub organisation README, companion to a mathematical control-room personal banner.
Primary request: a restrained cinematic isometric workshop of mathematical instruments. Three connected platforms form an elegant continuous circuit, a wireframe geometric surface on one, a small ivory mechanical computing instrument on another, and a fine-lined racing trajectory curling around a central architectural ring. Fine technical engraving, dark midnight blue paper, ice cyan route, warm ivory forms and tiny vermilion accents. Suggest an original indie exploration video game's world map and the precision of a motorsport engineering studio, with subtle film edge marks. Wide 3:1 landscape, generous breathing room, strong readable silhouettes at 720px wide, no text. Quiet, specific and sophisticated. No logos, no protected game or Formula 1 branding, no people, no screens, no dashboard cards, no trophy, no watermark. Atmospheric artwork only; do not imply real project dependencies or measurements.

## Maintenance

Both originals were 2172 by 724 PNGs. JPEG delivery copies are 1440 by 480, made with
`sips -s format jpeg -s formatOptions 85 --resampleWidth 1440 INPUT --out OUTPUT`.
No compositing, textual overlay or creative retouching follows generation.

Personal artwork is `assets/control-room.jpg`. Its map is regenerated with
`python3 scripts/render_identity.py`. The existing daily workflow maintains public contribution
data on `profile-data`. Both activity feeds display two events. Statistical definitions remain
separate for the individual and the organisation.

Organisation artwork source is `dot-github/profile/assets/control-room.jpg.b64`.
To inspect it, decode with `base64 -D -i SOURCE -o PREVIEW.jpg` on macOS.
Keep the encoded source below 1 MB. The snapshot generator decodes it and the existing
workflow publishes `control-room.jpg` with the statistics on `profile-data`. Do not put binary
files in the Terraform text fileset. The authored map is regenerated with
`python3 dot-github/profile/scripts/identity.py`. See ADR-0059 and the published lifecycle page.

After changing projects, verify public ownership and site behavior, change the native README
and the small project registry, regenerate the SVG, then inspect actual GitHub rendering.
The map groups projects editorially, not as a dependency graph. Descriptive alt text and native
links retain meaning when an image cannot load. Expanding details reveals retained calendars,
recent activity and repository context. The snapshot README provides accessible text numbers.

Delivered JPEG SHA-256: `85e378c4a13f97963c2874a215142cc9da7e3391d521e025a4d7a67b386af341`.
