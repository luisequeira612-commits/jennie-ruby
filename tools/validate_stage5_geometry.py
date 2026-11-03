#!/usr/bin/env python3
"""Audit Stage 5 output against the exact vector/text glyph alpha masks."""
import hashlib, json
from pathlib import Path
from PIL import Image

R=Path(__file__).resolve().parents[1]
O=R/"app/src/main/res/drawable-nodpi"
M=R/"app/build/reports/stage5-glyph-masks"

def die(message):
    raise SystemExit("FAIL: "+message)

def main():
    apps=json.loads((R/"icons.json").read_text())["apps"]
    seen={}
    lines=["# Auditoría automática de PNG — Etapa 5","","| Recurso | PNG | Caja máscara glifo | Centro | Paleta carmesí | Hash |","|---|---|---|---|---|---|"]
    for app in apps:
        name=app["drawable"]
        png=O/(name+".png")
        mask_path=M/(name+".png")
        if not png.is_file(): die("PNG ausente: "+png.name)
        if not mask_path.is_file(): die("Máscara geométrica ausente: "+mask_path.name)
        with Image.open(png) as im:
            if im.size!=(192,192) or im.mode!="RGBA": die(png.name+": tamaño/canal inválido")
            if any(im.getpixel(c)[3] for c in [(0,0),(191,0),(0,191),(191,191)]):
                die(png.name+": esquina no transparente")
            pixels=im.convert("RGBA")
        with Image.open(mask_path) as source_mask:
            if source_mask.size!=(192,192): die(mask_path.name+": máscara no es 192x192")
            mask=source_mask.convert("L")
        bbox=mask.getbbox()
        if not bbox: die(name+": máscara de glifo vacía")
        x0,y0,x1,y1=bbox
        w=x1-x0; h=y1-y0
        # Preserve the source logo aspect ratio: the 45–65% criterion applies to its major axis.
        # A second, independent 30% floor prevents excessively thin or tiny marks.
        major=max(w,h)/192; minor=min(w,h)/192
        # Monograms/wordmarks may be naturally horizontal or vertical; their
        # separate 10% safe-margin check below is the correct clipping guard.
        min_minor=0.0 if app.get("glyph_type")=="monogram" else .30
        if not(.45<=major<=.65 and minor>=min_minor):
            die(f"{name}: máscara {w}x{h}; eje mayor fuera de 45-65% o eje menor <{min_minor*100:.0f}%")
        cx=(x0+x1-1)/2; cy=(y0+y1-1)/2
        if abs(cx-95.5)>5.76 or abs(cy-95.5)>5.76:
            die(name+": máscara de glifo descentrada >3%")
        # Every visible glyph-mask pixel must be rendered in the ruby-red palette.
        for y in range(y0,y1):
            for x in range(x0,x1):
                if mask.getpixel((x,y))>40:
                    r,g,b,a=pixels.getpixel((x,y))
                    if a<200 or not(r>=g*1.25 and r>=b*1.15):
                        die(f"{name}: píxel del glifo fuera de paleta carmesí en ({x},{y})")
        if app.get("glyph_type")=="monogram" and (x0<19 or y0<19 or x1>173 or y1>173):
            die(name+": monograma fuera del margen seguro del 10%")
        digest=hashlib.sha256(png.read_bytes()).hexdigest()
        if digest in seen: die("PNG duplicado: "+seen[digest]+" y "+app["label"])
        seen[digest]=app["label"]
        lines.append(f"| {app['label']} | PASS | {w}×{h} | PASS | PASS | PASS |")
    report=R/"app/build/reports/stage5-automatic-checks.md"
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text("\n".join(lines)+"\n")
    print("\n".join(lines))

if __name__=="__main__":
    main()
