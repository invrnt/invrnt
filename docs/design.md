# The quiet machine

A GitHub profile for Juan Camilo Grisales. One ceramic control hides an entire precision machine. The same material, camera and amber signal connect every scene.

## Build

```sh
python3 tools/build.py
python3 tools/validate.py
```

The builder uses only Python's standard library. Edit the drawings and copy in `tools/build.py`, then rebuild. It writes `README.md`, 16 SVGs and the optional control study in STL. No runtime service or build step is needed on GitHub.

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
- A source selected for a narrow viewport uses a separately composed 640-unit scene. Desktop scenes are 1200 units wide. SVGs adapt their own palettes to the embedding page's color scheme, including when GitHub's theme differs from the operating system.
- Keep `picture` media conditions limited to viewport width. GitHub's `themed-picture` component replaces an entire media condition when it finds `prefers-color-scheme`, discarding a combined width condition. Internal SVG theme queries avoid this conflict. This was checked in GitHub's live page with local assets substituted in the browser, without publishing changes.
- `prefers-reduced-motion` stops animations and reveals a coherent static state. Count shows the completed example; the hero remains open for inspection.
- No sequence depends on another file's timeline, scrolling, hover, or user interaction inside the SVG. The Count choices are an illustration, not real buttons.
- The profile can be read through image alternatives and a native Text edition. SVG `title` and `desc` are supplementary; scraping them is not assumed.
- Count is labeled as a product concept in development. No animated amount is represented as a live financial balance or an investment projection.
- `control.stl` is a geometric study of the ceramic control, viewable through GitHub's native 3D file viewer. It is not a manufacturing specification.

## Sources

Content was checked against [juancamilo.me](https://juancamilo.me), [invrnt](https://github.com/invrnt), [Orientador](https://orientador.co) and [Bento](https://github.com/invrnt/bento), along with the owner's Count description and philosophy.

Platform references: [GitHub picture elements](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github), [collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections), [native diagrams and STL](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams), and [SVG image restrictions](https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image).
