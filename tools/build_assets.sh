#!/usr/bin/env bash
# Regenerates all generated assets (SVG themes, icons, cursors, Aurorae fallback).
# Needs python3; cursors additionally need rsvg-convert and xcursorgen.
set -euo pipefail
cd "$(dirname "$0")/.."
python3 tools/build_plasma_theme.py plasma/desktoptheme/haiku
python3 tools/build_aurorae.py aurorae/themes/Haiku
rm -rf icons/Haiku && python3 tools/build_icons.py icons/Haiku
if command -v xcursorgen >/dev/null && command -v rsvg-convert >/dev/null; then
    rm -rf cursors/Haiku-Cursors && python3 tools/build_cursors.py cursors/Haiku-Cursors
else
    echo "xcursorgen/rsvg-convert fehlen – vorgefertigte Cursor bleiben unverändert."
fi
