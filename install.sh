#!/usr/bin/env bash
# Haiku / BeOS Theme für KDE Plasma 6 – Installation
#
#   ./install.sh              alles bauen, installieren und anwenden
#   ./install.sh --no-build   nur Daten (Farben, Plasma-Stil, Icons, Cursor, Aurorae, globales Theme)
#   ./install.sh --layout     zusätzlich das Panel-Layout (Deskbar oben, blauer Desktop) setzen
#   ./install.sh --no-apply   nur installieren, nichts aktivieren
set -euo pipefail

SRC="$(cd "$(dirname "$0")" && pwd)"
DATA="${XDG_DATA_HOME:-$HOME/.local/share}"
BUILD=1; APPLY=1; LAYOUT=0
for a in "$@"; do
    case "$a" in
        --no-build) BUILD=0 ;;
        --no-apply) APPLY=0 ;;
        --layout)   LAYOUT=1 ;;
        -h|--help)  sed -n '2,9p' "$0"; exit 0 ;;
        *) echo "Unbekannte Option: $a"; exit 1 ;;
    esac
done

say() { printf '\033[1;33m==>\033[0m %s\n' "$*"; }
KW=$(command -v kwriteconfig6 || true)

# ---------------------------------------------------------------- C++ plugins
STYLE_OK=0; DECO_OK=0
if [ "$BUILD" = 1 ]; then
    if command -v pacman >/dev/null; then
        say "Prüfe Build-Abhängigkeiten (pacman)…"
        missing=$(pacman -T base-devel cmake qt6-base kdecoration kcoreaddons extra-cmake-modules 2>/dev/null || true)
        if [ -n "$missing" ]; then
            say "Installiere fehlende Pakete: $missing"
            sudo pacman -S --needed $missing
        fi
    fi
    if pacman -Q haiku-plasma-theme-plugins >/dev/null 2>&1; then
        say "Anwendungsstil ist als Paket haiku-plasma-theme-plugins installiert – wird nicht gebaut."
        STYLE_OK=1
    else
    say "Baue Qt6-Anwendungsstil »Haiku«…"
    if cmake -S "$SRC/style" -B "$SRC/build/style" -DCMAKE_BUILD_TYPE=Release >/dev/null &&
       cmake --build "$SRC/build/style" -j"$(nproc)"; then
        sudo cmake --install "$SRC/build/style" && STYLE_OK=1
    else
        echo "!! Anwendungsstil konnte nicht gebaut werden."
    fi
    fi
    if pacman -Q haiku-plasma-theme-plugins >/dev/null 2>&1; then
        say "Fensterdekoration ist als Paket haiku-plasma-theme-plugins installiert – wird nicht gebaut."
        DECO_OK=1
    else
    say "Baue Fensterdekoration »Haiku« (KDecoration3)…"
    if cmake -S "$SRC/decoration" -B "$SRC/build/decoration" -DCMAKE_BUILD_TYPE=Release >/dev/null &&
       cmake --build "$SRC/build/decoration" -j"$(nproc)"; then
        sudo cmake --install "$SRC/build/decoration" && DECO_OK=1
    else
        echo "!! Dekoration konnte nicht gebaut werden – Aurorae-Fallback wird verwendet."
    fi
    fi
fi

# ---------------------------------------------------------------- data files
say "Installiere Daten nach $DATA …"
mkdir -p "$DATA/color-schemes" "$DATA/plasma/desktoptheme" "$DATA/plasma/look-and-feel" \
         "$DATA/icons" "$DATA/aurorae/themes"
cp -f  "$SRC/colors/HaikuR1.colors"                 "$DATA/color-schemes/"
rm -rf "$DATA/plasma/desktoptheme/haiku" "$DATA/plasma/look-and-feel/org.haiku.desktop" \
       "$DATA/icons/Haiku" "$DATA/icons/Haiku-Cursors" "$DATA/aurorae/themes/Haiku"
cp -a  "$SRC/plasma/desktoptheme/haiku"             "$DATA/plasma/desktoptheme/"
cp -a  "$SRC/plasma/look-and-feel/org.haiku.desktop" "$DATA/plasma/look-and-feel/"
cp -a  "$SRC/icons/Haiku"                           "$DATA/icons/"
cp -a  "$SRC/cursors/Haiku-Cursors"                 "$DATA/icons/"
cp -a  "$SRC/aurorae/themes/Haiku"                  "$DATA/aurorae/themes/"
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -q -f "$DATA/icons/Haiku" 2>/dev/null || true

# Is the compiled decoration available (now or from an earlier run)?
if [ "$DECO_OK" = 0 ]; then
    d="$(qtpaths6 --plugin-dir 2>/dev/null || echo /usr/lib/qt6/plugins)"
    if [ -e "$d/org.kde.kdecoration3/org.haiku.decoration.so" ]; then DECO_OK=1; fi
fi

# ---------------------------------------------------------------- apply
if [ "$APPLY" = 1 ]; then
    say "Wende globales Theme an…"
    if [ "$LAYOUT" = 1 ]; then
        plasma-apply-lookandfeel -a org.haiku.desktop --resetLayout || true
    else
        plasma-apply-lookandfeel -a org.haiku.desktop || true
    fi
    if [ -n "$KW" ]; then
        # Haiku-Knöpfe: Schließen links, (Minimieren +) Zoom rechts; Doppelklick minimiert
        $KW --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnLeft "X"
        $KW --file kwinrc --group org.kde.kdecoration2 --key ButtonsOnRight "IA"
        $KW --file kwinrc --group Windows --key TitlebarDoubleClickCommand "Minimize"
        if [ "$DECO_OK" = 1 ]; then
            $KW --file kwinrc --group org.kde.kdecoration2 --key library "org.haiku.decoration"
            $KW --file kwinrc --group org.kde.kdecoration2 --key theme "Haiku"
        else
            $KW --file kwinrc --group org.kde.kdecoration2 --key library "org.kde.kwin.aurorae"
            $KW --file kwinrc --group org.kde.kdecoration2 --key theme "__aurorae__svg__Haiku"
        fi
        # Plasma-Stil, Cursor und Icons explizit setzen (falls der Global-Theme-Dialog Teile auslässt)
        $KW --file plasmarc --group Theme --key name haiku
        $KW --file kcminputrc --group Mouse --key cursorTheme Haiku-Cursors
        $KW --file kdeglobals --group Icons --key Theme Haiku
        if [ "$STYLE_OK" = 1 ] || ls "$(qtpaths6 --plugin-dir 2>/dev/null || echo /usr/lib/qt6/plugins)"/styles/libhaikustyle.so >/dev/null 2>&1; then
            $KW --file kdeglobals --group KDE --key widgetStyle Haiku
        fi
    fi
    command -v plasma-apply-colorscheme >/dev/null && plasma-apply-colorscheme HaikuR1 >/dev/null || true
    command -v plasma-apply-cursortheme >/dev/null && plasma-apply-cursortheme Haiku-Cursors >/dev/null || true
    command -v plasma-apply-desktoptheme >/dev/null && plasma-apply-desktoptheme haiku >/dev/null || true
    (qdbus6 org.kde.KWin /KWin reconfigure || qdbus org.kde.KWin /KWin reconfigure) >/dev/null 2>&1 || true
fi

say "Fertig."
[ "$DECO_OK" = 1 ] && echo "   Fensterdekoration: Haiku (C++)" || echo "   Fensterdekoration: Haiku (Aurorae-Fallback)"
[ "$STYLE_OK" = 1 ] && echo "   Anwendungsstil: Haiku – laufende Programme bitte neu starten."
echo "   Für Cursor und Anwendungsstil überall: einmal ab- und wieder anmelden."
