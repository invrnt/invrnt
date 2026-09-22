# The quiet machine

A GitHub profile for Juan Camilo Grisales. One ceramic control hides an entire precision machine. The same material, camera and amber signal connect every scene.

## Build

```sh
python3 tools/build.py
python3 tools/validate.py
```

The builder uses only Python's standard library. Edit the drawings and copy in `tools/build.py`, then rebuild. It writes `README.md`, 32 animated SVG variants, 32 corresponding stills and the optional control study in STL. No runtime service or build step is needed on GitHub.

Manrope is embedded as a small WOFF2 subset in every SVG, so typography does not depend on the viewer's installed fonts or external requests. The bundled subsets are in `tools/fonts`; the SIL Open Font License is in `Manrope-OFL.txt`.

## Scenes

| Scene | Purpose | Motion |
| --- | --- | --- |
| Hero | One simple control hides substantial capability | Enclosure opens, arms process, shuttle advances, enclosure closes. 18 seconds. |
| Count | One natural-language instruction becomes precise accounting | Voice note, ambiguity, selection, balanced posting, passage of time. 24 seconds. |
| Architecture | Detail remains inspectable | Sequential signals connect five layers. |
| Classmate | Different materials share one context | Source signals converge on an open book and an output document. 12 seconds. |
| Orientador | Documentation leaves room for human attention | Conversation signal becomes a draft for professional review. 12 seconds. |
| Bento | The user's files remain local | Files settle into an organized enclosure. 12 seconds. |
| Ambition | Productivity enables larger projects | A workshop, research instrument and greenhouse become available in sequence. 24 seconds. |
| Contact | Return to the simple control | A quiet amber indicator. |

## GitHub constraints

- The README uses native links, `picture`, `source`, `img`, `details` and `summary`. There is no page CSS or JavaScript.
- All artwork is external, self-contained SVG loaded as an image. Internal CSS animates transforms, opacity and strokes. No scripts, `foreignObject`, external fonts, external images, event handlers or SVG links.
- A source selected for a narrow viewport uses a separately composed 640-unit scene. Desktop scenes are 1200 units wide. Explicit light and dark assets preserve contrast even when GitHub's theme differs from the operating system.
- Keep `picture` media conditions limited to viewport width. GitHub's `themed-picture` component replaces an entire media condition when it finds `prefers-color-scheme`, discarding a combined width condition. Theme selection instead uses GitHub's native `#gh-light-mode-only` and `#gh-dark-mode-only` link fragments. GitHub hides the matching link and its contained picture, preserving the width query. SVG-internal theme inheritance was unreliable in Firefox and is deliberately avoided.
- These theme fragments are GitHub-specific. A generic Markdown viewer may show both themes. A browser may fetch the hidden theme too. All 64 SVG variants total approximately 2.4 MB; a visitor only needs the assets selected for their viewport and motion preference, potentially in both palettes.
- A `picture` source selects a prepared still when `prefers-reduced-motion` is enabled. This avoids relying on motion-preference propagation into external SVG images. The animation rules are unconditionally disabled in still assets. Count shows the completed example; the hero remains open for inspection.
- No sequence depends on another file's timeline, scrolling, hover, or user interaction inside the SVG. The Count choices are an illustration, not real buttons.
- The profile can be read through image alternatives and a native Text edition. SVG `title` and `desc` are supplementary; scraping them is not assumed.
- Count is labeled as a product concept in development. No animated amount is represented as a live financial balance or an investment projection.
- `control.stl` is a geometric study of the ceramic control, viewable through GitHub's native 3D file viewer. It is not a manufacturing specification.

## Sources

Content was checked against [juancamilo.me](https://juancamilo.me), [invrnt](https://github.com/invrnt), [Orientador](https://orientador.co) and [Bento](https://github.com/invrnt/bento), along with the owner's Count description and philosophy.

Platform references: [GitHub picture elements](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github), [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections), [native diagrams and STL](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams), and [SVG image restrictions](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).

## Verification

Checked on September 22, 2026:

- GitHub's Markdown API accepted the README and preserved the picture sources, theme fragments, links and details elements.
- The rendered HTML was placed in a live GitHub profile page with asset requests fulfilled locally in the browser. This did not publish or change the remote repository.
- The actual GitHub page selected desktop art at a 1380 px viewport and mobile art at 390 px, in both themes. Content widths were 846 px and 308 px. No horizontal overflow or page errors appeared.
- With reduced motion enabled, the actual GitHub page selected the prepared still files. Repeated screenshots of an externally embedded hero were identical.
- Chromium and Firefox rendered the local preview in both palettes, including a dark page with a light operating-system preference. The native details control opened successfully. WebKit could not be launched because its system dependencies were unavailable; Safari is not claimed as tested.
- The illustrations were visually inspected at several animation stages. Text bounds, isolated resources, XML references, static variants and all 2,304 STL facets passed structural validation. Rebuilding produced byte-identical assets.

Review captures and the local HTML preview are kept in the ignored `work/` directory. The profile itself only needs `README.md` and `assets/`.
