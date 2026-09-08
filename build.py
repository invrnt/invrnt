from pathlib import Path
from html import escape
import math

ROOT = Path(__file__).parent
A = ROOT / 'assets'
A.mkdir(exist_ok=True)
G='#C9A96E'; W='#F3F0E8'; M='#B2AEA5'; D='#55472F'
def text(x,y,s,size=18,color=W,weight=400,spacing=0,mono=False):
    font='monospace' if mono else 'Arial, Helvetica, sans-serif'
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{font}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}">{escape(s)}</text>'
def line(x,y,xx,yy,color=D):
    return f'<path d="M{x} {y}H{xx}" stroke="{color}"/>' if y==yy else f'<path d="M{x} {y}L{xx} {yy}" stroke="{color}"/>'
def seal(cx,cy,r):
    # Two steady pillars inside an open measuring ring: a new monogram for invrnt.
    z=f'<g transform="translate({cx} {cy})" fill="none" stroke="{G}">'
    z+=f'<circle r="{r}" stroke-width="1" opacity=".5" stroke-dasharray="{r*2.6} {r*.54}" transform="rotate(-74)"/>'
    z+=f'<path d="M{-r*.28} {-r*.45}V{r*.45}M{r*.28} {-r*.45}V{r*.45}" stroke-width="{r*.075}"/>'
    z+=f'<path d="M{-r*.45} {-r*.6}H{r*.45}M{-r*.45} {r*.6}H{r*.45}" stroke-width="{r*.04}"/>'
    z+=f'<circle cx="0" cy="0" r="{r*.045}" fill="{G}" stroke="none"/>'
    return z+'</g>'
def svg(name,h,body,title):
    (A/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="896" height="{h}" viewBox="0 0 896 {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title><rect width="896" height="{h}" rx="8" fill="#000000"/>'+body+'</svg>')

b=seal(73,68,22)+text(111,74,'INVRNT',14,G,500,4)+text(661,73,'COLOMBIA / REMOTE',11,M,400,1,True)
b+=line(48,108,848,108)
b+=text(48,164,'AI ENGINEER  /  PRODUCT BUILDER',12,G,400,2,True)
b+=text(45,236,'Juan Camilo',61,W,500,-2)
b+=text(48,288,'Complex systems.',29,W)+text(48,328,'Simple experiences.',29,G)
b+=text(48,390,'AI products · Automation · Serverless systems',15,M)
b+=seal(724,262,76)
for i in range(48):
    angle=i*math.pi/24
    r1=103 if i%4==0 else 108
    b+=line(round(724+r1*math.cos(angle),2),round(262+r1*math.sin(angle),2),round(724+114*math.cos(angle),2),round(262+114*math.sin(angle),2),D)
b+=line(610,262,634,262)+line(814,262,838,262)
svg('hero.svg',432,b,'Juan Camilo / invrnt. AI engineer and product builder. Complex systems. Simple experiences. Colombia / Remote.')

b=text(48,46,'01 / ABOUT',11,G,400,2,True)
for y,s in [(89,'I build AI products, from architecture to the experience people use.'),(120,'My work brings together agent workflows, automation and serverless systems.'),(163,'Studying Computer Engineering and Public Accounting in Colombia.'),(194,'Interested in the details that make complex software feel simple.')]:
    b+=text(48,y,s,18 if y<150 else 16,W if y<150 else M)
svg('about.svg',230,b,'I build AI products, from architecture to user experience. Agent workflows, automation and serverless systems. Studying Computer Engineering and Public Accounting in Colombia.')

svg('selected.svg',88,text(48,50,'02 / SELECTED PRODUCTS',11,G,400,2,True)+line(293,46,848,46),'Selected products')
projects=[('classmate','01','Classmate Studio','AI FOR UNIVERSITY LIFE',['A conversational assistant for academic workflows,','with research and document generation.'],'Next.js / FastAPI / AI agents / Cloudflare','CLASSMATE.STUDIO'),('orientador','02','Orientador.co','AI FOR SCHOOL COUNSELORS',['School documentation and support workflows,','designed for counselors in Colombia.'],'Document automation / Human review','ORIENTADOR.CO'),('count','03','Count','AI FOR PERSONAL FINANCE',['Personal finances with AI. Powerful capabilities,','with as little complexity as possible for the person using them.'],'Product focus / Personal finance / AI','PRIVATE PROJECT')]
for name,num,title,kicker,lines,stack,link in projects:
    b=text(48,43,num,12,G,400,1,True)+text(88,43,kicker,11,M,400,1.5,True)
    b+=text(48,94,title,32,W,500,-.5)
    b+=text(48,131,lines[0],17,M)+text(48,157,lines[1],17,M)
    b+=line(48,183,848,183)+text(48,213,stack,12,M)+text(655,213,link,11,G,400,0,True)
    if name!='count': b+=text(822,92,'↗',26,G)
    svg(name+'.svg',246,b,title+'. '+ ' '.join(lines)+'. '+stack)

b=text(48,45,'03 / HOW I WORK',11,G,400,2,True)
for y,n,t,s in [(91,'01','Architecture to delivery','I design, build and deploy complete products.'),(158,'02','AI-assisted engineering','I orchestrate agents and review the systems they help build.'),(225,'03','Domain knowledge','Accounting studies inform how I think about financial workflows.')]:
    b+=text(48,y,n,12,G,400,0,True)+text(87,y,t,20,W)+text(87,y+28,s,15,M)
svg('approach.svg',289,b,'How I work: architecture to delivery, AI-assisted engineering and domain knowledge.')

b=text(48,45,'04 / WORKING TOOLKIT',11,G,400,2,True)
b+=text(48,88,'Python / FastAPI',20,W)+text(464,88,'TypeScript / React / Next.js',20,W)
b+=text(48,126,'LangChain / LangGraph',20,W)+text(464,126,'Cloudflare / PostgreSQL / Docker',20,W)
b+=text(48,170,'Agent orchestration · Human-in-the-loop · Automation',14,M)
svg('toolkit.svg',204,b,'Working toolkit: Python, FastAPI, TypeScript, React, Next.js, LangChain, LangGraph, Cloudflare, PostgreSQL and Docker.')

b=text(48,46,'05 / CONNECT',11,G,400,2,True)+text(48,99,'Let’s build something useful.',30,W,500,-.5)
b+=text(48,139,'Open to conversations with engineering teams and collaborators.',17,M)
b+=line(48,172,848,172)+text(48,208,'JUANCAMILO.ME',12,G,400,2,True)+text(615,208,'HI@JUANCAMILO.ME',12,G,400,1,True)
svg('connect.svg',243,b,'Open to conversations with engineering teams and collaborators. juancamilo.me / hi@juancamilo.me')

(A/'avatar.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><rect width="512" height="512" fill="#000"/>'+seal(256,256,168)+'</svg>')

readme='''<!-- Profile artwork is editable SVG. Text equivalents are provided as image alt text. -->
<p align="center">
  <a href="https://juancamilo.me"><img src="assets/hero.svg" width="100%" alt="Juan Camilo / invrnt. AI engineer and product builder. Complex systems. Simple experiences. Colombia / Remote." /></a>
</p>

<p align="center">
  <a href="https://juancamilo.me">Portfolio</a> &nbsp; · &nbsp;
  <a href="mailto:hi@juancamilo.me">Contact</a> &nbsp; · &nbsp;
  <a href="https://github.com/invrnt?tab=repositories">Repositories</a>
</p>

<img src="assets/about.svg" width="100%" alt="I build AI products, from architecture to user experience, with agent workflows, automation and serverless systems. Studying Computer Engineering and Public Accounting in Colombia." />

<img src="assets/selected.svg" width="100%" alt="Selected products" />

<a href="https://classmate.studio"><img src="assets/classmate.svg" width="100%" alt="Classmate Studio: a conversational assistant for university workflows, with research and document generation. Next.js, FastAPI, AI agents and Cloudflare. Visit Classmate Studio." /></a>

<a href="https://orientador.co"><img src="assets/orientador.svg" width="100%" alt="Orientador.co: school documentation and support workflows for counselors in Colombia. Document automation with human review. Visit Orientador.co." /></a>

<img src="assets/count.svg" width="100%" alt="Count: AI for personal finance. Powerful capabilities with as little complexity as possible for the person using them. Private project." />

<img src="assets/approach.svg" width="100%" alt="How I work. Architecture to delivery: I design, build and deploy complete products. AI-assisted engineering: I orchestrate agents and review the systems they help build. Domain knowledge: accounting studies inform how I think about financial workflows." />

<img src="assets/toolkit.svg" width="100%" alt="Working toolkit: Python, FastAPI, TypeScript, React, Next.js, LangChain, LangGraph, Cloudflare, PostgreSQL and Docker. Agent orchestration, human-in-the-loop and automation." />

<p align="center">
  <a href="https://github.com/invrnt/goalwatch"><img src="https://img.shields.io/github/last-commit/invrnt/goalwatch?style=flat-square&amp;label=GoalWatch&amp;labelColor=000000&amp;color=C9A96E" alt="GoalWatch latest public commit" /></a>
  &nbsp;
  <a href="https://github.com/invrnt?tab=repositories">Occasional open-source work ↗</a>
</p>

<a href="https://juancamilo.me"><img src="assets/connect.svg" width="100%" alt="Let’s build something useful. Open to conversations with engineering teams and collaborators. Visit juancamilo.me." /></a>

<p align="center"><a href="mailto:hi@juancamilo.me">hi@juancamilo.me</a></p>
'''
(ROOT/'README.md').write_text(readme)

# Compact artboards keep body copy readable on narrow GitHub profiles.
import textwrap, re
def mobile(name, h, body, title):
    (A/(name+'-mobile.svg')).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="400" height="{h}" viewBox="0 0 400 {h}" role="img"><title>{escape(title)}</title><rect width="400" height="{h}" rx="6" fill="#000"/>'+body+'</svg>')
def paragraphs(name,label,blocks):
    b=text(24,40,label,12,G,400,1,True); y=84
    for s in blocks:
        for row in textwrap.wrap(s,32):
            b+=text(24,y,row,20,W); y+=29
        y+=16
    mobile(name,y+8,b,' '.join(blocks))
b=seal(43,45,19)+text(78,50,'INVRNT',13,G,400,3)
b+=text(24,113,'Juan Camilo',43,W,500,-1)
b+=text(24,151,'AI ENGINEER / PRODUCT BUILDER',12,G,400,0,True)
b+=line(24,178,376,178)+text(24,225,'Complex systems.',27,W)+text(24,262,'Simple experiences.',27,G)
b+=text(24,314,'Colombia / Remote',14,M)
mobile('hero',344,b,'Juan Camilo / invrnt. AI engineer and product builder. Complex systems. Simple experiences.')
paragraphs('about','01 / ABOUT',['I build AI products, from architecture to the experience people use.','Agent workflows, automation and serverless systems.','Studying Computer Engineering and Public Accounting in Colombia.'])
mobile('selected',78,text(24,47,'02 / SELECTED PRODUCTS',12,G,400,1,True),'Selected products')
for name,num,title,kicker,lines,stack,link in projects:
    b=text(24,40,num+' / '+kicker,11,G,400,0,True)+text(24,88,title,29,W,500,-.4); y=132
    for row in textwrap.wrap(' '.join(lines),33):
        b+=text(24,y,row,19,M);y+=28
    b+=line(24,y+1,376,y+1)+text(24,y+33,link,12,G,400,0,True)
    mobile(name,y+62,b,title+'. '+ ' '.join(lines))
paragraphs('approach','03 / HOW I WORK',['Architecture to delivery. I design, build and deploy complete products.','AI-assisted engineering. I orchestrate agents and review the systems they help build.','Domain knowledge. Accounting studies inform how I think about financial workflows.'])
paragraphs('toolkit','04 / WORKING TOOLKIT',['Python / FastAPI','TypeScript / React / Next.js','LangChain / LangGraph','Cloudflare / PostgreSQL / Docker'])
paragraphs('connect','05 / CONNECT',['Let’s build something useful.','Open to conversations with engineering teams and collaborators.','juancamilo.me'])
readme=re.sub(r'(<img src="assets/([a-z]+)\.svg"[^>]+/>)',lambda m: '<picture><source media="(max-width: 600px)" srcset="assets/'+m[2]+'-mobile.svg" />'+m[1]+'</picture>',readme)
(ROOT/'README.md').write_text(readme)
