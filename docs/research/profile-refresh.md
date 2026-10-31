# Profile refresh research

Research date 2026-10-31. Goal is two distinctive graphical GitHub profiles whose factual content and generated activity remain useful and maintainable. Research only. No source edits, publication, or visual acceptance performed by this worker.

## Existing content and decisions

Inspected the [personal profile](https://github.com/jerome-queck), [organisation profile](https://github.com/Jerome-Group), and both local README sources. Web extraction provides content evidence, not a pixel render. Its cached crawl dates ranged from today to last month, so final publication must use fresh GitHub/browser readback.

Personal source has a plain introduction and links, contribution counters/calendar/activity, separate Mathematics and Software sections, and an upstream OpenClaw contribution. Organisation source has identity, community policy links, working conventions, activity and declared assistance panels, Mathematics, Software, and shared standards. Preserve these useful destinations and reporting definitions.

Current personal `docs/design/decisions.md` records important owner decisions. Mathematics and Software remain separate. Graphical contributions should be prominent. Swiss Grid was rejected as boring. Generated A/B/C artwork was rejected as artificial. Algebra/Calculus screenshots were removed as unnecessary on 2026-09-10. Clarifold and Doomsday Protocol remain excluded. Refreshing dashboard graphics respects these decisions; restoring screenshots requires an explicit new decision.

## Primary-source comparison

| Example | Observed mechanism | Useful lesson |
| --- | --- | --- |
| [DenverCoder1](https://github.com/DenverCoder1/DenverCoder1) | Custom name image, animated typing image, social icons, project cards and generated activity. Raw README confirmed external graphic endpoints. | Strong hierarchy and recognisable colour are possible; borrow hierarchy, retain owned generated assets rather than add endpoint dependencies. |
| [Sindre Sorhus](https://github.com/sindresorhus/sindresorhus) | Repository owns many retro GIFs and badges; links and short text supply destinations. | A coherent visual vocabulary creates personality without custom page CSS. Its busy retro language is a reference, not the proposed style. |
| [Anthony Fu](https://github.com/antfu/antfu) | README source is a centred compact line of links in `samp`. | Deliberate editing and few destinations can establish identity. Too little visual content for this request. |
| [Microsoft](https://github.com/microsoft/.github/blob/main/profile/README.md) | Owned banner, short participation links, explicit support routing, Code of Conduct. | Organisation profiles can be visually identifiable and still make engagement the main task. |
| [ReadMe](https://github.com/readmeio/.github/blob/main/profile/README.md) | Right-aligned owl illustration, compact brand badge, native headings and audience-specific links. | One recognisable asset can carry identity. Avoid copying its external S3 asset dependency or treating its inline style as guaranteed support. |

## Rendering and accessibility boundaries

GitHub documents `picture` with light/dark `prefers-color-scheme` sources plus an `img` fallback and alt text. Use this supported mechanism if the graphics need theme variants. [Official quickstart](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github).

The rendering pipeline sanitizes HTML, removing scripts, inline styles, and class/id attributes. A local HTML approximation cannot establish GitHub fidelity. Custom fonts and colour fields can exist inside an SVG, but surrounding README typography and page layout belong to GitHub. [GitHub markup pipeline](https://github.com/github/markup).

Images accept alt text and repository-relative URLs; GitHub recommends relative image links for repository assets. Use absolute raw URLs for generated assets on the separate `profile-data` branch. [Official syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax).

GitHub's own documentation accessibility guidance keeps instructions in text, requires useful image descriptions, and avoids obscured or low-contrast content. Apply that principle to activity graphs by linking to their underlying textual records and definitions. This is design guidance, not a GitHub README validator requirement. [Screenshot accessibility guidance](https://docs.github.com/en/contributing/writing-for-github-docs/creating-screenshots).

Mermaid is supported, but GitHub documents accessibility limitations for some charts. Prefer native text and purpose-built SVG data graphics for the profile's dashboard; reserve Mermaid for an actual relationship diagram. [Diagram syntax](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams), [known accessibility limits](https://docs.github.com/en/repositories/working-with-files/using-files/working-with-non-code-files).

Public personal profiles render the public matching-name repository's root README. Public organisation profiles use `.github/profile/README.md`; signed-in members may instead see the member view. Check public view explicitly. [Personal prerequisites](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [organisation profiles](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile).

## Recommended direction

Use a shared mathematical visual language, but give each profile its own identity. Personal profile should feel like a working mathematician's notebook. Organisation should feel like its project collection and operating system. Keep personal first-person voice and organisation contributor-facing voice.

Make the existing generated activity graphics the distinctive visual centre. A restrained ink background, cyan/teal data, clear metric typography and a mathematical coordinate/grid motif can unify them. These are proposed aesthetic choices, not measured preferences. Avoid generic skill badges, visitor counts, typing animations, and fake terminal introductions.

Keep introductions and all project descriptions as selectable native text. Use an optional compact owned graphic for identity only if a live GitHub prototype earns its place. Keep useful links beside graphics so a missing image never removes navigation or provenance.

Put meaningful work before governance detail on the organisation page. Retain community policy navigation near the top, but let projects and activity establish what the organisation does. Keep working conventions near the bottom. Preserve assistance definitions, mixed/undeclared categories, and the explicit PR-count scope.

At mobile width, prioritise readable counters and recent activity. A full 365-day calendar may remain a broad overview, but its tiny labels must not carry the only metric definitions. Use short lines, generous labels, one graphic per row and textual records. Avoid table-based project-card grids and dense full-width raster text.

## Verification handoff

1. Publish prototype branch assets and inspect the actual GitHub document before selecting the final treatment.
2. Capture light and dark at desktop and narrow mobile widths. Check SVG text legibility, overflow, correct theme selection, no missing assets, and all destinations.
3. Inspect images-disabled/alt-text fallback and the linked underlying metric records. Keep freshness and public-only scope visible.
4. Confirm generators still create every linked SVG, preserve numeric semantics, escape public titles, and tolerate empty activity.
5. After merge/publish, capture the actual personal and public organisation profile placements. Branch README rendering alone does not prove final profile width or publication.

PASS for research coverage. Visual design selection and final browser verification remain with the implementation/root worker.
