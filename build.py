from pathlib import Path
import math

root=Path(__file__).parent
assets=root/'assets'
def build(light=False,static=False):
    gold='#92703B' if light else '#C9A96E'
    faint='#CABDA6' if light else '#514936'
    ink='#554631' if light else '#DDD3BF'
    p=[f'''<svg xmlns="http://www.w3.org/2000/svg" width="896" height="248" viewBox="0 0 896 248" role="img" aria-labelledby="title desc">
<title id="title">The working desk of invrnt</title>
<desc id="desc">A transparent gold line drawing of an open notebook, a pencil and a drafting instrument. A pencil line slowly traces an idea across the page.</desc>
<style>@media(prefers-reduced-motion:reduce){{.motion{{display:none}}}}</style>
<defs><linearGradient id="edge"><stop stop-color="{gold}" stop-opacity="0"/><stop offset=".35" stop-color="{gold}" stop-opacity=".45"/><stop offset=".7" stop-color="{gold}" stop-opacity=".45"/><stop offset="1" stop-color="{gold}" stop-opacity="0"/></linearGradient></defs>
<g fill="none" stroke="{faint}" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
<path d="M52 209H844" stroke="url(#edge)"/>
<path d="M98 72h54m-54 8h34m-34 8h43"/>
<path d="M112 117h74v48h-74zM120 109h74v48"/>
<path d="M124 132h19m-19 9h42m-42 9h29"/>
<path d="M256 64Q313 47 390 65Q467 47 524 64V181Q462 166 390 186Q318 166 256 181Z" stroke="{gold}" stroke-width="1.5"/>
<path d="M250 69v119q68-15 140 4q72-19 140-4V69M390 66v120"/>
<path d="M280 88q39-7 84 1m-84 14q39-7 84 1m-84 14q25-5 46-3"/>
<path d="M414 148q37-8 85-2m-85 14q28-7 56-4"/>
<path d="M421 66v29l7-5l7 4V64" stroke="{gold}"/>
<path d="M280 157l17-19l25 11l23-22l19 7"/>
<circle cx="280" cy="157" r="2"/><circle cx="364" cy="134" r="2"/>
<g transform="rotate(18 567 128)"><path d="M564 58h7v124l-3.5 12-3.5-12Z" stroke="{gold}"/><path d="M564 68h7M564 178h7M568 70v102"/></g>
<circle cx="697" cy="124" r="53"/><circle cx="697" cy="124" r="38" stroke-dasharray="164 75" transform="rotate(-70 697 124)"/>
<path d="M628 124h22m94 0h22M697 55v22m0 94v22"/>
<path d="M679 106l36 36m-36 0l36-36" stroke="{gold}"/>
<circle cx="697" cy="124" r="7" stroke="{gold}"/>
''']
    for i in range(32):
        a=i*math.pi/16;r=48 if i%4==0 else 50
        p.append(f'<path d="M{697+r*math.cos(a):.2f} {124+r*math.sin(a):.2f}L{697+53*math.cos(a):.2f} {124+53*math.sin(a):.2f}"/>')
    p.append(f'</g><g fill="{ink}" font-family="monospace" font-size="9" letter-spacing="2"><text x="98" y="57">INVRNT</text><text x="278" y="39" fill="{gold}">WORK IN PROGRESS</text><text x="668" y="208">FIG. 01</text></g>')
    # The static drawing always remains visible. Only decorative overlays move.
    if not static:
        p.append(f'''<g class="motion" fill="none" stroke="{gold}" stroke-width="1.7" stroke-linecap="round">
<path d="M280 157l17-19l25 11l23-22l19 7" pathLength="100" stroke-dasharray="100" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" values="100;0;0;100" keyTimes="0;.45;.85;1" dur="14s" repeatCount="indefinite"/></path>
<circle cx="0" cy="0" r="2.5" fill="{gold}" stroke="none"><animateMotion path="M697 86 A38 38 0 1 1 696.99 86" dur="32s" repeatCount="indefinite"/></circle>
<path d="M414 121q18-29 37-12t48-15" pathLength="100" stroke-dasharray="100" stroke-dashoffset="0" opacity=".7"><animate attributeName="stroke-dashoffset" values="100;100;0;0;100" keyTimes="0;.2;.6;.88;1" dur="14s" repeatCount="indefinite"/></path></g>''')
    else:p.append(f'<path d="M414 121q18-29 37-12t48-15" fill="none" stroke="{gold}" stroke-width="1.7" opacity=".7"/>')
    p.append('</svg>')
    return ''.join(p)
for light in (False,True):
    for static in (False,True):
        name='desk'+('-light' if light else '-dark')+('-still' if static else '')+'.svg'
        (assets/name).write_text(build(light,static))
(root/'README.md').write_text('''<picture>
  <source media="(prefers-color-scheme: light) and (prefers-reduced-motion: reduce)" srcset="assets/desk-light-still.svg" />
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/desk-dark-still.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/desk-light.svg" />
  <img src="assets/desk-dark.svg" width="100%" alt="An open notebook, a pencil and a drafting instrument, drawn in gold. A small glimpse of my working desk." />
</picture>

### Juan Camilo

I build AI products and the systems behind them. Based in Colombia, studying Computer Engineering and Public Accounting.

<sub>Agent workflows, automation, and a particular interest in making complex software simple to use.</sub>

<br />

#### On my desk

**Count** · Personal finance with AI. Keeping the experience simple while building the capabilities underneath. Private project.

**[Classmate Studio](https://classmate.studio)** · A conversational assistant for university life, with academic workflows, research and document generation.

**[Orientador.co](https://orientador.co)** · AI-assisted documentation for school counselors in Colombia, with human review.

<br />

#### Outside the main projects

Occasionally, I turn a tool I want into something public. [GoalWatch](https://github.com/invrnt/goalwatch) is one of those: AI-assisted focus for the Linux desktop.

<details>
<summary>A little more about how I build</summary>

I work across architecture, implementation and deployment. I use AI agents throughout development and review the systems they help produce.

My usual tools are Python, FastAPI, TypeScript, React, Next.js, LangChain, LangGraph, Cloudflare and PostgreSQL. My accounting studies also inform my interest in financial workflows.

</details>

<br />

Open to conversations with engineering teams and fellow builders.

[Website](https://juancamilo.me) &nbsp; / &nbsp; [Email](mailto:hi@juancamilo.me) &nbsp; / &nbsp; [Repositories](https://github.com/invrnt?tab=repositories)
''')
