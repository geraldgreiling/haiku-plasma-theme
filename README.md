# Haiku / BeOS Theme for KDE Plasma 6

A global Plasma 6 theme in the style of the Haiku R1 desktop: yellow window tabs, grey bevelled widgets, blue desktop.

![Preview](plasma/look-and-feel/org.haiku.desktop/contents/previews/fullscreenpreview.jpg)

## Components

| Component | Folder | Implementation |
|---|---|---|
| Global theme | `plasma/look-and-feel/org.haiku.desktop` | Defaults, Deskbar layout (panel at the top), splash screen with icons lighting up |
| Colours | `colors/HaikuR1.colors` | KDE colour scheme with Haiku's interface colours, including `[WM]` (yellow tab) |
| Application style | `style/` | Native Qt6 style plugin (C++, `QProxyStyle` based on Fusion) |
| Window decoration | `decoration/` | KDecoration3 plugin (C++): tab only as wide as the title, close button left, zoom right |
| Decoration (fallback) | `aurorae/themes/Haiku` | Aurorae SVG theme, no compiling needed (title bar spans the full width) |
| Plasma style | `plasma/desktoptheme/haiku` | Panel, dialogs, tooltips, task manager, buttons, text fields; everything else inherits from Breeze |
| Icons | `icons/Haiku` | 48 original icons (folders, places, drives, file types, core apps) + ~130 alias names, everything else inherits from Breeze |
| Cursors | `cursors/Haiku-Cursors` | Xcursor theme, 21 cursors + alias names, 24/32/48/64 px, animated busy cursor |

## Requirements

- Plasma **6.3 or newer** (the decoration uses the KDecoration3 API; checked against the headers of 6.3.0, 6.4.5 and the current development branch)
- For building (Arch / CachyOS): `sudo pacman -S --needed base-devel cmake qt6-base kdecoration kcoreaddons`
  – the install script checks this itself and asks before installing anything.

## Installation

**Arch / CachyOS / Manjaro:** ~~the compiled parts (window decoration and application style) are available as AUR package `haiku-plasma-theme-plugins`.~~ 
As new account registration on AUR is temporarily closed, I can't provide an AUR package currently. You can still install from source (see below) if you want the native application style and window decoration (which IMHO looks much better than the aurorae fallback).
Global theme, Plasma style, colour scheme, icons, cursors and the Aurorae decoration are available on [store.kde.org](https://store.kde.org) (search for "Haiku").

**From source:**

```bash
git clone https://github.com/geraldgreiling/haiku-plasma-theme.git
cd haiku-plasma-theme
./install.sh            # builds both plugins (sudo for the Qt plugin folders), installs and applies everything
./install.sh --layout   # same, plus panel layout and blue desktop (replaces your current panel!)
./install.sh --no-build # data parts only; the decoration falls back to Aurorae
```

Log out and back in afterwards so that cursors and the application style apply to all programs.

The parts can also be selected individually in *System Settings → Colors & Themes* (global theme "Haiku", application style "Haiku", Plasma style "Haiku", window decoration "Haiku", icons "Haiku", cursors "Haiku Cursors").

Uninstall: `./uninstall.sh`

## Haiku-like behaviour

- Buttons: close on the left, minimise + zoom on the right of the tab (`ButtonsOnLeft=X`, `ButtonsOnRight=IA`). Haiku itself has no minimise button; remove it under *Window Decorations → Titlebar Buttons* if you don't want it.
- Double-clicking the tab minimises the window (as in Haiku).
- Blue keyboard focus indicator (B_NAVIGATION_BASE_COLOR) on input fields, check marks drawn as a cross, scroll bars with arrows at both ends.

## Window decoration colours

The C++ decoration always draws the tab in Haiku yellow, regardless of the colour scheme. Reason: KWin ignores the `[WM]` section of a colour scheme as soon as it contains a `[Colors:Header]` set and then returns the grey header colour for both title bar *and* frame.
The colours can be changed in `~/.config/haikudecorationrc`:

```ini
[Colors]
ActiveTab=255,203,0
InactiveTab=232,232,232
ActiveFrame=224,224,224
InactiveFrame=232,232,232
ActiveText=0,0,0
InactiveText=80,80,80
# true = take the colours from the KWin colour scheme after all
UseColorScheme=false
```

Changes apply after `qdbus6 org.kde.KWin /KWin reconfigure` or when the next window opens.

## Distribution (~~AUR +~~ store.kde.org)

- ~~**AUR:** `haiku-plasma-theme-plugins` – window decoration and application style (C++), PKGBUILD in `aur/haiku-plasma-theme-plugins/`.~~
- **store.kde.org:** global theme, Plasma style, colour scheme, icons, cursors and the Aurorae decoration. `tools/build_store.sh` creates one folder per store entry in `dist/store/`, containing the file, screenshots and description text.
- Step-by-step instructions and upload order: `store/README.md`.
- `tools/set_github_user.sh <name>` replaces the GitHub user placeholder in the PKGBUILD, metadata and store texts.

All parts can also be installed without the store via "Install from File…" in System Settings, or with `kpackagetool6 -t Plasma/LookAndFeel -i Haiku-Global-Theme.tar.gz`.

## Known limitations

- Developed and tested on CachyOS (Arch) with Plasma 6; other distributions have not been tested.
- To the right of the tab the decoration is transparent, but KWin still treats it as the top border: clicking there starts a resize instead of passing the click through.
- Tabs cannot be moved with Shift-drag as in Haiku; no stacking/tiling via tabs.
- The Haiku colour values follow the defaults from Haiku's `InterfaceDefs.cpp` (e.g. tab 255/203/0, panel 216/216/216, desktop 51/102/152) as far as known; they have not been verified against the current Haiku source.
- No GTK theme: GTK programs only get the colours via Plasma's GTK integration.
- The icons only cover the core set; everything else comes from Breeze and looks stylistically different.
- A vertical Deskbar in the top right corner (Haiku's default) is impractical with Plasma's built-in tools, because the application launcher then takes up the full panel width. The layout therefore uses a horizontal Deskbar at the top (also an option in Haiku).

## Regenerating assets

Icons, cursors, Plasma style and the Aurorae fallback are generated with Python:

```bash
tools/build_assets.sh   # cursors additionally need rsvg-convert (librsvg) and xcursorgen (xorg-xcursorgen)
```

Widget gallery for testing the application style:

```bash
cmake -S style -B build/gallery -DBUILD_GALLERY=ON && cmake --build build/gallery
build/gallery/haiku-gallery /tmp/gallery.png
```

## License and notice

MIT. All artwork (icons, cursors, SVGs) is original and only inspired by Haiku; no Haiku or BeOS artwork has been copied, including logos. This is not an official project of Haiku, Inc.; "Haiku" and "BeOS" are trademarks of their respective owners.
