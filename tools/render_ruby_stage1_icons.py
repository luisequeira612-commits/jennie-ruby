#!/usr/bin/env python3
"""Render the ten Stage-1 Ruby icons as high-quality PNG resources."""
from pathlib import Path
import xml.etree.ElementTree as ET
import io
import cairosvg
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "tools" / "ruby_icon_sources"
OUT = ROOT / "app" / "src" / "main" / "res" / "drawable-nodpi"
NAMES = ("youtube", "spotify", "tiktok", "instagram", "whatsapp",
         "google", "google_play_store", "configuracion", "galeria", "camara")
NS = "{http://schemas.android.com/apk/res/android}"
SIZE = 512

def rgba(hex_color, alpha=255):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)

def gradient(size, top, bottom):
    im = Image.new("RGBA", (size, size))
    px = im.load()
    a, b = rgba(top), rgba(bottom)
    for y in range(size):
        t = y / max(1, size - 1)
        c = tuple(round(a[k] * (1-t) + b[k] * t) for k in range(4))
        for x in range(size):
            px[x, y] = c
    return im

def svg_mask(path_el, color="#FFFFFF"):
    d = path_el.get(NS + "pathData")
    if not d:
        return Image.new("L", (SIZE, SIZE), 0)
    fill = path_el.get(NS + "fillColor", "#000000")
    stroke = path_el.get(NS + "strokeColor")
    sw = path_el.get(NS + "strokeWidth", "0")
    # Android pathData uses the same path command grammar supported by SVG.
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 108 108">
      <path d="{d}" fill="{color if fill not in ("#00000000",) else "none"}"
      stroke="{color if stroke and stroke != "#00000000" else "none"}"
      stroke-width="{float(sw) * SIZE / 108}" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>'''
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=SIZE, output_height=SIZE)
    return Image.open(io.BytesIO(png)).convert("RGBA").getchannel("A")

def render(name, size):
    global SIZE
    SIZE = 512
    root = ET.parse(SOURCES / f"ruby_{name}.xml").getroot()
    paths = root.findall("path")
    scale = size / 512

    # True blurred drop shadow, shifted down four output pixels, 45% opacity.
    shadow_mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle((25, 25, 487, 487), radius=112, fill=255)
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(8 * 512 / 192))
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow.putalpha(shadow_mask.point(lambda v: round(v * .46)))
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(shadow, (0, 4 * 512 // 192))

    # Almost-black glass base, with wine tint confined to the lower-right corner.
    base_mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(base_mask).rounded_rectangle((25, 25, 487, 487), radius=112, fill=255)
    bg = gradient(SIZE, "#080304", "#080304")
    wine = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    wp = wine.load()
    for y in range(SIZE):
        for x in range(SIZE):
            dx, dy = max(0, (x - SIZE*.53)/(SIZE*.47)), max(0, (y - SIZE*.50)/(SIZE*.50))
            strength = min(0.34, (dx*dy)**1.15 * .34)
            wp[x, y] = (*rgba("#2A0A10")[:3], round(255*strength))
    bg.alpha_composite(wine)
    bg.putalpha(base_mask)
    canvas.alpha_composite(bg)

    # Extract glyph geometry from the original paths; paths with dark fill carve holes.
    glyph_mask = Image.new("L", (SIZE, SIZE), 0)
    for el in paths[5:]:
        fill = el.get(NS + "fillColor", "#000000").upper()
        stroke = el.get(NS + "strokeColor", "").upper()
        mask = svg_mask(el)
        if fill in ("#080304", "#000000", "#00000000"):
            glyph_mask = Image.composite(Image.new("L", (SIZE, SIZE), 0), glyph_mask, mask)
        else:
            glyph_mask = ImageChops.lighter(glyph_mask, mask)
        if stroke in ("#080304", "#000000"):
            glyph_mask = ImageChops.subtract(glyph_mask, mask)

    glyph = gradient(SIZE, "#E0334B", "#8E0B20")
    # Subtle inner glow from a softly expanded, low-opacity crimson mask.
    glow = glyph_mask.filter(ImageFilter.GaussianBlur(5))
    glow_layer = Image.new("RGBA", (SIZE, SIZE), (224, 51, 75, 0))
    glow_layer.putalpha(glow.point(lambda v: round(v * .18)))
    canvas.alpha_composite(glow_layer)
    glyph.putalpha(glyph_mask)
    canvas.alpha_composite(glyph)

    # 2.5px ruby perimeter and a brighter, restrained upper-edge highlight.
    border = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(border)
    bd.rounded_rectangle((25, 25, 487, 487), radius=112, outline="#7A1624", width=round(2.5*512/108))
    bd.arc((25, 25, 487, 487), 180, 270, fill=(194, 58, 75, 92), width=round(1.8*512/108))
    canvas.alpha_composite(border)

    # Soft glass reflection, 9% at the top, fading out within ~35% of icon height.
    reflection = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    rd = ImageDraw.Draw(reflection)
    rd.rounded_rectangle((29, 29, 483, 225), radius=105, fill=(255, 238, 242, 23))
    fade = Image.new("L", (SIZE, SIZE), 0)
    fp = fade.load()
    for y in range(SIZE):
        alpha = round(255 * max(0, 1 - y / (SIZE * .35)))
        for x in range(SIZE):
            fp[x, y] = alpha
    reflection.putalpha(ImageChops.multiply(reflection.getchannel("A"), fade))
    canvas.alpha_composite(reflection)

    if size != SIZE:
        canvas = canvas.resize((size, size), Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    canvas.save(OUT / f"ruby_{name}.png", optimize=True)

from PIL import ImageChops
for icon in NAMES:
    render(icon, 192)
    render(icon, 512)
print(f"Generated {len(NAMES)*2} transparent PNGs (192px and 512px).")
