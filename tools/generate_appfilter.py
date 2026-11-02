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

    for row in rows:
        component = row["component"]
        drawable = row["drawable"]
        if not re.fullmatch(r"[A-Za-z0-9_.]+/[A-Za-z0-9_.$]+", component):
            fail(f"Invalid component syntax: {component}")
        if not re.fullmatch(r"ruby_[a-z0-9_]+", drawable):
            fail(f"Invalid drawable name: {drawable}")
        candidates = [DRAWABLE_DIR / f"{drawable}.{ext}" for ext in ("png", "webp", "xml")]
        if not any(path.is_file() for path in candidates):
            fail(f"Missing artwork for {row['name']}: expected {drawable}.png, .webp or .xml")

    root = ET.Element("resources")
    for row in rows:
        ET.SubElement(root, "item", {
            "component": f"ComponentInfo{{{row['component']}}}",
            "drawable": row["drawable"],
        })

    ET.indent(root, space="    ")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    ET.ElementTree(root).write(OUTPUT, encoding="utf-8", xml_declaration=True)
    print(f"Generated {OUTPUT.relative_to(ROOT)} with {len(rows)} app mappings.")


if __name__ == "__main__":
    main()
