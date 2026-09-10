# GitHub profile README constraints

Checked 2026-09-10 against official documentation and public repository READMEs.

## Profile surface

A public repository named exactly like the account, with a nonempty root README.md, displays that README on the profile. Local folder names do not matter. [GitHub requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)

GitHub sanitizes HTML, removing scripts, inline styles and class/id attributes. A custom CSS layout or JavaScript application cannot execute inside the README. [Rendering pipeline](https://github.com/github/markup)

Images, including SVG and GIF, offer the main visual freedom. The picture element supports theme-specific image sources. Retain fallback images and meaningful alt text. [Image guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github)

LaTeX expressions and Mermaid diagrams are supported. Use them where they communicate actual content. [Math](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/writing-mathematical-expressions) · [Diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

Dynamic cards are generated images or periodically edited Markdown, not live widgets. Remote images may be cached. Scheduled Actions can be delayed and public-repository schedules disable after 60 days without repository activity. [Schedules](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)

## Other public uses

Supporting files can include project case studies, posters, a CV, artwork, a curated project catalogue and generation scripts. Link them explicitly from the README. They do not automatically become profile sections.

GitHub Pages publishes a separate static HTML/CSS/JavaScript website. It is distinct from the profile README. An existing homepage already provides a destination for richer interaction. [Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

## Project sources

- [Algebra](https://github.com/Jerome-Group/algebra): groups, rings, fields and representations, with chapters and visual laboratories. [Live](https://algebra.jeromegroup.org)
- [Calculus](https://github.com/Jerome-Group/calculus): multivariable calculus through visual explanations and 3D geometry. [Live](https://calculus.jeromegroup.org)
- [Academic OS](https://github.com/Jerome-Group/academic-os): module organisation, tasks, calendar and data behind the homepage.
- [NTULearn](https://github.com/Jerome-Group/ntulearn): imports course pages, announcements and attachments into module folders.
- [Syrax](https://github.com/Jerome-Group/syrax): public personal chatbot system and setup.

Repository descriptions and the Algebra/Calculus READMEs were read live. Hosted URLs above come from those READMEs; this record does not claim a full deployment test. LinkedIn was accessible only behind a sign-in overlay, so detailed biography is deferred.
