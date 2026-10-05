#!/usr/bin/env bash
# Builds everything for store.kde.org into dist/store/<component>/:
#   archive + screenshots + description (store/*.md).
# Compiled parts (window decoration, application style) are distributed via
# the AUR package in aur/haiku-plasma-theme-plugins instead.
#
# Needs: tar, python3 + Pillow, rsvg-convert, g++ with Qt6 Gui+Svg (for screenshots).
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT=$(pwd)
OUT="$ROOT/dist/store"
rm -rf "$ROOT/dist"; mkdir -p "$OUT"
TAR=(tar --owner=0 --group=0 --numeric-owner --sort=name -czf)
PREV=$(mktemp -d)

# --- screenshots
python3 tools/previews/sheets.py "$ROOT" "$PREV" >/dev/null
if command -v g++ >/dev/null && pkg-config --exists Qt6Gui Qt6Svg 2>/dev/null; then
    g++ -std=c++17 -fPIC tools/previews/storepreviews.cpp $(pkg-config --cflags --libs Qt6Gui Qt6Svg) -o "$PREV/sp"
    QT_QPA_PLATFORM=offscreen "$PREV/sp" "$ROOT" "$PREV" 2>/dev/null
fi
cp plasma/look-and-feel/org.haiku.desktop/contents/previews/fullscreenpreview.jpg "$PREV/preview-global-theme.jpg"

pack() {  # pack <dir> <description.md> <screenshots...>
    local d="$OUT/$1" md="$2"; shift 2
    mkdir -p "$d"; cp "store/$md" "$d/BESCHREIBUNG.md"
    for s in "$@"; do [ -f "$PREV/$s" ] && cp "$PREV/$s" "$d/"; done
}

pack 1-global-theme global-theme.md preview-global-theme.jpg preview-plasma-style.png
(cd plasma/look-and-feel && "${TAR[@]}" "$OUT/1-global-theme/Haiku-Global-Theme.tar.gz" org.haiku.desktop)

pack 2-plasma-style plasma-style.md preview-plasma-style.png
(cd plasma/desktoptheme && "${TAR[@]}" "$OUT/2-plasma-style/Haiku-Plasma-Style.tar.gz" haiku)

pack 3-colors colors.md preview-colors.png
cp colors/HaikuR1.colors "$OUT/3-colors/"

pack 4-icons icons.md preview-icons.png preview-icons-sizes.png
(cd icons && "${TAR[@]}" "$OUT/4-icons/Haiku-Icons.tar.gz" Haiku)

pack 5-cursors cursors.md preview-cursors.png
(cd cursors && "${TAR[@]}" "$OUT/5-cursors/Haiku-Cursors.tar.gz" Haiku-Cursors)

pack 6-aurorae aurorae.md preview-aurorae.png
(cd aurorae/themes && "${TAR[@]}" "$OUT/6-aurorae/Haiku-Aurorae.tar.gz" Haiku)

rm -rf "$PREV"
find "$OUT" -type f | sort
