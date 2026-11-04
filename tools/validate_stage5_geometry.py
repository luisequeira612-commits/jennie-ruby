#!/usr/bin/env python3
"""Strict Stage 5 glyph audit: geometry, type provenance, solid marks and perceptual uniqueness."""
import hashlib, json
from pathlib import Path
from collections import deque
import numpy as np
from PIL import Image
R=Path(__file__).resolve().parents[1]; O=R/"app/src/main/res/drawable-nodpi"
M=R/"app/build/reports/stage5-glyph-masks"; SOURCES=R/"tools/ruby_icon_sources/stage5-glyph-sources.json"
def die(s): raise SystemExit("FAIL: "+s)
def holes(binary):
    h,w=binary.shape; seen=np.zeros((h,w),bool); count=0
    for y in range(h):
      for x in range(w):
        if binary[y,x] or seen[y,x]: continue
        q=deque([(y,x)]); seen[y,x]=True; edge=False
        while q:
          cy,cx=q.popleft()
          if cy in (0,h-1) or cx in (0,w-1): edge=True
          for ny,nx in ((cy-1,cx),(cy+1,cx),(cy,cx-1),(cy,cx+1)):
            if 0<=ny<h and 0<=nx<w and not binary[ny,nx] and not seen[ny,nx]:
              seen[ny,nx]=True; q.append((ny,nx))
        if not edge: count+=1
    return count
def dhash(mask):
    a=np.asarray(mask.resize((17,16),Image.Resampling.LANCZOS),dtype=np.uint8)
    bits=(a[:,1:]>=a[:,:-1]).flatten()
    return sum((int(v)<<i) for i,v in enumerate(bits))
def main():
    apps=json.loads((R/"icons.json").read_text())["apps"]
    sources=json.loads(SOURCES.read_text())
    seen_hash={}; hashes=[]; rows=[]
    for a in apps:
      name=a["drawable"]; png=O/(name+".png"); mp=M/(name+".png")
      if not png.is_file() or not mp.is_file(): die("PNG/máscara ausente: "+name)
      src=sources.get(name)
      if not src: die("Sin procedencia de glifo: "+name)
      if src["resolved_type"]=="brand" and (src["source"]!="simple-icons" or not src.get("slug")):
        die("Etiqueta brand sin slug Simple Icons real: "+a["label"])
      if src["resolved_type"] not in ("brand","generic","monogram"): die("Tipo real inválido: "+name)
      with Image.open(png) as im:
        if im.size!=(192,192) or im.mode!="RGBA": die("PNG inválido: "+name)
        pixels=im.convert("RGBA")
        if any(pixels.getpixel(c)[3] for c in ((0,0),(191,0),(0,191),(191,191))): die("Esquina opaca: "+name)
      with Image.open(mp) as m: mask=m.convert("L")
      arr=np.asarray(mask,dtype=np.uint8); bbox=mask.getbbox()
      if not bbox: die("Glifo vacío: "+name)
      x0,y0,x1,y1=bbox; w=x1-x0; h=y1-y0; major=max(w,h)/192; minor=min(w,h)/192
      if not(.45<=major<=.65 and (src["resolved_type"]=="monogram" or minor>=.30)): die(f"{name}: geometría {w}x{h} fuera de rango")
      cx=(x0+x1-1)/2; cy=(y0+y1-1)/2
      if abs(cx-95.5)>5.76 or abs(cy-95.5)>5.76: die("Glifo descentrado: "+name)
      crop=arr[y0:y1,x0:x1]>40; occupancy=float(crop.mean()); variance=float(crop.astype(np.float32).var()); hole_count=holes(crop)
      if occupancy>.85 and (variance<.02 or hole_count<2): die(f"Glifo macizo sin detalle interior: {name} ocupación={occupancy:.3f}, var={variance:.4f}, huecos={hole_count}")
      if src["resolved_type"]=="monogram" and (x0<19 or y0<19 or x1>173 or y1>173): die("Monograma fuera de área segura: "+name)
      for y in range(y0,y1):
       for x in range(x0,x1):
        if arr[y,x]>40:
         r,g,b,alpha=pixels.getpixel((x,y))
         if alpha<200 or not(r>=g*1.25 and r>=b*1.15): die(f"Paleta carmesí inválida: {name} ({x},{y})")
      digest=hashlib.sha256(png.read_bytes()).hexdigest()
      if digest in seen_hash: die("PNG idéntico: "+seen_hash[digest]+" y "+a["label"])
      seen_hash[digest]=a["label"]; hashes.append((a["label"],dhash(mask)))
      rows.append(f"| {a['label']} | {src['resolved_type']} | PASS | {w}×{h} | {hole_count} | PASS |")
    for i,(label,hv) in enumerate(hashes):
      for other,ov in hashes[i+1:]:
        distance=(hv^ov).bit_count()
        if distance<10: die(f"Parecido perceptual <10/256: {label} vs {other} = {distance}")
    report=R/"app/build/reports/stage5-automatic-checks.md"; report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text("# Auditoría automática — Etapa 5\n\n| App | Tipo real | PNG | Caja | Huecos | dHash |\n|---|---|---|---|---:|---|\n"+"\n".join(rows)+"\n")
    print(f"PASS: {len(apps)} iconos; procedencia real; glifos macizos; dHash 16×16 con distancia mínima 10.")
if __name__=="__main__": main()
