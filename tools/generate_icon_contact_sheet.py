#!/usr/bin/env python3
"""Build a self-contained HTML contact sheet for visual review of all app icons."""
from __future__ import annotations

import base64
import csv
import html
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "device-app-catalog.tsv"
DRAWABLE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
OUTPUT = ROOT / "build/reports/icon-contact-sheet.html"
ANDROID = "{http://schemas.android.com/apk/res/android}"
EXPECTED = 146

ATTRIBUTES = {
    "pathData": "d",
    "fillColor": "fill",
    "strokeColor": "stroke",
    "strokeWidth": "stroke-width",
    "strokeLineCap": "stroke-linecap",
    "strokeLineJoin": "stroke-linejoin",
    "strokeMiterLimit": "stroke-miterlimit",
    "fillAlpha": "fill-opacity",
    "strokeAlpha": "stroke-opacity",
    "fillType": "fill-rule",
}


def svg_color(value: str) -> str:
    """Convert Android #AARRGGBB colors to SVG rgba; retain other CSS colors."""
    if len(value) == 9 and value.startswith("#"):
        alpha = int(value[1:3], 16) / 255
        return f"rgba({int(value[3:5],16)},{int(value[5:7],16)},{int(value[7:9],16)},{alpha:.4f})"
    return value


def render_icon(drawable: str) -> str:
    """Render a generated raster asset or convert an Android vector to inline SVG."""
    for extension, mime in (("png", "image/png"), ("webp", "image/webp")):
        raster = DRAWABLE_DIR / f"{drawable}.{extension}"
        if raster.is_file():
            encoded = base64.b64encode(raster.read_bytes()).decode("ascii")
            return f'<img src="data:{mime};base64,{encoded}" alt="{html.escape(drawable)}"/>'

    path = DRAWABLE_DIR / f"{drawable}.xml"
    if not path.is_file():
        # Resolve dock aliases to their generated *_art PNGs.
        aliases_path = ROOT / "app/src/main/res/values/drawable.xml"
        if aliases_path.is_file():
            aliases_root = ET.parse(aliases_path).getroot()
            for item in aliases_root.findall("item"):
                if item.get("type") == "drawable" and item.get("name") == drawable:
                    target = (item.text or "").strip().removeprefix("@drawable/")
                    if target and target != drawable:
                        return render_icon(target)
        raise ValueError(f"Missing vector, raster or resolvable drawable alias: {drawable}")
    root = ET.parse(path).getroot()
    if root.tag != "vector":
        raise ValueError(f"{path.name}: root is not <vector>")
    width = root.get(ANDROID + "viewportWidth")
    height = root.get(ANDROID + "viewportHeight")
    if not width or not height:
        raise ValueError(f"{path.name}: missing viewport dimensions")

    paths = []
    for node in root.findall("path"):
        attrs = []
        for android_name, svg_name in ATTRIBUTES.items():
            value = node.get(ANDROID + android_name)
            if value is None:
                continue
            if android_name in ("fillColor", "strokeColor"):
                value = svg_color(value)
            if android_name == "fillType":
                value = "evenodd" if value == "evenOdd" else "nonzero"
            attrs.append(f'{svg_name}="{html.escape(value, quote=True)}"')
        paths.append("<path " + " ".join(attrs) + "/>")
    if not paths:
        raise ValueError(f"{path.name}: vector has no paths")
    return (
        f'<svg viewBox="0 0 {html.escape(width)} {html.escape(height)}" '
        f'role="img" aria-label="{html.escape(drawable)}">'
        + "".join(paths) + "</svg>"
    )

def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    if len(rows) != EXPECTED:
        raise ValueError(f"Expected {EXPECTED} catalog rows; found {len(rows)}")

    cards = []
    seen = set()
    for row in rows:
        name, drawable = row["name"], row["drawable"]
        if drawable in seen:
            raise ValueError(f"Duplicate drawable in catalog: {drawable}")
        seen.add(drawable)
        cards.append(
            '<article class="card">'
            f'<div class="icon">{render_icon(drawable)}</div>'
            f'<strong>{html.escape(name)}</strong>'
            f'<small>{html.escape(drawable)}</small>'
            '</article>'
        )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    document = """<!doctype html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>JENNIE RUBY · Revisión visual de iconos</title>
<style>
:root{color-scheme:dark;font-family:system-ui,sans-serif;background:#10070c;color:#f8e8ee}
body{margin:0;padding:24px}header{max-width:1200px;margin:0 auto 24px}
h1{margin:0;color:#f3b7c8}p{color:#c9aab5}
.grid{max-width:1200px;margin:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(112px,1fr));gap:14px}
.card{min-width:0;text-align:center;background:#211019;border:1px solid #542238;border-radius:14px;padding:12px 8px}
.icon{width:76px;height:76px;margin:0 auto 10px;display:grid;place-items:center}
.icon svg,.icon img{width:100%;height:100%;overflow:visible;object-fit:contain}
strong,small{display:block;overflow-wrap:anywhere}strong{font-size:13px}
small{margin-top:4px;color:#c58da1;font-size:10px}
@media(min-width:900px){.grid{grid-template-columns:repeat(10,minmax(0,1fr))}}
@media(max-width:420px){body{padding:12px}.grid{grid-template-columns:repeat(3,minmax(0,1fr));gap:8px}.card{padding:10px 5px}.icon{width:64px;height:64px}}
</style></head><body>
<header><h1>JENNIE RUBY</h1>
<p>Hoja de contacto · 146 iconos · PNG generados y vectores SVG a escala uniforme para detectar similitudes, legibilidad y desequilibrios visuales. No sustituye la comprobación en Nova Launcher.</p></header>
<main class="grid">
""" + "\n".join(cards) + """
</main></body></html>
"""
    OUTPUT.write_text(document, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(cards)} icons.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, ET.ParseError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
