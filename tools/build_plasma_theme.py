#!/usr/bin/env python3
"""Generates the Haiku Plasma style (desktoptheme) SVGs.

Every frame is built from 1px "rings" (outer -> inner) plus a centre fill, which
matches Haiku's pixel bevels and gives FrameSvg pixel-exact slices.
"""
import json
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "plasma/desktoptheme/haiku"


def tint(c, t):
    f = (lambda v: 255 - (255 - v) * t) if t < 1 else (lambda v: v * (2 - t))
    return tuple(max(0, min(255, int(f(v)))) for v in c)


def hx(c):
    if c is None:
        return None
    if len(c) == 4:
        return "rgba(%d,%d,%d,%.3f)" % c
    return "#%02x%02x%02x" % c


PANEL = (216, 216, 216)
WHITE = (255, 255, 255)
NAV = (0, 0, 229)
TIP = (255, 255, 216)
YELLOW = (255, 203, 0)

# ring helpers: (top, left, bottom, right)
def solid(c):
    return (c, c, c, c)


def raised(base, lt=0.25, dk=1.15):
    return (tint(base, lt), tint(base, lt), tint(base, dk), tint(base, dk))


def sunken(base, lt=0.25, dk=1.15):
    return (tint(base, dk), tint(base, dk), tint(base, lt), tint(base, lt))


class Svg:
    def __init__(self):
        self.parts = []
        self.y = 0

    def rect(self, x, y, w, h, color):
        if color is None or w <= 0 or h <= 0:
            return ""
        return '<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x, y, w, h, hx(color))

    def frame(self, prefix, rings, fill, margins=None, mid=12, extra_hints=()):
        """Adds the nine elements of one FrameSvg prefix."""
        n = max(1, len(rings))
        p = (prefix + "-") if prefix else ""
        ox, oy = 2, self.y + 2
        size = 2 * n + mid
        X = [ox, ox + n, ox + n + mid]
        Y = [oy, oy + n, oy + n + mid]
        W = [n, mid, n]
        names = [["topleft", "top", "topright"], ["left", "center", "right"],
                 ["bottomleft", "bottom", "bottomright"]]
        for row in range(3):
            for col in range(3):
                x0, y0, w, h = X[col], Y[row], W[col], W[row]
                content = []
                if fill is not None or (row == 1 and col == 1):
                    content.append(self.rect(x0, y0, w, h, fill))
                # draw rings that intersect this slice
                for i, (ct, cl, cb, cr) in enumerate(rings):
                    # ring i occupies: top line y=oy+i, x in [ox+i, ox+size-i)
                    segs = [
                        (ox + i, oy + i, size - 2 * i, 1, ct),               # top
                        (ox + i, oy + i, 1, size - 2 * i, cl),               # left
                        (ox + i, oy + size - 1 - i, size - 2 * i, 1, cb),    # bottom
                        (ox + size - 1 - i, oy + i, 1, size - 2 * i, cr),    # right
                    ]
                    for sx, sy, sw, sh, c in segs:
                        ix0, iy0 = max(sx, x0), max(sy, y0)
                        ix1, iy1 = min(sx + sw, x0 + w), min(sy + sh, y0 + h)
                        if ix1 > ix0 and iy1 > iy0:
                            content.append(self.rect(ix0, iy0, ix1 - ix0, iy1 - iy0, c))
                if not any(content):
                    content.append('<rect x="%g" y="%g" width="%g" height="%g" fill="none"/>' % (x0, y0, w, h))
                self.parts.append('<g id="%s%s">%s</g>' % (p, names[row][col], "".join(content)))
        hx0 = ox + size + 4
        if margins is not None:
            t, l, b, r = margins
            self.parts.append('<rect id="%shint-top-margin" x="%d" y="%d" width="4" height="%d" fill="none"/>' % (p, hx0, oy, t))
            self.parts.append('<rect id="%shint-bottom-margin" x="%d" y="%d" width="4" height="%d" fill="none"/>' % (p, hx0 + 6, oy, b))
            self.parts.append('<rect id="%shint-left-margin" x="%d" y="%d" width="%d" height="4" fill="none"/>' % (p, hx0 + 12, oy, l))
            self.parts.append('<rect id="%shint-right-margin" x="%d" y="%d" width="%d" height="4" fill="none"/>' % (p, hx0 + 12, oy + 6, r))
        for h in extra_hints:
            self.parts.append('<rect id="%s" x="%d" y="%d" width="2" height="2" fill="none"/>' % (h, hx0 + 30, oy))
        self.y += size + 8

    def raw(self, s):
        self.parts.append(s)

    def save(self, path):
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        h = max(self.y + 4, 40)
        with open(full, "w") as f:
            f.write('<svg xmlns="http://www.w3.org/2000/svg" width="140" height="%d" viewBox="0 0 140 %d">\n' % (h, h))
            f.write("\n".join(self.parts))
            f.write("\n</svg>\n")


def panel_like(path, fill, border, margins, bevel=True):
    s = Svg()
    rings = [solid(border)] + ([raised(fill)] if bevel else [])
    s.frame("", rings, fill, margins)
    s.save(path)


# --- panel (Deskbar look) -------------------------------------------------
panel_like("widgets/panel-background.svg", PANEL, tint(PANEL, 1.42), (4, 4, 4, 4))
# --- dialogs, desktop widgets, tooltips -----------------------------------
panel_like("dialogs/background.svg", PANEL, tint(PANEL, 1.6), (6, 6, 6, 6))
panel_like("widgets/background.svg", PANEL, tint(PANEL, 1.5), (8, 8, 8, 8))
panel_like("widgets/translucentbackground.svg", PANEL, tint(PANEL, 1.5), (8, 8, 8, 8))
panel_like("widgets/tooltip.svg", TIP, tint(TIP, 1.7), (4, 6, 4, 6), bevel=False)

# --- task manager -----------------------------------------------------------
s = Svg()
btn = tint(PANEL, 0.5)
s.frame("normal", [solid(tint(PANEL, 1.25)), raised(btn, 0.2, 1.08)], btn, (3, 4, 3, 4))
s.frame("hover", [solid(tint(PANEL, 1.35)), raised(tint(PANEL, 0.3), 0.1, 1.05)], tint(PANEL, 0.3), (3, 4, 3, 4))
s.frame("focus", [solid(tint(PANEL, 1.45)), sunken(tint(PANEL, 1.08), 0.4, 1.2)], tint(PANEL, 1.08), (3, 4, 3, 4))
s.frame("attention", [solid(tint(YELLOW, 1.4)), raised(YELLOW, 0.3, 1.1)], tint(YELLOW, 0.6), (3, 4, 3, 4))
s.frame("minimized", [solid(tint(PANEL, 1.15))], None, (3, 4, 3, 4))
s.frame("progress", [solid(tint((50, 150, 255), 1.3))], tint((50, 150, 255), 0.5), (3, 4, 3, 4))
# group expander arrows
ar = hx(tint(PANEL, 1.7))
s.raw('<g id="group-expander-top"><rect x="100" y="0" width="10" height="6" fill="none"/><path d="M100 6 L105 1 L110 6Z" fill="%s"/></g>' % ar)
s.raw('<g id="group-expander-bottom"><rect x="100" y="10" width="10" height="6" fill="none"/><path d="M100 10 L105 15 L110 10Z" fill="%s"/></g>' % ar)
s.raw('<g id="group-expander-left"><rect x="114" y="0" width="6" height="10" fill="none"/><path d="M120 0 L115 5 L120 10Z" fill="%s"/></g>' % ar)
s.raw('<g id="group-expander-right"><rect x="124" y="0" width="6" height="10" fill="none"/><path d="M124 0 L129 5 L124 10Z" fill="%s"/></g>' % ar)
s.save("widgets/tasks.svg")

# --- list/view items (Kickoff, KRunner, …) ---------------------------------
s = Svg()
SEL = (190, 190, 190)
s.frame("normal", [solid((0, 0, 0, 0))], None, (2, 4, 2, 4))
s.frame("hover", [solid(tint(PANEL, 1.25))], tint(PANEL, 0.55), (2, 4, 2, 4))
s.frame("selected", [solid(tint(SEL, 1.35)), sunken(SEL, 0.6, 1.08)], SEL, (2, 4, 2, 4))
s.frame("selected+hover", [solid(tint(SEL, 1.45)), sunken(tint(SEL, 1.05), 0.6, 1.1)], tint(SEL, 1.05), (2, 4, 2, 4))
s.save("widgets/viewitem.svg")

# --- frames -------------------------------------------------------------------
s = Svg()
s.frame("sunken", [sunken(PANEL, 0.2, 1.15), solid(tint(PANEL, 1.4))], tint(PANEL, 0.6), (3, 3, 3, 3))
s.frame("plain", [solid(tint(PANEL, 1.3))], None, (2, 2, 2, 2))
s.frame("raised", [solid(tint(PANEL, 1.42)), raised(PANEL)], PANEL, (3, 3, 3, 3))
s.save("widgets/frame.svg")

# --- push / tool buttons ------------------------------------------------------
s = Svg()
B = (232, 232, 232)
bd = tint(B, 1.55)
m = (5, 7, 5, 7)
s.frame("normal", [solid(bd), raised(tint(B, 0.5), 0.0, 1.05)], tint(B, 0.6), m)
s.frame("hover", [solid(bd), raised(tint(B, 0.25), 0.0, 1.03)], tint(B, 0.3), m)
s.frame("pressed", [solid(bd), sunken(tint(B, 1.1), 0.7, 1.22)], tint(B, 1.12), m)
s.frame("focus", [solid(bd), solid(NAV)], tint(B, 0.6), m)
s.frame("toolbutton-hover", [solid(bd), raised(tint(B, 0.3), 0.0, 1.03)], tint(B, 0.35), m)
s.frame("toolbutton-pressed", [solid(bd), sunken(tint(B, 1.1), 0.7, 1.22)], tint(B, 1.12), m)
s.frame("toolbutton-focus", [solid(bd), solid(NAV)], tint(B, 0.6), m)
s.save("widgets/button.svg")

# --- line edits -----------------------------------------------------------------
s = Svg()
s.frame("base", [sunken(PANEL, 0.25, 1.12), solid(tint(PANEL, 1.45))], WHITE, (4, 4, 4, 4),
        extra_hints=("hint-focus-over-base",))
s.frame("hover", [solid((0, 0, 0, 0)), solid((102, 152, 203))], None, (4, 4, 4, 4))
s.frame("focus", [solid((0, 0, 0, 0)), solid(NAV)], None, (4, 4, 4, 4))
s.frame("focusframe", [solid((0, 0, 0, 0)), solid(NAV)], None, (4, 4, 4, 4))
s.save("widgets/lineedit.svg")

# --- plasmoid headings (popup header/footer) ------------------------------------
s = Svg()
s.frame("header", [(tint(PANEL, 0.4), PANEL, tint(PANEL, 1.4), PANEL)], tint(PANEL, 0.7), (4, 6, 4, 6))
s.frame("footer", [(tint(PANEL, 1.4), PANEL, PANEL, PANEL)], tint(PANEL, 0.85), (4, 6, 4, 6))
s.raw('<rect id="hint-stretch-borders" x="130" y="0" width="2" height="2" fill="none"/>')
s.save("widgets/plasmoidheading.svg")

# --- metadata & config ----------------------------------------------------------
os.makedirs(OUT, exist_ok=True)
meta = {
    "KPackageStructure": "Plasma/Theme",
    "KPlugin": {
        "Id": "haiku",
        "Name": "Haiku",
        "Description": "Plasma style inspired by the Haiku / BeOS desktop",
        "Description[de]": "Plasma-Stil im Stil der Haiku-/BeOS-Oberfläche",
        "Authors": [{"Name": "Gerald Greiling"}],
        "License": "MIT",
        "Version": "1.0.0",
        "Website": "https://github.com/geraldgreiling/haiku-plasma-theme",
        "Category": "",
    },
    "X-Plasma-API": "5.0",
    "X-Plasma-API-Minimum-Version": "6.0",
}
with open(os.path.join(OUT, "metadata.json"), "w") as f:
    json.dump(meta, f, indent=4, ensure_ascii=False)
with open(os.path.join(OUT, "plasmarc"), "w") as f:
    f.write("[AdaptiveTransparency]\nenabled=false\n\n[ContrastEffect]\nenabled=false\n\n"
            "[BlurBehindEffect]\nenabled=false\n")
print("plasma theme ok")
