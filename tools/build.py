#!/usr/bin/env python3
"""Build the profile's self-contained SVG scenes. Python standard library only."""

from base64 import b64encode
from html import escape
from math import cos, sin, pi
from pathlib import Path
import struct

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


def svg(name, theme, width, height, title, desc, body, css=""):
    palette = PALETTES[theme]
    variables = ";".join(f"--{k}:{v}" for k, v in palette.items())
    palette = {k:f"var(--{k})" for k in palette}
    regular = b64encode((FONTS / "manrope-regular.woff2").read_bytes()).decode()
    semibold = b64encode((FONTS / "manrope-semibold.woff2").read_bytes()).decode()
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title>
<desc id="desc">{escape(desc)}</desc>
<defs>
<linearGradient id="porcelain" x1="0" y1="0" x2="0.8" y2="1" gradientUnits="objectBoundingBox"><stop stop-color="{palette['top']}"/><stop offset="1" stop-color="{palette['middle']}"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{palette['metalhi']}"/><stop offset=".35" stop-color="{palette['metalmid']}"/><stop offset=".6" stop-color="{palette['metalhi']}"/><stop offset="1" stop-color="{palette['metallo']}"/></linearGradient>
<linearGradient id="brass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{palette['goldhi']}"/><stop offset=".42" stop-color="{palette['gold']}"/><stop offset="1" stop-color="{palette['goldlo']}"/></linearGradient>
<linearGradient id="brass-edge" x1="0" y1="0" x2="0" y2="1"><stop stop-color="{palette['gold']}"/><stop offset="1" stop-color="{palette['goldlo']}"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="{palette['metalhi']}" stop-opacity=".13"/><stop offset=".55" stop-color="{palette['metalhi']}" stop-opacity=".01"/><stop offset="1" stop-color="{palette['metalhi']}" stop-opacity=".16"/></linearGradient>
<radialGradient id="halo"><stop stop-color="{palette['gold']}" stop-opacity=".12"/><stop offset="1" stop-color="{palette['gold']}" stop-opacity="0"/></radialGradient>
<filter id="shadow" x="-50%" y="-60%" width="200%" height="230%"><feGaussianBlur stdDeviation="14"/></filter>
</defs>
<style>
@font-face{{font-family:Manrope;src:url(data:font/woff2;base64,{regular}) format('woff2');font-weight:400}}
@font-face{{font-family:Manrope;src:url(data:font/woff2;base64,{semibold}) format('woff2');font-weight:500 800}}
:root{{{variables}}}
svg{{font-family:Manrope,Arial,sans-serif;text-rendering:geometricPrecision}}
.mono{{font-family:ui-monospace,'SFMono-Regular',Consolas,monospace}}
.rotate{{animation:rotate 24s linear infinite;transform-box:fill-box;transform-origin:center}}
.rotate-reverse{{animation:rotate 32s linear infinite reverse;transform-box:fill-box;transform-origin:center}}
.pulse{{animation:pulse 5s ease-in-out infinite}}
.flow{{stroke-dasharray:4 120;animation:flow 6s linear infinite}}
@keyframes rotate{{to{{transform:rotate(360deg)}}}}
@keyframes pulse{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@keyframes flow{{to{{stroke-dashoffset:-248}}}}
{css}
@media(prefers-reduced-motion:reduce){{*,*::before,*::after{{animation:none!important}}.motion-only{{display:none!important}}.still-only{{display:inline!important}}}}
</style>
{body}
</svg>\n'''


# An orthographic engineering drawing. All objects share this camera and lighting.
def point(x, y, z=0):
    return (round(380 + (x - y) * .94, 2), round(185 + (x + y) * .42 - z, 2))


def poly(points, fill, stroke="edge", extra=""):
    f = fill if fill.startswith("url(") else f"var(--{fill})"
    s = stroke if stroke == "none" else f"var(--{stroke})"
    return '<polygon points="' + " ".join(f"{a},{b}" for a, b in points) + f'" fill="{f}" stroke="{s}" stroke-width="1" stroke-linejoin="round" {extra}/>'


def box(x, y, z, w, d, h, top="url(#porcelain)", side="side", front="deep", edge="edge"):
    a,b,c,e = [point(*p) for p in [(x,y,z+h),(x+w,y,z+h),(x+w,y+d,z+h),(x,y+d,z+h)]]
    b0,c0,e0 = [point(*p) for p in [(x+w,y,z),(x+w,y+d,z),(x,y+d,z)]]
    return poly([b,b0,c0,c],side,edge)+poly([e,c,c0,e0],front,edge)+poly([a,b,c,e],top,edge)


def iso_line(coords, color="line", width=1, extra=""):
    pts = [point(*p) for p in coords]
    return path("M"+" L".join(f"{a} {b}" for a,b in pts),stroke=color,width=width,extra=extra)


def disk(x,y,z,r,thickness=10,fill="url(#metal)",edge="edge"):
    cx,cy=point(x,y,z)
    rx,ry=r*1.329,r*.594
    out=f'<path d="M{cx-rx} {cy}v{thickness}a{rx} {ry} 0 0 0 {2*rx} 0v-{thickness}" fill="var(--deep)" stroke="var(--{edge})"/>'
    out+=f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill if fill.startswith("url(") else f"var(--{fill})"}" stroke="var(--{edge})"/>'
    return out


def fastener(x,y,z):
    cx,cy=point(x,y,z)
    return f'<ellipse cx="{cx}" cy="{cy}" rx="3.5" ry="1.65" fill="var(--deep)"/>'+line(cx-1.5,cy,cx+1.5,cy,"edge",.6)


def arm(x,y,z,mirror=False,cls=""):
    # Three solid articulated links; concentric bearings show actual pivots.
    cx,cy=point(x,y,z)
    s=-1 if mirror else 1
    parts=disk(x,y,z,27,13)
    parts+=group(group(
        path(f"M0 0 L{-32*s} -64 L{18*s} -112",stroke="deep",width=28,extra='stroke-linecap="round" stroke-linejoin="round"')+
        path(f"M0 0 L{-32*s} -64 L{18*s} -112",stroke="metalmid",width=21,extra='stroke-linecap="round" stroke-linejoin="round"')+
        path(f"M{-3*s} -5 L{-36*s} -64 L{14*s} -110",stroke="metalhi",width=3,extra='stroke-linecap="round" stroke-linejoin="round"')+
        path(f"M{7*s} -4 Q{14*s} -58 {-24*s} -68 Q{-17*s} -105 {16*s} -117",stroke="gold",width=2)+
        circle(-32*s,-64,17,"url(#brass)","goldlo")+
        circle(-32*s,-64,10,"deep","metalhi")+
        circle(-32*s,-64,4,"url(#metal)","edge")+
        circle(18*s,-112,11,"url(#metal)","deep")+
        path(f"M{18*s} -116l{24*s} 9l{7*s} 13m{-7*s} -13l{15*s} -2",stroke="metalmid",width=6,extra='stroke-linecap="round"')+
        circle(18*s,-112,3,"gold","none"),cls=cls),f'translate({cx} {cy})')
    return parts


def machine():
    out='<ellipse cx="475" cy="560" rx="390" ry="58" fill="var(--shadow)" opacity=".13" filter="url(#shadow)"/>'
    # A pair of finely milled feet, then the lower enclosure.
    for x,y in [(20,245),(495,245),(495,20)]:
        out+=box(x,y,-84,28,28,86,"url(#metal)","side","deep")
    out+=box(0,0,-16,560,300,22,top="url(#porcelain)")
    out+=box(16,16,6,528,268,8,top="well",side="deep",front="deep",edge="deep")
    internals=''
    # Circuit traces connect memory, the reasoning core and the output rail.
    routes=[[(45,55,16),(185,55,16),(185,142,16),(260,142,16)],
            [(45,79,16),(162,79,16),(162,174,16),(260,174,16)],
            [(308,142,16),(405,142,16),(405,45,16),(505,45,16)],
            [(305,164,16),(452,164,16),(452,235,16),(512,235,16)],
            [(62,237,16),(216,237,16),(216,198,16),(272,198,16)]]
    for route in routes:
        internals+=iso_line(route,"edge",1.4)
        internals+=iso_line(route,"glow",2.2,'class="flow"')
    for x in range(46,132,17):
        internals+=box(x,40,18,9,93,31,"url(#metal)","side","deep")
    for y in [38,70,102]:
        internals+=box(430,y,18,78,20,22,"url(#porcelain)")
        internals+=iso_line([(441,y+7,42),(495,y+7,42)],"gold",2)
    internals+=box(226,108,18,116,114,18,top="url(#metal)")
    internals+=disk(284,165,53,50,12,fill="url(#brass)")
    internals+=disk(284,165,56,40,2,fill="deep")
    cx,cy=point(284,165,57)
    ring=''
    for i in range(32):
        a=i*2*pi/32
        ring+=line(cos(a)*40,sin(a)*40,cos(a)*47,sin(a)*47,"gold" if i%4==0 else "edge",1.6)
    internals+=group(group(ring,cls="rotate"),f'translate({cx} {cy}) scale(1.329 .594)')
    internals+=disk(284,165,61,18,3,fill="url(#metal)")
    internals+=arm(110,209,35,cls="arm-a")
    internals+=arm(440,220,35,mirror=True,cls="arm-b")
    # A precision shuttle advances only while the enclosure opens.
    shuttle=box(332,228,24,66,32,16,"url(#brass)","goldlo","goldlo")
    internals+=group(shuttle,cls="shuttle")
    for y in [230,272]:
        internals+=iso_line([(230,y,20),(508,y,20)],"metalmid",3)
    for x,y in [(25,25),(535,25),(25,275),(535,275)]:
        internals+=fastener(x,y,19)
    out+=group(internals,cls="internals")
    shell=poly([point(560,0,150),point(560,300,150),point(560,300,6),point(560,0,6)],"side")
    shell+=poly([point(0,300,150),point(560,300,150),point(560,300,6),point(0,300,6)],"middle")
    out+=group(shell,cls="shell")
    # Four registration pins visually explain how the lid fits the base.
    pins=''
    for x,y in [(18,18),(542,18),(18,282),(542,282)]:
        pins+=iso_line([(x,y,12),(x,y,159)],"edge",1,'stroke-dasharray="3 6"')
    out+=group(pins,cls="internals")
    lid=box(-5,-5,150,570,310,16,"url(#porcelain)","side","middle")
    lid+=iso_line([(14,288,166),(544,288,166)],"metalhi",1.1)
    for x,y in [(13,13),(547,13),(13,287),(547,287)]:
        lid+=fastener(x,y,167)
    lid+=disk(280,150,184,57,17,fill="url(#metal)")
    lid+=disk(280,150,188,49,4,fill="url(#porcelain)")
    pxc,pyc=point(280,150,189)
    lid+=f'<ellipse cx="{pxc}" cy="{pyc}" rx="54" ry="24" fill="none" stroke="var(--gold)" stroke-width="1.1"/>'
    lid+=line(pxc-14,pyc,pxc+14,pyc,"glow",3.3,'stroke-linecap="round" class="pulse"')
    # Engraved mark and a subtle horizontal sweep on the ceramic surface.
    ex,ey=point(40,260,168)
    lid+=group(text(0,0,"invrnt",14,"muted",600),f'translate({ex} {ey}) matrix(.94 .42 -.94 .42 0 0)')
    out+=group(lid,cls="lid")
    return out


HERO_CSS='''
.lid{animation:lid 18s cubic-bezier(.45,0,.2,1) infinite}
.internals{animation:internals 18s ease-in-out infinite}
.shell{animation:shell 18s ease-in-out infinite}
.arm-a{animation:arm-a 18s ease-in-out infinite;transform-origin:0 0}
.arm-b{animation:arm-b 18s ease-in-out infinite;transform-origin:0 0}
.shuttle{animation:shuttle 18s ease-in-out infinite}
@keyframes lid{0%,12%,88%,100%{transform:translateY(0)}35%,65%{transform:translateY(-110px)}}
@keyframes internals{0%,12%,92%,100%{opacity:.08}28%,72%{opacity:1}}
@keyframes shell{0%,12%,92%,100%{opacity:1}28%,72%{opacity:0}}
@keyframes arm-a{0%,25%,75%,100%{transform:rotate(0deg)}42%{transform:rotate(13deg)}58%{transform:rotate(-4deg)}}
@keyframes arm-b{0%,27%,76%,100%{transform:rotate(0deg)}46%{transform:rotate(-14deg)}60%{transform:rotate(4deg)}}
@keyframes shuttle{0%,30%,80%,100%{transform:translate(0,0)}52%,64%{transform:translate(39px,17px)}}
@media(prefers-reduced-motion:reduce){.lid{transform:translateY(-72px)}.internals{opacity:1}.shell{opacity:0}}
'''


def hero(theme,mobile=False):
    w,h=(640,990) if mobile else (1200,1110)
    margin=36 if mobile else 64
    out=label(margin,49 if mobile else 55,"JUAN CAMILO GRISALES", "ink",size=24 if mobile else 15)
    if not mobile:
        out+=label(w-margin,55,"INVRNT / COLOMBIA",anchor="end")
    out+=line(margin,79,w-margin,79)
    if mobile:
        out+=text(margin,174,"More possible.",67,"ink",500,spacing=-3.6)
        out+=text(margin,255,"Less in the way.",67,"ink",500,spacing=-3.6)
        out+=text(margin,322,"Powerful systems. Simple experiences.",25,"muted")
        out+=group(machine(),"translate(15 420) scale(.63)")
        out+=label(margin,902,"AI ENGINEER & PRODUCT BUILDER",size=20)
        out+=text(margin,948,"One intention. An entire machine behind it.",25,"muted")
    else:
        out+=text(margin,188,"More possible.",100,"ink",500,spacing=-5)
        out+=text(margin,300,"Less in the way.",100,"ink",500,spacing=-5)
        out+=text(margin,355,"Powerful systems. Simple experiences.",27,"muted")
        out+=group(machine(),"translate(172 503) scale(.87)")
        out+=label(margin,452,"THE QUIET MACHINE",size=13)
        out+=label(margin,478,"ONE INTENTION IN.",size=11)
        out+=line(margin,498,margin+42,498,"gold",2)
        out+=label(w-margin,1042,"AI ENGINEER & PRODUCT BUILDER",anchor="end",size=13)
        out+=label(w-margin,1072,"MEDELLÍN, CO · UTC−05",anchor="end",size=12)
    return svg("hero",theme,w,h,"Juan Camilo Grisales. More possible. Less in the way.",
               "AI engineer and product builder in Medellín, Colombia. A single ceramic control sits on a quiet desk. The lid lifts to reveal a precision machine: memory, a reasoning core, articulated arms and a balanced output. The mechanism returns to one simple control.",out,HERO_CSS)


def waveform(x,y,width=190,height=24,step=8,cls="voice"):
    out=''
    n=int(width/step)
    for i in range(n):
        h=height*(.18+.82*abs(sin(i*1.73)*sin(i*.32+.4)))
        out+=line(x+i*step,y-h/2,x+i*step,y+h/2,"glow",3,
                  f'stroke-linecap="round" class="{cls}" style="animation-delay:{-i*.09}s;transform-origin:{x+i*step}px {y}px"')
    return out


def section_top(w,mobile,number,name,meta):
    m=36 if mobile else 64
    out=line(m,20,w-m,20)
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
        out+=line(m,732,w-m,732)
        out+=label(m,770,"SAY IT NATURALLY.",size=13)+label(w-m,770,"KEEP EVERY DETAIL.",anchor="end",size=13)
    return svg("count",theme,w,h,"Count. Finance, in your own words. Product concept, in development.",
               "An illustrated voice note lends Kevin US$5,000 from a Bancolombia Pod at 12% interest. Count asks whether the rate is effective annual or monthly. Annual is selected. A bank decrease and an equal receivable are recorded; the twelve-month dial represents time-aware accounting. This is a product concept, not a live app.",out,COUNT_CSS)


def architecture(theme,mobile=False):
    w,h=(640,1100) if mobile else (1200,860)
    m=36 if mobile else 64
    out=label(m,51,"INSIDE COUNT",size=17 if mobile else 14)
    out+=text(m,117,"Simple is engineered.",44 if mobile else 53,"ink",500,spacing=-2)
    # A vertical stack acts as a legible, physical architecture diagram.
    plates=''
    captions=[("01","INTENT","Voice · text · receipts"),("02","CLARIFICATION","Ask only what is missing"),
              ("03","LEDGER","Pods · exact, balanced entries"),("04","TIME","Accruals · scheduled work"),
              ("05","RESULT","A clear answer. An inspectable record.")]
    for i,(n,title,description) in enumerate(captions):
        yy=210+i*(174 if mobile else 127)
        # Same micro-controller shape becomes five transparent layers.
        xx=40 if mobile else 685
        plate=box(0,0,0,185,98,12,"url(#porcelain)")
        for x,y in [(18,18),(166,18),(18,80),(166,80)]:
            plate+=fastener(x,y,14)
        plate+=disk(93,49,18,21,6,fill="url(#brass)" if i==2 else "url(#metal)")
        plate+=iso_line([(28,49,14),(65,49,14)],"gold",2)
        plate+=iso_line([(120,49,14),(159,49,14)],"gold",2)
        plate=group(plate,"translate(-290 -168)")
        plates+=group(plate,f"translate({xx} {yy})"+(" scale(.68)" if mobile else ""))
        plates+=circle(231 if mobile else 630,yy+12,4,"gold","none",extra=f'class="pulse" style="animation-delay:{-i}s"')
        if mobile:
            out+=label(268,yy+11,n+" / "+title,"ink",size=18)
            words=description.split(". ") if i==4 else description.split(" · ")
            for j,s in enumerate(words):
                out+=text(268,yy+47+j*31,s,23,"muted")
        else:
            out+=label(m,yy,n+" / "+title,"ink",size=15)
            out+=text(m,yy+39,description,25,"muted")
            out+=line(460,yy+12,640,yy+12,"line",1)
    out+=plates
    if not mobile:
        out+=path("M935 254v516",stroke="line",width=1)
        out+=path("M935 254v516",stroke="glow",width=2,extra='stroke-dasharray="8 100" class="flow"')
    return svg("architecture",theme,w,h,"Inside Count. Simple is engineered.",
               "Five layers of the planned system: understand intent from voice, text and receipts; ask about missing context; record exact balanced entries in account-specific Pods; account for time; return a clear result with inspectable records.",out)


PRODUCT_CSS='''
.sheet-a{animation:sheet-a 12s cubic-bezier(.4,0,.2,1) infinite}
.sheet-b{animation:sheet-b 12s cubic-bezier(.4,0,.2,1) infinite}
.write-line{stroke-dasharray:200;stroke-dashoffset:200;animation:write 12s ease-in-out infinite}
.scan-line{animation:scan 12s ease-in-out infinite}
.file-a{animation:file-a 12s cubic-bezier(.4,0,.2,1) infinite}
.file-b{animation:file-b 12s cubic-bezier(.4,0,.2,1) infinite}
.voice{animation:voice 3s ease-in-out infinite}
@keyframes sheet-a{0%,100%{transform:translateY(-8px)}40%,70%{transform:translateY(6px)}}
@keyframes sheet-b{0%,100%{transform:translateY(6px)}40%,70%{transform:translateY(-8px)}}
@keyframes write{0%,18%,100%{stroke-dashoffset:200}48%,88%{stroke-dashoffset:0}}
@keyframes scan{0%,12%,92%,100%{transform:translateY(0);opacity:0}20%{opacity:1}80%{transform:translateY(136px);opacity:1}}
@keyframes file-a{0%,12%,96%,100%{transform:translateY(-26px)}42%,78%{transform:translateY(0)}}
@keyframes file-b{0%,22%,96%,100%{transform:translateY(-35px)}52%,83%{transform:translateY(0)}}
@keyframes voice{0%,100%{transform:scaleY(.5)}50%{transform:scaleY(1)}}
@media(prefers-reduced-motion:reduce){.write-line{stroke-dashoffset:0}.scan-line{opacity:0}}
'''


def sheet(x,y,w,h,kind="document",cls=""):
    out=rect(0,0,w,h,9,"url(#porcelain)","edge")
    out+=line(10,h+4,w-4,h+4,"line",1)
    if kind=="audio":
        out+=circle(27,28,10,"none","gold",1)
        out+=line(24,22,24,34,"gold",2)+line(29,22,29,34,"gold",2)
        out+=waveform(23,76,w-42,38,7)
        out+=line(22,h-31,w-22,h-31,"line",1.2)
        out+=circle(45,h-31,3,"gold","none")
    else:
        out+=rect(20,20,25,5,2,"gold","none")
        for i,frac in enumerate([.78,1,.91,.62]):
            out+=line(20,51+i*15,20+(w-40)*frac,51+i*15,"muted",1.7)
        if kind=="result":
            out+=rect(20,120,w-40,43,5,"faint","line")
            out+=line(30,134,w-34,134,"gold",2,extra='class="write-line"')
            out+=line(30,149,w-64,149,"gold",2,extra='class="write-line" style="animation-delay:.35s"')
            for i in range(3):
                out+=circle(25+i*20,h-24,4,"none","gold")
    return group(group(out,cls=cls),f"translate({x} {y})")


def classmate_art():
    out='<ellipse cx="321" cy="401" rx="206" ry="30" fill="var(--shadow)" opacity=".1" filter="url(#shadow)"/>'
    # An open book, with a real shared spine. Materials flow toward one source-aware result.
    out+=path("M98 297Q195 259 310 305Q419 259 520 297L506 377Q406 346 310 392Q213 346 111 377Z","url(#porcelain)","edge")
    out+=path("M98 286Q195 248 310 294Q419 248 520 286L506 364Q406 333 310 379Q213 333 111 364Z","url(#porcelain)","edge")
    out+=path("M100 280Q201 240 310 287Q418 240 518 280L504 355Q409 326 310 371Q211 326 113 355Z","paper","edge")
    out+=path("M310 287v84",stroke="gold",width=1.4)
    for i in range(4):
        yy=286+i*15
        out+=path(f"M137 {yy}Q211 {yy-19} 282 {yy+8}",stroke="line",width=1.2)
        out+=path(f"M338 {yy+8}Q411 {yy-19} 484 {yy}",stroke="line",width=1.2)
    out+=path("M148 192C140 247 190 232 252 271M473 177C505 234 434 227 385 265",stroke="line",width=1.2)
    out+=path("M148 192C140 247 190 232 252 271M473 177C505 234 434 227 385 265",stroke="glow",width=2,extra='class="flow"')
    out+=sheet(52,36,157,161,"audio","sheet-a")
    out+=sheet(413,27,141,151,"document","sheet-b")
    out+=sheet(226,66,171,223,"result")
    out+=label(312,327,"CONTEXT",anchor="middle",size=12)
    return out


def chair(x,y,mirror=False):
    # Bent-metal frame, upholstered back and seat. Human space is kept still.
    sign=-1 if mirror else 1
    out=path("M-46 52L-39 143M34 52L43 143",stroke="metalmid",width=5,extra='stroke-linecap="round"')
    out+=path("M-46 50V-45Q-46 -60 -32 -60H24Q38 -60 38 -46V50",stroke="metalmid",width=6,extra='stroke-linejoin="round"')
    out+=rect(-50,-67,91,93,15,"url(#porcelain)","edge")
    out+=path("M-46 42Q-10 31 49 44L58 57Q-2 69 -49 57Z","url(#porcelain)","edge")
    out+=line(-48,59,56,58,"metalhi",1.1)
    return group(out,f"translate({x} {y}) skewY({-8*sign})")


def orientador_art():
    out='<ellipse cx="230" cy="407" rx="203" ry="28" fill="var(--shadow)" opacity=".1" filter="url(#shadow)"/>'
    out+=chair(101,251)+chair(338,251,True)
    # A conversation remains central while documentation assembles to the side.
    out+=path("M142 216Q218 158 292 216",stroke="line",width=1.2)
    out+=waveform(178,183,70,29,7)
    out+=path("M248 183C361 90 360 77 422 106",stroke="line",width=1.1)
    out+=path("M248 183C361 90 360 77 422 106",stroke="glow",width=2,extra='class="flow"')
    report=rect(0,0,150,208,10,"url(#porcelain)","edge")
    report+=label(22,31,"SESSION",size=11)
    report+=line(22,55,121,55,"line",1.5)
    for i,length in enumerate([103,88,103,72,97]):
        report+=line(22,77+i*18,22+length,77+i*18,"muted",1.6,extra=f'class="write-line" style="animation-delay:{i*.25}s"')
    report+=rect(22,170,105,23,5,"faint","gold")
    report+=text(75,186,"FOR REVIEW",10,"glow",500,"middle",1.1)
    out+=group(report,"translate(422 30)")
    return out


def bento_art():
    out='<ellipse cx="315" cy="406" rx="231" ry="33" fill="var(--shadow)" opacity=".1" filter="url(#shadow)"/>'
    # Files descend into a local enclosure with visible, orderly compartments.
    out+=group(box(0,0,0,300,183,19,"url(#porcelain)"),"translate(-16 70)")
    out+=group(box(10,12,20,279,158,13,"well","side","deep"),"translate(-16 70)")
    for x,y in [(36,35),(134,35),(222,35),(36,114),(134,114),(222,114)]:
        out+=group(box(x,y,36,58,38,18,"url(#metal)"),"translate(-16 70)")
    tile=rect(0,0,130,150,12,"url(#porcelain)","edge")
    tile+=rect(13,14,104,77,6,"faint","line")
    tile+=circle(88,36,11,"url(#brass)","none")
    tile+=path("M18 78L42 47L68 72L83 58L110 82Z","metalmid","none")
    tile+=line(19,113,108,113,"muted",2)+line(19,127,73,127,"line",2)
    out+=group(group(tile,cls="file-a"),"translate(147 111) rotate(-8)")
    out+=sheet(283,66,142,178,"document","file-b")
    # Near wall occludes the lower part of the files, so they really enter the box.
    near=poly([point(0,183,110),point(300,183,110),point(300,183,19),point(0,183,19)],"url(#porcelain)")
    near+=poly([point(300,0,110),point(300,183,110),point(300,183,19),point(300,0,19)],"side")
    out+=group(near,"translate(-16 70)")
    cx,cy=point(150,184,71)
    out+=group(label(0,0,"LOCAL",size=13),f"translate({cx-16} {cy+70}) matrix(.94 .42 0 1 0 0)")
    out+=circle(504,314,4,"gold","none",extra='class="pulse"')
    return out


PRODUCTS={
    "classmate":("02","CLASSMATE STUDIO","Room to think.",["Course materials, recordings and AI.","One shared context."],classmate_art,
                 "Classmate Studio. Course materials, recordings and AI in one academic workspace. A voice recording and document join a shared, source-aware context, illustrated as an open book."),
    "orientador":("03","ORIENTADOR","Time to listen.",["AI-assisted documentation", "for school counselors."],orientador_art,
                  "Orientador. AI-assisted documentation for school counselors. Two chairs face each other while a session document assembles to the side, ready for professional review."),
    "bento":("04","BENTO","Yours to keep.",["A local-first home", "for your files."],bento_art,
             "Bento. A local-first home for your files. Photos and documents settle into an organized local enclosure. Your files remain on your own device by default."),
}


def product(name,theme,mobile=False):
    number,title,headline,body,draw,desc=PRODUCTS[name]
    w,h=(640,780) if mobile else (1200,546)
    m=36 if mobile else 64
    out=section_top(w,mobile,number,title,"")
    out+=text(m,149 if mobile else 197,headline,55 if mobile else 57,"ink",500,spacing=-2.7)
    for i,value in enumerate(body):
        out+=text(m,(209 if mobile else 255)+i*37,value,29 if mobile else 26,"muted")
    cta={"classmate":"EXPLORE CLASSMATE ↗","orientador":"EXPLORE ORIENTADOR ↗","bento":"VIEW THE SOURCE ↗"}[name]
    out+=label(m,296 if mobile else 368,cta,"glow",size=17 if mobile else 13)
    placement=("translate(22 350) scale(.85)" if mobile else "translate(558 110) scale(.88)") if name=="bento" else ("translate(25 305) scale(.96)" if mobile else "translate(558 101) scale(.99)")
    out+=group(draw(),placement)
    return svg(name,theme,w,h,title+". "+headline,desc,out,PRODUCT_CSS)


AMBITION_CSS='''
.build-one{animation:build-one 24s cubic-bezier(.4,0,.2,1) infinite}
.build-two{animation:build-two 24s cubic-bezier(.4,0,.2,1) infinite}
.build-three{animation:build-three 24s cubic-bezier(.4,0,.2,1) infinite}
.research{animation:research 8s ease-in-out infinite}
.work-arm{animation:work-arm 8s ease-in-out infinite;transform-origin:0 0}
.growth{animation:growth 24s ease-in-out infinite;transform-box:fill-box;transform-origin:center bottom}
@keyframes build-one{0%,100%{opacity:.7;transform:translateY(12px)}12%,92%{opacity:1;transform:translateY(0)}}
@keyframes build-two{0%,12%,100%{opacity:.55;transform:translateY(18px)}28%,92%{opacity:1;transform:translateY(0)}}
@keyframes build-three{0%,28%,100%{opacity:.4;transform:translateY(22px)}45%,92%{opacity:1;transform:translateY(0)}}
@keyframes research{0%,100%{transform:translateY(0)}50%{transform:translateY(8px)}}
@keyframes work-arm{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(18deg)}}
@keyframes growth{0%,30%,100%{transform:scaleY(.35);opacity:.3}62%,92%{transform:scaleY(1);opacity:1}}
@media(prefers-reduced-motion:reduce){.build-one,.build-two,.build-three,.growth{opacity:1;transform:none}}
'''


def workshop():
    out=box(0,0,0,190,150,16,"url(#porcelain)")
    out+=box(13,12,17,162,120,6,"well","side","deep")
    out+=iso_line([(34,30,26),(150,30,26),(150,120,26)],"gold",1.6)
    out+=arm(62,92,34,cls="work-arm")
    out+=box(118,37,25,38,42,27,"url(#brass)","goldlo","goldlo")
    out+=disk(139,58,55,12,3,"url(#metal)")
    for yy in [35,51,67,83]:
        out+=iso_line([(16,yy,24),(37,yy,24)],"edge",2)
    return group(out,"translate(-239 -103)")


def laboratory():
    out=box(0,0,0,190,150,16,"url(#porcelain)")
    out+=box(24,25,16,140,100,21,"url(#porcelain)")
    cx,cy=point(88,83,40)
    instrument=disk(88,83,46,40,8,"url(#metal)")
    # A microscope's load-bearing arm, optical tube, stage and focus adjustment.
    body=path("M-32 0Q-54 -74 -26 -127L-7 -135",stroke="deep",width=22,extra='stroke-linecap="round"')
    body+=path("M-32 0Q-54 -74 -26 -127L-7 -135",stroke="metalmid",width=16,extra='stroke-linecap="round"')
    body+=path("M-35 -3Q-56 -75 -28 -127",stroke="metalhi",width=2.2)
    body+=group(rect(-10,-148,28,76,5,"url(#metal)","edge")+rect(-6,-160,20,15,3,"deep","edge")+
                rect(-5,-71,18,22,2,"url(#brass)","goldlo"),cls="research")
    body+=path("M-28 -33L30 -46L55 -32L-5 -17Z","deep","edge")
    body+=path("M-13 -33L15 -39L32 -30L4 -24Z","url(#glass)","gold")
    body+=circle(-36,-59,15,"url(#brass)","goldlo")+circle(-36,-59,6,"url(#metal)","edge")
    body+=path("M8 -64L8 -34",stroke="glow",width=2,extra='class="pulse"')
    instrument+=group(body,f"translate({cx} {cy})")
    out+=instrument
    for x in [140,159]:
        out+=disk(x,111,48,6,27,"url(#glass)")
    return group(out,"translate(-239 -103)")


def greenhouse():
    out=box(0,0,0,190,150,16,"url(#porcelain)")
    for x in [32,82,132]:
        out+=box(x,23,17,26,102,9,"deep","side","deep")
        for yy in [41,75,108]:
            cx,cy=point(x+13,yy,29)
            plant=path("M0 0V-25",stroke="metalmid",width=2)
            plant+=path("M0 -12Q-18 -33 -20 -16Q-17 -9 0 -12M0 -19Q17 -41 18 -22Q12 -16 0 -19", "metalmid","metalhi",.6)
            out+=group(group(plant,cls="growth"),f"translate({cx} {cy})")
    # Repeated arches make a greenhouse, not an arbitrary glass box.
    for x in [9,65,123,180]:
        a=point(x,10,18);b=point(x,10,102);c=point(x,75,164);d=point(x,140,102);e=point(x,140,18)
        out+=path(f"M{a[0]} {a[1]}L{b[0]} {b[1]}Q{c[0]} {c[1]} {d[0]} {d[1]}L{e[0]} {e[1]}",stroke="metalmid",width=2)
    for yy,zz in [(10,101),(75,133),(140,101)]:
        out+=iso_line([(9,yy,zz),(180,yy,zz)],"edge",1.2)
    out+=poly([point(9,140,17),point(180,140,17),point(180,140,102),point(9,140,102)],"url(#glass)","edge")
    return group(out,"translate(-239 -103)")


def ambition(theme,mobile=False):
    w,h=(640,1200) if mobile else (1200,875)
    m=36 if mobile else 64
    out=section_top(w,mobile,"05","AMBITION","CAPABILITY → PROSPERITY")
    if mobile:
        out+=text(m,150,"Make room for",59,"ink",500,spacing=-2.6)
        out+=text(m,219,"bigger ambitions.",59,"ink",500,spacing=-2.6)
        for i,value in enumerate(["Make valuable work cheaper.","Help every industry attempt more."]):
            out+=text(m,285+i*38,value,26,"muted")
        placements=[(56,464,.77),(334,662,.77),(56,868,.77)]
        out+=path("M239 587C420 564 454 645 448 747S235 829 227 960",stroke="line",width=1.4)
        out+=path("M239 587C420 564 454 645 448 747S235 829 227 960",stroke="glow",width=2,extra='class="flow"')
    else:
        out+=text(m,164,"Make room for",72,"ink",500,spacing=-3.2)
        out+=text(m,247,"bigger ambitions.",72,"ink",500,spacing=-3.2)
        out+=text(m,314,"Make valuable work cheaper. Help every industry attempt more.",27,"muted")
        placements=[(110,478,1),(454,432,1),(796,477,1)]
        out+=path("M287 688C446 716 458 629 579 641S864 756 961 692",stroke="line",width=1.3)
        out+=path("M287 688C446 716 458 629 579 641S864 756 961 692",stroke="glow",width=2,extra='class="flow"')
    for (x,y,s),draw,cls,caption in zip(placements,[workshop,laboratory,greenhouse],["build-one","build-two","build-three"],["BUILD","DISCOVER","GROW"]):
        out+=group(group(draw(),cls=cls),f"translate({x} {y}) scale({s})")
        out+=label(x+145*s,y+248*s,caption,anchor="middle",size=17 if mobile else 13)
    out+=line(m,h-103,w-m,h-103)
    out+=text(m,h-54,"Toward ASI. Toward shared abundance.",25 if mobile else 29,"ink",500,spacing=-.4)
    return svg("ambition",theme,w,h,"Make room for bigger ambitions.",
               "I want AI to make economically valuable work dramatically cheaper, so people across every industry can attempt more. As we move toward ASI, I want to help turn that capability into broadly shared abundance. A precision workshop enables scientific instruments and a greenhouse, representing building, discovery and growth.",out,AMBITION_CSS)


def contact(theme,mobile=False):
    w,h=(640,420) if mobile else (1200,414)
    m=36 if mobile else 64
    out=line(m,20,w-m,20)
    out+=label(m,68,"THE NEXT THING",size=17 if mobile else 14)
    out+=text(m,151,"What should" if mobile else "What should become simpler?",57 if mobile else 58,"ink",500,spacing=-2.6)
    if mobile:
        out+=text(m,216,"become simpler?",57,"ink",500,spacing=-2.6)
    out+=text(m,281 if mobile else 211,"Let's build it.",32,"muted")
    # The entire machine resolves to the same simple control as the opening.
    mark=circle(0,0,45,"url(#metal)","edge")+circle(0,0,36,"url(#porcelain)","edge")
    mark+=circle(0,0,28,"none","gold",1)
    mark+=line(-9,0,9,0,"glow",2.5,extra='class="pulse" stroke-linecap="round"')
    if mobile:
        out+=group(mark,"translate(550 350) scale(.65)")
        out+=label(m,362,"INVRNT",size=17)
    else:
        out+=group(mark,"translate(1070 276)")
        out+=label(m,332,"JUAN CAMILO GRISALES",size=14)
        out+=label(m,364,"MEDELLÍN, COLOMBIA",size=12)
    return svg("contact",theme,w,h,"What should become simpler? Let's build it.",
               "Contact Juan Camilo Grisales at juan@juancamilo.me or visit juancamilo.me. The precision machine resolves to one simple ceramic control.",out)


SCENES={"hero":hero,"count":count,"architecture":architecture,
        **{name:(lambda t,m,n=name:product(n,t,m)) for name in PRODUCTS},
        "ambition":ambition,"contact":contact}


def picture(name,alt,href=None):
    alt=escape(alt,quote=True)
    blocks=[]
    for theme in PALETTES:
        target=href if href and not href.startswith('mailto:') else ("https://juancamilo.me" if href else f"assets/{name}-{theme}.svg")
        blocks.append(f'''<a href="{target}#gh-{theme}-mode-only">
<picture>
  <source media="(max-width: 600px) and (prefers-reduced-motion: reduce)" srcset="assets/{name}-mobile-{theme}-still.svg">
  <source media="(prefers-reduced-motion: reduce)" srcset="assets/{name}-{theme}-still.svg">
  <source media="(max-width: 600px)" srcset="assets/{name}-mobile-{theme}.svg">
  <img src="assets/{name}-{theme}.svg" width="100%" alt="{alt}">
</picture>
</a>''')
    return "\n".join(blocks)


def readme():
    parts=["<!-- Generated with python3 tools/build.py. Text edition below. -->",
           picture("hero","Juan Camilo Grisales, AI engineer and product builder in Medellín, Colombia. More possible. Less in the way. Powerful systems, simple experiences."),
           '<p align="center">\n  <a href="https://juancamilo.me">Website ↗</a> &nbsp; · &nbsp; <a href="mailto:juan@juancamilo.me">Email ↗</a>\n</p>',
           picture("count","Count. Finance, in your own words. Product concept, in development. A voice note becomes a precise, balanced financial record. When a rate is ambiguous, Count asks a clear question."),
           '<details>\n<summary>Open the machine</summary>\n',
           picture("architecture","Inside Count. Simple is engineered: intent, clarification, exact double-entry records, time-aware calculations, and an inspectable result."),
           "Count is in development. The animation illustrates the intended experience. Its design combines account-specific Pods, double-entry accounting and time-aware calculations. Ambiguity becomes a clear question. The detail stays available.",
           "[Inspect the control in 3D ↗](assets/control.stl)",
           '</details>',
           picture("classmate","Classmate Studio. Room to think. Course materials, recordings and AI in one shared context. Explore Classmate.","https://classmate.studio"),
           picture("orientador","Orientador. Time to listen. AI-assisted documentation for school counselors, with professional review. Explore Orientador.","https://orientador.co"),
           picture("bento","Bento. Yours to keep. A local-first home for your files. Explore the source.","https://github.com/invrnt/bento"),
           picture("ambition","Make room for bigger ambitions. I want AI to make economically valuable work cheaper and help every industry attempt more. Toward ASI, toward broadly shared abundance."),
           picture("contact","What should become simpler? Let's build it. Contact Juan Camilo Grisales.","mailto:juan@juancamilo.me"),
           '<p align="center">\n  <a href="mailto:juan@juancamilo.me">juan@juancamilo.me ↗</a> &nbsp; · &nbsp; <a href="https://juancamilo.me">juancamilo.me ↗</a>\n</p>',
           '''<details>
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

</details>''']
    return "\n\n".join(parts)+"\n"


def control_stl():
    """A closed, rotationally symmetric control for GitHub's native 3D viewer."""
    profiles=[[(0,0),(58,0),(62,3),(62,10),(58,14),(0,14)],
              [(49,14.5),(52,14.5),(52,17),(49,17),(49,14.5)],
              [(0,15),(46,15),(47,17),(47,21),(45,23),(0,23)]]
    triangles=[]
    for profile in profiles:
        for i in range(96):
            a,b=2*pi*i/96,2*pi*(i+1)/96
            for (r0,z0),(r1,z1) in zip(profile,profile[1:]):
                v=[(r0*cos(a),r0*sin(a),z0),(r0*cos(b),r0*sin(b),z0),
                   (r1*cos(b),r1*sin(b),z1),(r1*cos(a),r1*sin(a),z1)]
                for p,q,r in [(v[0],v[1],v[2]),(v[0],v[2],v[3])]:
                    u=[q[j]-p[j] for j in range(3)]; vv=[r[j]-p[j] for j in range(3)]
                    n=[u[1]*vv[2]-u[2]*vv[1],u[2]*vv[0]-u[0]*vv[2],u[0]*vv[1]-u[1]*vv[0]]
                    length=sum(a*a for a in n)**.5
                    if length<1e-8:
                        continue
                    n=[a/length for a in n]
                    triangles.append(struct.pack('<12fH',*n,*p,*q,*r,0))
    header=b'The quiet machine / invrnt / control study / arbitrary units'.ljust(80,b'\0')
    return header+struct.pack('<I',len(triangles))+b''.join(triangles)


def build():
    ASSETS.mkdir(exist_ok=True)
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
    (ROOT/"README.md").write_text(readme())
    (ASSETS/"control.stl").write_bytes(control_stl())


if __name__=="__main__":
    build()
