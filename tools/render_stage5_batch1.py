#!/usr/bin/env python3
"""Render Stage 5 catalog assets and an unbounded, labeled contact sheet."""
from __future__ import annotations
import importlib.util, json, subprocess, xml.etree.ElementTree as ET
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT=Path(__file__).resolve().parents[1]
CATALOG=ROOT/"icons.json"; STAGE1=ROOT/"tools/render_ruby_stage1_icons.py"
SOURCE_DIR=ROOT/"tools/ruby_icon_sources"; OUT=ROOT/"app/src/main/res/drawable-nodpi"
REPORT=ROOT/"app/build/reports"
MASK_DIR=REPORT/"stage5-glyph-masks"

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

def normalize_small_glyph(target, mask, renderer):
    """Uniformly enlarge undersized vector marks without distorting their aspect ratio."""
    bbox=mask.getbbox()
    if not bbox: raise RuntimeError("Empty glyph mask")
    x0,y0,x1,y1=bbox; w=x1-x0; h=y1-y0
    major=max(w,h)/192; minor=min(w,h)/192
    cx=(x0+x1-1)/2; cy=(y0+y1-1)/2
    centered=abs(cx-95.5)<=5.76 and abs(cy-95.5)<=5.76
    if .45<=major<=.65 and minor>=.30 and centered:
        return mask
    crop=mask.crop(bbox)
    scale=124/max(w,h)
    nw=max(1,round(w*scale)); nh=max(1,round(h*scale))
    resized=crop.resize((nw,nh),Image.Resampling.LANCZOS)
    normalized=Image.new("L",(192,192),0)
    nx=(192-nw)//2; ny=(192-nh)//2
    normalized.paste(resized,(nx,ny))
    # The source mark was too small: replace only its central glyph field,
    # keeping the original ruby tile, border, shadow and glass treatment intact.
    with Image.open(target) as src:
        base=src.convert("RGBA")
    ImageDraw.Draw(base).rectangle((42,42,150,150),fill="#080304")
    glow=normalized.filter(ImageFilter.GaussianBlur(2.0))
    gl=Image.new("RGBA",(192,192),(224,51,75,0))
    gl.putalpha(glow.point(lambda value:round(value*.14)))
    base.alpha_composite(gl)
    glyph=renderer.vertical_gradient("#E0334B","#8E0B20")
    glyph.putalpha(normalized)
    base.alpha_composite(glyph)
    base.save(target,optimize=True)
    return normalized

def main():
    data=json.loads(CATALOG.read_text(encoding="utf-8")); apps=data["apps"]
    if not apps: raise RuntimeError("icons.json has no apps")
    names=[a["drawable"] for a in apps]
    if len(names)!=len(set(names)): raise RuntimeError("Duplicate drawable names in icons.json")
    subprocess.run(["node",str(ROOT/"tools/extract_stage5_simple_icons.mjs"),str(CATALOG),str(SOURCE_DIR)],check=True,cwd=ROOT)
    renderer=load_renderer(); OUT.mkdir(parents=True,exist_ok=True)
    sources=json.loads((SOURCE_DIR/"stage5-glyph-sources.json").read_text(encoding="utf-8"))
    MASK_DIR.mkdir(parents=True,exist_ok=True)
    for stale in MASK_DIR.glob("*.png"): stale.unlink()
    for app in apps:
        key=app["drawable"].removeprefix("ruby_"); source=SOURCE_DIR/f"ruby_{key}.xml"
        backup=source.read_bytes() if source.exists() else None
        try:
            renderer.render(key)
            root=ET.parse(source).getroot()
            view_w=float(root.get("{http://schemas.android.com/apk/res/android}viewportWidth","108"))
            view_h=float(root.get("{http://schemas.android.com/apk/res/android}viewportHeight","108"))
            resolved_type=sources[app["drawable"]]["resolved_type"]
            if resolved_type=="monogram":
                text=app.get("monogram") or app.get("glyph")
                if not isinstance(text,str) or not text.strip(): raise RuntimeError(f"Missing glyph/monogram text in icons.json: {app['label']}")
                text=text.strip()
                target=OUT/(app["drawable"]+".png")
                with Image.open(target) as src: base=src.convert("RGBA")
                # Replace only the glyph field; preserve the Ruby surface and border.
                ImageDraw.Draw(base).rectangle((42,42,150,150),fill="#080304")
                mask=Image.new("L",(192,192),0); d=ImageDraw.Draw(mask)
                f,b=fit_text(d,text,ROOT/"app/src/main/res/font/playfair_display.ttf",(42,42,150,150),116,116)
                x=(192-(b[2]-b[0]))/2-b[0]; y=(192-(b[3]-b[1]))/2-b[1]
                d.text((x,y),text,font=f,fill=255)
                glow=mask.filter(ImageFilter.GaussianBlur(2.0))
                gl=Image.new("RGBA",(192,192),(224,51,75,0)); gl.putalpha(glow.point(lambda v:round(v*.14))); base.alpha_composite(gl)
                glyph=renderer.vertical_gradient("#E0334B","#8E0B20"); glyph.putalpha(mask); base.alpha_composite(glyph); base.save(target,optimize=True)
            else:
                mask=renderer.make_glyph_mask(root.findall("path"),view_w,view_h,key)
                mask=normalize_small_glyph(OUT/(app["drawable"]+".png"),mask,renderer)
            mask.save(MASK_DIR/(app["drawable"]+".png"))
        finally:
            if backup is None: source.unlink(missing_ok=True)
            else: source.write_bytes(backup)
    for name in names:
        (OUT/(name+".xml")).unlink(missing_ok=True)
    selector=['<?xml version="1.0" encoding="utf-8"?>','<icons>']
    for a in apps: selector.append(f'    <icon name="{a["label"]}" drawable="{a["drawable"]}" glyph-type="{sources[a["drawable"]]["resolved_type"]}" />')
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
        for candidate in a.get("activity_candidates",[]):
            candidate_status=candidate.get("status","estimated")
            if candidate_status not in {"verified","estimated"}: raise RuntimeError(f"Invalid candidate activity_status: {a['label']}/{candidate.get('activity')}")
            activity=candidate["activity"]
            if activity==a["activity"]:
                continue
            lines.append(f'| {a["label"]} (candidata) | {a["package"]} | {activity} | {candidate_status} |')
            if candidate_status=="estimated": pending.append(f'{a["label"]}: {a["package"]}/{activity} — candidata estimada')
    (ROOT/"docs/ACTIVITIES.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (REPORT/"stage5-activities.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    (ROOT/"appfilter_pendientes.txt").write_text("\n".join(pending)+"\n",encoding="utf-8")
    batch1=["Maps","Gmail","Drive","Photos","Calendar","YouTube Music","Facebook","Messenger","Telegram","Snapchat","X","Pinterest","Reddit","Netflix","Disney+","HBO Max","Crunchyroll","Twitch","ChatGPT","Claude"]
    batch2=["Aniyomi","Mihon","Brave","CapCut","Gemini","DeepSeek","Duolingo","Excel","WPS Office","Files de Google","Kodi","VLC","Stremio","Shazam","Picsart","Weverse","Roblox","Termux","AnkiDroid","WeChat"]
    batch3=["Memrise","Drops","HelloTalk","Falou","Ling","LingQ","LangReactor","Reelang","Write Greek","Moon+ Reader","ReadEra","Lector de PDF","LNReader","Shosetsu","bilibili","CloudStream","Inkaplay","Lark Player","MXL TV","Xuper","Rave","Mnet Plus","Songstats","Soundcharts","SportzX","GeeSports","Lean Remote","LGRemote"]
    batch4=["rednote","NGL","Zangi","Labalabi For WhatsApp","SocialAut","Sticker.ly","StickerVibe","Reface","Viggle AI","HoYoLAB","MCPEDL","MU Fan","Duskwood","Blackjack Trainer","AHA Games","Meu Tarot","Windy","Moovit","Google Earth","DeepStateMap","PedidosYa","Mi Claro","Mi Tigo","Tor Browser","Urban VPN"]
    batch5=["Acode","Administrador de archivos","AnkuLua","App Manager","Asistente","Autenticador","Calculadora","Carlcare","Clima","Creador de atajos","Cx Explorador de Archivos","Escáner inteligente","EX Explorador de Archivos","Flud","Grabadora de sonido","iAdb","Kit de herramientas de SIM","Kustom Widget","MarkClear","Mobile Cloner"]
    lotes=["# Lotes de iconos — Etapa 5","","El catálogo maestro es `icons.json`. Cada activity se marca `verified` solo tras contrastar el manifiesto instalado; las candidatas no contrastadas quedan `estimated`.","","## Lote 1 — 20 aplicaciones",""," "+", ".join(batch1),"","## Lote 2 — 20 aplicaciones",""," "+", ".join(batch2),"","## Lote 3 — correcciones solicitadas",""," "+", ".join(batch3),"","## Lote 4 — 25 de 28 apps disponibles",""," "+", ".join(batch4),"","## Lote 5 — 20 aplicaciones",""," "+", ".join(batch5),"","No se añadieron Palm Store (com.transsnet.store), TECNO ID (tech.palm.id) ni Hola (com.talpa.hibrowser): no existen en el catálogo del dispositivo ni en appfilter.xml. Se requiere confirmar los paquetes instalados antes de inventar activities.","","Duolingo incluye la activity principal `com.duolingo/com.duolingo.app.LoginActivity` y actividades candidatas adicionales; todas permanecen `estimated` hasta contrastarlas en el dispositivo.","","La hoja de contacto se genera desde los diez PNG de Etapa 1, cinco PNG del dock y todos los PNG del catálogo. El generador de Etapa 1, sus diez PNG aprobados, el dock, los widgets y `docs/ESTILO.md` permanecen protegidos."]
    (ROOT/"docs/LOTES.md").write_text("\n".join(lotes)+"\n",encoding="utf-8")
    stage1=["ruby_youtube","ruby_spotify","ruby_tiktok","ruby_instagram","ruby_whatsapp","ruby_google","ruby_google_play_store","ruby_configuracion","ruby_galeria","ruby_camara"]
    dock=["ruby_dock_telefono_art","ruby_dock_contactos_art","ruby_dock_mensajes_art","ruby_dock_chrome_art","ruby_dock_cajon_apps_art"]
    labels=["YouTube","Spotify","TikTok","Instagram","WhatsApp","Google","Play Store","Ajustes","Galería","Cámara","Teléfono","Contactos","Mensajes","Chrome","Cajón apps"]+[a["label"] for a in apps]
    types=["marca"]*7+["genérico"]*3+["genérico"]*3+["marca"]+["genérico"]*2+[{"brand":"marca","generic":"genérico","monogram":"monograma"}[sources[a["drawable"]]["resolved_type"]] for a in apps]
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
