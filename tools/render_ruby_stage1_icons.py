#!/usr/bin/env python3
"""Generate the Stage 1 Ruby icon PNGs during CI. Any missing/bad source fails the build."""
from pathlib import Path
import io
import xml.etree.ElementTree as ET

import cairosvg
from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "tools" / "ruby_icon_sources"
OUT = ROOT / "app" / "src" / "main" / "res" / "drawable-nodpi"
NAMES = (
    "youtube", "spotify", "tiktok", "instagram", "whatsapp",
    "google", "google_play_store", "configuracion", "galeria", "camara",
)
ANDROID = "{http://schemas.android.com/apk/res/android}"
SIZE = 192
SQUIRCLE = (13, 13, 179, 179)  # 166 x 166 px = 86.46% of the 192px canvas
RADIUS = 43

def color(hex_value):
    value = hex_value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

def vertical_gradient(top, bottom):
    top, bottom = color(top), color(bottom)
    image = Image.new("RGBA", (SIZE, SIZE))
    pixels = image.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        row = tuple(round(top[c] * (1 - t) + bottom[c] * t) for c in range(3)) + (255,)
        for x in range(SIZE):
            pixels[x, y] = row
    return image

def path_mask(element, view_w, view_h):
    d = element.get(ANDROID + "pathData")
    if not d:
        raise ValueError("An SVG source path has no pathData")
    fill = element.get(ANDROID + "fillColor", "#FFFFFF")
    stroke = element.get(ANDROID + "strokeColor")
    stroke_width = float(element.get(ANDROID + "strokeWidth", "0"))
    fill_enabled = fill.upper() not in ("#00000000", "#00FFFFFF")
    stroke_enabled = bool(stroke) and stroke.upper() not in ("#00000000", "#00FFFFFF")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" viewBox="0 0 {view_w} {view_h}">
      <path d="{d}" fill="#FFFFFF" fill-rule="evenodd" if="unused"
        stroke="#FFFFFF" stroke-width="{stroke_width}" stroke-linecap="{element.get(ANDROID + "strokeLineCap", "butt")}"
        stroke-linejoin="{element.get(ANDROID + "strokeLineJoin", "miter")}"
        style="fill:{'#FFFFFF' if fill_enabled else 'none'};stroke:{'#FFFFFF' if stroke_enabled else 'none'}"/>
    </svg>'''
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"), output_width=SIZE, output_height=SIZE)
    return Image.open(io.BytesIO(png)).convert("RGBA").getchannel("A")

def custom_glyph_mask(name):
    mask = Image.new("L", (SIZE, SIZE), 0)
    d = ImageDraw.Draw(mask)
    if name == "camara":
        d.rounded_rectangle((43, 67, 149, 137), radius=17, fill=255)
        d.rounded_rectangle((62, 55, 101, 78), radius=8, fill=255)
        d.ellipse((73, 77, 119, 123), fill=255)
        d.ellipse((84, 88, 108, 112), fill=0)
        d.ellipse((128, 77, 138, 87), fill=255)
        return mask
    if name == "instagram":
        d.rounded_rectangle((48, 48, 144, 144), radius=25, outline=255, width=9)
        d.ellipse((70, 70, 122, 122), outline=255, width=8)
        d.ellipse((124, 61, 135, 72), fill=255)
        return mask
    if name == "galeria":
        for bounds in ((82,42,110,82),(111,68,151,96),(99,105,127,147),(65,105,93,147),(41,68,81,96)):
            d.ellipse(bounds, fill=255)
        d.ellipse((79, 80, 113, 114), fill=0)
        return mask
    return None

def make_glyph_mask(paths, view_w, view_h, name):
    custom = custom_glyph_mask(name)
    if custom is not None:
        return custom
    # The first six source paths are the old tile/background treatment; only retain
    # the original logo geometry after those paths and recolor it as one ruby glyph.
    if len(paths) < 7:
        raise ValueError("Expected at least one logo path after the six tile paths")
    mask = Image.new("L", (SIZE, SIZE), 0)
    for element in paths[6:]:
        part = path_mask(element, view_w, view_h)
        fill = element.get(ANDROID + "fillColor", "#FFFFFF").upper()
        stroke = element.get(ANDROID + "strokeColor", "").upper()
        if fill in ("#080304", "#000000", "#00000000") or stroke in ("#080304", "#000000"):
            mask = ImageChops.subtract(mask, part)
        else:
            mask = ImageChops.lighter(mask, part)
    if mask.getbbox() is None:
        raise ValueError("Logo mask is empty")
    return mask

def render(name):
    source = SOURCE_DIR / f"ruby_{name}.xml"
    if not source.is_file():
        raise FileNotFoundError(f"Missing vector source: {source}")
    root = ET.parse(source).getroot()
    view_w = float(root.get(ANDROID + "viewportWidth", "108"))
    view_h = float(root.get(ANDROID + "viewportHeight", "108"))
    paths = root.findall("path")
    glyph_mask = make_glyph_mask(paths, view_w, view_h, name)

    # Drop shadow: Pillow GaussianBlur radius 8px, offset +0px/+4px, opacity 46%.
    tile_mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(tile_mask).rounded_rectangle(SQUIRCLE, radius=RADIUS, fill=255)
    blurred = tile_mask.filter(ImageFilter.GaussianBlur(radius=8))
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow_alpha = blurred.point(lambda value: round(value * 0.46))
    shadow.putalpha(shadow_alpha)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(shadow, (0, 4))

    # Near-black surface; wine tint is a continuous localized gradient at bottom-right.
    bg = vertical_gradient("#080304", "#080304")
    wine = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    wp = wine.load()
    wine_rgb = color("#2A0A10")
    for y in range(SIZE):
        for x in range(SIZE):
            dx = max(0.0, (x - 82) / 97)
            dy = max(0.0, (y - 88) / 91)
            strength = min(0.38, (dx * dy) ** 1.10 * 0.38)
            wp[x, y] = (*wine_rgb, round(255 * strength))
    bg.alpha_composite(wine)
    bg.putalpha(tile_mask)
    canvas.alpha_composite(bg)

    # Ruby glyph gradient is applied through a vector-derived alpha mask.
    glyph = vertical_gradient("#E0334B", "#8E0B20")
    glow = glyph_mask.filter(ImageFilter.GaussianBlur(radius=2.2))
    glow_layer = Image.new("RGBA", (SIZE, SIZE), (224, 51, 75, 0))
    glow_layer.putalpha(glow.point(lambda value: round(value * 0.16)))
    canvas.alpha_composite(glow_layer)
    glyph.putalpha(glyph_mask)
    canvas.alpha_composite(glyph)

    # Fine ruby outline plus a subdued upper-edge highlight.
    border = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(border)
    draw.rounded_rectangle(SQUIRCLE, radius=RADIUS, outline="#7A1624", width=3)
    canvas.alpha_composite(border)

    # Upper ruby bevel: 60% peak highlight, softened and faded at both ends.
    bevel = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bevel)
    bd.arc(SQUIRCLE, 180, 360, fill=(194, 58, 75, 255), width=3)
    bevel = bevel.filter(ImageFilter.GaussianBlur(radius=1.2))
    bp = bevel.load()
    for y in range(SIZE):
        for x in range(SIZE):
            edge_fade = min(1.0, x / 28, (SIZE - 1 - x) / 28)
            lower_fade = max(0.0, 1.0 - y / 82)
            r, g, b, a = bp[x, y]
            bp[x, y] = (r, g, b, round(a * 0.60 * edge_fade * lower_fade))
    canvas.alpha_composite(bevel)

    # Soft glass wash only: no rounded-rectangle edge or hard reflection contour.
    reflection = Image.new("RGBA", (SIZE, SIZE), (255, 238, 242, 0))
    rp = reflection.load()
    for y in range(SIZE):
        vertical = max(0.0, 1.0 - y / (SIZE * 0.35))
        for x in range(SIZE):
            horizontal = min(1.0, x / 22, (SIZE - 1 - x) / 22)
            rp[x, y] = (255, 238, 242, round(255 * 0.09 * vertical * horizontal))
    reflection.putalpha(ImageChops.multiply(reflection.getchannel("A"), tile_mask))
    reflection = reflection.filter(ImageFilter.GaussianBlur(radius=7))
    canvas.alpha_composite(reflection)

    target = OUT / f"ruby_{name}.png"
    canvas.save(target, format="PNG", optimize=True)
    with Image.open(target) as check:
        if check.size != (192, 192) or check.mode != "RGBA":
            raise RuntimeError(f"Invalid generated resource: {target}")
        if check.getpixel((0, 0))[3] != 0:
            raise RuntimeError(f"Transparent corners lost: {target}")
    return target

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    # Remove previous generated resources first: a partial failure cannot leave stale PNGs.
    for name in NAMES:
        (OUT / f"ruby_{name}.png").unlink(missing_ok=True)
    generated = [render(name) for name in NAMES]
    if len(generated) != 10 or any(not path.is_file() for path in generated):
        raise RuntimeError("Stage 1 icon generation incomplete")
    sheet = Image.new("RGB", (2000, 900), "#10070A")
    sd = ImageDraw.Draw(sheet)
    labels = ("YouTube", "Spotify", "TikTok", "Instagram", "WhatsApp",
              "Google", "Play Store", "Ajustes", "Galería", "Cámara")
    for index, (name, label) in enumerate(zip(NAMES, labels)):
        icon = Image.open(OUT / f"ruby_{name}.png").convert("RGBA").resize((300, 300), Image.Resampling.LANCZOS)
        x = (index % 5) * 400 + 50
        y = (index // 5) * 450 + 35
        sheet.paste(icon, (x, y), icon)
        sd.text((x + 150, y + 325), label, fill="#F3E6E6", anchor="mm")
    report = ROOT / "app" / "build" / "reports"
    report.mkdir(parents=True, exist_ok=True)
    contact = report / "jennie-ruby-stage1-contact-sheet.png"
    sheet.save(contact, optimize=True)
    print(f"Contact sheet: {contact.relative_to(ROOT)} (2000x900)")
    print("Generated Stage 1 PNGs:")
    for path in generated:
        print(f" - {path.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
