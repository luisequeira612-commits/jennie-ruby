#!/usr/bin/env python3
"""Verify generated Stage 1 PNGs against permanent SHA-256 baselines in the repository."""
from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HASH_FILE = ROOT / "docs/hashes-etapa1.txt"
OUTPUT_DIR = ROOT / "app/src/main/res/drawable-nodpi"
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


def main() -> None:
    expected = {}
    for line in HASH_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, filename = line.split(None, 1)
        expected[filename.strip()] = digest

    failures = []
    for filename in NAMES:
        baseline = expected.get(filename)
        if not baseline:
            failures.append(f"{filename}: missing SHA-256 baseline")
            continue
        generated = OUTPUT_DIR / filename
        if not generated.is_file():
            failures.append(f"{filename}: generated PNG is missing")
            continue
        actual = sha256(generated)
        if actual != baseline:
            failures.append(
                f"{filename}: SHA-256 mismatch "
                f"(expected {baseline}, generated {actual})"
            )
            continue
        print(f"PASS {filename}: SHA-256 matches the approved baseline")

    unexpected = sorted(set(expected) - set(NAMES))
    if unexpected:
        failures.append("unexpected baseline entries: " + ", ".join(unexpected))

    if failures:
        print("REJECT: Stage 1 PNG integrity check failed:")
        for failure in failures:
            print(" - " + failure)
        raise SystemExit(1)

    print("PASS: all ten Stage 1 PNGs exactly match permanent repository baselines.")


if __name__ == "__main__":
    main()
