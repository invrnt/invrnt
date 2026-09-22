#!/usr/bin/env python3
"""Check the shipped assets, README references, SVG isolation and STL integrity."""

from collections import Counter
from html.parser import HTMLParser
from math import isfinite
from pathlib import Path
import re
import struct
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SVG="{http://www.w3.org/2000/svg}"
errors=[]


def check(condition,message):
    if not condition:
        errors.append(message)


class Readme(HTMLParser):
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        check(tag not in {"script","style","iframe","object","svg"},f"README contains {tag}")
        if tag=="img":
            check(bool(attrs.get("alt")),"README image missing alt")
        for key in ["src","srcset","href"]:
            value=attrs.get(key,"")
            if value.startswith("assets/"):
                check((ROOT/value).is_file(),f"Missing README target: {value}")


files=sorted((ROOT/"assets").glob("*.svg"))
check(len(files)==16,f"Expected 16 art-directed variants, found {len(files)}")
for file in files:
    raw=file.read_text()
    doc=ET.fromstring(raw)
    check(doc.find(SVG+"title") is not None,f"{file.name}: missing title")
    check(doc.find(SVG+"desc") is not None,f"{file.name}: missing description")
    check("prefers-reduced-motion:reduce" in raw,f"{file.name}: no motion preference")
    check("prefers-color-scheme:dark" in raw,f"{file.name}: no adaptive palette")
    check(file.stat().st_size<100_000,f"{file.name}: oversized asset")
    ids=[n.attrib["id"] for n in doc.iter() if "id" in n.attrib]
    check(len(ids)==len(set(ids)),f"{file.name}: duplicate IDs")
    for ref in re.findall(r"url\(#([^\)]+)\)",raw):
        check(ref in ids,f"{file.name}: unresolved reference {ref}")
    for element in doc.iter():
        tag=element.tag.replace(SVG,"")
        check(tag not in {"script","foreignObject","image","a","iframe","animate","animateTransform"},f"{file.name}: unexpected element {tag}")
        for key,value in element.attrib.items():
            check(not key.startswith("on"),f"{file.name}: event handler")
            check("href" not in key,f"{file.name}: external or interactive dependency")
    check("url(http" not in raw,f"{file.name}: network resource")

Readme().feed((ROOT/"README.md").read_text())

# Weld vertices only for topology validation; the STL itself keeps full precision.
model=(ROOT/"assets/control.stl").read_bytes()
count=struct.unpack_from('<I',model,80)[0]
check(len(model)==84+count*50,"STL size does not match its facet count")
edges=Counter()
for index in range(count):
    facet=struct.unpack_from('<12fH',model,84+index*50)
    check(all(isfinite(x) for x in facet[:12]),"Non-finite STL coordinate")
    vertices=[tuple(round(v,4) for v in facet[i:i+3]) for i in (3,6,9)]
    for a,b in zip(vertices,vertices[1:]+vertices[:1]):
        edges[tuple(sorted((a,b)))]+=1
check(all(n==2 for n in edges.values()),"STL is not closed after vertex welding")

if errors:
    raise SystemExit("\n".join(errors))
total=sum(p.stat().st_size for p in files)
print(f"PASS: {len(files)} SVGs, README references, isolated resources, reduced motion, and {count} closed STL facets.")
print(f"SVG variants: {total:,} bytes total. Only one variant per scene is loaded.")
