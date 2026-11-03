#!/usr/bin/env python3
"""Structural quality gate for the JENNIE RUBY Nova icon collection."""
from __future__ import annotations

import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAWABLE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
ANDROID = "{http://schemas.android.com/apk/res/android}"
EXPECTED_COUNT = 146
SUPPORTED_DIMENSIONS = {
    ("48dp", "48dp", "28", "28"),
    ("108dp", "108dp", "108", "108"),
}


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    files = sorted(DRAWABLE_DIR.glob("ruby_*.xml"))
    errors: list[str] = []
    if len(files) != EXPECTED_COUNT:
        errors.append(f"Expected {EXPECTED_COUNT} vector icons; found {len(files)}.")

    dimension_counts: Counter[tuple[str, str, str, str]] = Counter()
    path_counts: Counter[int] = Counter()
    for path in files:
        try:
            root = ET.parse(path).getroot()
        except (ET.ParseError, OSError) as exc:
            errors.append(f"{path.name}: invalid XML ({exc}).")
            continue

        if root.tag != "vector":
            errors.append(f"{path.name}: root element must be <vector>.")
            continue

        dimensions = tuple(root.get(ANDROID + key, "") for key in (
            "width", "height", "viewportWidth", "viewportHeight"
        ))
        dimension_counts[dimensions] += 1
        if dimensions not in SUPPORTED_DIMENSIONS:
            errors.append(
                f"{path.name}: unsupported vector dimensions {dimensions}; "
                "use the established 48dp/28 or 108dp/108 format."
            )

        paths = root.findall("path")
        path_counts[len(paths)] += 1
        # Two-layer icons are valid: background + glyph; frame/highlight layers are optional.
        if len(paths) < 2:
            errors.append(f"{path.name}: only {len(paths)} path(s); expected at least background and glyph.")
        for index, node in enumerate(paths, start=1):
            if not node.get(ANDROID + "pathData", "").strip():
                errors.append(f"{path.name}: path {index} has no pathData.")
            if not (node.get(ANDROID + "fillColor") or node.get(ANDROID + "strokeColor")):
                errors.append(f"{path.name}: path {index} has neither fillColor nor strokeColor.")

    print(f"Checked {len(files)} icon vectors.")
    print("Dimension groups:")
    for dimensions, count in sorted(dimension_counts.items()):
        print(f"  {count} × {dimensions}")
    if len(dimension_counts) > 1:
        print("WARNING: more than one established vector size is present; "
              "visual scale still requires device-level review.")
    print("Path-count groups:")
    for count, total in sorted(path_counts.items()):
        print(f"  {total} icon(s) with {count} path(s)")

    if errors:
        fail(errors)
    print("Vector XML structure and supported dimension formats passed.")


if __name__ == "__main__":
    main()
