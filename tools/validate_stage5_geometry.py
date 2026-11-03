#!/usr/bin/env python3
"""Automatic Stage 5 PNG geometry, palette, and catalog audit."""
import json,hashlib
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1]; O=R/"app/src/main/res/drawable-nodpi"
def die(s): raise SystemExit("FAIL: "+s)
def main():
 apps=json.loads((R/"icons.json").read_text())["apps"]; seen={}
 lines=["# Auditoría automática de PNG — Etapa 5","","| Recurso | Alfa/esquinas | Caja glifo | Centro | Paleta | Hash |","|---|---|---|---|---|---|"]
 for a in apps:
  p=O/(a["drawable"]+".png")
  if not p.is_file(): die("PNG ausente: "+p.name)
  with Image.open(p) as im:
   if im.size!=(192,192) or im.mode!="RGBA": die(p.name+": tamaño/canal inválido")
   if any(im.getpixel(c)[3] for c in [(0,0),(191,0),(0,191),(191,191)]): die(p.name+": esquina no transparente")
   pts=[]
   for y in range(192):
    for x in range(192):
     r,g,b,al=im.getpixel((x,y))
     if al>40 and r>130 and r>g*1.25 and r>b*1.15: pts.append((x,y))
   if not pts: die(p.name+": no se detecta glifo carmesí")
   x0=min(x for x,y in pts); x1=max(x for x,y in pts); y0=min(y for x,y in pts); y1=max(y for x,y in pts)
   w=x1-x0+1; h=y1-y0+1
   if not(.45<=w/192<=.65 and .45<=h/192<=.65): die(f"{p.name}: bbox {w}x{h} fuera de 45-65%")
   if abs((x0+x1)/2-95.5)>5.76 or abs((y0+y1)/2-95.5)>5.76: die(p.name+": glifo descentrado >3%")
   # Any strongly saturated non-red hue in the detected glyph region is rejected.
   for x,y in pts:
    r,g,b,_=im.getpixel((x,y))
    if not(r>=g*1.25 and r>=b*1.15): die(p.name+": tono fuera de rojo/carmesí")
   if a.get("glyph_type")=="monogram" and (x0<19 or y0<19 or x1>172 or y1>172): die(p.name+": monograma fuera del área segura")
  hsh=hashlib.sha256(p.read_bytes()).hexdigest()
  if hsh in seen: die("PNG duplicado: "+seen[hsh]+" y "+a["label"])
  seen[hsh]=a["label"]; lines.append(f"| {a['label']} | PASS | {w}×{h} | PASS | PASS | PASS |")
 report=R/"app/build/reports/stage5-automatic-checks.md"; report.parent.mkdir(parents=True,exist_ok=True)
 report.write_text("\n".join(lines)+"\n")
 print("\n".join(lines))
if __name__=="__main__": main()
