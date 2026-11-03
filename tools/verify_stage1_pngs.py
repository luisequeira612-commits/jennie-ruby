#!/usr/bin/env python3
"""Verify regenerated Stage 1 pixels against the immutable historical workflow artifact."""
from __future__ import annotations

import hashlib
import struct
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / "docs/hashes-etapa1.txt"
NAMES = (
    "ruby_camara.png", "ruby_configuracion.png", "ruby_galeria.png",
    "ruby_google.png", "ruby_google_play_store.png", "ruby_instagram.png",
    "ruby_spotify.png", "ruby_tiktok.png", "ruby_whatsapp.png", "ruby_youtube.png",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def png_chunks(path: Path) -> dict[str, list[str]]:
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Not a PNG file: {path}")
    pos = 8
    chunks: dict[str, list[str]] = {}
    while pos + 12 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        kind = data[pos + 4:pos + 8].decode("ascii", "replace")
        payload = data[pos + 8:pos + 8 + length]
        chunks.setdefault(kind, []).append(hashlib.sha256(payload).hexdigest())
        pos += length + 12
        if kind == "IEND":
            break
    return chunks


def pixel_difference_count(left: Path, right: Path) -> tuple[int, tuple[int, int], tuple[int, int]]:
    with Image.open(left) as image:
        a = image.convert("RGBA")
    with Image.open(right) as image:
        b = image.convert("RGBA")
    size_a, size_b = a.size, b.size
    width, height = max(a.width, b.width), max(a.height, b.height)
    if a.size != (width, height):
        padded = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        padded.alpha_composite(a, (0, 0))
        a = padded
    if b.size != (width, height):
        padded = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        padded.alpha_composite(b, (0, 0))
        b = padded
    raw_a, raw_b = a.tobytes(), b.tobytes()
    differing = sum(
        1 for offset in range(0, len(raw_a), 4)
        if raw_a[offset:offset + 4] != raw_b[offset:offset + 4]
    )
    return differing, size_a, size_b


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_stage1_pngs.py HISTORICAL_ARTIFACT_DIRECTORY")
    historical_root = Path(sys.argv[1])
    expected = {}
    for line in HASH_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, filename = line.split(None, 1)
        expected[filename.strip()] = digest

    failures = []
    metadata_only = []
    for filename in NAMES:
        if filename not in expected:
            failures.append(f"{filename}: missing SHA-256 reference")
            continue
        candidates = list(historical_root.rglob(filename))
        if len(candidates) != 1:
            failures.append(f"{filename}: expected exactly one historical PNG, found {len(candidates)}")
            continue
        old = candidates[0]
        new = ROOT / "app/src/main/res/drawable-nodpi" / filename
        if not new.is_file():
            failures.append(f"{filename}: regenerated PNG is missing")
            continue
        old_hash, new_hash = sha256(old), sha256(new)
        if old_hash == expected[filename] and new_hash == expected[filename]:
            print(f"PASS {filename}: SHA-256 identical")
            continue

        count, old_size, new_size = pixel_difference_count(old, new)
        if count:
            failures.append(
                f"{filename}: {count} differing RGBA pixels "
                f"(historical {old_size}, generated {new_size}; "
                f"historical SHA {old_hash}; generated SHA {new_hash})"
            )
            continue

        old_chunks, new_chunks = png_chunks(old), png_chunks(new)
        changed_metadata = sorted(
            kind for kind in set(old_chunks) | set(new_chunks)
            if kind not in {"IHDR", "IDAT", "IEND", "PLTE"}
            and old_chunks.get(kind) != new_chunks.get(kind)
        )
        encoding_changed = old_chunks.get("IDAT") != new_chunks.get("IDAT")
        details = []
        if changed_metadata:
            details.append("metadata chunks changed: " + ", ".join(changed_metadata))
        if encoding_changed:
            details.append("IDAT/compression encoding changed")
        if old_size != new_size:
            details.append(f"canvas dimensions changed {old_size} -> {new_size}, but padded RGBA pixels match")
        if not details:
            details.append("PNG container/chunk representation changed")
        message = f"{filename}: RGBA pixels identical; " + "; ".join(details)
        metadata_only.append(message)
        print("ACCEPT " + message)

    if failures:
        print("REJECT: Stage 1 pixel integrity check failed:")
        for failure in failures:
            print(" - " + failure)
        raise SystemExit(1)
    print("PASS: all ten Stage 1 icons preserve their historical RGBA pixels.")
    if metadata_only:
        print("NOTICE: SHA-256 differed for pixel-identical PNGs; see ACCEPT lines above.")


if __name__ == "__main__":
    main()
