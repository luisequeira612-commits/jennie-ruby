#!/usr/bin/env python3
"""Fail CI if either widget, its fonts, licenses, or picker previews are incomplete."""
from pathlib import Path
import xml.etree.ElementTree as ET

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ANDROID = "{http://schemas.android.com/apk/res/android}"

def require(condition, message):
    if not condition:
        raise SystemExit(f"FAIL: {message}")

def read_xml(relative):
    path = ROOT / relative
    require(path.is_file(), f"Missing XML resource: {relative}")
    return ET.parse(path).getroot()

def check_preview(relative, expected_size):
    path = ROOT / relative
    require(path.is_file(), f"Missing generated preview: {relative}")
    with Image.open(path) as image:
        require(image.mode == "RGBA", f"Preview must be RGBA: {relative}")
        require(image.size == expected_size, f"Unexpected preview size for {relative}: {image.size}")
        require(image.getpixel((0, 0))[3] == 0, f"Preview background must be transparent: {relative}")

font_names = ("playfair_display.ttf", "cormorant_garamond.ttf", "allura.ttf")
for name in font_names:
    path = ROOT / "app/src/main/res/font" / name
    require(path.is_file() and path.stat().st_size > 1000, f"Missing or invalid font: {name}")

license_names = (
    "OFL-PlayfairDisplay.txt",
    "OFL-CormorantGaramond.txt",
    "OFL-Allura.txt",
)
for name in license_names:
    path = ROOT / "app/src/main/assets/fonts/licenses" / name
    require(path.is_file() and path.stat().st_size > 1000, f"Missing OFL license: {name}")

clock = read_xml("app/src/main/res/xml/ruby_clock_widget_info.xml")
signature = read_xml("app/src/main/res/xml/ruby_signature_widget_info.xml")
for name, root, height in (("clock", clock, "2"), ("signature", signature, "1")):
    require(root.get(ANDROID + "targetCellWidth") == "3", f"{name} widget must target three columns")
    require(root.get(ANDROID + "targetCellHeight") == height, f"{name} widget has the wrong target row count")
    require(root.get(ANDROID + "resizeMode") == "horizontal|vertical", f"{name} widget must be resizable")
    require(root.get(ANDROID + "updatePeriodMillis") == "0", f"{name} widget must not poll periodically")
    require(root.get(ANDROID + "previewImage") is not None, f"{name} widget needs a picker preview image")
    require(root.get(ANDROID + "previewLayout") is not None, f"{name} widget needs a live preview layout")

clock_layout = read_xml("app/src/main/res/layout/widget_ruby_clock.xml")
signature_layout = read_xml("app/src/main/res/layout/widget_ruby_signature.xml")
require(clock_layout.get(ANDROID + "background") == "@android:color/transparent", "Clock widget background must be transparent")
require(signature_layout.get(ANDROID + "background") == "@android:color/transparent", "Signature widget background must be transparent")

clock_text = (ROOT / "app/src/main/res/layout/widget_ruby_clock.xml").read_text(encoding="utf-8")
require('android:id="@+id/ruby_clock_bitmap"' in clock_text, "Clock widget must display its custom-drawn bitmap")
bitmap_source = (ROOT / "app/src/main/java/com/luisequeira612/jennieruby/RubyWidgetBitmap.java").read_text(encoding="utf-8")
for resource in ("R.font.playfair_display", "R.font.cormorant_garamond", "R.font.allura"):
    require(resource in bitmap_source, f"Custom widget renderer must use {resource}")
provider_source = (ROOT / "app/src/main/java/com/luisequeira612/jennieruby/RubyClockWidgetProvider.java").read_text(encoding="utf-8")
require("setInexactRepeating" in provider_source and "60000" in provider_source, "Clock provider must schedule minute refreshes")
require("setImageViewBitmap" in provider_source, "Clock provider must publish its custom-drawn bitmap")

manifest = (ROOT / "app/src/main/AndroidManifest.xml").read_text(encoding="utf-8")
require(".RubyClockWidgetProvider" in manifest, "Clock AppWidgetProvider is not registered")
require(".RubySignatureWidgetProvider" in manifest, "Signature AppWidgetProvider is not registered")
require("ruby_clock_widget_label" in manifest and "ruby_signature_widget_label" in manifest, "Widget picker labels are missing")

check_preview("app/src/main/res/drawable-nodpi/widget_ruby_clock_preview.png", (600, 300))
check_preview("app/src/main/res/drawable-nodpi/widget_ruby_signature_preview.png", (600, 210))

print("PASS: both transparent widgets, their fonts, OFL licenses and generated previews are complete.")
