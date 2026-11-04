#!/usr/bin/env python3
"""Fail if Stage 5 assets, appfilter mappings, or selector lists drift."""
import json, re, xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/"icons.json").read_text(encoding="utf-8"))
apps=data["apps"]
assert len(apps)>=1, "icons.json must contain at least one entry"
names=[a["drawable"] for a in apps]
assert len(names)==len(set(names)), "Duplicate drawable names"
components=[a["package"]+"/"+a["activity"] for a in apps]
assert len(components)==len(set(components)), "Duplicate launcher components"
for a in apps:
    candidates=a.get("activity_candidates",[])
    candidate_names=[x["activity"] for x in candidates]
    assert len(candidate_names)==len(set(candidate_names)), f"Duplicate activity candidates: {a['label']}"
    for candidate in candidates:
        assert candidate.get("status") in {"verified","estimated"}, f"Invalid candidate status: {a['label']}"
for a in apps:
    assert a["glyph_type"] in {"brand","generic","monogram"}, a
    assert a["activity_status"] in {"verified","estimated"}, a
    p=ROOT/"app/src/main/res/drawable-nodpi"/(a["drawable"]+".png")
    assert p.is_file(), f"Missing generated PNG: {p}"
    assert not p.with_suffix(".xml").exists(), f"Duplicate vector drawable remains: {p.with_suffix('.xml')}"
    from PIL import Image
    with Image.open(p) as im:
        assert im.size==(192,192) and im.mode=="RGBA", f"Invalid PNG: {p}"
        assert im.getpixel((0,0))[3]==0, f"Nontransparent corner: {p}"
filter_root=ET.parse(ROOT/"app/src/main/res/xml/appfilter.xml").getroot()
for layer in ("iconback","iconmask","iconupon"):
    node=filter_root.find(layer)
    assert node is not None and node.find("item") is not None, f"Missing Nova fallback layer: {layer}"
    drawable=node.find("item").get("drawable")
    assert (ROOT/"app/src/main/res/drawable"/(drawable+".xml")).is_file(), f"Missing fallback drawable: {drawable}"
mapping={}
for item in filter_root.findall("item"):
    comp=item.get("component","")
    if comp in mapping: raise SystemExit("Duplicate appfilter component: "+comp)
    mapping[comp]=item.get("drawable")
for a,comp in zip(apps,components):
    key="ComponentInfo{"+comp+"}"
    assert mapping.get(key)==a["drawable"], f"appfilter mismatch for {a['label']}: {mapping.get(key)}"
    # Every legacy launcher component for this package must now point to the
    # Stage 5 PNG resource; old aliases may not keep a stale vector mapping.
    package_prefix="ComponentInfo{"+a["package"]+"/"
    package_rows=[(component,drawable) for component,drawable in mapping.items() if component.startswith(package_prefix)]
    assert package_rows, f"No appfilter mapping for catalog package: {a['label']}"
    for component,drawable in package_rows:
        assert drawable==a["drawable"], f"Legacy component {component} for {a['label']} still points to {drawable}, expected {a['drawable']}"
    for candidate in a.get("activity_candidates",[]):
        candidate_key="ComponentInfo{"+a["package"]+"/"+candidate["activity"]+"}"
        assert mapping.get(candidate_key)==a["drawable"], f"appfilter mismatch for candidate {a['label']}: {candidate_key}"
xml=ROOT/"app/src/main/res/xml/drawable.xml"
asset=ROOT/"app/src/main/assets/drawable.xml"
assert xml.read_bytes()==asset.read_bytes(), "assets/drawable.xml differs from res/xml/drawable.xml"
selector=ET.parse(xml).getroot()
items=selector.findall("icon")
assert len(items)==len(apps), f"Expected {len(apps)} selector entries, got {len(items)}"
assert [x.get("drawable") for x in items]==names, "Selector order/content mismatch"
assert len({x.get("drawable") for x in items})==len(apps), "Duplicate selector resources"
pending=(ROOT/"appfilter_pendientes.txt").read_text(encoding="utf-8")
for a in apps:
    if a["activity_status"]=="estimated":
        assert a["label"] in pending, f"Missing pending activity: {a['label']}"
print(f"PASS: {len(apps)} PNGs, unique resources, Nova appfilter, selector copy, and activity ledger.")
