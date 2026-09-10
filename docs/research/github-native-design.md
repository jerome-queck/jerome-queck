# Designing within GitHub

Researched 2026-09-10 after the generated page mockups were rejected.

## The correction

The earlier board showed a custom web layout, not a faithful README preview. Its typefaces, full-panel backgrounds, rounded cards, equal-height grid and detailed spacing were not demonstrated in GitHub. Flattening those designs into images could reproduce their appearance, but sacrifices selectable text, meaningful individual links and comfortable reading at narrow widths. It is the wrong default for this profile.

## What is possible

| Technique | What GitHub provides | Fit for this profile |
| --- | --- | --- |
| Native Markdown | GitHub headings, paragraphs, links, lists, tables and rules | Strong baseline; text adapts to the available width and theme |
| Small SVG or PNG accent | A bounded image inside the document | A restrained mathematical drawing can add identity without becoming the whole page |
| Real project screenshots | Linked images of the actual work | More specific than invented artwork; use only a few and keep captions as text |
| Light/dark artwork | `picture` with `prefers-color-scheme` sources | Useful when an image needs theme-specific colours; it does not theme the whole README |
| GIF animation | Animation inside an image | Technically viable; likely distracting unless demonstrating actual project behaviour |
| Tables / limited HTML | Basic rows, cells, alignment and image sizing | Good for data; avoid treating tables as responsive card layouts |
| Math / Mermaid | GitHub-rendered equations and diagrams | Use for actual mathematical or architectural content, not decoration |
| Stats cards | Generated images embedded in Markdown | Feasible but generic; outsourced endpoints add maintenance and availability concerns |
| Custom CSS / JavaScript | Sanitized rather than executed as page styling or scripts | Cannot implement a custom interactive portfolio inside the README |

The exact boundary matters: a custom typeface or complex colour treatment can be drawn *inside an image*. That does not grant control over GitHub’s surrounding text, page background, spacing, hover behaviour or mobile layout. An ordinary linked image has one destination; it is not a collection of independently clickable HTML project cards.

Sources: [GitHub HTML sanitization](https://github.com/github/markup), [official profile formatting guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github), [math](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions), [diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

## Real examples inspected

- [Anthony Fu](https://github.com/antfu/antfu): the README source is a small centred line of links using `samp`. Evidence that a profile can be deliberate and personal with almost no graphic content. This is a restraint reference, not a proposed copy of its navigation-only content.
- [Sindre Sorhus](https://github.com/sindresorhus/sindresorhus): a retro collection of GIFs, image badges and plain links. Evidence that strong visual personality is possible, but delivered as embedded assets. Its deliberately busy style is not recommended here.
- [GitHub Readme Stats](https://github.com/anuraghazra/github-readme-stats): demonstrates that dashboard-like cards are generated images. The repository now reports it is unmaintained and points to successors; do not introduce this dependency for decoration.

README sources were read through GitHub’s API in addition to their public pages. The comparison distinguishes an observed mechanism from an aesthetic recommendation.

## Initial visual budget — superseded by screenshot selection

The owner subsequently selected authentic screenshots with native text; see [current decisions](../design/decisions.md). The initial options below remain as research history.

1. Keep GitHub’s typography and a short personal introduction.
2. Use five project entries in two sections, each with one concrete sentence.
3. Compare the native version with one small, mathematically defined line drawing. No large hero, invented sculpture or text baked into images.
4. If more visual evidence is wanted, prefer actual Algebra and Calculus screenshots to decorative project cards.
5. Assess the actual GitHub-rendered documents before selecting the design. A repository Markdown render proves the document’s mechanisms, not the exact width of the account-profile placement.

[Native version](../../README.md) · [Optional-accent sample](../design/rendering-sample.md)

## Copy sources

Current public READMEs were read for [Academic OS](https://github.com/Jerome-Group/academic-os), [NTULearn](https://github.com/Jerome-Group/ntulearn), and [Syrax](https://github.com/Jerome-Group/syrax). The Algebra and Calculus scope is supported by their previously checked READMEs and the owner’s description of them as notes websites. Syrax is described as its existing Telegram/OpenClaw setup, without claiming planned worker tools are implemented. Doomsday Protocol and Clarifold are excluded.
