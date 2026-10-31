#!/usr/bin/env python3
"""Build the profile's self-contained SVG scenes. Python standard library only."""

from base64 import b64encode
from html import escape
from math import cos, sin, pi
from pathlib import Path
import struct

from surface import DATA, GRID_X, GRID_Y, MANROPE, NATIVE, PITCH, calendar, feed, file_list, measure, rrect
from surface import fit, t as t_native

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
FONTS = Path(__file__).parent / "fonts"

PALETTES = {
    "light": dict(bg="#ffffff", ink="#202a2c", muted="#65706f", line="#d5dcd8", faint="#eef1ee",
                  paper="#f7f8f4", top="#f4f5ed", middle="#dde2d9", edge="#b5c0b9", side="#c9d2ca",
                  deep="#445553", well="#243733", glow="#a06a24", gold="#b9873f", goldhi="#eed6a6",
                  goldlo="#74542d", metalhi="#f7f8f3", metalmid="#a5b3aa", metallo="#52695e",
                  shadow="#375044", white="#ffffff", grid="#e5eae5"),
    "dark": dict(bg="#0d1117", ink="#e9eee8", muted="#9daea6", line="#34433e", faint="#14221d",
                 paper="#15201d", top="#36453e", middle="#26362f", edge="#59695c", side="#22352b",
                 deep="#131f18", well="#090f0c", glow="#ebc17e", gold="#c69b54", goldhi="#ffe3a9",
                 goldlo="#755b31", metalhi="#b2c3ad", metalmid="#647962", metallo="#263d2d",
                 shadow="#000000", white="#172119", grid="#25362c"),
}


def text(x, y, value, size=24, fill="ink", weight=400, anchor="start", spacing=None, cls=""):
    attrs = f' class="{cls}"' if cls else ''
    attrs += f' letter-spacing="{spacing}"' if spacing is not None else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" fill="var(--{fill})"{attrs}>{escape(value)}</text>')


def label(x, y, value, fill="muted", anchor="start", size=14):
    return text(x, y, value, size, fill, 500, anchor, 2.1, "mono")


def line(x1, y1, x2, y2, color="line", width=1, extra=""):
    return f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="var(--{color})" stroke-width="{width}" {extra}/>'


def circle(x, y, r, fill="none", stroke="line", sw=1, extra=""):
    f = fill if fill.startswith("url(") or fill == "none" else f"var(--{fill})"
    s = stroke if stroke == "none" else f"var(--{stroke})"
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{f}" stroke="{s}" stroke-width="{sw}" {extra}/>'


def rect(x, y, w, h, r=0, fill="paper", stroke="line", extra=""):
    f = fill if fill.startswith("url(") or fill == "none" else f"var(--{fill})"
    s = stroke if stroke == "none" else f"var(--{stroke})"
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}" stroke="{s}" {extra}/>'


def path(d, fill="none", stroke="line", width=1, extra=""):
    f = fill if fill.startswith("url(") or fill == "none" else f"var(--{fill})"
    s = stroke if stroke == "none" else f"var(--{stroke})"
    return f'<path d="{d}" fill="{f}" stroke="{s}" stroke-width="{width}" {extra}/>'


def group(body, transform="", cls="", extra=""):
    return f'<g transform="{transform}" class="{cls}" {extra}>{body}</g>'


def font_face(family, file, weight):
    data = b64encode((FONTS / file).read_bytes()).decode()
    return f"@font-face{{font-family:{family};src:url(data:font/woff2;base64,{data}) format('woff2');font-weight:{weight}}}"


def svg(name, theme, width, height, title, desc, body, css="", native=False, defs=""):
    palette = PALETTES[theme]
    variables = ";".join(f"--{k}:{v}" for k, v in palette.items())
    palette = {k:f"var(--{k})" for k in palette}
    fonts = font_face("Manrope", "manrope-regular.woff2", 400) + font_face("Manrope", "manrope-semibold.woff2", "500 800")
    if native:
        # GitHub's own typeface, so the imitated interface matches the page around it.
        fonts += font_face("MonaSans", "mona-sans-regular.woff2", 400) + font_face("MonaSans", "mona-sans-semibold.woff2", "500 800")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<defs>
<linearGradient id="porcelain" x1="0" y1="0" x2="0.8" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="{palette['top']}"/><stop offset="1" stop-color="{palette['middle']}"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{palette['metalhi']}"/><stop offset=".35" stop-color="{palette['metalmid']}"/><stop offset=".6" stop-color="{palette['metalhi']}"/><stop offset="1" stop-color="{palette['metallo']}"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{palette['goldhi']}"/><stop offset=".42" stop-color="{palette['gold']}"/><stop offset="1" stop-color="{palette['goldlo']}"/></linearGradient>
<radialGradient id="halo"><stop stop-color="{palette['gold']}" stop-opacity=".12"/><stop offset="1" stop-color="{palette['gold']}" stop-opacity="0"/></radialGradient>
<filter id="shadow" x="-50%" y="-60%" width="200%" height="230%"><feGaussianBlur stdDeviation="14"/></filter>
{defs}
</defs>
<style>
{fonts}
:root{{{variables}}}
svg{{font-family:Manrope,Arial,sans-serif;text-rendering:geometricPrecision}}
.mono{{font-family:ui-monospace,'SFMono-Regular',Consolas,monospace}}
.gh{{font-family:MonaSans,-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif}}
.rotate{{animation:rotate 24s linear infinite;transform-box:fill-box;transform-origin:center}}
.rotate-reverse{{animation:rotate 32s linear infinite reverse;transform-box:fill-box;transform-origin:center}}
.pulse{{animation:pulse 5s ease-in-out infinite}}
.flow{{stroke-dasharray:4 120;animation:flow 6s linear infinite}}
.rail-pulse{{animation-duration:7s;animation-timing-function:cubic-bezier(.5,0,.5,1);animation-iteration-count:infinite}}
@keyframes rotate{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@keyframes flow{{to{{stroke-dashoffset:-248}}}}
{css}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important}}.motion-only{{display:none!important}}.still-only{{display:inline!important}}}}
</style>
{body}
</svg>\n'''


# The surface: GitHub's contribution graph and activity, redrawn at native size.
# It splits between Wednesday and Thursday and the lower half drops away.
CUT=32+35+4*13-1.5


def hero_css(drop):
    return f"""
.upper{{animation:upper 20s linear infinite}}
.lower{{animation:lower 20s linear infinite}}
.cavity{{animation:cavity 20s ease-in-out infinite}}
.seam{{animation:seam 20s linear infinite}}
.slab{{animation:slab 20s ease-out infinite;transform-box:fill-box;transform-origin:top}}
.flick{{animation:flick 20s steps(1) infinite}}
@keyframes upper{{0%,13.9%,17.6%,100%{{transform:translate(0,0)}}14.2%{{transform:translate(-5px,0)}}14.8%{{transform:translate(3px,0)}}15.6%{{transform:translate(-2px,0)}}16.4%{{transform:translate(6px,0)}}17%{{transform:translate(-1px,0)}}}}
@keyframes lower{{0%,13.9%{{transform:translate(0,0);animation-timing-function:steps(1)}}14.2%{{transform:translate(6px,1px)}}14.8%{{transform:translate(-4px,0)}}15.6%{{transform:translate(3px,2px)}}16.4%{{transform:translate(-6px,1px)}}17%{{transform:translate(0,3px);animation-timing-function:cubic-bezier(.6,0,.2,1)}}27%,84%{{transform:translate(0,{drop}px);animation-timing-function:cubic-bezier(.5,0,.3,1)}}94%,100%{{transform:translate(0,0)}}}}
@keyframes cavity{{0%,17%,94%,100%{{opacity:0}}26%,84%{{opacity:1}}}}
@keyframes seam{{0%,13.8%,96%,100%{{opacity:0}}14%,15%{{opacity:1}}15.3%{{opacity:.2}}16%,84%{{opacity:1}}92%{{opacity:.6}}}}
@keyframes slab{{0%,17%,94%,100%{{transform:scaleY(0)}}21%,90%{{transform:scaleY(1)}}}}
@keyframes flick{{0%,14%,17%,100%{{opacity:0}}14.5%,15.8%{{opacity:1}}15.2%,16.5%{{opacity:0}}}}
@media(prefers-reduced-motion:reduce){{.lower{{transform:translate(0,{drop}px)}}.cavity,.seam{{opacity:1}}.slab{{transform:none}}.flick{{opacity:0}}}}
"""


def unit_noise(i,j=0):
    """Deterministic texture, so rebuilds stay byte-identical."""
    v=sin(i*12.9898+j*78.233)*43758.5453
    return v-int(v) if v>=0 else v-int(v)+1


DIE_CSS="""
.bus-flow{stroke-dasharray:4 52;animation:bus 2.8s linear infinite}
.mem{animation:mem 3.6s steps(1) infinite}
.unit{animation:unit 3.2s ease-in-out infinite}
@keyframes bus{to{stroke-dashoffset:-56}}
@keyframes mem{0%,100%{opacity:.18}40%{opacity:1}70%{opacity:.45}}
@keyframes unit{0%,100%{opacity:.16}50%{opacity:.95}}
@media(prefers-reduced-motion:reduce){.mem,.unit{opacity:.7}.bus-flow{stroke-dasharray:none;opacity:.5}}
"""


def bus(x1,x2,ys,flow=(),vertical=False):
    out=path("".join(f"M{y} {x1}V{x2}" if vertical else f"M{x1} {y}H{x2}" for y in ys),stroke="edge",width=1.3)
    for i,y in enumerate(ys):
        d=f"M{y} {x1}V{x2}" if vertical else f"M{x1} {y}H{x2}"
        if i in flow:
            out+=path(d,stroke="glow",width=2,extra=f'stroke-linecap="round" class="bus-flow" style="animation-delay:{-i*.37:.2f}s"')
    return out


def block(x,y,w,h,name):
    return rect(x,y,w,h,6,"paper","edge")+label(x+12,y+21,name,size=11)


def die():
    """Beneath the interface: the system, as a die photographed from above. 1072 × 440."""
    w,h=1072,440
    out=path("".join(f"M{x} -9h11v12h-11ZM{x} {h-3}h11v12h-11Z" for x in range(56,w-40,26)),"line","none")
    out+=rect(0,0,w,h,16,"paper","edge")
    out+=rect(28,28,w-56,h-56,8,"faint","line")
    for cx,cy in [(40,40),(w-40,40),(40,h-40),(w-40,h-40)]:
        out+=circle(cx,cy,3,"none","edge")
    # Signal enters on the left, is understood, remembered, reasoned over, checked, and leaves as one control.
    out+=bus(28,64,[214,225,236],flow=(1,))
    out+=bus(194,250,[184,193,202,211],flow=(0,2))
    out+=bus(194,250,[266,274],flow=(1,))
    out+=bus(480,536,range(86,196,10),flow=(1,4,8))
    out+=bus(480,536,range(282,372,10),flow=(2,6))
    out+=bus(786,842,range(86,196,10),flow=(0,5,9))
    out+=bus(786,842,range(282,372,10),flow=(3,7))
    out+=bus(214,262,range(872,980,12),flow=(2,6),vertical=True)
    out+=bus(1008,w-28,[312,320,328],flow=(1,))
    out+=block(64,170,130,110,"01 INTENT")
    for i in range(12):
        hh=8+22*abs(sin(i*1.7)*sin(i*.45+.3))
        out+=line(84+i*8,240-hh/2,84+i*8,240+hh/2,"glow",3,'stroke-linecap="round"')
    out+=block(250,64,230,150,"02 MEMORY")
    for r in range(5):
        for c in range(11):
            v=unit_noise(r,c)
            cls=f' class="mem" style="animation-delay:{-v*3.6:.2f}s"' if v>.72 else ''
            out+=f'<rect x="{266+c*18}" y="{94+r*22}" width="13" height="13" rx="2.5" fill="var(--gold)" fill-opacity="{.12+.75*v*v:.2f}"{cls}/>'
    out+=block(250,262,230,116,"03 TOOLS")
    for i,name in enumerate(["FILES","WEB","CODE","MAIL"]):
        out+=rect(266+i*52,292,42,70,4,"faint","line")+label(287+i*52,352,name,anchor="middle",size=8)
        out+=line(274+i*52,306,300+i*52,306,"gold",1.5)
    out+=block(536,64,250,314,"04 REASONING")
    # Compute units light in diagonal waves; one path per diagonal keeps the file small.
    for d in range(22):
        cells=''.join(cell_path(553+c*20,94+(d-c)*23,13,2) for c in range(11) if 0<=d-c<12)
        out+=f'<path class="unit" d="{cells}" fill="var(--glow)" style="animation-delay:{d*.11:.2f}s"/>'
    out+=block(842,64,166,150,"05 VERIFY")
    out+=path("M895 149l16 16l34 -38",stroke="glow",width=3,extra='stroke-linecap="round" stroke-linejoin="round"')
    out+=block(842,262,166,116,"06 OUTPUT")
    out+=circle(925,328,27,"url(#metal)","edge")+circle(925,328,21,"url(#porcelain)","edge")+circle(925,328,16,"none","gold")
    out+=line(919,328,931,328,"glow",2.2,'stroke-linecap="round" class="pulse"')
    out+=label(w-40,h-42,"INVRNT · MDE · 2026",anchor="end",size=9)
    out+=label(48,h-42,"ONE INTENTION IN · ONE CONTROL OUT",size=9)
    return out


def hero(theme,mobile=False):
    n=NATIVE[theme]
    width=308 if mobile else 846
    w=640 if mobile else 1200
    k=w/width
    weeks=DATA["weeks"][-19:] if mobile else DATA["weeks"]
    pieces,box_w=calendar(n,width,weeks,years=not mobile)
    stream,stream_bottom=feed(n,232,width,compact=mobile)
    drop=350 if mobile else 640
    h_px=max(stream_bottom+12,CUT+drop+120)
    h=round(h_px*k)
    box=rrect(.5,32.5,box_w-1,160,6,n["canvas"],n["border"])
    upper=box.replace("/>",' clip-path="url(#above)"/>')+"".join(svg for y,svg in pieces if y<CUT)
    lower=box.replace("/>",' clip-path="url(#below)"/>')+"".join(svg for y,svg in pieces if y>=CUT)+stream
    # A few days flash amber as the surface fails.
    sparks="".join(rrect(GRID_X+c*PITCH+.5,32+GRID_Y+r*PITCH+.5,9,9,2,"var(--glow)") for c,r in
                   ([(3,2),(8,3),(14,3),(15,1),(31,3),(44,2)] if not mobile else [(2,3),(9,2),(14,3)]))
    seam=f'<path d="M0 {CUT}H{width}" stroke="var(--glow)" stroke-width="1.5"/>'
    seam+=f'<path d="M0 {CUT}H{width}" stroke="var(--glow)" stroke-width="7" opacity=".18"/>'
    slab=f'<rect x="0" y="{CUT}" width="{box_w}" height="7" fill="url(#slab-face)"/>'
    slab+=f'<rect x="0" y="{CUT+7}" width="{width}" height="46" fill="url(#slab-shadow)"/>'
    native=group(group(group(upper,cls="upper")+group(sparks,cls="flick")+group(slab,cls="slab"),"")
                 +group(group(lower+group(seam,cls="seam"),cls="lower")),f"scale({k:.5f})")
    # Beneath the surface: a quiet drafting grid, the promise, and the system that keeps it.
    top=CUT*k
    floor=(CUT+drop)*k
    m=36 if mobile else 64
    step=40
    grid="".join(f"M{x} {top+14:.0f}V{floor:.0f}" for x in range(step,w,step))
    grid+="".join(f"M0 {y}H{w}" for y in range(int(top)+step,int(floor),step))
    under=path(grid,stroke="faint")
    if mobile:
        under+=label(m,top+66,"BENEATH THE SURFACE","glow",size=17)
        under+=text(m,top+152,"More possible.",64,"ink",500,spacing=-3.4)
        under+=text(m,top+228,"Less in the way.",64,"ink",500,spacing=-3.4)
        under+=text(m,top+288,"Powerful systems. Simple experiences.",24,"muted")
        under+=group(die(),f"translate(36 {top+350}) scale({568/1072:.4f})")
        under+=label(m,floor-36,"JUAN CAMILO GRISALES · MEDELLÍN",size=16)
    else:
        under+=label(m,top+70,"BENEATH THE SURFACE","glow",size=13)
        under+=line(m,top+90,m+42,top+90,"gold",2)
        under+=label(w-m,top+70,"JUAN CAMILO GRISALES",anchor="end",size=13)
        under+=label(w-m,top+98,"AI ENGINEER & PRODUCT BUILDER · MEDELLÍN, CO",anchor="end",size=11)
        under+=text(m,top+212,"More possible.",100,"ink",500,spacing=-5)
        under+=text(m,top+324,"Less in the way.",100,"ink",500,spacing=-5)
        under+=text(m,top+382,"Powerful systems. Simple experiences.",27,"muted")
        under+=group(die(),f"translate(64 {top+440})")
    cavity=f'<g clip-path="url(#cavity)">{group(under,cls="cavity")}</g>'
    defs=(f'<clipPath id="above"><rect width="{width}" height="{CUT}"/></clipPath>'
          f'<clipPath id="below"><rect y="{CUT}" width="{width}" height="{h_px}"/></clipPath>'
          f'<clipPath id="cavity"><rect y="{top:.1f}" width="{w}" height="{floor-top:.1f}"/></clipPath>'
          '<linearGradient id="slab-face" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--middle)"/><stop offset="1" stop-color="var(--edge)"/></linearGradient>'
          '<linearGradient id="slab-shadow" x1="0" y1="0" x2="0" y2="1"><stop stop-color="var(--shadow)" stop-opacity=".32"/><stop offset="1" stop-color="var(--shadow)" stop-opacity="0"/></linearGradient>')
    return svg("hero",theme,w,h,"Juan Camilo Grisales. More possible. Less in the way.",
               f"What looks like GitHub's own contribution graph and activity feed ({DATA['total']:,} contributions in the last year) splits open between Wednesday and Thursday. The lower half drops away. Beneath the surface: More possible. Less in the way. Powerful systems, simple experiences. Under the interface lies the system itself, drawn like a chip seen from above: intent comes in, memory, tools and a reasoning core work on it, the result is verified, and it leaves as one simple control. AI engineer and product builder in Medellín, Colombia.",
               cavity+native,hero_css(drop)+DIE_CSS,native=True,defs=defs)


def waveform(x,y,width=190,height=24,step=8,cls="voice"):
    out=''
    n=int(width/step)
    for i in range(n):
        h=height*(.18+.82*abs(sin(i*1.73)*sin(i*.32+.4)))
        out+=line(x+i*step,y-h/2,x+i*step,y+h/2,"glow",3,
                  f'stroke-linecap="round" class="{cls}" style="animation-delay:{-i*.09}s;transform-origin:{x+i*step}px {y}px"')
    return out


def rail_x(mobile):
    return 14 if mobile else 28


def rail(h,mobile,top=0,bottom=None,route=None,socket_top=False,socket_bottom=False):
    """One signal line runs down the whole page. Every scene draws its own stretch at the same x."""
    x=rail_x(mobile)
    bottom=h if bottom is None else bottom
    d=route or f"M{x} {top}V{bottom}"
    length=round(bottom-top) if route is None else 2600
    out=path(d,stroke="line",width=1.5)
    out+=path(d,stroke="glow",width=2.4,extra=f'stroke-linecap="round" stroke-dasharray="70 {length+140}" class="rail-pulse" style="animation-name:rail-{length}"')
    css=f"@keyframes rail-{length}{{from{{stroke-dashoffset:70}}to{{stroke-dashoffset:-{length}}}}}"
    for y,present in [(top,socket_top),(bottom,socket_bottom)]:
        if present:
            out+=rect(x-7,y-4 if y else 0,14,8,2,"paper","edge")+line(x-3,y,x+3,y,"gold",1.5)
    return out,css


def node(x,y,cls="pulse"):
    return circle(x,y,7,"bg","gold",1.5)+circle(x,y,2.6,"glow","none",extra=f'class="{cls}"')


def section_top(w,mobile,number,name,meta):
    m=36 if mobile else 64
    x=rail_x(mobile)
    y=63 if mobile else 64
    out=line(x+7,y,m-12,y,"gold",1.2)+node(x,y)
    out+=label(m,69,number+" / "+name,"ink",size=18 if mobile else 15)
    if not mobile:
        out+=label(w-m,69,meta,anchor="end",size=12)
    return out


COUNT_CSS='''
.voice{animation:voice 2.8s ease-in-out infinite}
.question{animation:question 24s ease-in-out infinite}
.confirmed{opacity:0;animation:confirmed 24s ease-in-out infinite}
.selected{opacity:0;animation:selected 24s ease-in-out infinite}
.journal{animation:journal 24s ease-in-out infinite}
.interest-hand{animation:interest 24s cubic-bezier(.45,0,.2,1) infinite}
.posting{stroke-dasharray:5 95;animation:posting 24s linear infinite}
@keyframes voice{0%,100%{transform:scaleY(.45);opacity:.5}45%{transform:scaleY(1);opacity:1}}
@keyframes question{0%,9%,98%,100%{opacity:0}16%,46%{opacity:1}52%,94%{opacity:0}}
@keyframes selected{0%,34%,98%,100%{opacity:0}40%,46%{opacity:1}52%,94%{opacity:0}}
@keyframes confirmed{0%,49%,97%,100%{opacity:0}55%,91%{opacity:1}}
@keyframes journal{0%,44%,100%{opacity:.5}55%,91%{opacity:1}}
@keyframes interest{0%,55%{transform:rotate(-90deg);opacity:0}58%{transform:rotate(-90deg);opacity:1}83%,94%{transform:rotate(0deg);opacity:1}97%{transform:rotate(0deg);opacity:0}100%{transform:rotate(-90deg);opacity:0}}
@keyframes posting{0%,47%{stroke-dashoffset:0;opacity:0}51%,88%{opacity:1}92%,100%{stroke-dashoffset:-400;opacity:0}}
@media(prefers-reduced-motion:reduce){.question,.selected{opacity:0}.confirmed,.journal{opacity:1}.interest-hand{transform:rotate(0deg)}}
'''


def count_engine():
    # Two coupled accounts live inside a time-aware, twelve-month instrument.
    out=circle(0,0,204,"url(#halo)","none")
    out+=circle(0,0,180,"none","line")+circle(0,0,166,"none","edge")
    for i in range(60):
        a=i*2*pi/60
        r=153 if i%5==0 else 158
        out+=line(cos(a)*r,sin(a)*r,cos(a)*163,sin(a)*163,"gold" if i%5==0 else "line",1.6 if i%5==0 else 1)
    out+=group(path("M0 0L150 0",stroke="gold",width=1.4)+circle(151,0,4,"gold","none"),cls="interest-hand")
    out+=circle(0,0,111,"url(#porcelain)","edge",1.3)
    out+=circle(0,0,103,"none","metalhi",.9)
    out+=circle(0,0,83,"paper","line")
    out+=text(0,3,"12%",41,"ink",500,"middle",-2)
    out+=group(label(0,30,"ANNUAL",anchor="middle",size=12),cls="confirmed")
    out+=group(label(0,30,"RATE",anchor="middle",size=12),cls="question")
    out+=circle(0,-180,4,"gold","none")
    # Opposite signs move together. No fabricated balance or projected return.
    out+=path("M-137 -9C-200 -64 -236 54 -144 84L144 84C236 54 200 -64 137 -9",stroke="edge",width=1.4)
    out+=path("M-137 -9C-200 -64 -236 54 -144 84L144 84C236 54 200 -64 137 -9",stroke="glow",width=2.8,extra='class="posting"')
    return out


def count(theme,mobile=False):
    w,h=(640,1120) if mobile else (1200,790)
    m=36 if mobile else 64
    out=section_top(w,mobile,"01","COUNT","PRODUCT CONCEPT · IN DEVELOPMENT")
    if mobile:
        out+=text(m,140,"Finance, in your",49,"ink",500,spacing=-2)
        out+=text(m,199,"own words.",49,"ink",500,spacing=-2)
        out+=label(m,242,"IN DEVELOPMENT",size=16)
        ox,oy=36,286
    else:
        out+=text(m,155,"Finance, in your own words.",59,"ink",500,spacing=-2.7)
        ox,oy=64,219
    transcript=rect(0,0,520,185,20,"paper","line")
    transcript+=waveform(26,33,116,22)
    transcript+=label(492,39,"VOICE NOTE",anchor="end",size=12)
    transcript+=text(26,87,"Lent Kevin US$5,000",31,"ink",500,spacing=-.7)
    transcript+=text(26,128,"from Bancolombia",31,"ink",500,spacing=-.7)
    transcript+=text(26,163,"at 12% interest.",27,"muted")
    out+=group(transcript,f"translate({ox} {oy})")
    q=text(0,0,"Is that an effective annual",30,"ink",500,spacing=-.5)
    q+=text(0,39,"or monthly rate?",30,"ink",500,spacing=-.5)
    q+=rect(0,64,239,66,14,"paper","line")+rect(253,64,239,66,14,"paper","line")
    q+=text(119,106,"Annual",28,"ink",500,"middle")+text(372,106,"Monthly",28,"muted",400,"middle")
    select=rect(0,64,239,66,14,"faint","gold")+text(119,106,"Annual",28,"glow",500,"middle")
    q+=group(select,cls="selected")
    out+=group(group(q,cls="question"),f"translate({ox+14} {oy+245})")
    saved=circle(27,30,27,"paper","gold")
    saved+=path("M15 30l8 8l17 -19",stroke="glow",width=2.5,extra='stroke-linecap="round" stroke-linejoin="round"')
    saved+=text(78,39,"Recorded.",38,"ink",500,spacing=-1)
    saved+=text(0,98,"The right Pod. A balanced entry.",25,"muted")
    saved+=text(0,134,"Time taken into account.",25,"muted")
    out+=group(group(saved,cls="confirmed"),f"translate({ox+14} {oy+223})")
    if mobile:
        out+=group(count_engine(),"translate(320 823) scale(.82)")
        out+=group(text(76,1051,"Bancolombia",23,"muted")+text(76,1088,"− US$5,000",28,"ink",500)+
                   text(564,1051,"Kevin · receivable",23,"muted",anchor="end")+text(564,1088,"+ US$5,000",28,"ink",500,"end"),cls="journal")
    else:
        out+=group(count_engine(),"translate(890 410)")
        out+=group(text(686,639,"Bancolombia",22,"muted")+text(686,682,"− US$5,000",30,"ink",500)+
                   text(1100,639,"Kevin · receivable",22,"muted",anchor="end")+text(1100,682,"+ US$5,000",30,"ink",500,"end"),cls="journal")
        out+=line(m,732,w-m,732,"line")
        out+=label(m,770,"SAY IT NATURALLY.",size=13)+label(w-m,770,"KEEP EVERY DETAIL.",anchor="end",size=13)
    r,rcss=rail(h,mobile,socket_top=True,socket_bottom=True)
    out=r+out
    return svg("count",theme,w,h,"Count. Finance, in your own words. Product concept, in development.",
               "An illustrated voice note lends Kevin US$5,000 from a Bancolombia Pod at 12% interest. Count asks whether the rate is effective annual or monthly. Annual is selected. A bank decrease and an equal receivable are recorded; the twelve-month dial represents time-aware accounting. This is a product concept, not a live app.",out,COUNT_CSS+rcss)


# Five layers of Count, each shown as the interface it produces. 536 × 100 each.
LAYER_W,LAYER_H=536,100


def layer_intent():
    # Words are placed one by one: SVG drops trailing spaces, and entities need room for their outline.
    tokens=[("Lent",0),("Kevin","PERSON"),("US$5,000","AMOUNT"),("from",0),("Bancolombia","POD"),("at",0),("12%","RATE"),("interest.",0)]
    size=21
    while True:
        gap=measure(" ",size,400,MANROPE)+5
        total=sum(measure(t,size,500 if tag else 400,MANROPE) for t,tag in tokens)+gap*(len(tokens)-1)
        if total<=LAYER_W-48:
            break
        size-=.5
    x,out,body=24,'',''
    for value,tag in tokens:
        weight=500 if tag else 400
        width=measure(value,size,weight,MANROPE)
        if tag:
            out+=rect(round(x-4,1),48,round(width+8,1),29,6,"faint","gold")
            out+=label(round(x+width/2,1),37,tag,"glow",anchor="middle",size=9)
        body+=text(round(x,1),68,value,size,"ink",weight)
        x+=width+gap
    return out+body


def layer_clarify():
    out=text(22,46,"12% — effective annual,",20,"ink",500)
    out+=text(22,74,"or monthly?",20,"ink",500)
    out+=rect(300,30,104,40,20,"faint","gold")+text(342,56,"Annual",18,"glow",500,"middle")
    out+=path("M379 50l4 4l8 -9",stroke="glow",width=2,extra='stroke-linecap="round" stroke-linejoin="round"')
    out+=rect(414,30,104,40,20,"paper","line")+text(466,56,"Monthly",18,"muted",400,"middle")
    return out


def layer_ledger():
    out=label(22,28,"ACCOUNT",size=9)+label(330,28,"AMOUNT",anchor="end",size=9)
    out+=text(22,57,"Bancolombia · Pod",18,"ink")+text(330,57,"− 5,000.00",18,"ink",500,"end")
    out+=line(22,68,330,68,"line")
    out+=text(22,88,"Kevin · receivable",18,"ink")+text(330,88,"+ 5,000.00",18,"ink",500,"end")
    out+=line(362,20,362,84,"line")
    out+=text(384,57,"Σ 0.00",22,"ink",500)
    out+=label(384,83,"BALANCED","glow",size=10)
    return out


def layer_time():
    out=label(22,28,"12% EFFECTIVE ANNUAL · ACCRUES MONTHLY",size=9)
    for i,month in enumerate("JFMAMJJASOND"):
        x=36+i*40
        height=6+i*3.6
        out+=rect(x-7,78-height,14,height,3,"gold","none",f'fill-opacity="{.35+.05*i:.2f}"')
        out+=label(x,94,month,anchor="middle",size=9)
    out+=line(22,80,LAYER_W-22,80,"line")
    return out


def layer_result():
    out=circle(46,50,20,"faint","gold")
    out+=path("M37 50l7 7l13 -14",stroke="glow",width=2.4,extra='stroke-linecap="round" stroke-linejoin="round"')
    out+=text(80,46,"Recorded.",22,"ink",500)
    out+=text(80,74,"Kevin owes US$5,000 at 12% E.A.",17,"muted")
    out+=label(LAYER_W-22,48,"INSPECT ↗","glow",anchor="end",size=10)
    return out


ARCH_CSS="""
.lit{opacity:0;animation:lit 12.5s ease-in-out infinite}
.beam{stroke-dasharray:40 900;animation:beam 12.5s linear infinite}
@keyframes lit{0%,100%{opacity:0}4%,16%{opacity:1}22%{opacity:0}}
@keyframes beam{from{stroke-dashoffset:40}to{stroke-dashoffset:-860}}
@media(prefers-reduced-motion:reduce){.lit{opacity:0}.beam{stroke-dasharray:none;opacity:.35}}
"""


def architecture(theme,mobile=False):
    w,h=(640,1310) if mobile else (1200,860)
    m=36 if mobile else 64
    out=line(rail_x(mobile)+7,46,m-12,46,"gold",1.2)+node(rail_x(mobile),46)
    out+=label(m,51,"INSIDE COUNT",size=17 if mobile else 14)
    out+=text(m,117,"Simple is engineered.",44 if mobile else 53,"ink",500,spacing=-2)
    # One real sentence passes through every layer; each layer is shown as what it produces.
    captions=[("01","INTENT","Voice · text · receipts",layer_intent),("02","CLARIFICATION","Ask only what is missing",layer_clarify),
              ("03","LEDGER","Pods · exact, balanced entries",layer_ledger),("04","TIME","Accruals · scheduled work",layer_time),
              ("05","RESULT","A clear answer. An inspectable record.",layer_result)]
    scale=568/LAYER_W if mobile else 1
    cards=''
    for i,(n,title,description,draw) in enumerate(captions):
        if mobile:
            yy=200+i*218
            cx,cy=m,yy+58
            out+=label(m,yy,n+" / "+title,"ink",size=18)
            out+=text(m,yy+36,description,23,"muted")
        else:
            yy=210+i*127
            cx,cy=600,yy-34
            out+=label(m,yy,n+" / "+title,"ink",size=15)
            out+=text(m,yy+39,description,25,"muted")
            out+=line(470,yy+12,cx-14,yy+12,"line",1)+circle(cx-14,yy+12,3,"gold","none")
        card=rect(0,0,LAYER_W,LAYER_H,14,"paper","line")+draw()
        card+=rect(0,0,LAYER_W,LAYER_H,14,"none","gold",f'stroke-width="1.6" class="lit" style="animation-delay:{i*2.5}s"')
        cards+=group(card,f"translate({cx} {cy})"+(f" scale({scale:.4f})" if mobile else ""))
    if not mobile:
        out+=path("M580 186V752",stroke="line")
        out+=path("M580 186V752",stroke="glow",width=2,extra='class="beam"')
    out+=cards
    r,rcss=rail(h,mobile,socket_bottom=True)
    return svg("architecture",theme,w,h,"Inside Count. Simple is engineered.",
               "One sentence passes through the five layers of the planned system. Intent: Kevin, US$5,000, Bancolombia and 12% are recognised as person, amount, Pod and rate. Clarification: effective annual or monthly? Annual. Ledger: Bancolombia Pod minus 5,000.00, Kevin receivable plus 5,000.00, balanced at zero. Time: interest accrues monthly at 12% effective annual. Result: recorded, with the record open to inspection.",
               r+out,ARCH_CSS+rcss)


PRODUCT_CSS='''
.voice{animation:voice 3s ease-in-out infinite}
.talk{opacity:0;animation:talk 12s ease-out infinite}
.write{stroke-dasharray:1 1;stroke-dashoffset:1;animation:write 12s ease-in-out infinite}
.cite{opacity:0;animation:cite 12s ease-in-out infinite}
.link{stroke-dasharray:1 1;stroke-dashoffset:1;animation:link 12s ease-in-out infinite}
.seal{stroke-dasharray:1 1;stroke-dashoffset:1;animation:seal 12s ease-in-out infinite}
@keyframes voice{0%,100%{transform:scaleY(.5)}50%{transform:scaleY(1)}}
@keyframes talk{0%{opacity:0;transform:translateY(10px)}5%,90%{opacity:1;transform:translateY(0)}97%,100%{opacity:0}}
@keyframes write{0%,6%{stroke-dashoffset:1}18%,90%{stroke-dashoffset:0}97%,100%{stroke-dashoffset:1}}
@keyframes cite{0%,40%{opacity:0}46%,90%{opacity:1}97%,100%{opacity:0}}
@keyframes link{0%,44%{stroke-dashoffset:1}58%,90%{stroke-dashoffset:0}97%,100%{stroke-dashoffset:1}}
@keyframes seal{0%,74%{stroke-dashoffset:1}80%,92%{stroke-dashoffset:0}97%,100%{stroke-dashoffset:1}}
@media(prefers-reduced-motion:reduce){.write,.link,.seal{stroke-dashoffset:0}.talk,.cite{opacity:1}}
'''


def write(x1,y,x2,delay,color="muted",width=2.6):
    return path(f"M{x1} {y}H{x2}",stroke=color,width=width,
                extra=f'pathLength="1" stroke-linecap="round" class="write" style="animation-delay:{delay:.2f}s"')


def source_card(y,title,tag,kind):
    out=rect(0,y,210,112,12,"paper","line")
    out+=text(18,y+32,title,17,"ink",500)+label(18,y+53,tag,size=9)
    if kind=="audio":
        out+=waveform(20,y+84,170,22,8)
    elif kind=="pdf":
        for i,frac in enumerate([1,.82,.94]):
            out+=line(18,y+74+i*12,18+150*frac,y+74+i*12,"line",2.4,'stroke-linecap="round"')
    else:
        out+=rect(18,y+66,82,34,4,"faint","line")+line(26,y+76,70,y+76,"gold",2)+line(26,y+87,88,y+87,"line",2)
        out+=rect(110,y+66,82,34,4,"faint","line")+line(118,y+76,160,y+76,"gold",2)+line(118,y+87,180,y+87,"line",2)
    return out


def classmate_art():
    # Three kinds of material, one answer that cites each of them back to its source.
    out=source_card(16,"Lecture 07","AUDIO · 48 MIN","audio")
    out+=source_card(150,"Syllabus.pdf","PDF · 12 PAGES","pdf")
    out+=source_card(284,"Week 7 slides","SLIDES · 34","slides")
    out+=rect(258,0,362,410,16,"paper","line")
    out+=label(282,34,"ASK YOUR COURSE",size=10)
    out+=rect(282,52,314,46,23,"faint","line")+text(302,81,"What will the midterm cover?",17,"ink",500)
    # Citations sit in the card's left gutter, so each link crosses only the gap to its source.
    lines=[(140,560,None),(166,520,2),(192,580,None),(218,470,1),(244,550,None),(270,500,3)]
    for i,(y,end,cite) in enumerate(lines):
        out+=write(314,y,end,i*.35)
        if cite:
            out+=group(rect(276,y-10,24,20,6,"faint","gold")+label(288,y+4,str(cite),"glow",anchor="middle",size=10),
                       cls="cite",extra=f'style="animation-delay:{i*.35:.2f}s"')
            target=[None,72,206,340][cite]
            out+=path(f"M276 {y}C244 {y} 244 {target} 212 {target}",stroke="glow",width=1.6,
                      extra=f'pathLength="1" class="link" style="animation-delay:{i*.35:.2f}s"')
            out+=circle(212,target,3,"glow","none",extra=f'class="cite" style="animation-delay:{i*.35+.6:.2f}s"')
    out+=line(282,330,596,330,"line")
    out+=label(282,362,"3 SOURCES · ONE CONTEXT",size=10)
    for i in range(3):
        out+=circle(560+i*14,358,3.5,"gold" if i==0 else "none","gold")
    return out


def bubble(x,y,w,h,who,bars,counselor,delay):
    out=rect(x,y,w,h,16,"faint" if counselor else "paper","gold" if counselor else "line")
    out+=label(x+18,y+26,who,"glow" if counselor else "muted",size=9)
    for i,frac in enumerate(bars):
        out+=line(x+18,y+46+i*14,x+18+(w-36)*frac,y+46+i*14,"line" if not counselor else "gold",3,'stroke-linecap="round"')
    return group(out,cls="talk",extra=f'style="animation-delay:{delay:.2f}s;transform-box:fill-box"')


def orientador_art():
    # The conversation stays abstract: the point is to listen, not to read. The note assembles beside it.
    out=bubble(0,10,236,78,"STUDENT",[1,.7],False,0)
    out+=bubble(64,104,236,64,"COUNSELOR",[.8],True,.9)
    out+=bubble(0,184,236,92,"STUDENT",[1,.9,.55],False,1.8)
    out+=bubble(64,292,236,64,"COUNSELOR",[.6],True,2.7)
    out+=circle(8,392,4,"glow","none",extra='class="pulse"')+waveform(26,392,90,16,6)
    out+=label(128,397,"LISTENING",size=10)
    out+=rect(330,0,290,410,16,"paper","line")
    out+=text(354,44,"Session note",20,"ink",500)
    out+=rect(354,60,172,24,12,"faint","gold")+label(440,76,"DRAFT · FOR REVIEW","glow",anchor="middle",size=9)
    fields=[("REASON FOR VISIT",120,[.9,.6]),("OBSERVATIONS",192,[1,.85,.7]),("AGREEMENTS",278,[.95,.5])]
    delay=1.2
    for name,y,bars in fields:
        out+=label(354,y,name,size=9)
        for i,frac in enumerate(bars):
            out+=write(354,y+22+i*16,354+236*frac,delay,width=2.4)
            delay+=.45
    out+=rect(354,356,20,20,5,"none","gold")
    out+=path("M358 366l4 4l8 -9",stroke="glow",width=2.2,extra='pathLength="1" class="seal" stroke-linecap="round" stroke-linejoin="round"')
    out+=text(384,372,"Reviewed by the counselor",15,"muted")
    out+=path("M300 230C318 230 312 206 328 206",stroke="gold",width=1.4,extra='stroke-dasharray="2 4"')
    return out


# Bento's own window: where the rows from GitHub's table come to rest, each in its own tile.
WINDOW_W,WINDOW_H=576,292
TILE_W,TILE_H,TILE_GAP=164,86,16


def tile_centre(i):
    return 22+(i%3)*(TILE_W+TILE_GAP)+TILE_W/2,64+(i//3)*(TILE_H+TILE_GAP)+TILE_H/2


def bento_window(names,delays):
    out=f'<ellipse cx="{WINDOW_W/2}" cy="{WINDOW_H+14}" rx="{WINDOW_W/2-40}" ry="12" fill="var(--shadow)" opacity=".12" filter="url(#shadow)"/>'
    out+=rect(0,0,WINDOW_W,WINDOW_H,16,"paper","line")
    for i in range(3):
        out+=circle(24+i*18,24,5,"faint","line")
    out+=text(90,30,"Bento",17,"ink",500)
    out+=rect(WINDOW_W-176,11,156,26,13,"faint","gold")
    out+=path(f"M{WINDOW_W-160} 23v-3a4 4 0 0 1 8 0v3",stroke="glow",width=1.4)+rect(WINDOW_W-162,22,12,9,2,"glow","none")
    out+=label(WINDOW_W-142,29,"ON THIS DEVICE","glow",size=9)
    out+=line(0,46,WINDOW_W,46,"line")
    for i,(name,delay) in enumerate(zip(names,delays)):
        cx,cy=tile_centre(i)
        x,y=cx-TILE_W/2,cy-TILE_H/2
        tile=rect(x,y,TILE_W,TILE_H,10,"faint","line")
        tile+=path(f"M{x+16} {y+22}h12l4 4h16v18h-32Z","gold","none")
        tile+=text(x+16,y+68,name,15,"ink",500)
        out+=group(tile,cls="settle",extra=f'style="animation-delay:{delay:.2f}s"')
    out+=label(22,WINDOW_H-18,"0 BYTES UPLOADED · YOUR FILES STAY HERE",size=9)
    return out


BENTO_CSS="""
.peel{animation:peel 12s cubic-bezier(.55,0,.35,1) infinite;transform-box:fill-box;transform-origin:center}
.settle{animation:settle 12s ease-out infinite}
.empty{opacity:0;animation:empty 12s ease-in-out infinite}
@keyframes peel{0%,10%{transform:translate(0,0) scale(1);opacity:1}24%{opacity:.85}30%,80%{transform:translate(var(--dx),var(--dy)) scale(.12);opacity:0}80.1%{transform:translate(0,0) scale(1);opacity:0}92%,100%{transform:translate(0,0) scale(1);opacity:1}}
@keyframes settle{0%,27%,94%,100%{opacity:.22}31%,86%{opacity:1}}
@keyframes empty{0%,44%,80%,100%{opacity:0}50%,76%{opacity:1}}
@media(prefers-reduced-motion:reduce){.peel{transform:none;opacity:1}.settle{opacity:1}.empty{opacity:0}}
"""


def bento(theme,mobile=False):
    n=NATIVE[theme]
    w,h=(640,1300) if mobile else (1200,860)
    m=36 if mobile else 64
    out=section_top(w,mobile,"04","BENTO","")
    out+=text(m,149 if mobile else 197,"Yours to keep.",55 if mobile else 57,"ink",500,spacing=-2.7)
    for i,value in enumerate(["A local-first home","for your files."]):
        out+=text(m,(209 if mobile else 255)+i*37,value,29 if mobile else 26,"muted")
    out+=label(m,296 if mobile else 368,"VIEW THE SOURCE ↗","glow",size=17 if mobile else 13)
    # GitHub's own file table, then the files leave it for Bento, on your own device.
    k=w/(308 if mobile else 846)
    list_x,list_y=(m,340) if mobile else (560,96)
    list_w=round((w-m-list_x)/k)
    rows=6
    wx,wy=(m,950) if mobile else (560,530)
    ws=(w-m-wx)/WINDOW_W
    frame,body=file_list(n,list_w,rows)
    names=[name for name,kind in sorted(DATA["bento"]["entries"],key=lambda e:(e[1]!="tree",e[0].lower()))[:rows]]
    # The bottom row leaves first, so every row falls through space that is already clear.
    delays=[(len(body)-1-i)*.3 for i in range(len(body))]
    peeled=""
    for i,row in enumerate(body):
        tx,ty=tile_centre(i)
        dx=(wx+tx*ws-list_x)/k-list_w/2
        dy=(wy+ty*ws-list_y)/k-(49+i*37+18)
        peeled+=f'<g class="peel" style="--dx:{dx:.0f}px;--dy:{dy:.0f}px;animation-delay:{delays[i]:.2f}s">{row}</g>'
    out+=group(bento_window(names,delays),f"translate({wx} {wy})"+(f" scale({ws:.4f})" if ws!=1 else ""))
    # While the rows are away, the table says where they went, in GitHub's own voice.
    mid=49+rows*37/2
    empty=(t_native(list_w/2,mid-4,"Nothing to see here.",16,n["fg"],600,"middle")
           +t_native(list_w/2,mid+20,fit("These files live in Bento, on your device.",14,list_w-32),14,n["muted"],anchor="middle"))
    peeled+=group(empty,cls="empty")
    out+=group(frame+peeled,f"translate({list_x} {list_y}) scale({k:.5f})")
    r,rcss=rail(h,mobile)
    return svg("bento",theme,w,h,"Bento. Yours to keep.",
               "Bento. A local-first home for your files. What looks like GitHub's own file list for the Bento repository comes apart: each row lifts away and comes to rest in its own tile inside the Bento window, on this device. Nothing is uploaded. Your files remain on your own device by default.",
               r+out,BENTO_CSS+rcss,native=True)


PRODUCTS={
    "classmate":("02","CLASSMATE STUDIO","Room to think.",["Course materials, recordings and AI.","One shared context."],classmate_art,
                 "Classmate Studio. Course materials, recordings and AI in one academic workspace. A lecture recording, the syllabus and the week's slides sit beside one answer. As the answer is written, each claim is cited back to the source it came from."),
    "orientador":("03","ORIENTADOR","Time to listen.",["AI-assisted documentation", "for school counselors."],orientador_art,
                  "Orientador. AI-assisted documentation for school counselors. The conversation between a student and a counselor is shown only as its rhythm, never its words. Beside it a session note assembles, marked as a draft for professional review, and the counselor signs it off."),
}


def product(name,theme,mobile=False):
    number,title,headline,body,draw,desc=PRODUCTS[name]
    w,h=(640,780) if mobile else (1200,546)
    m=36 if mobile else 64
    out=section_top(w,mobile,number,title,"")
    out+=text(m,149 if mobile else 197,headline,55 if mobile else 57,"ink",500,spacing=-2.7)
    for i,value in enumerate(body):
        out+=text(m,(209 if mobile else 255)+i*37,value,29 if mobile else 26,"muted")
    cta={"classmate":"EXPLORE CLASSMATE ↗","orientador":"EXPLORE ORIENTADOR ↗"}[name]
    out+=label(m,296 if mobile else 368,cta,"glow",size=17 if mobile else 13)
    placement="translate(25 305) scale(.96)" if mobile else "translate(558 101) scale(.99)"
    out+=group(draw(),placement)
    r,rcss=rail(h,mobile,socket_top=name=="classmate")
    return svg(name,theme,w,h,title+". "+headline,desc,r+out,PRODUCT_CSS+rcss)


# A contribution graph for every industry: seven rows, like the seven days of the week.
INDUSTRIES=["HEALTH","ENERGY","MATERIALS","FOOD","EDUCATION","HOUSING","SCIENCE"]
ABUNDANCE={"dark":["#17211d","#3f3321","#6e5530","#c69b54","#f0c985"],
           "light":["#eef1ee","#f1dfb8","#ddbb7c","#b9873f","#7d5a2b"]}

AMBITION_CSS="""
.bloom{opacity:0;animation:bloom 24s ease-out infinite}
.cost{stroke-dasharray:1 1;stroke-dashoffset:1;animation:cost 24s ease-in-out infinite}
@keyframes bloom{0%,3%{opacity:0}8%,86%{opacity:1}94%,100%{opacity:0}}
@keyframes cost{0%,4%{stroke-dashoffset:1}48%,88%{stroke-dashoffset:0}95%,100%{stroke-dashoffset:1}}
@media(prefers-reduced-motion:reduce){.bloom{opacity:1}.cost{stroke-dashoffset:0}}
"""


def cell_path(x,y,size,radius):
    r=radius
    return f"M{x+r:.1f} {y:.1f}h{size-2*r}a{r} {r} 0 0 1 {r} {r}v{size-2*r}a{r} {r} 0 0 1 -{r} {r}h-{size-2*r}a{r} {r} 0 0 1 -{r} -{r}v-{size-2*r}a{r} {r} 0 0 1 {r} -{r}"


def abundance(theme,x0,y0,cols,pitch,size):
    """Empty days as one path; each column's lit cells bloom in turn as the cost of trying falls."""
    colors=ABUNDANCE[theme]
    base=''.join(cell_path(x0+c*pitch,y0+r*pitch,size,size*.2) for c in range(cols) for r in range(7))
    out=f'<path d="{base}" fill="{colors[0]}"/>'
    for c in range(cols):
        levels={}
        for r in range(7):
            # More attempts as the cost falls, unevenly across industries, never all at once.
            reach=(c+1)/cols
            v=reach*(.55+.9*unit_noise(c,r))-.18*unit_noise(r,c+40)
            level=0 if v<.16 else 1 if v<.38 else 2 if v<.6 else 3 if v<.82 else 4
            if level:
                levels.setdefault(level,[]).append(cell_path(x0+c*pitch,y0+r*pitch,size,size*.2))
        if levels:
            lit=''.join(f'<path d="{"".join(d)}" fill="{colors[l]}"/>' for l,d in sorted(levels.items()))
            out+=group(lit,cls="bloom",extra=f'style="animation-delay:{c*10/cols:.2f}s"')
    return out


def ambition(theme,mobile=False):
    w,h=(640,860) if mobile else (1200,875)
    m=36 if mobile else 64
    out=section_top(w,mobile,"05","AMBITION","CAPABILITY → PROSPERITY")
    if mobile:
        out+=text(m,150,"Make room for",59,"ink",500,spacing=-2.6)
        out+=text(m,219,"bigger ambitions.",59,"ink",500,spacing=-2.6)
        for i,value in enumerate(["Make valuable work cheaper.","Help every industry attempt more."]):
            out+=text(m,285+i*38,value,26,"muted")
        x0,y0,cols,pitch,size,top=180,520,19,22,17,390
        label_size=13
    else:
        out+=text(m,164,"Make room for",72,"ink",500,spacing=-3.2)
        out+=text(m,247,"bigger ambitions.",72,"ink",500,spacing=-3.2)
        out+=text(m,314,"Make valuable work cheaper. Help every industry attempt more.",27,"muted")
        x0,y0,cols,pitch,size,top=210,530,36,26,20,392
        label_size=11
    right=x0+cols*pitch-(pitch-size)
    # The cost of trying falls; underneath, every industry fills in.
    curve=f"M{x0} {top+12}C{x0+(right-x0)*.35} {top+18} {x0+(right-x0)*.45} {y0-34} {right} {y0-28}"
    out+=label(x0,top,"COST OF TRYING",size=label_size)
    out+=path(curve,stroke="line",width=1.4)
    out+=path(curve,stroke="glow",width=2.4,extra='pathLength="1" class="cost" stroke-linecap="round"')
    for r,name in enumerate(INDUSTRIES):
        out+=label(m,y0+r*pitch+size*.72,name,size=label_size)
    out+=abundance(theme,x0,y0,cols,pitch,size)
    legend_y=y0+7*pitch+24
    out+=label(x0,legend_y,"TODAY",size=label_size)
    out+=label(right,legend_y,"MORE",anchor="end",size=label_size)
    lx=right-(64 if mobile else 50)
    for i,color in enumerate(reversed(ABUNDANCE[theme])):
        out+=f'<path d="{cell_path(lx-(i+1)*(size*.62+4),legend_y-size*.62+2,size*.62,size*.12)}" fill="{color}"/>'
    out+=label(lx-5*(size*.62+4)-8,legend_y,"LESS",anchor="end",size=label_size)
    out+=line(m,h-103,w-m,h-103)
    out+=text(m,h-54,"Toward ASI. Toward shared abundance.",25 if mobile else 29,"ink",500,spacing=-.4)
    r,rcss=rail(h,mobile)
    out=r+out
    return svg("ambition",theme,w,h,"Make room for bigger ambitions.",
               "I want AI to make economically valuable work dramatically cheaper, so people across every industry can attempt more. As we move toward ASI, I want to help turn that capability into broadly shared abundance. Drawn as a contribution graph for whole industries: health, energy, materials, food, education, housing and science. As the cost of trying falls, every row fills in.",out,AMBITION_CSS+rcss)


def contact(theme,mobile=False):
    w,h=(640,430) if mobile else (1200,430)
    m=36 if mobile else 64
    x=rail_x(mobile)
    out=line(x+7,64,m-12,64,"gold",1.2)+node(x,64)
    out+=label(m,69,"THE NEXT THING",size=17 if mobile else 14)
    out+=text(m,151,"What should" if mobile else "What should become simpler?",57 if mobile else 58,"ink",500,spacing=-2.6)
    if mobile:
        out+=text(m,216,"become simpler?",57,"ink",500,spacing=-2.6)
    out+=text(m,281 if mobile else 211,"Let's build it.",32,"muted")
    # The whole signal, from the surface down, resolves into the same simple control.
    mark=circle(0,0,45,"url(#metal)","edge")+circle(0,0,36,"url(#porcelain)","edge")
    mark+=circle(0,0,28,"none","gold",1)
    mark+=line(-9,0,9,0,"glow",2.5,extra='class="pulse" stroke-linecap="round"')
    if mobile:
        cx,cy,r,turn=550,330,29,392
        out+=label(m,362,"INVRNT",size=17)
    else:
        cx,cy,r,turn=1070,276,45,372
        out+=label(m,332,"JUAN CAMILO GRISALES",size=14)
        out+=label(m,364,"MEDELLÍN, COLOMBIA",size=12)
    route=f"M{x} 0V{turn-20}Q{x} {turn} {x+20} {turn}H{cx-20}Q{cx} {turn} {cx} {turn-20}V{cy+r}"
    r_svg,rcss=rail(h,mobile,route=route)
    out=r_svg+out
    out+=group(mark,f"translate({cx} {cy})"+(" scale(.65)" if mobile else ""))
    return svg("contact",theme,w,h,"What should become simpler? Let's build it.",
               "Contact Juan Camilo Grisales at juan@juancamilo.me or visit juancamilo.me. The signal that ran through the whole profile ends in one simple ceramic control.",out,rcss)


# Physical controls are drawn in fixed porcelain so they read on either GitHub theme.
# They need no theme switch, so they can be real links, and no motion, so no still copy.
NEUTRAL=PALETTES["light"]


def port(mobile=False):
    w,h=(640,170) if mobile else (1200,150)
    x=rail_x(mobile)
    cy=h/2
    m=36 if mobile else 64
    cap_w=568 if mobile else 470
    out=path(f"M{x} 0V{h}",stroke="#7d8a84",width=1.5,extra='stroke-opacity=".55"')
    out+=line(x+7,cy,m,cy,"gold",1.2)+circle(x,cy,7,"top","gold",1.5)+circle(x,cy,2.6,"glow","none")
    out+=f'<ellipse cx="{m+cap_w/2}" cy="{cy+44}" rx="{cap_w/2-20}" ry="10" fill="#000" opacity=".16" filter="url(#shadow)"/>'
    out+=rect(m,cy-36,cap_w,80,40,"side","edge")
    out+=rect(m,cy-42,cap_w,80,40,"url(#porcelain)","edge")
    out+=circle(m+42,cy-2,19,"url(#brass)","goldlo")+circle(m+42,cy-2,11,"deep","metalhi")+circle(m+42,cy-2,3.4,"goldhi","none")
    out+=text(m+78,cy+8,"Open the machine",34 if mobile else 30,"ink",500,spacing=-.6)
    out+=label(m+cap_w-34,cy+4,"↓",fill="glow",anchor="end",size=20 if mobile else 18)
    if not mobile:
        out+=label(m+cap_w+28,cy-6,"INSIDE COUNT",size=13)
        out+=label(m+cap_w+28,cy+20,"FIVE LAYERS · ONE CONTROL IN 3D",size=11)
    return svg("port","light",w,h,"Open the machine",
               "A porcelain button on the signal line. Opening it shows how Count is built and a 3D model of the control.",out)


KEYS=[("website","Website","juancamilo.me","https://juancamilo.me"),
      ("email","Email","juan@juancamilo.me","mailto:juan@juancamilo.me"),
      ("source","Repositories","github.com/invrnt","https://github.com/invrnt?tab=repositories")]


def key(name,mobile=False):
    _,title,caption,_=next(k for k in KEYS if k[0]==name)
    w,h=(214,190) if mobile else (400,150)
    x0,x1,top,face=(12,202,22,118) if mobile else (24,376,16,98)
    out=f'<ellipse cx="{w/2}" cy="{top+face+18}" rx="{(x1-x0)/2-10}" ry="10" fill="#000" opacity=".2" filter="url(#shadow)"/>'
    out+=rect(x0,top+12,x1-x0,face,18,"side","edge")
    out+=rect(x0,top,x1-x0,face,18,"url(#porcelain)","edge")
    out+=line(x0+18,top+1.5,x1-18,top+1.5,"white",1.2,'stroke-opacity=".9"')
    out+=circle(x1-26,top+24,4.5,"glow","none")+circle(x1-26,top+24,9,"none","gold",1)
    if mobile:
        out+=text(x0+20,top+64,title if len(title)<10 else "Repos",34,"ink",500,spacing=-.8)
        out+=label(x0+20,top+96,"↗",fill="glow",size=22)
    else:
        out+=text(x0+30,top+50,title,30,"ink",500,spacing=-.6)
        out+=label(x0+30,top+78,caption+" ↗",size=12)
    return svg("key","light",w,h,title,f"{title}: {caption}. A porcelain key that opens the link.",out)


SCENES={"hero":hero,"count":count,"architecture":architecture,
        **{name:(lambda t,m,n=name:product(n,t,m)) for name in ["classmate","orientador"]},
        "bento":bento,"ambition":ambition,"contact":contact}


def sources(base,still=True):
    out=""
    if still:
        out+=f'<source media="(max-width: 600px) and (prefers-reduced-motion: reduce)" srcset="assets/{base[0]}-still.svg">'
        out+=f'<source media="(prefers-reduced-motion: reduce)" srcset="assets/{base[1]}-still.svg">'
    return out+f'<source media="(max-width: 600px)" srcset="assets/{base[0]}.svg">'


def picture(name,alt,href=None):
    """Both themes of one scene. align=top removes the inline baseline gap, so scenes join seamlessly."""
    alt=escape(alt,quote=True)
    blocks=[]
    for theme in PALETTES:
        target=href or f"assets/{name}-{theme}.svg"
        blocks.append(f'<a href="{target}#gh-{theme}-mode-only"><picture>{sources((f"{name}-mobile-{theme}",f"{name}-{theme}"))}'
                      f'<img src="assets/{name}-{theme}.svg" width="100%" align="top" alt="{alt}"></picture></a>')
    return "\n".join(blocks)


def neutral(name,alt,width="100%",href=None):
    """A theme-neutral control. Without a theme fragment it can sit inside a summary or point at mailto."""
    img=(f'<picture>{sources((f"{name}-mobile",name),still=False)}'
         f'<img src="assets/{name}.svg" width="{width}" align="top" alt="{escape(alt,quote=True)}"></picture>')
    return f'<a href="{href}">{img}</a>' if href else img


TEXT_EDITION="""<details>
<summary>Text edition</summary>

# Juan Camilo Grisales

AI engineer and product builder in Medellín, Colombia.

**More possible. Less in the way.**

I build powerful systems that ask less of the people using them. Push capability inward. Make the experience simpler. Keep the underlying detail available to inspect.

- **Count**, in development. A personal finance system designed to turn everyday messages into precise records. In the illustrated example, a US$5,000 loan comes from a Bancolombia Pod. Count clarifies whether 12% is an effective annual or monthly rate before recording the bank decrease and the equal receivable.
- [Classmate Studio](https://classmate.studio). Course materials, recordings and AI in one academic workspace.
- [Orientador](https://orientador.co). AI-assisted documentation for school counselors, with professional review.
- [Bento](https://github.com/invrnt/bento). A local-first home for your files.

I want AI to make economically valuable work dramatically cheaper, so people across every industry can attempt more. As we move toward ASI, I want to help turn that capability into broadly shared abundance.

What should become simpler? [Let's build it](mailto:juan@juancamilo.me).

[Website](https://juancamilo.me) · [Email](mailto:juan@juancamilo.me)

</details>"""


def readme():
    surface=[picture("hero",f"What looks like GitHub's own contribution graph splits open. Beneath the surface: Juan Camilo Grisales, AI engineer and product builder in Medellín, Colombia. More possible. Less in the way. Powerful systems, simple experiences."),
             picture("count","Count. Finance, in your own words. Product concept, in development. A voice note becomes a precise, balanced financial record. When a rate is ambiguous, Count asks a clear question.")]
    work=[picture("classmate","Classmate Studio. Room to think. Course materials, recordings and AI in one shared context. Explore Classmate.","https://classmate.studio"),
          picture("orientador","Orientador. Time to listen. AI-assisted documentation for school counselors, with professional review. Explore Orientador.","https://orientador.co"),
          picture("bento","Bento. Yours to keep. A local-first home for your files. View the source.","https://github.com/invrnt/bento"),
          picture("ambition","Make room for bigger ambitions. I want AI to make economically valuable work cheaper and help every industry attempt more. Toward ASI, toward broadly shared abundance."),
          picture("contact","What should become simpler? Let's build it. Contact Juan Camilo Grisales."),
          "".join(neutral(f"key-{name}",f"{title}: {caption}","33.333%",href) for name,title,caption,href in KEYS)]
    parts=["<!-- Generated with python3 tools/build.py. Edit the builder, not this file. -->",
           "<p>\n"+"\n".join(surface)+"\n</p>",
           "<details>\n<summary>"+neutral("port","Open the machine: how Count is built, and the control in 3D")+"</summary>",
           "<p>\n"+picture("architecture","Inside Count. Simple is engineered: intent, clarification, exact double-entry records, time-aware calculations, and an inspectable result.")+"\n</p>",
           "Count is in development. The animation illustrates the intended experience. Its design combines account-specific Pods, double-entry accounting and time-aware calculations. Ambiguity becomes a clear question. The detail stays available.",
           "The one control that everything resolves to. Drag to turn it.",
           "```stl\n"+control_stl_ascii()+"```",
           "</details>",
           "<p>\n"+"\n".join(work)+"\n</p>",
           TEXT_EDITION]
    return "\n\n".join(parts)+"\n"


def control_facets(segments=96):
    """A closed, rotationally symmetric control: (normal, a, b, c) for each facet."""
    profiles=[[(0,0),(58,0),(62,3),(62,10),(58,14),(0,14)],
              [(49,14.5),(52,14.5),(52,17),(49,17),(49,14.5)],
              [(0,15),(46,15),(47,17),(47,21),(45,23),(0,23)]]
    for profile in profiles:
        for i in range(segments):
            a,b=2*pi*i/segments,2*pi*(i+1)/segments
            for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
                v=[(r0*cos(a),r0*sin(a),z0),(r0*cos(b),r0*sin(b),z0),
                   (r1*cos(b),r1*sin(b),z1),(r1*cos(a),r1*sin(a),z1)]
                for p,q,r in [(v[0],v[1],v[2]),(v[0],v[2],v[3])]:
                    u=[q[j]-p[j] for j in range(3)]; vv=[r[j]-p[j] for j in range(3)]
                    n=[u[1]*vv[2]-u[2]*vv[1],u[2]*vv[0]-u[0]*vv[2],u[0]*vv[1]-u[1]*vv[0]]
                    length=sum(a*a for a in n)**.5
                    if length<1e-8:
                        continue
                    yield [a/length for a in n],p,q,r


def control_stl():
    """The full-resolution study for GitHub's 3D file viewer."""
    triangles=[struct.pack('<12fH',*n,*p,*q,*r,0) for n,p,q,r in control_facets()]
    header=b'The quiet machine / invrnt / control study / arbitrary units'.ljust(80,b'\0')
    return header+struct.pack('<I',len(triangles))+b''.join(triangles)


def control_stl_ascii(segments=32):
    """A lighter copy of the control for the README's inline viewer."""
    facets=[]
    for normal,*vertices in control_facets(segments):
        facets.append("facet normal "+" ".join(f"{v:.3g}" for v in normal)+"\nouter loop\n"+
                      "".join("vertex "+" ".join(f"{c:.4g}" for c in v)+"\n" for v in vertices)+"endloop\nendfacet\n")
    return "solid control\n"+"".join(facets)+"endsolid control\n"


def build():
    ASSETS.mkdir(exist_ok=True)
    for old in ASSETS.glob("*.svg"):
        old.unlink()
    for name,fn in SCENES.items():
        for theme in PALETTES:
            for mobile in (False,True):
                suffix="-mobile" if mobile else ""
                target=ASSETS/f"{name}{suffix}-{theme}.svg"
                artwork=fn(theme,mobile)
                target.write_text(artwork)
                still=ASSETS/f"{name}{suffix}-{theme}-still.svg"
                still.write_text(artwork.replace('@media(prefers-reduced-motion:reduce)','@media all'))
                print(f"{target.relative_to(ROOT)}  {target.stat().st_size:,} bytes")
    controls={"port":port,**{f"key-{k[0]}":(lambda mobile,k=k[0]:key(k,mobile)) for k in KEYS}}
    for name,fn in controls.items():
        for mobile in (False,True):
            target=ASSETS/f"{name}{'-mobile' if mobile else ''}.svg"
            target.write_text(fn(mobile))
            print(f"{target.relative_to(ROOT)}  {target.stat().st_size:,} bytes")
    (ROOT/"README.md").write_text(readme())
    (ASSETS/"control.stl").write_bytes(control_stl())


if __name__=="__main__":
    build()
