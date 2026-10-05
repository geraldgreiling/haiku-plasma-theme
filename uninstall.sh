#!/usr/bin/env bash
# Entfernt das Haiku-Theme und schaltet auf Breeze zurück.
set -uo pipefail
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
SRC="$(cd "$(dirname "$0")" && pwd)"

plasma-apply-lookandfeel -a org.kde.breeze.desktop 2>/dev/null
if command -v kwriteconfig6 >/dev/null; then
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key library org.kde.breeze
    kwriteconfig6 --file kwinrc --group org.kde.kdecoration2 --key theme Breeze
    kwriteconfig6 --file kwinrc --group Windows --key TitlebarDoubleClickCommand Maximize
    kwriteconfig6 --file kdeglobals --group KDE --key widgetStyle Breeze
fi
(qdbus6 org.kde.KWin /KWin reconfigure || true) >/dev/null 2>&1

rm -rf "$DATA/plasma/desktoptheme/haiku" "$DATA/plasma/look-and-feel/org.haiku.desktop" \
       "$DATA/icons/Haiku" "$DATA/icons/Haiku-Cursors" "$DATA/aurorae/themes/Haiku" \
       "$DATA/color-schemes/HaikuR1.colors"

for m in "$SRC/build/style/install_manifest.txt" "$SRC/build/decoration/install_manifest.txt"; do
    [ -f "$m" ] && xargs -a "$m" sudo rm -f
done
echo "Haiku-Theme entfernt. Bitte ab- und wieder anmelden."
