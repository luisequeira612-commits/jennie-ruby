#!/usr/bin/env python3
"""Render Stage 5 catalog assets and an unbounded, labeled contact sheet."""
from __future__ import annotations
import importlib.util, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"icons.json"; STAGE1=ROOT/"tools/render_ruby_stage1_icons.py"
SOURCE_DIR=ROOT/"tools/ruby_icon_sources"; OUT=ROOT/"app/src/main/res/drawable-nodpi"
REPORT=ROOT/"app/build/reports"

def load_renderer():
    spec=importlib.util.spec_from_file_location("ruby_stage1_renderer",STAGE1)
    if spec is None or spec.loader is None: raise RuntimeError("Cannot load protected Stage 1 renderer")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def font(size):
    candidates=[ROOT/"app/src/main/res/font/playfair_display.ttf",Path("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf")]
    for p in candidates:
        if p.is_file(): return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()

def fit_text(draw,text,font_path,box,max_width,max_height):
    lo,hi=8,160; best=None
    while lo<=hi:
        mid=(lo+hi)//2; f=ImageFont.truetype(str(font_path),mid) if font_path.is_file() else font(mid)
        b=draw.textbbox((0,0),text,font=f)
        if b[2]-b[0]<=max_width and b[3]-b[1]<=max_height: best=(f,b); lo=mid+1
        else: hi=mid-1
    if best is None: raise RuntimeError(f"Monogram {text!r} cannot fit safe area at readable size")
    f,b=best; return f,b

def main():
    data=json.loads(CATALOG.read_text(encoding="utf-8")); apps=data["apps"]
    if not apps: raise RuntimeError("icons.json has no apps")
    names=[a["drawable"] for a in apps]
    if len(names)!=len(set(names)): raise RuntimeError("Duplicate drawable names in icons.json")
    subprocess.run(["node",str(ROOT/"tools/extract_stage5_simple_icons.mjs"),str(CATALOG),str(SOURCE_DIR)],check=True,cwd=ROOT)
    renderer=load_renderer(); OUT.mkdir(parents=True,exist_ok=True)
    for app in apps:
        key=app["drawable"].removeprefix("ruby_"); source=SOURCE_DIR/f"ruby_{key}.xml"
        backup=source.read_bytes() if source.exists() else None
        try:
            renderer.render(key)
            if app["glyph_type"]=="monogram":
                text=app.get("glyph") or app.get("monogram")
                if not isinstance(text,str) or not text.strip(): raise RuntimeError(f"Missing glyph/monogram text in icons.json: {app['label']}")
                text=text.strip()
                target=OUT/(app["drawable"]+".png")
                with Image.open(target) as src: base=src.convert("RGBA")
                # Replace only the glyph field; preserve the Ruby surface and border.
                ImageDraw.Draw(base).rectangle((42,42,150,150),fill="#080304")
                mask=Image.new("L",(192,192),0); d=ImageDraw.Draw(mask)
                f,b=fit_text(d,text,ROOT/"app/src/main/res/font/playfair_display.ttf",(42,42,150,150),96,96)
                x=(192-(b[2]-b[0]))/2-b[0]; y=(192-(b[3]-b[1]))/2-b[1]
                d.text((x,y),text,font=f,fill=255)
                glow=mask.filter(ImageFilter.GaussianBlur(2.0))
                gl=Image.new("RGBA",(192,192),(224,51,75,0)); gl.putalpha(glow.point(lambda v:round(v*.14))); base.alpha_composite(gl)
                glyph=renderer.vertical_gradient("#E0334B","#8E0B20"); glyph.putalpha(mask); base.alpha_composite(glyph); base.save(target,optimize=True)
        finally:
            if backup is None: source.unlink(missing_ok=True)
            else: source.write_bytes(backup)
    for name in names:
        (OUT/(name+".xml")).unlink(missing_ok=True)
    selector=['<?xml version="1.0" encoding="utf-8"?>','<icons>']
    for a in apps: selector.append(f'    <icon name="{a["label"]}" drawable="{a["drawable"]}" glyph-type="{a["glyph_type"]}" />')
    selector.append('</icons>'); xml_text="\n".join(selector)+"\n"
    for p in (ROOT/"app/src/main/res/xml/drawable.xml",ROOT/"app/src/main/assets/drawable.xml"):
        p.parent.mkdir(parents=True,exist_ok=True); p.write_text(xml_text,encoding="utf-8")
    REPORT.mkdir(parents=True,exist_ok=True)
    lines=["# Actividades de launcher — catálogo Etapa 5","","| Aplicación | Paquete | Activity | Estado |","|---|---|---|---|"]
    pending=["ACTIVIDADES PENDIENTES — estimadas; confirmar manifiesto instalado antes de verificar",""]
    for a in apps:
        status=a.get("activity_status","estimated")
        if status not in {"verified","estimated"}: raise RuntimeError(f"Invalid activity_status: {a['label']}")
        lines.append(f'| {a["label"]} | {a["package"]} | {a["activity"]} | {status} |')
        if status=="estimated": pending.append(f'{a["label"]}: {a["package"]}/{a["activity"]} — estimada')
    (ROOT/"docs/ACTIVITIES.md").write_text("\n".join(lines)+"\n",encoding="utf-8")\n    (REPORT/"stage5-activities.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (ROOT/"appfilter_pendientes.txt").write_text("\n".join(pending)+"\n",encoding="utf-8")
    (ROOT/"docs/LOTES.md").write_text("# Lotes de iconos — Etapa 5\n\nEl catálogo maestro es `icons.json`. Cada activity debe declararse `verified` solo tras contrastar el manifiesto instalado; de lo contrario queda `estimated`.\n\nLa hoja de contacto se genera desde los PNG presentes y el catálogo, no desde una lista fija.\n",encoding="utf-8")
    stage1=["ruby_youtube","ruby_spotify","ruby_tiktok","ruby_instagram","ruby_whatsapp","ruby_google","ruby_google_play_store","ruby_configuracion","ruby_galeria","ruby_camara"]
    dock=["ruby_dock_telefono_art","ruby_dock_contactos_art","ruby_dock_mensajes_art","ruby_dock_chrome_art","ruby_dock_cajon_apps_art"]
    labels=["YouTube","Spotify","TikTok","Instagram","WhatsApp","Google","Play Store","Ajustes","Galería","Cámara","Teléfono","Contactos","Mensajes","Chrome","Cajón apps"]+[a["label"] for a in apps]
    types=["Etapa 1"]*10+["Dock"]*5+[a["glyph_type"] for a in apps]
    all_names=stage1+dock+names
    cell_w,cell_h,cols=400,450,5; rows=(len(all_names)+cols-1)//cols
    sheet=Image.new("RGB",(cols*cell_w,rows*cell_h+100),"#10070A"); draw=ImageDraw.Draw(sheet)
    draw.text((cols*cell_w//2,35),f"ICONOS GENERADOS POR BUILD — {len(all_names)} recursos; no es captura del teléfono",font=font(22),fill="#F3E6E6",anchor="mm")
    label_font=font(20); type_font=font(18)
    for i,(name,label,kind) in enumerate(zip(all_names,labels,types)):
        p=OUT/(name+".png")
        if not p.is_file(): raise RuntimeError(f"Missing contact-sheet PNG: {p}")
        with Image.open(p) as im: icon=im.convert("RGBA").resize((300,300),Image.Resampling.LANCZOS)
        x=(i%cols)*cell_w+50; y=(i//cols)*cell_h+65
        sheet.paste(icon,(x,y),icon)
        draw.text((x+150,y+320),label,font=label_font,fill="#F3E6E6",anchor="mm")
        draw.text((x+150,y+352),kind,font=type_font,fill="#D58A98",anchor="mm")
    sheet.save(REPORT/"jennie-ruby-stage5-contact-sheet.png",optimize=True)
    print(f"PASS: generated {len(apps)} Stage 5 icons and {len(all_names)}-asset contact sheet")

if __name__=="__main__": main()
