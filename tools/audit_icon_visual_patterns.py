#!/usr/bin/env python3
"""Report repeated geometry and dimensions for manual icon-design review."""
from __future__ import annotations
from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DRAWABLE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
OUTPUT = ROOT / "build/reports/icon-pattern-audit.md"
ANDROID = "{http://schemas.android.com/apk/res/android}"

def main() -> None:
    files = sorted(DRAWABLE_DIR.glob("ruby_*.xml"))
    first_shapes = defaultdict(list)
    all_shapes = defaultdict(list)
    dimensions = Counter()
    colors = Counter()
    errors = []

    for file in files:
        try:
            root = ET.parse(file).getroot()
        except (ET.ParseError, OSError) as exc:
            errors.append(f"- {file.name}: {exc}")
            continue
        if root.tag != "vector":
            errors.append(f"- {file.name}: root is not vector")
            continue
        dims = tuple(root.get(ANDROID + key, "") for key in (
            "width", "height", "viewportWidth", "viewportHeight"
        ))
        dimensions[dims] += 1
        paths = root.findall("path")
        if paths:
            shape = paths[0].get(ANDROID + "pathData", "").strip()
            if shape:
                first_shapes[shape].append(file.stem)
        for node in paths:
            shape = node.get(ANDROID + "pathData", "").strip()
            if shape:
                all_shapes[shape].append(file.stem)
            for key in ("fillColor", "strokeColor"):
                color = node.get(ANDROID + key)
                if color:
                    colors[color.upper()] += 1

    repeated_backgrounds = sorted(
        (names for names in first_shapes.values() if len(names) > 1),
        key=lambda names: (-len(names), names),
    )
    repeated_geometry = sorted(
        ((shape, sorted(set(names))) for shape, names in all_shapes.items() if len(set(names)) > 1),
        key=lambda item: (-len(item[1]), item[1]),
    )

    lines = [
        "# JENNIE RUBY — Icon pattern audit", "",
        f"- Icon vector files scanned: **{len(files)}**",
        f"- Repeated first-layer geometries: **{len(repeated_backgrounds)} groups**",
        f"- Reused path geometries across multiple icons: **{len(repeated_geometry)} groups**",
        "", "## Resource dimensions", "",
        "| Count | Width | Height | Viewport |",
        "|---:|---:|---:|---:|",
    ]
    for (width, height, vw, vh), count in sorted(dimensions.items()):
        lines.append(f"| {count} | {width} | {height} | {vw} × {vh} |")

    lines += ["", "## Repeated first-layer shapes", ""]
    if repeated_backgrounds:
        lines.append("These icons begin with exactly the same path geometry. This is a review candidate, not automatically a defect.")
        for names in repeated_backgrounds:
            lines.append(f"- {len(names)} icons: " + ", ".join(names))
    else:
        lines.append("No exact repeated first-layer path geometry found.")

    lines += ["", "## Reused path geometry", ""]
    if repeated_geometry:
        lines.append("Exact path reuse can be intentional (for example, a shared frame or common motif). Review the listed groups visually.")
        for _, names in repeated_geometry:
            lines.append(f"- {len(names)} icons: " + ", ".join(names))
    else:
        lines.append("No exact path geometry reused across different icons.")

    lines += ["", "## Most-used colors", "", "| Occurrences | Color |", "|---:|---|"]
    for color, count in colors.most_common(12):
        lines.append(f"| {count} | {color} |")

    lines += ["", "## Parse issues", ""]
    lines.extend(errors or ["None."])
    lines += ["", "> This report detects exact geometry reuse and resource-size differences only. It does not judge recognizability, aesthetics, visual balance, or Nova Launcher rendering.", ""]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} from {len(files)} icon vectors.")
    print(f"Repeated first-layer groups: {len(repeated_backgrounds)}; reused geometry groups: {len(repeated_geometry)}.")
    if errors:
        raise SystemExit(f"{len(errors)} vector parse issue(s); see report.")

if __name__ == "__main__":
    main()
