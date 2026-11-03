#!/usr/bin/env python3
"""Render the first Stage 5 icon batch through the protected Stage 1 renderer."""
from __future__ import annotations
import importlib.util, json, shutil, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"icons.json"
STAGE1=ROOT/"tools/render_ruby_stage1_icons.py"
SOURCE_DIR=ROOT/"tools/ruby_icon_sources"
OUT=ROOT/"app/src/main/res/drawable-nodpi"
REPORT=ROOT/"app/build/reports"
ANDROID="{http://schemas.android.com/apk/res/android}"

def load_renderer():
    spec=importlib.util.spec_from_file_location("ruby_stage1_renderer",STAGE1)
    if spec is None or spec.loader is None: raise RuntimeError("Cannot load protected Stage 1 renderer")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

def main():
    data=json.loads(CATALOG.read_text(encoding="utf-8"))
    apps=data["apps"]
    if len(apps)!=20: raise RuntimeError(f"Expected 20 icons, found {len(apps)}")
    names=[a["drawable"] for a in apps]
    if len(set(names))!=len(names): raise RuntimeError("Duplicate drawable names in icons.json")
    subprocess.run(["node",str(ROOT/"tools/extract_stage5_simple_icons.mjs"),str(CATALOG),str(SOURCE_DIR)],check=True,cwd=ROOT)
    renderer=load_renderer()
    OUT.mkdir(parents=True,exist_ok=True); SOURCE_DIR.mkdir(parents=True,exist_ok=True)
    for app in apps:
        source=SOURCE_DIR/f"ruby_{app['drawable'][5:]}.xml"
        backup=source.read_bytes() if source.exists() else None
        try:
            # Extractor writes a vector with six unused legacy slots followed by the brand silhouette.
            renderer.render(app["drawable"][5:])
            if app["glyph_type"]=="monogram":
                font_path=ROOT/"app/src/main/res/font/playfair_display.ttf"
                if not font_path.is_file(): raise RuntimeError("Playfair Display font missing for monogram fallback")
                target=OUT/(app["drawable"]+".png")
                with Image.open(target) as source_image: base=source_image.convert("RGBA")
                # The centered field is nearly the base surface color; replace the placeholder glyph with real Playfair lettering.
                ImageDraw.Draw(base).rectangle((48,48,144,144),fill="#080304")
                mask=Image.new("L",(192,192),0)
                font=ImageFont.truetype(str(font_path),64)
                box=font.getbbox("AI")
                tx=(192-(box[2]-box[0]))/2-box[0]
                ty=(192-(box[3]-box[1]))/2-box[1]
                ImageDraw.Draw(mask).text((tx,ty),"AI",font=font,fill=255)
                glow=mask.filter(ImageFilter.GaussianBlur(radius=2.2))
                glow_layer=Image.new("RGBA",(192,192),(224,51,75,0))
                glow_layer.putalpha(glow.point(lambda value: round(value*0.16)))
                base.alpha_composite(glow_layer)
                glyph=renderer.vertical_gradient("#E0334B","#8E0B20")
                glyph.putalpha(mask); base.alpha_composite(glyph)
                base.save(target,format="PNG",optimize=True)
        finally:
            if backup is None: source.unlink(missing_ok=True)
            else: source.write_bytes(backup)
    # Replace the old generic vector resources with the newly generated PNGs.
    # Keeping both formats under the same Android drawable name causes a resource-merger collision.
    for name in names:
        obsolete=OUT/(name+".xml")
        if obsolete.exists(): obsolete.unlink()
    # Single-source Nova drawable list and identical assets copy.
    selector=['<?xml version="1.0" encoding="utf-8"?>','<icons>']
    for a in apps:
        selector.append(f'    <icon name="{a["label"]}" drawable="{a["drawable"]}" glyph-type="{a["glyph_type"]}" />')
    selector.append('</icons>')
    selector_text="\n".join(selector)+"\n"
    xml_path=ROOT/"app/src/main/res/xml/drawable.xml"
    xml_path.parent.mkdir(parents=True,exist_ok=True); xml_path.write_text(selector_text,encoding="utf-8")
    assets=ROOT/"app/src/main/assets"; assets.mkdir(parents=True,exist_ok=True)
    (assets/"drawable.xml").write_text(selector_text,encoding="utf-8")
    # Activity confidence ledger: none are certified against installed manifests yet.
    pending=["ACTIVIDADES PENDIENTES — estimadas; confirmar en dispositivo antes de marcarlas verificadas",""]
    for a in apps:
        if a.get("activity_status")!="verified":
            pending.append(f'{a["label"]}: {a["package"]}/{a["activity"]} — estimada')
    (ROOT/"appfilter_pendientes.txt").write_text("\n".join(pending)+"\n",encoding="utf-8")
    # Glyph-type table for review.
    lines=["# Tipos de glifo — Etapa 5, lote 1","","| Aplicación | Tipo | Fuente | Estado de actividad |","|---|---|---|---|"]
    for a in apps: lines.append(f'| {a["label"]} | {a["glyph_type"]} | {("Simple Icons: "+a["glyph"]) if a["glyph_type"]=="brand" else ("Material-style generic path" if a["glyph_type"]=="generic" else "Playfair Display serif monogram")} | {a["activity_status"]} |')
    (REPORT/"stage5-batch1-glyph-types.md").parent.mkdir(parents=True,exist_ok=True)
    (REPORT/"stage5-batch1-glyph-types.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    # Actual PNG contact sheet: ten Stage 1 + five dock + twenty new resources.
    stage1=["ruby_youtube","ruby_spotify","ruby_tiktok","ruby_instagram","ruby_whatsapp","ruby_google","ruby_google_play_store","ruby_configuracion","ruby_galeria","ruby_camara"]
    dock=["ruby_dock_telefono_art","ruby_dock_contactos_art","ruby_dock_mensajes_art","ruby_dock_chrome_art","ruby_dock_cajon_apps_art"]
    labels=["YouTube","Spotify","TikTok","Instagram","WhatsApp","Google","Play Store","Ajustes","Galería","Cámara","Teléfono","Contactos","Mensajes","Chrome","Cajón apps"]+[a["label"] for a in apps]
    all_names=stage1+dock+names
    if len(all_names)!=35: raise RuntimeError("35-icon contact sheet count mismatch")
    sheet=Image.new("RGB",(2000,3350),"#10070A"); draw=ImageDraw.Draw(sheet)
    draw.text((1000,38),"SIMULACIÓN DE ICONOS — PNG generados por build; no es captura del teléfono",fill="#F3E6E6",anchor="mm")
    for i,(name,label) in enumerate(zip(all_names,labels)):
        path=OUT/f"{name}.png"
        if not path.is_file(): raise RuntimeError(f"Missing contact-sheet asset: {path}")
        with Image.open(path) as im: icon=im.convert("RGBA").resize((300,300),Image.Resampling.LANCZOS)
        x=(i%5)*400+50; y=(i//5)*450+100
        sheet.paste(icon,(x,y),icon); draw.text((x+150,y+325),label,fill="#F3E6E6",anchor="mm")
    REPORT.mkdir(parents=True,exist_ok=True)
    sheet.save(REPORT/"jennie-ruby-stage5-batch1-35-icons.png",optimize=True)
    print("PASS: generated 20 Stage 5 icons through protected Stage 1 render()")
    print("Contact sheet: app/build/reports/jennie-ruby-stage5-batch1-35-icons.png")
if __name__=="__main__": main()
