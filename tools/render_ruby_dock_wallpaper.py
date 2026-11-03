#!/usr/bin/env python3
"""Build the 720x1640 Jennie wallpaper and its integrated ruby-glass dock.

The source photo is resized by width only. Its aspect ratio is preserved; the
extra canvas height is extended from the dark lower edge without stretching
or cropping the photograph. The no-bar variant is also emitted for review.
"""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "app/src/main/res/drawable-nodpi/jennie_ruby_wallpaper.jpg"
CONFIG = ROOT / "tools/dock_bar.json"
OUT = ROOT / "app/build/reports"


def extend_canvas(photo: Image.Image, width: int, height: int) -> Image.Image:
    scaled_h = round(photo.height * width / photo.width)
    scaled = photo.resize((width, scaled_h), Image.Resampling.LANCZOS)
    if scaled_h > height:
        raise ValueError("Photo is taller than target canvas; refusing to crop.")
    canvas = Image.new("RGB", (width, height), "#080304")
    canvas.paste(scaled, (0, 0))
    extra = height - scaled_h
    if extra:
        # Extend only the dark bottom edge; the photograph itself is untouched.
        edge = scaled.crop((0, max(0, scaled_h - 32), width, scaled_h))
        strip = edge.resize((width, extra), Image.Resampling.BICUBIC)
        strip = strip.filter(ImageFilter.GaussianBlur(radius=18))
        fade = Image.new("L", (width, extra), 0)
        fd = ImageDraw.Draw(fade)
        for y in range(extra):
            alpha = round(255 * min(1.0, y / max(1, min(120, extra))))
            fd.line((0, y, width, y), fill=alpha)
        dark = Image.new("RGB", (width, extra), "#080304")
        canvas.paste(Image.composite(dark, strip, fade), (0, scaled_h))
    return canvas


def draw_glass_bar(base: Image.Image, cfg: dict) -> Image.Image:
    x, y, w, h = (int(cfg[k]) for k in ("x", "y", "width", "height"))
    radius = int(cfg["radius"])
    border = int(cfg["border_px"])
    if x < 0 or y < 0 or x + w > base.width or y + h > base.height:
        raise ValueError("Dock bar is outside the wallpaper canvas.")

    # Soft, restrained shadow below the glass.
    shadow_mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle(
        (x, y + 4, x + w, y + h + 4), radius=radius, fill=110
    )
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(13))
    shadow = Image.new("RGBA", base.size, (0, 0, 0, 0))
    shadow.putalpha(shadow_mask)
    out = base.convert("RGBA")
    out = Image.alpha_composite(out, shadow)

    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    mask = Image.new("L", base.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (x, y, x + w, y + h), radius=radius, fill=255
    )

    # Dark glass with a subtly brighter top and deeper lower edge.
    gradient = Image.new("RGBA", (w + 1, h + 1), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gradient)
    top = (24, 7, 12)
    bottom = (5, 3, 4)
    opacity = int(cfg["fill_alpha"])
    for yy in range(h + 1):
        t = yy / max(1, h)
        color = tuple(round(top[i] * (1-t) + bottom[i] * t) for i in range(3))
        gd.line((0, yy, w, yy), fill=(*color, opacity))
    layer.alpha_composite(gradient, (x, y))
    layer.putalpha(Image.composite(layer.getchannel("A"), Image.new("L", base.size, 0), mask))

    # Hairline ruby border and soft top highlight.
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((x, y, x+w, y+h), radius=radius,
                           outline=(122, 22, 36, 190), width=border)
    highlight = Image.new("RGBA", base.size, (0, 0, 0, 0))
    hm = Image.new("L", base.size, 0)
    ImageDraw.Draw(hm).rounded_rectangle(
        (x+3, y+2, x+w-3, y+int(h*0.48)), radius=max(1, radius-3), fill=20
    )
    hm = hm.filter(ImageFilter.GaussianBlur(9))
    highlight.putalpha(hm)
    tint = Image.new("RGBA", base.size, (242, 170, 185, 0))
    tint.putalpha(hm.point(lambda p: round(p * 0.28)))
    layer = Image.alpha_composite(layer, tint)
    ImageDraw.Draw(layer).line((x+radius, y+2, x+w-radius, y+2),
                               fill=(194, 58, 75, 95), width=1)
    out = Image.alpha_composite(out, layer)
    return out.convert("RGB")


def main() -> None:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    width, height = int(cfg["canvas_width"]), int(cfg["canvas_height"])
    with Image.open(SOURCE) as src:
        photo = src.convert("RGB")
    base = extend_canvas(photo, width, height)
    OUT.mkdir(parents=True, exist_ok=True)
    clean = OUT / "jennie-ruby-wallpaper-no-dock.png"
    final = OUT / "jennie-ruby-wallpaper-ruby-glass-dock.png"
    base.save(clean, optimize=True)
    draw_glass_bar(base, cfg).save(final, optimize=True)
    for path in (clean, final):
        with Image.open(path) as check:
            if check.size != (width, height) or check.mode != "RGB":
                raise RuntimeError(f"Invalid wallpaper output: {path}")
    print(f"Wallpaper outputs: {clean.name}, {final.name} ({width}x{height})")


if __name__ == "__main__":
    main()
