#!/usr/bin/env python3
"""Generate Nova Launcher's appfilter.xml from the verified device catalog.

The generator intentionally refuses to emit an incomplete filter: every app must
have its own drawable resource before the mapping is written.
"""
from __future__ import annotations

import csv
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "device-app-catalog.tsv"
DRAWABLE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
OUTPUT = ROOT / "app/src/main/res/xml/appfilter.xml"
EXPECTED_APPS = 146
ALIASES = ROOT / "device-app-aliases.tsv"
RESOURCE_ALIASES = ROOT / "app/src/main/res/values/drawable.xml"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    with CATALOG.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))

    if len(rows) != EXPECTED_APPS:
        fail(f"Expected {EXPECTED_APPS} catalog entries; found {len(rows)}.")

    components = [row["component"] for row in rows]
    if len(set(components)) != len(components):
        fail("Duplicate launcher components detected.")

    resource_aliases = {}
    if RESOURCE_ALIASES.exists():
        try:
            resource_root = ET.parse(RESOURCE_ALIASES).getroot()
        except ET.ParseError as exc:
            fail(f"Invalid drawable resource aliases XML: {exc}")
        for item in resource_root.findall("item"):
            if item.get("type") != "drawable":
                continue
            alias_name = item.get("name", "")
            target = (item.text or "").strip()
            match = re.fullmatch(r"@drawable/(ruby_[a-z0-9_]+)", target)
            if not re.fullmatch(r"ruby_[a-z0-9_]+", alias_name) or not match:
                fail(f"Invalid drawable alias: {alias_name} -> {target}")
            if alias_name in resource_aliases:
                fail(f"Duplicate drawable resource alias: {alias_name}")
            resource_aliases[alias_name] = match.group(1)

    for row in rows:
        component = row["component"]
        drawable = row["drawable"]
        if not re.fullmatch(r"[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+", component):
            fail(f"Invalid component syntax: {component}")
        if not re.fullmatch(r"ruby_[a-z0-9_]+", drawable):
            fail(f"Invalid drawable name: {drawable}")
        candidates = [DRAWABLE_DIR / f"{drawable}.{ext}" for ext in ("png", "webp", "xml")]
        if not any(path.is_file() for path in candidates):
            target = resource_aliases.get(drawable)
            target_candidates = ([DRAWABLE_DIR / f"{target}.{ext}" for ext in ("png", "webp", "xml")]
                                 if target else [])
            if not target or not any(path.is_file() for path in target_candidates):
                fail(f"Missing artwork for {row['name']}: expected {drawable} or a valid drawable.xml alias")

    alias_rows = []
    if ALIASES.exists():
        with ALIASES.open(encoding="utf-8", newline="") as stream:
            alias_rows = list(csv.DictReader(stream, delimiter="\t"))
    alias_components = [row["component"] for row in alias_rows]
    if len(set(alias_components)) != len(alias_components) or set(alias_components) & set(components):
        fail("Duplicate launcher components detected in aliases.")
    for row in alias_rows:
        if not re.fullmatch(r"[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+", row["component"]):
            fail(f"Invalid alias component syntax: {row['component']}")
        if row["drawable"] not in {item["drawable"] for item in rows}:
            fail(f"Alias references unknown drawable: {row['drawable']}")

    root = ET.Element("resources")
    for layer, drawable in (("iconback", "ruby_iconback"), ("iconmask", "ruby_iconmask"), ("iconupon", "ruby_iconupon")):
        parent = ET.SubElement(root, layer)
        ET.SubElement(parent, "item", {"drawable": drawable})
    for row in rows + alias_rows:
        ET.SubElement(root, "item", {
            "component": f"ComponentInfo{{{row['component']}}}",
            "drawable": row["drawable"],
        })

    ET.indent(root, space="    ")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    # Keep byte-for-byte output stable so CI can detect real catalog drift.
    body = ET.tostring(root, encoding="unicode")
    OUTPUT.write_text('<?xml version="1.0" encoding="utf-8"?>\n' + body + "\n", encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(rows)} app mappings.")


if __name__ == "__main__":
    main()
