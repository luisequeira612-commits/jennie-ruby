#!/usr/bin/env bash
set -euo pipefail

# Pinned immutable Google Fonts revision. The downloaded fonts are bundled in the APK.
FONT_REV="2fe1e8c6b137fb13041a7cfca6fdcd8a910ea4dc"
BASE="https://raw.githubusercontent.com/google/fonts/${FONT_REV}/ofl"
FONT_DIR="app/src/main/res/font"
LICENSE_DIR="app/src/main/assets/fonts/licenses"

mkdir -p "$FONT_DIR" "$LICENSE_DIR"

download() {
  local url="$1"
  local destination="$2"
  curl --fail --location --retry 3 --retry-delay 2 --connect-timeout 20 "$url" --output "$destination"
  test -s "$destination" || { echo "Missing or empty font asset: $destination" >&2; exit 1; }
}

download "$BASE/playfairdisplay/PlayfairDisplay%5Bwght%5D.ttf" "$FONT_DIR/playfair_display.ttf"
download "$BASE/cormorantgaramond/CormorantGaramond%5Bwght%5D.ttf" "$FONT_DIR/cormorant_garamond.ttf"
download "$BASE/allura/Allura-Regular.ttf" "$FONT_DIR/allura.ttf"

download "$BASE/playfairdisplay/OFL.txt" "$LICENSE_DIR/OFL-PlayfairDisplay.txt"
download "$BASE/cormorantgaramond/OFL.txt" "$LICENSE_DIR/OFL-CormorantGaramond.txt"
download "$BASE/allura/OFL.txt" "$LICENSE_DIR/OFL-Allura.txt"

echo "PASS: three OFL fonts and their license texts downloaded from Google Fonts revision $FONT_REV."
