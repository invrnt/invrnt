# The interface steps aside

A GitHub profile for Juan Camilo Grisales. It opens as GitHub's own contribution graph and activity feed, redrawn at native size with real data. Then the surface splits between Wednesday and Thursday, the lower half drops away, and beneath it is the promise and the system that keeps it, drawn as a chip seen from above: *More possible. Less in the way.* One amber signal runs from under that surface through every scene and ends in a single ceramic control.

## Visual language

Interface on top, system underneath. There are no isometric illustrations. Each scene shows what a product produces as interface, at a fidelity close to the real thing, and lets the mechanism show through: entities outlined in a sentence, citations wired to their sources, files leaving one window for another. GitHub's own interface is set in Mona Sans; everything that belongs to Juan's products is set in Manrope. The one physical object, the ceramic control, is real 3D in GitHub's viewer.

## Avatar

`assets/avatar.png` is the profile picture: one porcelain day among eight unlit neighbours of the contribution graph, cut open by a line of amber light. The cut sits slightly below the middle, like the hero's split between Wednesday and Thursday, so the icon and the page make the same gesture.

It was generated with an image model from a composition drawn in the profile's palette, then cropped to the central 72% so the lit cell still reads at 20 px and the neighbours run past the circle, as if the graph continued. GitHub does not allow setting avatars through the API; it is uploaded by hand in profile settings. The README does not reference it.

## Build

```sh
GH_TOKEN=$(gh auth token) python3 tools/fetch.py   # optional: refresh the data snapshot
python3 tools/build.py
python3 tools/validate.py
```

The builder uses only Python's standard library and never touches the network. It reads `tools/data/github.json`, a snapshot written by `tools/fetch.py`, and writes `README.md`, 32 animated scenes, 32 corresponding stills, 8 theme-neutral controls and the STL study. Rebuilding produces byte-identical output.

`.github/workflows/refresh.yml` refreshes the snapshot daily and commits only when something changed. It uses a `PROFILE_TOKEN` secret if one exists and falls back to the workflow token. It can also be started by hand from the Actions tab.

## Files

| File | Role |
| --- | --- |
| `tools/build.py` | Scenes, drawing primitives, the die, product interfaces, README generation, STL. |
| `tools/surface.py` | GitHub's interface at native pixel size: calendar, activity feed, file table, Octicons. |
| `tools/fetch.py` | Snapshot of the contribution calendar, this month's activity and Bento's file list. |
| `tools/fonts` | Manrope and Mona Sans subsets, plus precomputed advance widths for both, used to fit text without a browser. |

Manrope (`docs/Manrope-OFL.txt`) sets the profile's own voice. Mona Sans (`docs/MonaSans-OFL.txt`) is GitHub's typeface, embedded only where the interface is imitated, so the imitation matches the page around it. Octicons are MIT licensed.

## Scenes

| Scene | Purpose | Motion |
| --- | --- | --- |
| Hero | The interface steps aside | Native graph and feed for 2.8 s, a glitch along the cut, the lower half drops. Beneath, a die: intent, memory, tools, a reasoning core, verification, one control out. Buses carry pulses; compute units light in diagonal waves. 20 s. |
| Count | One natural-language instruction becomes precise accounting | Voice note, ambiguity, selection, balanced posting. 24 s. |
| Port | Detail stays available | A porcelain button on the signal line. It is the `summary` of a native `details`. |
| Architecture | Simple is engineered | One real sentence through five layers, each shown as its interface: entities, a clarifying question, a balanced entry, monthly accrual, the record. Layers light in turn. Plus the control in GitHub's inline 3D viewer. |
| Classmate | Different materials share one context | Audio, PDF and slides beside one answer; as it is written, citations wire each claim to its source. 12 s. |
| Orientador | Documentation leaves room to listen | The conversation appears only as rhythm, never words. A session note assembles as a draft and the counselor signs it off. 12 s. |
| Bento | Your files stay yours | GitHub's file table for Bento drains row by row; each file lands in its own tile in Bento's window, on this device, and the table says where they went. 12 s. |
| Ambition | Productivity enables larger projects | A contribution graph for whole industries, seven rows like seven days. The cost of trying falls and the columns bloom in turn. 24 s. |
| Contact and keys | Return to one simple control | The signal turns and ends in the control. Three porcelain keys are real links. |

## GitHub constraints

Verified on the live profile on October 31, 2026, with the README rendered through GitHub's Markdown API and injected into the real profile page.

- **Seamless joins.** Images inside one `<p>` with `align="top"` stack with no gap; without `align` each join leaves a 6 px baseline strip. The open content of a `details` also joins its `summary` image exactly. Scenes have transparent backgrounds, so joins are invisible in both themes.
- **The signal line** sits at x = 28 of 1200 (desktop) and x = 14 of 640 (mobile) in every scene, so it continues across files. It breaks only at the two native gaps: before the port's `summary` (the disclosure marker sits on its own line) and after the details.
- **Themes** use GitHub's `#gh-light-mode-only` and `#gh-dark-mode-only` link fragments; GitHub hides any element whose `href` ends in one. `picture` media conditions stay limited to width and reduced motion, because GitHub's `themed-picture` rewrites any condition containing `prefers-color-scheme`.
- **Controls are theme-neutral.** A link inside `summary` would navigate instead of toggling, and a fragment on a `mailto:` link would leak into the address. The port and keys are drawn in fixed porcelain that reads on both themes, so they need no fragment.
- **A bare `img` in `summary` is wrapped in a link to the image** by GitHub; a `picture` is not. The port always uses `picture`.
- **Three links in one row:** three images at 33.333% in the same paragraph share a line with no gap. GitHub strips `<map>`, so this is how one composition gets several real targets.
- **Inline 3D.** A ```` ```stl ```` block renders GitHub's interactive viewer inside the README on the profile page. The README carries a 32-segment ASCII copy of the control (~100 KB); `assets/control.stl` keeps the full binary study.
- All artwork is self-contained SVG loaded as an image: internal CSS animation of transforms, opacity and strokes. No scripts, `foreignObject`, external fonts, images or links.
- A `picture` source selects a prepared still under `prefers-reduced-motion`. In the hero still, the surface is open.
- The imitation is the profile's own public data. No sequence depends on another file's timeline, hover or interaction inside the SVG.
- The profile remains readable through image alternatives and the native Text edition.

## Verification

- Chromium on the live profile page at 1380 px and 390 px, dark and light, closed and open details, reduced motion. No horizontal overflow or page errors. Joins measured to the hundredth of a pixel.
- The inline STL viewer rendered in the profile page with software WebGL.
- Firefox on the live profile page (joins, themes) and on individual scenes at several animation times, including the glitch and the Bento rows, which use CSS custom properties inside keyframes. Safari was not tested.

Review captures stay in the ignored `work/` directory. The profile itself only needs `README.md` and `assets/`.
