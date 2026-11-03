#!/usr/bin/env python3
"""Render the five Stage 3 dock icons without modifying the Stage 1 renderer."""
from __future__ import annotations

import importlib.util
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/src/main/res/drawable-nodpi"
REPORT = ROOT / "app/build/reports"
STAGE1 = ROOT / "tools/render_ruby_stage1_icons.py"
STAGE1_BLOB = "7eae0f7904744e190d520d9e9fe4ad131414d815"
DOCK_ART = ("dock_telefono_art", "dock_contactos_art", "dock_mensajes_art", "dock_chrome_art")
SIZE = 192
SQUIRCLE = (13, 13, 179, 179)


def load_stage1_renderer():
    spec = importlib.util.spec_from_file_location("ruby_stage1_renderer", STAGE1)
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load the protected Stage 1 renderer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_drawer() -> Path:
    """The app-drawer glyph is the approved circular exception to the squircle."""
    OUT.mkdir(parents=True, exist_ok=True)
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).ellipse(SQUIRCLE, fill=255)

    blurred = mask.filter(ImageFilter.GaussianBlur(radius=8))
    shadow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    shadow.putalpha(blurred.point(lambda value: round(value * 0.46)))
    canvas = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(shadow, (0, 4))

    surface = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(surface).ellipse(SQUIRCLE, fill="#080304")
    canvas.alpha_composite(surface)

    details = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(details)
    draw.ellipse(SQUIRCLE, outline="#7A1624", width=3)
    draw.arc(SQUIRCLE, 180, 360, fill="#C23A4B", width=3)
    # Nine evenly spaced dots; alternating pale pink and soft silver.
    centers = (72, 96, 120)
    colors = ("#F3DDE2", "#D8D1D3", "#F3DDE2")
    for row, y in enumerate(centers):
        for col, x in enumerate(centers):
            radius = 5
            draw.ellipse((x-radius, y-radius, x+radius, y+radius),
                         fill=colors[(row + col) % len(colors)])
    canvas.alpha_composite(details)
    target = OUT / "ruby_dock_cajon_apps_art.png"
    canvas.save(target, format="PNG", optimize=True)
    with Image.open(target) as check:
        if check.size != (SIZE, SIZE) or check.mode != "RGBA":
            raise RuntimeError(f"Invalid drawer PNG: {target}")
        if check.getpixel((0, 0))[3] != 0:
            raise RuntimeError("Drawer icon corners must remain transparent")
    return target


def make_contact_sheet(names: tuple[str, ...]) -> Path:
    REPORT.mkdir(parents=True, exist_ok=True)
    labels = (
        "YouTube", "Spotify", "TikTok", "Instagram", "WhatsApp",
        "Google", "Play Store", "Ajustes", "Galería", "Cámara",
        "Teléfono", "Contactos", "Mensajes", "Chrome", "Cajón apps",
    )
    if len(names) != 15:
        raise RuntimeError(f"Expected 15 icons for contact sheet, found {len(names)}")
    sheet = Image.new("RGB", (2000, 1350), "#10070A")
    draw = ImageDraw.Draw(sheet)
    for index, (name, label) in enumerate(zip(names, labels)):
        path = OUT / f"{name}.png"
        with Image.open(path) as source:
            icon = source.convert("RGBA").resize((300, 300), Image.Resampling.LANCZOS)
        x = (index % 5) * 400 + 50
        y = (index // 5) * 450 + 35
        sheet.paste(icon, (x, y), icon)
        draw.text((x + 150, y + 325), label, fill="#F3E6E6", anchor="mm")
    target = REPORT / "jennie-ruby-stage3-contact-sheet.png"
    sheet.save(target, optimize=True)
    return target


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    renderer = load_stage1_renderer()
    generated = []
    for name in DOCK_ART:
        generated.append(renderer.render(name))
    generated.append(render_drawer())

    dock_names = (
        "ruby_dock_telefono_art", "ruby_dock_contactos_art",
        "ruby_dock_mensajes_art", "ruby_dock_chrome_art",
        "ruby_dock_cajon_apps_art",
    )
    for name in dock_names:
        path = OUT / f"{name}.png"
        with Image.open(path) as image:
            if image.size != (192, 192) or image.mode != "RGBA":
                raise RuntimeError(f"Invalid dock artwork: {path}")
            if image.getpixel((0, 0))[3] != 0:
                raise RuntimeError(f"Dock artwork corner is not transparent: {path}")

    stage1_names = (
        "ruby_youtube", "ruby_spotify", "ruby_tiktok", "ruby_instagram",
        "ruby_whatsapp", "ruby_google", "ruby_google_play_store",
        "ruby_configuracion", "ruby_galeria", "ruby_camara",
    )
    sheet = make_contact_sheet(stage1_names + dock_names)
    print(f"Generated five dock PNGs: {len(generated)}")
    print(f"Contact sheet: {sheet.relative_to(ROOT)} (2000x1350, 15 icons)")


if __name__ == "__main__":
    main()
