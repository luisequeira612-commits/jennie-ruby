#!/usr/bin/env python3
"""Generate transparent AppWidget picker preview PNGs from the bundled font files.

These images are static previews for widget pickers and CI review. The real widgets
are Android RemoteViews layouts and must still be checked on the target phone.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
FONT_DIR = ROOT / "app" / "src" / "main" / "res" / "font"
OUT_DIR = ROOT / "app" / "src" / "main" / "res" / "drawable-nodpi"
PINK = (232, 160, 168, 255)
WHITE_PINK = (243, 230, 230, 255)

def load_font(name: str, size: int):
    path = FONT_DIR / name
    if not path.is_file() or path.stat().st_size < 1000:
        raise FileNotFoundError(f"Required widget font is missing: {path}")
    return ImageFont.truetype(str(path), size=size)

def spaced_text(draw, xy, text, font, fill, spacing):
    x, y = xy
    for character in text:
        draw.text((x, y), character, font=font, fill=fill)
        x += draw.textlength(character, font=font) + spacing
    return x

def draw_crown(draw, center_x, top):
    points = [
        (center_x - 25, top + 8),
        (center_x - 14, top + 23),
        (center_x - 5, top + 3),
        (center_x + 5, top + 23),
        (center_x + 25, top + 8),
        (center_x + 20, top + 34),
        (center_x - 20, top + 34),
        (center_x - 25, top + 8),
    ]
    draw.line(points, fill=PINK, width=3, joint="curve")
    draw.line((center_x - 20, top + 34, center_x + 20, top + 34), fill=PINK, width=3)

def draw_heart(draw, center_x, center_y):
    # Thin outline; the real widget uses a rotated vector drawable.
    points = [
        (center_x, center_y + 17),
        (center_x - 18, center_y + 3),
        (center_x - 18, center_y - 8),
        (center_x - 10, center_y - 14),
        (center_x, center_y - 5),
        (center_x + 10, center_y - 14),
        (center_x + 18, center_y - 8),
        (center_x + 18, center_y + 3),
        (center_x, center_y + 17),
    ]
    draw.line(points, fill=PINK, width=3, joint="curve")

def make_clock_preview():
    image = Image.new("RGBA", (600, 300), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    time_font = load_font("playfair_display.ttf", 102)
    date_font = load_font("cormorant_garamond.ttf", 38)

    time_text = "12:45"
    time_box = draw.textbbox((0, 0), time_text, font=time_font)
    time_width = time_box[2] - time_box[0]
    time_x = 24
    crown_center = time_x + time_width // 2
    draw_crown(draw, crown_center, 8)

    # Subtle red shadow under the digits, matching the actual TextClock treatment.
    draw.text((time_x + 1, 67), time_text, font=time_font, fill=(122, 22, 36, 105))
    draw.text((time_x, 65), time_text, font=time_font, fill=PINK)
    draw.text((24, 183), "Sáb, 1 de Noviembre", font=date_font, fill=PINK)

    y = 258
    draw.line((24, y, 159, y), fill=PINK, width=2)
    draw.text((168, y - 18), "✦", font=load_font("cormorant_garamond.ttf", 34), fill=PINK)
    draw.line((199, y, 334, y), fill=PINK, width=2)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / "widget_ruby_clock_preview.png"
    image.save(destination, optimize=True)
    return destination

def make_signature_preview():
    image = Image.new("RGBA", (600, 210), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    signature_font = load_font("allura.ttf", 150)
    small_font = load_font("cormorant_garamond.ttf", 27)

    name_x, name_y = 24, 0
    draw.text((name_x, name_y), "Jennie", font=signature_font, fill=PINK)
    name_box = draw.textbbox((name_x, name_y), "Jennie", font=signature_font)
    heart_x = min(360, name_box[2] - 2)
    draw_heart(draw, heart_x, 27)

    label = "BLACKPINK"
    label_spacing = 4
    label_width = sum(draw.textlength(ch, font=small_font) for ch in label) + label_spacing * (len(label) - 1)
    total_width = label_width + 2 * 92 + 2 * 14
    start_x = 24
    center_y = 166
    line_length = 92
    draw.line((start_x, center_y, start_x + line_length, center_y), fill=PINK, width=2)
    text_x = start_x + line_length + 14
    spaced_text(draw, (text_x, center_y - 20), label, small_font, WHITE_PINK, label_spacing)
    right_start = text_x + label_width + 14
    draw.line((right_start, center_y, right_start + line_length, center_y), fill=PINK, width=2)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUT_DIR / "widget_ruby_signature_preview.png"
    image.save(destination, optimize=True)
    return destination

if __name__ == "__main__":
    print(f"Clock preview: {make_clock_preview()}")
    print(f"Signature preview: {make_signature_preview()}")
