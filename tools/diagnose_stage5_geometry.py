#!/usr/bin/env python3
"""Collect per-icon Stage 5 geometry diagnostics without stopping at first failure."""
import hashlib, json
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]
O=R/"app/src/main/res/drawable-nodpi"
M=R/"app/build/reports/stage5-glyph-masks"
rows=[]; seen={}
for app in json.loads((R/"icons.json").read_text(encoding="utf-8"))["apps"]:
    name=app["drawable"]; png=O/(name+".png"); mask_path=M/(name+".png"); errors=[]
    if not png.is_file() or not mask_path.is_file():
        rows.append((app["label"],"MISSING","—","—","—","—", "PNG or mask missing")); continue
    with Image.open(png) as im:
        if im.size!=(192,192) or im.mode!="RGBA": errors.append("PNG size/mode")
        pixels=im.convert("RGBA")
        if any(pixels.getpixel(c)[3] for c in [(0,0),(191,0),(0,191),(191,191)]): errors.append("opaque corner")
    with Image.open(mask_path) as im: mask=im.convert("L")
    bbox=mask.getbbox()
    if not bbox:
        rows.append((app["label"],"FAIL","empty","—","—","—","empty glyph mask")); continue
    x0,y0,x1,y1=bbox; w=x1-x0; h=y1-y0
    major=max(w,h)/192; minor=min(w,h)/192
    cx=(x0+x1-1)/2; cy=(y0+y1-1)/2
    if not(.45<=major<=.65): errors.append(f"major {major:.3f}")
    min_minor=0 if app.get("glyph_type")=="monogram" else .30
    if minor<min_minor: errors.append(f"minor {minor:.3f}")
    if abs(cx-95.5)>5.76 or abs(cy-95.5)>5.76: errors.append(f"center {cx:.1f},{cy:.1f}")
    bad=0
    for y in range(y0,y1):
        for x in range(x0,x1):
            if mask.getpixel((x,y))>40:
                r,g,b,a=pixels.getpixel((x,y))
                if a<200 or not(r>=g*1.25 and r>=b*1.15): bad+=1
    if bad: errors.append(f"{bad} non-crimson pixels")
    if app.get("glyph_type")=="monogram" and (x0<19 or y0<19 or x1>173 or y1>173): errors.append("monogram safe margin")
    digest=hashlib.sha256(png.read_bytes()).hexdigest()
    if digest in seen: errors.append("duplicate PNG hash with "+seen[digest])
    seen[digest]=app["label"]
    rows.append((app["label"],"FAIL" if errors else "PASS",f"{w}x{h}",f"{major:.3f}/{minor:.3f}",f"{cx:.1f},{cy:.1f}",digest[:12],"; ".join(errors) or "—"))
lines=["# Stage 5 per-icon diagnostic","", "| App | Result | Mask px | Major/minor | Center | SHA-256 | Details |","|---|---|---|---|---|---|---|"]
lines += [f"| {a} | {s} | {box} | {ratio} | {center} | {sha} | {detail} |" for a,s,box,ratio,center,sha,detail in rows]
out=R/"app/build/reports/stage5-diagnostics.md"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text("\n".join(lines)+"\n",encoding="utf-8")
print("\n".join(lines))
fails=[r for r in rows if r[1]!="PASS"]
print(f"DIAGNOSTIC SUMMARY: {len(rows)-len(fails)}/{len(rows)} pass; {len(fails)} fail")
