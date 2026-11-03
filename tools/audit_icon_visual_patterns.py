#!/usr/bin/env python3
"""Report repeated vector geometry, separating first layers from later layers."""
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DRAWABLE_DIR = ROOT / "app/src/main/res/drawable-nodpi"
OUTPUT = ROOT / "build/reports/icon-pattern-audit.md"
ANDROID = "{http://schemas.android.com/apk/res/android}"


def repeated_groups(shape_map: dict[str, list[str]]) -> list[list[str]]:
    """Return deterministic groups of icons sharing an exact path geometry."""
    groups = [sorted(set(names)) for names in shape_map.values() if len(set(names)) > 1]
    return sorted(groups, key=lambda names: (-len(names), names))


def main() -> None:
    files = sorted(DRAWABLE_DIR.glob("ruby_*.xml"))
    first_layers: dict[str, list[str]] = defaultdict(list)
    later_layers: dict[str, list[str]] = defaultdict(list)
    all_layers: dict[str, list[str]] = defaultdict(list)
    dimensions = Counter()
    colors = Counter()
    path_counts = Counter()
    errors: list[str] = []
    parsed = 0

    for file in files:
        try:
            root = ET.parse(file).getroot()
        except (ET.ParseError, OSError) as exc:
            errors.append(f"- {file.name}: {exc}")
            continue
        if root.tag != "vector":
            errors.append(f"- {file.name}: root is not vector")
            continue
        parsed += 1
        dims = tuple(root.get(ANDROID + key, "") for key in (
            "width", "height", "viewportWidth", "viewportHeight"
        ))
        dimensions[dims] += 1
        paths = root.findall("path")
        path_counts[len(paths)] += 1
        for index, node in enumerate(paths):
            shape = node.get(ANDROID + "pathData", "").strip()
            if shape:
                all_layers[shape].append(file.stem)
                (first_layers if index == 0 else later_layers)[shape].append(file.stem)
            for key in ("fillColor", "strokeColor"):
                color = node.get(ANDROID + key)
                if color:
                    colors[color.upper()] += 1

    repeated_first = repeated_groups(first_layers)
    repeated_later = repeated_groups(later_layers)
    repeated_all = repeated_groups(all_layers)
    lines = [
        "# JENNIE RUBY — Icon pattern audit", "",
        f"- Vector files found: **{len(files)}**",
        f"- Successfully parsed vectors: **{parsed}**",
        f"- Repeated first-layer geometry groups: **{len(repeated_first)}**",
        f"- Repeated non-first-layer geometry groups: **{len(repeated_later)}**",
        f"- Repeated geometry groups across any layer: **{len(repeated_all)}**",
        "", "## Resource dimensions", "",
        "| Count | Width | Height | Viewport |", "|---:|---:|---:|---:|",
    ]
    for (width, height, vw, vh), count in sorted(dimensions.items()):
        lines.append(f"| {count} | {width} | {height} | {vw} × {vh} |")
    lines += ["", "## Path-count distribution", "", "| Icons | Paths per icon |", "|---:|---:|"]
    for count, total in sorted(path_counts.items()):
        lines.append(f"| {total} | {count} |")

    def add_groups(title: str, groups: list[list[str]], explanation: str) -> None:
        lines.extend(["", f"## {title}", "", explanation])
        if groups:
            for names in groups:
                lines.append(f"- {len(names)} icons: " + ", ".join(names))
        else:
            lines.append("No exact repeated path geometry found.")

    add_groups(
        "Repeated first-layer geometry", repeated_first,
        "This section isolates the first path in each vector. It may be a shared base, background, or frame; repetition alone is not evidence that complete icons look alike.",
    )
    add_groups(
        "Repeated later-layer geometry", repeated_later,
        "These paths occur after the first path. They may be inner backgrounds, frames, borders, glyphs, or decorative details. Repetition alone does not identify their role; review the rendered icons before treating a group as a duplicate symbol.",
    )
    add_groups(
        "Repeated geometry across all layers", repeated_all,
        "A combined inventory for traceability. It deliberately does not label every repeated path as a defect.",
    )
    lines += ["", "## Most-used colors", "", "| Occurrences | Color |", "|---:|---|"]
    for color, count in colors.most_common(12):
        lines.append(f"| {count} | {color} |")
    lines += ["", "## Parse issues", ""]
    lines.extend(errors or ["None."])
    lines += [
        "",
        "> This audit compares exact pathData strings. It separates first-layer reuse from later-layer reuse, but does not compare rendered pixels, recognize app symbols, or judge aesthetics, visual balance, or Nova Launcher rendering.",
        "",
    ]
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(ROOT)} from {parsed}/{len(files)} icon vectors.")
    print(f"Repeated first-layer groups: {len(repeated_first)}; later-layer groups: {len(repeated_later)}.")
    if errors:
        raise SystemExit(f"{len(errors)} vector parse issue(s); see report.")


if __name__ == "__main__":
    main()
