"""Haiku-style application icons for the KDE Gear applications (original artwork, MIT).

Loaded by build_icons.py: register(ns) receives build_icons' globals and adds
entries to its ICONS dict. Every app gets the names "<app>" and "org.kde.<app>"
plus known extra icon names.
"""
import math


def register(ns):
    Icon, tint, shadow, page, text_lines, badge, globe, box3d, monitor, gear, folder = (
        ns["Icon"], ns["tint"], ns["shadow"], ns["page"], ns["text_lines"], ns["badge"], ns["globe"],
        ns["box3d"], ns["monitor"], ns["gear"], ns["folder"])
    ICONS = ns["ICONS"]

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def dk(c, t=1.55):
        return tint(c, t)

    def txt(ic, x, y, s, size, col="#fff", stroke=None, weight="bold", rot=0, family="sans-serif"):
        st = ' stroke="%s" stroke-width="1" paint-order="stroke"' % stroke if stroke else ""
        tr = ' transform="rotate(%g %g %g)"' % (rot, x, y) if rot else ""
        ic.raw('<text x="%g" y="%g" font-family="%s" font-weight="%s" font-size="%g" fill="%s" '
               'text-anchor="middle"%s%s>%s</text>' % (x, y, family, weight, size, col, st, tr, s))

    def circ(ic, cx, cy, r, fill, stroke=None, sw=1.6):
        s = ' stroke="%s" stroke-width="%g"' % (stroke, sw) if stroke else ""
        ic.raw('<circle cx="%g" cy="%g" r="%g" fill="%s"%s/>' % (cx, cy, r, fill, s))

    def ball(ic, cx, cy, r, col, sw=1.4):
        circ(ic, cx, cy, r, ic.rgrad(tint(col, 0.35), col), dk(col), sw)

    def ell(ic, cx, cy, rx, ry, fill, stroke=None, sw=1.6):
        s = ' stroke="%s" stroke-width="%g"' % (stroke, sw) if stroke else ""
        ic.raw('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="%s"%s/>' % (cx, cy, rx, ry, fill, s))

    def quad(ic, pts, col, sw=1.8, grad=True, stroke=None):
        d = "M" + " L".join("%g %g" % p for p in pts) + " Z"
        fill = ic.grad(tint(col, 0.45), col, 0, 0, 0.4, 1) if grad else col
        ic.path(d, fill, stroke or dk(col), sw)

    def plate(ic, col, x=6, y=10, w=48, h=40, skew=4):
        """slightly tilted panel (screen, board, card base)"""
        quad(ic, [(x, y + skew), (x + w, y), (x + w + skew, y + h), (x + skew, y + h + skew)], col)

    def iso_board(ic, col, n=4, alt=None, cells=None):
        """board in perspective: (6,30)(32,16)(58,30)(32,46)"""
        shadow(ic, 32, 54, 26, 4)
        top = [(4, 30), (32, 15), (60, 30), (32, 45)]
        ic.path("M4 30 L32 45 L60 30 L60 35 L32 50 L4 35 Z", dk(col, 1.25), dk(col), 1.6)
        quad(ic, top, col)
        if alt:
            for i in range(n):
                for j in range(n):
                    if (i + j) % 2 == 0:
                        continue
                    p = lambda a, b: (4 + 28 * (a / n) + 28 * (b / n), 30 - 15 * (a / n) + 15 * (b / n))
                    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (*p(i, j), *p(i + 1, j), *p(i + 1, j + 1), *p(i, j + 1)), alt)
        else:
            for k in range(1, n):
                a = (4 + 28 * k / n, 30 - 15 * k / n)
                b = (32 + 28 * k / n, 45 - 15 * k / n)
                c = (4 + 28 * k / n, 30 + 15 * k / n)
                e = (32 + 28 * k / n, 15 + 15 * k / n)
                ic.path("M%g %g L%g %g M%g %g L%g %g" % (*a, *b, *c, *e), "none", dk(col, 1.35), 1)
        return lambda a, b: (4 + 28 * (a / n) + 28 * (b / n), 30 - 15 * (a / n) + 15 * (b / n))

    def disc_on(ic, pt, col, r=3.4):
        ell(ic, pt[0], pt[1] + 0.8, r * 1.2, r * 0.75, dk(col, 1.3))
        ell(ic, pt[0], pt[1], r * 1.2, r * 0.75, ic.rgrad(tint(col, 0.3), col), dk(col), 1)

    def card(ic, x, y, w, h, rot, sym="A", col="#d02020", back=False):
        tr = 'transform="rotate(%g %g %g)"' % (rot, x + w / 2, y + h)
        fill = ic.grad("#3060c0", "#183070") if back else ic.grad("#ffffff", "#e4e4e4")
        ic.raw('<g %s><rect x="%g" y="%g" width="%g" height="%g" rx="2.5" fill="%s" stroke="#333" stroke-width="1.5"/>'
               % (tr, x, y, w, h, fill))
        if not back:
            ic.raw('<text x="%g" y="%g" font-family="sans-serif" font-weight="bold" font-size="%g" fill="%s" '
                   'text-anchor="middle">%s</text>' % (x + w / 2, y + h * 0.66, h * 0.5, col, sym))
        else:
            ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="1.5" fill="none" stroke="#9ab4ff" stroke-width="1"/>'
                   % (x + 3, y + 3, w - 6, h - 6))
        ic.raw('</g>')

    def die(ic, x, y, s, pips, col="#ffffff"):
        quad(ic, [(x, y + s * 0.3), (x + s * 0.5, y), (x + s, y + s * 0.3), (x + s * 0.5, y + s * 0.6)], col, 1.4)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + s * 0.3, x + s * 0.5, y + s * 0.6, x + s * 0.5, y + s * 1.2,
                                                  x, y + s * 0.9), tint(col, 1.08), dk("#c0c0c0"), 1.4)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x + s * 0.5, y + s * 0.6, x + s, y + s * 0.3, x + s, y + s * 0.9,
                                                  x + s * 0.5, y + s * 1.2), tint(col, 1.18), dk("#c0c0c0"), 1.4)
        cx, cy = x + s * 0.5, y + s * 0.3
        offs = {1: [(0, 0)], 2: [(-0.18, 0), (0.18, 0)], 3: [(-0.22, 0), (0, 0), (0.22, 0)],
                4: [(-0.18, -0.08), (0.18, -0.08), (-0.18, 0.08), (0.18, 0.08)],
                5: [(-0.2, -0.08), (0.2, -0.08), (0, 0), (-0.2, 0.08), (0.2, 0.08)]}[pips]
        for ox, oy in offs:
            ell(ic, cx + ox * s, cy + oy * s * 1.4, s * 0.06, s * 0.04, "#222")

    def calendar(ic, col, x=10, y=10, w=44, h=44, num="12"):
        shadow(ic, x + w / 2 + 2, y + h + 4, w / 2, 3)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 4, x + w, y, x + w + 2, y + h, x + 2, y + h + 3),
                ic.grad("#ffffff", "#dcdcdc"), "#4a4a4a", 2)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 4, x + w, y, x + w + 0.6, y + 12, x + 0.6, y + 16),
                ic.grad(tint(col, 0.4), col), dk(col), 1.6)
        for i in range(4):
            ic.path("M%g %g l0 -6" % (x + 8 + i * 10, y + 6 - i * 0.9), "none", "#555", 2.2)
        txt(ic, x + w / 2 + 1, y + h - 4, num, 22, "#333")

    def clockface(ic, cx, cy, r, col="#f4f4f4", rim="#4a6fd0", h=-60, m=60):
        circ(ic, cx, cy, r, ic.rgrad(tint(rim, 0.3), rim), dk(rim), 2)
        circ(ic, cx, cy, r * 0.8, ic.rgrad("#ffffff", col), "#666", 1.2)
        for i in range(12):
            a = math.radians(i * 30)
            ic.path("M%g %g L%g %g" % (cx + math.sin(a) * r * 0.66, cy - math.cos(a) * r * 0.66,
                                       cx + math.sin(a) * r * 0.74, cy - math.cos(a) * r * 0.74), "none", "#444", 1.2)
        for ang, ln, w in ((h, 0.42, 2.6), (m, 0.62, 1.8)):
            a = math.radians(ang)
            ic.path("M%g %g L%g %g" % (cx, cy, cx + math.sin(a) * r * ln, cy - math.cos(a) * r * ln), "none", "#222", w)
        circ(ic, cx, cy, 1.6, "#c02020")

    def bubble(ic, col, x=6, y=8, w=46, h=32, tail_left=True):
        r = 6
        tx = x + 12 if tail_left else x + w - 20
        tip = tx + (2 if tail_left else 10)
        d = ("M%g %g H%g A%g %g 0 0 1 %g %g V%g A%g %g 0 0 1 %g %g H%g L%g %g L%g %g H%g A%g %g 0 0 1 %g %g V%g A%g %g 0 0 1 %g %g Z"
             % (x + r, y, x + w - r, r, r, x + w, y + r, y + h - r, r, r, x + w - r, y + h, tx + 8, tip, y + h + 9,
                tx, y + h, x + r, r, r, x, y + h - r, y + r, r, r, x + r, y))
        ic.path(d, ic.grad(tint(col, 0.4), col), dk(col), 2)

    def phone(ic, col="#3a3a3a", x=18, y=4, w=28, h=54, screen=None):
        shadow(ic, x + w / 2, y + h + 2, w / 2 + 2, 2.5)
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="5" fill="%s" stroke="#111" stroke-width="2"/>'
               % (x, y, w, h, ic.grad(tint(col, 0.6), col)))
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="1.5" fill="%s" stroke="#111" stroke-width="1"/>'
               % (x + 3, y + 6, w - 6, h - 14, screen or ic.grad("#9cd0ff", "#2a64b0")))
        circ(ic, x + w / 2, y + h - 4, 1.8, "#888")
        return (x + 3, y + 6, w - 6, h - 14)

    def magnifier(ic, cx, cy, r, glass="#9ad0ff"):
        ic.path("M%g %g L%g %g" % (cx + r * 0.7, cy + r * 0.7, cx + r * 1.7, cy + r * 1.7), "none", "#333", r * 0.55)
        ic.path("M%g %g L%g %g" % (cx + r * 0.95, cy + r * 0.95, cx + r * 1.6, cy + r * 1.6), "none", "#c08020", r * 0.4)
        circ(ic, cx, cy, r, ic.rgrad("#ffffff", glass), "#333", 2.2)
        ic.raw('<circle cx="%g" cy="%g" r="%g" fill="#fff" opacity="0.6"/>' % (cx - r * 0.35, cy - r * 0.35, r * 0.25))

    def book(ic, col, x=10, y=12, w=40, h=40):
        shadow(ic, x + w / 2 + 2, y + h + 4, w / 2 + 2, 3)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x + 4, y + 2, x + w + 4, y - 2, x + w + 4, y + h - 2, x + 4, y + h + 2),
                "#f8f8f0", "#555", 1.6)
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 4, x + w, y, x + w, y + h, x, y + h + 4),
                ic.grad(tint(col, 0.4), col, 0, 0, 1, 1), dk(col), 2)
        ic.path("M%g %g L%g %g" % (x + 5, y + 4, x + 5, y + h + 3), "none", dk(col, 1.25), 2)

    def openbook(ic, col="#ffffff", cover="#a0522d"):
        shadow(ic, 32, 56, 26, 3.5)
        ic.path("M4 18 Q18 12 32 18 Q46 12 60 18 L60 50 Q46 44 32 50 Q18 44 4 50 Z", cover, dk(cover), 2)
        ic.path("M6 16 Q19 10 32 16 L32 47 Q19 41 6 47 Z", ic.grad("#ffffff", "#e0e0d8"), "#666", 1.4)
        ic.path("M58 16 Q45 10 32 16 L32 47 Q45 41 58 47 Z", ic.grad("#ffffff", "#e0e0d8"), "#666", 1.4)
        for i in range(5):
            ic.path("M10 %g Q19 %g 28 %g" % (22 + i * 4.5, 18 + i * 4.5, 22 + i * 4.5), "none", "#999", 1)
            ic.path("M36 %g Q45 %g 54 %g" % (22 + i * 4.5, 18 + i * 4.5, 22 + i * 4.5), "none", "#999", 1)

    def envelope(ic, x=6, y=16, w=48, h=32, col="#ffffff"):
        ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 4, x + w, y, x + w + 3, y + h, x + 3, y + h + 4),
                ic.grad(col, "#d6d6d6", 0, 0, 1, 1), "#4a4a4a", 2)
        ic.path("M%g %g L%g %g L%g %g" % (x, y + 4, x + w / 2 + 2, y + h * 0.6, x + w, y), "none", "#4a4a4a", 1.8)

    def note(ic, x, y, s=1.0, col="#2a2a8a"):
        ic.path("M%g %g a%g %g -15 1 1 %g %g L%g %g L%g %g L%g %g a%g %g -15 1 1 %g %g L%g %g L%g %g Z"
                % (x, y, 4 * s, 3.2 * s, -1.4 * s, -1.4 * s, x - 1.4 * s, y - 16 * s, x + 12 * s, y - 19 * s,
                   x + 12 * s, y - 4 * s, 4 * s, 3.2 * s, -1.4 * s, -1.4 * s, x + 10.6 * s, y - 13 * s,
                   x, y - 11 * s), ic.grad(tint(col, 0.5), col), dk(col), 1)

    def arrow(ic, pts_dir, x, y, s, col="#3fae2f"):
        # simple fat arrow pointing down (dir="d"), up, right, left
        base = [(-3, -8), (3, -8), (3, 0), (7, 0), (0, 8), (-7, 0), (-3, 0)]
        rot = {"d": 0, "u": 180, "r": -90, "l": 90}[pts_dir]
        a = math.radians(rot)
        pts = [(x + (px * math.cos(a) - py * math.sin(a)) * s, y + (px * math.sin(a) + py * math.cos(a)) * s)
               for px, py in base]
        quad(ic, pts, col, 1.4)

    def gem(ic, cx, cy, r, col):
        pts = [(cx - r, cy - r * 0.3), (cx - r * 0.5, cy - r * 0.8), (cx + r * 0.5, cy - r * 0.8), (cx + r, cy - r * 0.3), (cx, cy + r)]
        quad(ic, pts, col, 1.2)
        ic.path("M%g %g L%g %g L%g %g" % (cx - r, cy - r * 0.3, cx + r, cy - r * 0.3, cx, cy + r), "none", tint(col, 0.3), 0.8)

    def tile(ic, x, y, col="#fbf6e6", sym=None, symcol="#2a7a2a", w=14, h=18):
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="%s" stroke="#5a4a2a" stroke-width="1.2"/>'
               % (x + 2, y + 2, w, h, "#3f8f4f"))
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="%s" stroke="#5a4a2a" stroke-width="1.2"/>'
               % (x, y, w, h, ic.grad("#ffffff", col)))
        if sym:
            sym(x + w / 2, y + h / 2)

    def grid(ic, x, y, w, h, n, m, col="#fff", line="#555", fills=None):
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="1.6"/>' % (x, y, w, h, col, line))
        cw, ch = w / n, h / m
        for (i, j), c in (fills or {}).items():
            ic.raw('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x + i * cw, y + j * ch, cw, ch, c))
        for i in range(1, n):
            ic.path("M%g %g L%g %g" % (x + i * cw, y, x + i * cw, y + h), "none", line, 0.8)
        for j in range(1, m):
            ic.path("M%g %g L%g %g" % (x, y + j * ch, x + w, y + j * ch), "none", line, 0.8)

    def screen_content(ic, sx, sy, sw, sh):
        return sx, sy, sw, sh

    def keyshape(ic, x, y, col="#e8b020", s=1.0):
        circ(ic, x, y, 7 * s, ic.rgrad(tint(col, 0.3), col), dk(col), 1.8)
        circ(ic, x, y, 2.6 * s, "#fff", dk(col), 1.2)
        ic.path("M%g %g L%g %g L%g %g M%g %g L%g %g" % (x + 6 * s, y + 3 * s, x + 22 * s, y + 11 * s, x + 20 * s, y + 15 * s,
                                                     x + 16 * s, y + 8 * s, x + 14 * s, y + 12 * s), "none", dk(col), 3 * s)
        ic.path("M%g %g L%g %g L%g %g M%g %g L%g %g" % (x + 6 * s, y + 3 * s, x + 22 * s, y + 11 * s, x + 20 * s, y + 15 * s,
                                                     x + 16 * s, y + 8 * s, x + 14 * s, y + 12 * s), "none", col, 1.6 * s)

    def padlock(ic, x, y, s=1.0, col="#e0b020"):
        ic.path("M%g %g v%g a%g %g 0 0 1 %g 0 v%g" % (x + 4 * s, y + 10 * s, -4 * s, 7 * s, 7 * s, 14 * s, 4 * s),
                "none", "#777", 3.2 * s)
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="%s" stroke-width="1.6"/>'
               % (x, y + 10 * s, 22 * s, 16 * s, 2.5 * s, ic.grad(tint(col, 0.35), col), dk(col)))
        circ(ic, x + 11 * s, y + 17 * s, 2.2 * s, "#333")

    def shield(ic, col, x=14, y=6, w=36, h=48):
        shadow(ic, x + w / 2, y + h + 3, w / 2, 3)
        ic.path("M%g %g Q%g %g %g %g Q%g %g %g %g Q%g %g %g %g Q%g %g %g %g Z"
                % (x + w / 2, y, x + w * 0.8, y + 6, x + w, y + 6, x + w, y + h * 0.55, x + w / 2, y + h,
                   x, y + h * 0.55, x, y + 6, x + w * 0.2, y + 6, x + w / 2, y), ic.grad(tint(col, 0.4), col, 0, 0, 1, 1),
                dk(col), 2.2)

    def tv(ic, screen_fill, x=6, y=12, w=52, h=36):
        shadow(ic, 32, 58, 24, 3)
        ic.path("M24 %g L18 %g M40 %g L46 %g" % (y + h + 2, y + h + 9, y + h + 2, y + h + 9), "none", "#333", 2.4)
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="4" fill="%s" stroke="#222" stroke-width="2"/>'
               % (x, y, w, h, ic.grad("#6a6a6a", "#2a2a2a")))
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="2" fill="%s" stroke="#111" stroke-width="1"/>'
               % (x + 4, y + 4, w - 8, h - 8, screen_fill))
        return (x + 4, y + 4, w - 8, h - 8)

    def mic(ic, x, y, s=1.0, col="#808890"):
        ic.raw('<rect x="%g" y="%g" width="%g" height="%g" rx="%g" fill="%s" stroke="#333" stroke-width="1.6"/>'
               % (x - 6 * s, y, 12 * s, 22 * s, 6 * s, ic.grad(tint(col, 0.2), col, 0, 0, 1, 0)))
        for i in range(3):
            ic.path("M%g %g h%g" % (x - 4 * s, y + (6 + 4 * i) * s, 8 * s), "none", "#555", 1)
        ic.path("M%g %g a%g %g 0 0 0 %g 0 M%g %g v%g M%g %g h%g" % (x - 9 * s, y + 14 * s, 9 * s, 10 * s, 18 * s,
                                                                 x, y + 28 * s, 6 * s, x - 7 * s, y + 34 * s, 14 * s),
                "none", "#333", 2.2 * s)

    def waves(ic, x, y, n=3, col="#3a7ad8", s=1.0):
        for i in range(n):
            r = (5 + i * 5) * s
            ic.path("M%g %g a%g %g 0 0 1 0 %g" % (x, y - r, r, r, 2 * r), "none", col, 2.2 * s)

    def person(ic, cx, cy, s=1.0, col="#4a7ad0"):
        circ(ic, cx, cy - 8 * s, 6 * s, ic.rgrad("#ffe0c0", "#e0a070"), "#7a4a20", 1.4)
        ic.path("M%g %g q%g %g %g 0 v%g h%g Z" % (cx - 11 * s, cy + 14 * s, 0, -16 * s, 22 * s, 0, -22 * s) if False else
                "M%g %g C%g %g %g %g %g %g Z" % (cx - 11 * s, cy + 12 * s, cx - 11 * s, cy - 2 * s, cx + 11 * s, cy - 2 * s,
                                                cx + 11 * s, cy + 12 * s), ic.grad(tint(col, 0.4), col), dk(col), 1.6)

    def spaceship(ic, x, y, rot, col):
        ic.raw('<g transform="rotate(%g %g %g)">' % (rot, x, y))
        quad(ic, [(x, y - 9), (x + 6, y + 7), (x, y + 4), (x - 6, y + 7)], col, 1.4)
        ic.raw('</g>')

    def robot(ic, cx, cy, col="#a0a8b8"):
        ic.path("M%g %g v-6" % (cx, cy - 16), "none", "#333", 2)
        circ(ic, cx, cy - 23, 2.4, "#e03030", "#600", 1)
        ic.raw('<rect x="%g" y="%g" width="28" height="22" rx="4" fill="%s" stroke="#333" stroke-width="2"/>'
               % (cx - 14, cy - 16, ic.grad(tint(col, 0.3), col)))
        circ(ic, cx - 6, cy - 6, 3.6, "#ffef60", "#333", 1.2)
        circ(ic, cx + 6, cy - 6, 3.6, "#ffef60", "#333", 1.2)
        ic.path("M%g %g h12" % (cx - 6, cy + 1), "none", "#333", 2)

    def ship(ic, y=36, col="#7a8898"):
        ic.path("M6 %g L58 %g L52 %g L12 %g Z" % (y, y, y + 12, y + 12), ic.grad(tint(col, 0.3), col), dk(col), 2)
        ic.path("M20 %g L20 %g L40 %g L40 %g Z" % (y, y - 8, y - 8, y), ic.grad("#d0d0d0", "#909090"), "#444", 1.6)
        ic.path("M26 %g L26 %g L32 %g L32 %g Z" % (y - 8, y - 16, y - 16, y - 8), "#555", "#222", 1.2)

    def plane(ic, cx, cy, s=1.0, col="#c8c8d0"):
        ic.path("M%g %g L%g %g L%g %g L%g %g L%g %g L%g %g L%g %g L%g %g L%g %g Z" % tuple(
            v for p in [(-20, 0), (-12, -2), (-2, -2), (6, -14), (11, -14), (6, -2), (18, -2), (22, 2), (-16, 3)]
            for v in (cx + p[0] * s, cy + p[1] * s)), ic.grad(tint(col, 0.2), col), "#333", 1.6)

    def bomb(ic, cx, cy, r):
        ball(ic, cx, cy, r, "#3a3a3a")
        ic.path("M%g %g q4 -8 10 -6" % (cx + r * 0.5, cy - r * 0.85), "none", "#7a5a2a", 2.2)
        circ(ic, cx + r * 0.5 + 10, cy - r * 0.85 - 6, 3, ic.rgrad("#ffff80", "#ff6000"))

    def flask(ic, x, y, col="#40c060"):
        ic.path("M%g %g v10 l-10 18 a3 3 0 0 0 3 4 h22 a3 3 0 0 0 3 -4 l-10 -18 v-10 Z" % (x - 4, y),
                "#eaf6ff", "#333", 1.8)
        ic.path("M%g %g l-6 11 a3 3 0 0 0 3 4 h22 a3 3 0 0 0 3 -4 l-6 -11 Z" % (x - 6, y + 17),
                ic.grad(tint(col, 0.3), col), dk(col), 1)

    def chart_bars(ic, x, y, vals, cols, w=6, gap=3, base=None):
        for i, (v, c) in enumerate(zip(vals, cols)):
            ic.raw('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" stroke="%s" stroke-width="1"/>'
                   % (x + i * (w + gap), y - v, w, v, ic.grad(tint(c, 0.4), c, 0, 0, 1, 0), dk(c)))

    def tomato(ic, cx, cy, r):
        ball(ic, cx, cy, r, "#e03a2a", 2)
        ic.path("M%g %g l4 -6 l3 5 l5 -3 l-1 6 l5 2 l-6 2 Z" % (cx - 8, cy - r + 3), "#3a9a2a", "#1a5a12", 1.2)

    def speaker(ic, x, y, s=1.0):
        quad(ic, [(x, y - 5 * s), (x + 6 * s, y - 5 * s), (x + 14 * s, y - 12 * s), (x + 14 * s, y + 12 * s),
                  (x + 6 * s, y + 5 * s), (x, y + 5 * s)], "#606870", 1.6)

    # ------------------------------------------------------------------
    # app definitions
    # ------------------------------------------------------------------
    APPS = {}

    def app(name, *extra):
        def deco(fn):
            APPS[name] = (fn, extra)
            return fn
        return deco

    # ---- education ----
    @app("artikulate")
    def _(ic):
        shadow(ic); bubble(ic, "#5ab0f0", 4, 6, 40, 30); txt(ic, 23, 27, "a e", 14, "#fff", "#1a4a80")
        mic(ic, 46, 22, 0.9)

    @app("blinken")
    def _(ic):
        shadow(ic)
        for (a0, col) in ((180, "#3a9a3a"), (270, "#d02a2a"), (0, "#2a5ad0"), (90, "#e8c020")):
            a1, a2 = math.radians(a0), math.radians(a0 + 90)
            ic.path("M%g %g L%g %g A22 22 0 0 1 %g %g Z" % (32 + 4 * math.cos(a1 + 0.78), 30 + 4 * math.sin(a1 + 0.78),
                                                           32 + 24 * math.cos(a1), 30 + 24 * math.sin(a1),
                                                           32 + 24 * math.cos(a2), 30 + 24 * math.sin(a2)),
                    ic.rgrad(tint(col, 0.3), col), dk(col), 1.6)
        circ(ic, 32, 30, 8, ic.rgrad("#ffffff", "#9a9a9a"), "#333", 1.6)

    @app("cantor")
    def _(ic):
        page(ic); ic.path("M18 22 L44 19 L46 48 L20 51 Z", "#1e2a3a", "#000", 1.2)
        txt(ic, 32, 42, "∑", 20, "#ffd040"); ic.path("M23 27 l4 2 l-4 2", "none", "#5f5", 1.4)

    @app("kalgebra")
    def _(ic):
        shadow(ic); plate(ic, "#f6f6ee", 6, 8, 48, 44)
        ic.path("M12 30 L54 27 M30 12 L32 54", "none", "#888", 1.2)
        ic.path("M12 44 C22 44 26 14 34 18 S44 40 52 22", "none", "#d03030", 2.6)
        txt(ic, 20, 22, "f(x)", 9, "#2a4ac0")

    @app("kalzium")
    def _(ic):
        shadow(ic)
        fills = {}
        cols = ["#7ab8f0", "#f0a060", "#a0d880", "#f07a9a"]
        for i in range(6):
            for j in range(4):
                if (j == 0 and 0 < i < 5) or (j == 1 and 1 < i < 4):
                    continue
                fills[(i, j)] = cols[(i + j) % 4]
        grid(ic, 6, 12, 52, 36, 6, 4, "none", "#444", fills)
        ic.raw('<rect x="34" y="24" width="17" height="15" fill="#ffe040" stroke="#333" stroke-width="2"/>')
        txt(ic, 42.5, 36, "Fe", 9, "#333")

    @app("kanagram")
    def _(ic):
        shadow(ic)
        for i, (ch, col) in enumerate((("A", "#e05050"), ("N", "#50a0e0"), ("G", "#50c060"))):
            x = 6 + i * 18
            box3d(ic, ic.grad(tint(col, 0.4), col), tint(col, 0.5), dk(col, 1.2), x, 26 - (i % 2) * 6, 14, 14, 5)
            txt(ic, x + 7, 37 - (i % 2) * 6, ch, 11)
        ic.path("M14 52 Q32 60 50 52", "none", "#333", 2); ic.path("M46 49 l4 3 l-5 2", "none", "#333", 2)

    @app("kbruch")
    def _(ic):
        shadow(ic); plate(ic, "#2f5a3a", 6, 10, 48, 40)
        txt(ic, 31, 27, "3", 15, "#fff"); ic.path("M22 31 L41 30", "none", "#fff", 2); txt(ic, 32, 46, "4", 15, "#fff")

    @app("kgeography")
    def _(ic):
        shadow(ic); globe(ic, 30, 32, 21)
        ic.path("M44 8 L44 34", "none", "#333", 2); quad(ic, [(44, 8), (58, 11), (44, 16)], "#e03030", 1.2)

    @app("khangman")
    def _(ic):
        shadow(ic); plate(ic, "#2f5a3a", 6, 10, 48, 40)
        txt(ic, 31, 36, "_ A _", 14, "#fff")

    @app("kig")
    def _(ic):
        shadow(ic); plate(ic, "#f6f6ee", 6, 10, 48, 40)
        ic.path("M14 46 L46 44 L28 16 Z", "none", "#2a5ad0", 2.2)
        circ(ic, 30, 36, 9, "none", "#d03030", 1.8)
        for p in ((14, 46), (46, 44), (28, 16)):
            circ(ic, p[0], p[1], 2.4, "#ffd040", "#333", 1)

    @app("kiten")
    def _(ic):
        book(ic, "#b03030"); circ(ic, 34, 32, 9, "#fff", dk("#b03030"), 1.4)
        ic.path("M29 27 h10 M34 24 v16 M29 33 h10", "none", "#222", 2)

    @app("klettres")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#ffd060", "#e8a020"), "#ffe8a0", "#c88010", 12, 22, 32, 30, 10)
        txt(ic, 28, 46, "a", 24, "#fff", "#7a4a00")

    @app("kmplot")
    def _(ic):
        shadow(ic); plate(ic, "#ffffff", 6, 8, 48, 44)
        for k in range(1, 6):
            ic.path("M%g 10 L%g 52 M8 %g L54 %g" % (6 + k * 8, 8 + k * 8, 10 + k * 7, 9 + k * 7), "none", "#cde", 0.8)
        ic.path("M10 31 L54 29 M31 12 L33 52", "none", "#444", 1.4)
        ic.path("M10 31 C16 16 22 16 28 30 S40 44 46 30 S52 18 54 22", "none", "#2a5ad0", 2.4)

    @app("kturtle")
    def _(ic):
        shadow(ic)
        ell(ic, 50, 34, 6, 5, "#7ac050", "#2a5a1a", 1.6)
        for (x, y) in ((16, 22), (16, 46), (44, 22), (44, 46)):
            ell(ic, x, y, 5, 3.5, "#7ac050", "#2a5a1a", 1.4)
        ell(ic, 30, 34, 20, 15, ic.rgrad("#a8e070", "#3a8a20"), "#1f4a12", 2)
        ic.path("M22 24 L38 24 L44 34 L38 44 L22 44 L16 34 Z", "none", "#1f4a12", 1.4)
        circ(ic, 52, 32, 1.2, "#000")

    @app("kwordquiz")
    def _(ic):
        shadow(ic)
        card(ic, 10, 14, 30, 38, -10, "?", "#2a5ad0"); card(ic, 24, 12, 30, 38, 8, "!", "#d03030")

    @app("marble")
    def _(ic):
        shadow(ic); globe(ic, 32, 32, 20)
        ell(ic, 32, 32, 28, 9, "none", "#e0a020", 2.4)
        ic.raw('<path d="M8 28 A28 9 0 0 1 56 28" fill="none" stroke="#fff" stroke-width="0" />')

    @app("minuet")
    def _(ic):
        shadow(ic)
        ic.path("M6 22 L58 18 L60 50 L8 54 Z", "#fff", "#333", 2)
        for i in range(1, 7):
            ic.path("M%g %g L%g %g" % (6 + i * 7.5, 21.4 - i * 0.55, 8 + i * 7.5, 53.6 - i * 0.55), "none", "#555", 1)
        for i in (0, 1, 3, 4, 5):
            x = 11 + i * 7.5
            ic.path("M%g %g l4 -0.3 l0.8 18 l-4 0.3 Z" % (x, 21 - i * 0.55), "#222")
        note(ic, 44, 14, 0.8, "#d03030")

    @app("parley")
    def _(ic):
        shadow(ic)
        card(ic, 8, 14, 30, 38, -8, "Aa", "#2a5ad0"); card(ic, 26, 12, 30, 38, 10, "Zz", "#3a9a3a")

    @app("rocs")
    def _(ic):
        shadow(ic)
        pts = [(14, 16), (48, 14), (32, 32), (12, 48), (52, 46)]
        for a, b in ((0, 2), (1, 2), (2, 3), (2, 4), (0, 3), (1, 4)):
            ic.path("M%g %g L%g %g" % (*pts[a], *pts[b]), "none", "#444", 2)
        for i, p in enumerate(pts):
            ball(ic, p[0], p[1], 6, ["#e05050", "#50a0e0", "#f0c030", "#50c060", "#a060d0"][i])

    @app("step")
    def _(ic):
        shadow(ic); ic.path("M8 8 L56 8", "none", "#555", 3)
        ic.path("M32 8 L44 40", "none", "#333", 1.8); ball(ic, 44, 42, 8, "#d04a3a")
        ic.path("M14 8 l0 6 l-4 3 l8 4 l-8 4 l8 4 l-4 3 l0 6", "none", "#666", 1.6); box3d(ic, "#7a9ad0", "#a8c0e8", "#4a6aa0", 8, 42, 12, 8, 4)

    @app("ktouch")
    def _(ic):
        shadow(ic, 32, 54, 28, 4)
        quad(ic, [(4, 34), (52, 20), (60, 34), (12, 50)], "#d8d8d8")
        for r in range(3):
            for c in range(6):
                x = 9 + c * 7.5 + r * 2.5
                y = 33 - c * 2.2 + r * 4.6
                ic.path("M%g %g l6 -1.8 l1.4 2.4 l-6 1.8 Z" % (x, y), "#fff" if (r, c) != (1, 3) else "#ffcb00", "#555", 0.9)

    @app("kalm")
    def _(ic):
        shadow(ic); circ(ic, 32, 30, 24, ic.rgrad("#d8f0ff", "#4a90d0"), "#1f4a7a", 2)
        for i in range(3):
            ic.path("M14 %g q6 -5 12 0 t12 0 t12 0" % (24 + i * 7), "none", "#fff", 2)

    # ---- games ----
    @app("bomber")
    def _(ic):
        shadow(ic); plane(ic, 30, 22, 1.2)
        bomb(ic, 30, 44, 7)

    @app("bovo")
    def _(ic):
        P = iso_board(ic, "#e8d090", 5)
        for (a, b, c) in ((1, 1, "#222"), (2, 2, "#222"), (3, 3, "#222"), (1, 3, "#fff"), (3, 1, "#fff")):
            p = P(a + 0.5, b + 0.5); disc_on(ic, p, c, 2.6)

    @app("granatier")
    def _(ic):
        shadow(ic); bomb(ic, 28, 38, 16)

    @app("kajongg")
    def _(ic):
        shadow(ic, 32, 54, 28, 3)
        for i, s in enumerate(("東", "南", "西", "北")):
            tile(ic, 5 + i * 14, 24, sym=lambda x, y, s=s: txt(ic, x, y + 4, ("E", "S", "W", "N")[("東南西北").index(s)], 10, "#222"),
                 w=12, h=18)

    @app("kapman")
    def _(ic):
        shadow(ic); plate(ic, "#1a1a6a", 6, 10, 48, 40)
        ic.path("M12 20 h36 M12 28 h10 M30 28 h18 M12 36 h24 M42 36 h6 M12 44 h36", "none", "#5a7aff", 2.4)
        for x in range(14, 50, 6):
            circ(ic, x, 24, 1.1, "#ffd0a0")
        ball(ic, 38, 40, 6, "#ffd020")

    @app("katomic")
    def _(ic):
        shadow(ic)
        ic.path("M20 22 L34 34 L48 22 M34 34 L34 50", "none", "#333", 3)
        ball(ic, 20, 22, 9, "#e04040"); ball(ic, 48, 22, 9, "#4070e0"); ball(ic, 34, 34, 8, "#f0f0f0"); ball(ic, 34, 50, 6, "#40b040")

    @app("kblackbox")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#4a4a4a", "#111"), "#6a6a6a", "#222", 14, 24, 32, 28, 10)
        ic.path("M2 30 L18 34", "none", "#ffcc00", 2.4); ic.path("M40 36 L60 18", "none", "#ffcc00", 2.4)
        quad(ic, [(60, 18), (54, 20), (58, 24)], "#ffcc00", 1)

    @app("kblocks")
    def _(ic):
        shadow(ic, 32, 58, 22, 3)
        cells = [((1, 0), "#e04040"), ((1, 1), "#e04040"), ((2, 1), "#e04040"), ((2, 2), "#e04040"),
                 ((0, 3), "#4070e0"), ((1, 3), "#4070e0"), ((2, 3), "#4070e0"), ((3, 3), "#f0c020"), ((3, 2), "#f0c020")]
        for (i, j), c in cells:
            ic.raw('<rect x="%g" y="%g" width="11" height="11" fill="%s" stroke="%s" stroke-width="1.4"/>'
                   % (10 + i * 11, 8 + j * 11, ic.grad(tint(c, 0.4), c, 0, 0, 1, 1), dk(c)))

    @app("kbounce")
    def _(ic):
        shadow(ic); plate(ic, "#2a3a6a", 6, 10, 48, 40)
        ic.path("M30 12 L32 50", "none", "#ffcc00", 3)
        ball(ic, 18, 24, 6, "#e04040"); ball(ic, 44, 38, 6, "#40c040")

    @app("kbreakout")
    def _(ic):
        shadow(ic); plate(ic, "#1a1a2a", 6, 10, 48, 40)
        cols = ["#e04040", "#f0a020", "#40c040", "#4070e0"]
        for r in range(3):
            for c in range(5):
                ic.raw('<rect x="%g" y="%g" width="8" height="4" fill="%s" stroke="#000" stroke-width="0.6"/>'
                       % (10 + c * 9, 15 + r * 5 - c * 0.4, cols[(r + c) % 4]))
        ball(ic, 34, 38, 2.8, "#ffffff"); ic.raw('<rect x="24" y="44" width="16" height="3" rx="1.5" fill="#ccc"/>')

    @app("kdiamond")
    def _(ic):
        shadow(ic); gem(ic, 22, 24, 13, "#3a90e0"); gem(ic, 44, 30, 11, "#e04060"); gem(ic, 28, 44, 9, "#40c060")

    @app("kdominate")
    def _(ic):
        shadow(ic)
        def hexa(cx, cy, r, col):
            pts = [(cx + r * math.cos(math.radians(60 * k + 30)), cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
            quad(ic, pts, col, 1.4)
        for (x, y, c) in ((20, 18, "#e04040"), (36, 18, "#e04040"), (12, 32, "#4070e0"), (28, 32, "#e04040"),
                          (44, 32, "#f0c020"), (20, 46, "#4070e0"), (36, 46, "#f0c020"), (52, 46, "#f0c020")):
            hexa(x, y, 9, c)

    @app("kfourinline")
    def _(ic):
        shadow(ic); ic.raw('<rect x="8" y="10" width="48" height="42" rx="3" fill="%s" stroke="#102a6a" stroke-width="2"/>'
                           % ic.grad("#4a7ae0", "#1a3a9a"))
        for r in range(4):
            for c in range(5):
                col = {(3, 0): "#e04040", (3, 1): "#f0d020", (2, 1): "#e04040", (3, 2): "#e04040", (2, 2): "#f0d020",
                       (1, 2): "#e04040", (3, 3): "#f0d020", (0, 3): "#e04040", (2, 3): "#f0d020", (1, 3): "#f0d020"}.get((r, c), "#ffffff")
                circ(ic, 15 + c * 8.5, 17 + r * 9.5, 3.4, col, "#102a6a", 1)

    @app("kgoldrunner")
    def _(ic):
        shadow(ic)
        ic.path("M10 8 L10 54 M22 8 L22 54", "none", "#8a5a2a", 2.6)
        for y in range(14, 54, 8):
            ic.path("M10 %g L22 %g" % (y, y), "none", "#8a5a2a", 2)
        for (x, y) in ((30, 44), (44, 44), (37, 34)):
            quad(ic, [(x, y), (x + 14, y), (x + 12, y + 8), (x + 2, y + 8)], "#ffcc20", 1.2)

    @app("kigo")
    def _(ic):
        P = iso_board(ic, "#e0b870", 6)
        for (a, b, c) in ((2, 2, "#222"), (3, 2, "#fff"), (3, 3, "#222"), (2, 4, "#fff"), (4, 3, "#222"), (1, 3, "#fff")):
            disc_on(ic, P(a, b), c, 2.8)

    @app("killbots")
    def _(ic):
        shadow(ic); robot(ic, 32, 36)

    @app("kiriki")
    def _(ic):
        shadow(ic, 32, 56, 26, 4); die(ic, 6, 18, 26, 5); die(ic, 32, 26, 24, 3, "#ffefc0")

    @app("kjumpingcube")
    def _(ic):
        shadow(ic)
        for i in range(3):
            for j in range(3):
                c = "#e04040" if (i + j) % 3 == 0 else ("#4070e0" if (i * j) % 2 else "#e8e8e8")
                ic.raw('<rect x="%g" y="%g" width="14" height="14" fill="%s" stroke="#333" stroke-width="1.4"/>'
                       % (10 + i * 15, 10 + j * 15, ic.grad(tint(c, 0.4), c, 0, 0, 1, 1)))
                for k in range((i + j) % 3 + 1):
                    circ(ic, 13.5 + i * 15 + k * 3.5, 17 + j * 15, 1.2, "#222")

    @app("klickety")
    def _(ic):
        shadow(ic)
        cols = ["#e04040", "#4070e0", "#40c040", "#f0c020"]
        for i in range(5):
            for j in range(5):
                if j < (i % 3):
                    continue
                c = cols[(i * 3 + j * 2) % 4]
                ic.raw('<rect x="%g" y="%g" width="9" height="9" rx="1" fill="%s" stroke="%s" stroke-width="1"/>'
                       % (8 + i * 10, 8 + j * 10, ic.grad(tint(c, 0.4), c, 0, 0, 1, 1), dk(c)))

    @app("klines")
    def _(ic):
        shadow(ic); grid(ic, 8, 8, 48, 48, 4, 4, "#d8d8d8", "#888")
        for (i, j, c) in ((0, 0, "#e04040"), (1, 1, "#e04040"), (2, 2, "#e04040"), (3, 1, "#4070e0"), (0, 3, "#40c040"), (2, 0, "#f0c020")):
            ball(ic, 14 + i * 12, 14 + j * 12, 4.6, c)

    @app("kmahjongg")
    def _(ic):
        shadow(ic, 32, 56, 26, 3)
        dot = lambda x, y: circ(ic, x, y, 3.5, "none", "#2a6aa0", 1.6)
        bam = lambda x, y: ic.path("M%g %g v10" % (x, y - 5), "none", "#2a8a3a", 2.4)
        for (x, y, s) in ((8, 30, dot), (22, 30, bam), (36, 30, dot), (15, 16, bam), (29, 16, dot), (43, 30, bam)):
            tile(ic, x, y, sym=s, w=13, h=18)

    @app("kmines")
    def _(ic):
        shadow(ic); grid(ic, 8, 8, 48, 48, 4, 4, "#c8c8c8", "#777", {(0, 0): "#eee", (1, 0): "#eee", (0, 1): "#eee"})
        for a in range(8):
            r = math.radians(a * 45)
            ic.path("M%g %g L%g %g" % (38 + 7 * math.cos(r), 38 + 7 * math.sin(r), 38 + 13 * math.cos(r), 38 + 13 * math.sin(r)),
                    "none", "#222", 2.4)
        ball(ic, 38, 38, 8, "#3a3a3a")
        ic.path("M14 26 V12", "none", "#333", 1.6); quad(ic, [(14, 12), (24, 15), (14, 19)], "#e03030", 1)

    @app("knavalbattle")
    def _(ic):
        shadow(ic); ic.path("M4 46 q7 -4 14 0 t14 0 t14 0 t14 0 V56 H4 Z", ic.grad("#5aa0e8", "#1a4a9a"), "#103060", 1.6)
        ship(ic, 30)

    @app("knetwalk")
    def _(ic):
        shadow(ic); grid(ic, 8, 8, 48, 48, 3, 3, "#e8e8e8", "#999")
        ic.path("M16 16 H40 V32 H16 V48 H48", "none", "#2a8a2a", 3)
        for (x, y) in ((16, 16), (48, 48), (16, 48)):
            ic.raw('<rect x="%g" y="%g" width="10" height="8" fill="%s" stroke="#222" stroke-width="1.2"/>'
                   % (x - 5, y - 4, ic.grad("#9ad0ff", "#2a64b0")))
        ball(ic, 40, 32, 5, "#e04040")

    @app("knights")
    def _(ic):
        shadow(ic, 32, 58, 16, 3)
        ic.path("M20 54 L44 54 L42 46 L38 44 C40 34 44 28 40 18 C36 10 26 8 20 14 L16 22 L22 26 L28 24 "
                "C26 32 20 38 24 44 L22 46 Z", ic.grad("#5a5a5a", "#1a1a1a", 0, 0, 1, 1), "#000", 2)
        circ(ic, 27, 17, 1.6, "#fff")

    @app("kolf")
    def _(ic):
        shadow(ic, 32, 54, 26, 4); ell(ic, 32, 46, 26, 8, ic.rgrad("#8ae070", "#3a9a2a"), "#1f5a12", 1.6)
        ell(ic, 40, 46, 4, 1.6, "#222"); ic.path("M40 46 V12", "none", "#333", 2)
        quad(ic, [(40, 12), (54, 16), (40, 21)], "#e03030", 1); ball(ic, 20, 44, 3.6, "#ffffff", 1)

    @app("kollision")
    def _(ic):
        shadow(ic); plate(ic, "#e8e8e8", 6, 10, 48, 40)
        ball(ic, 22, 26, 7, "#e04040"); ball(ic, 40, 36, 7, "#4070e0"); ball(ic, 40, 20, 4, "#40c040")

    @app("konquest")
    def _(ic):
        shadow(ic); circ(ic, 32, 32, 26, ic.rgrad("#2a2a5a", "#05051a"), "#000", 2)
        for (x, y) in ((14, 20), (50, 18), (46, 48), (20, 46), (34, 10)):
            circ(ic, x, y, 0.8, "#fff")
        ball(ic, 22, 30, 8, "#e08040"); ball(ic, 44, 36, 6, "#40a0e0")
        spaceship(ic, 36, 22, 60, "#d0d0d0")

    @app("kpat")
    def _(ic):
        shadow(ic, 32, 56, 26, 3)
        card(ic, 10, 14, 24, 34, -18, "♠", "#222"); card(ic, 20, 12, 24, 34, 0, "♥", "#d02020"); card(ic, 30, 14, 24, 34, 18, "♣", "#222")

    @app("kreversi")
    def _(ic):
        P = iso_board(ic, "#3a9a4a", 4)
        for (a, b, c) in ((1.5, 1.5, "#222"), (2.5, 2.5, "#222"), (1.5, 2.5, "#fff"), (2.5, 1.5, "#fff"), (3.5, 2.5, "#222")):
            disc_on(ic, P(a, b), c, 3.4)

    @app("kshisen")
    def _(ic):
        shadow(ic, 32, 56, 26, 3)
        dot = lambda x, y: circ(ic, x, y, 3.5, "#e04040", "#600", 1)
        tile(ic, 6, 30, sym=dot); tile(ic, 44, 12, sym=dot); tile(ic, 25, 30, sym=lambda x, y: ic.path("M%g %g v10" % (x, y - 5), "none", "#2a8a3a", 2.4))
        ic.path("M13 30 V20 H44", "none", "#2a6ad0", 2.4)

    @app("ksirk")
    def _(ic):
        shadow(ic); plate(ic, "#a8d0f0", 6, 10, 48, 40)
        ic.path("M12 22 Q20 14 28 20 Q30 30 22 32 Q14 34 12 22 Z", "#e0a040", "#7a4a10", 1.4)
        ic.path("M32 18 Q44 14 50 24 Q48 40 38 42 Q30 36 32 18 Z", "#80c060", "#2a5a1a", 1.4)
        ic.path("M18 46 Q22 38 30 42 Q30 50 18 46 Z", "#d07070", "#6a2020", 1.4)
        ic.path("M40 30 V12", "none", "#333", 1.6); quad(ic, [(40, 12), (50, 15), (40, 18)], "#e03030", 1)

    @app("ksnakeduel")
    def _(ic):
        shadow(ic); plate(ic, "#1a1a2a", 6, 10, 48, 40)
        ic.path("M12 20 H30 V34 H44", "none", "#40e040", 3.4); ic.path("M50 44 H34 V40 H18 V30", "none", "#40a0ff", 3.4)

    @app("kspaceduel")
    def _(ic):
        shadow(ic); circ(ic, 32, 32, 26, ic.rgrad("#2a2a5a", "#05051a"), "#000", 2)
        ball(ic, 32, 32, 7, "#ffcc30")
        spaceship(ic, 16, 18, 135, "#e04040"); spaceship(ic, 48, 46, -45, "#40a0ff")

    @app("ksquares")
    def _(ic):
        shadow(ic); plate(ic, "#ffffff", 6, 10, 48, 40)
        ic.raw('<rect x="14" y="16" width="12" height="12" fill="#f09090"/><rect x="26" y="28" width="12" height="12" fill="#90b0f0"/>')
        ic.path("M14 16 H38 M14 28 H38 V40 M14 16 V28 M26 16 V40 H38", "none", "#333", 2)
        for x in (14, 26, 38, 50):
            for y in (16, 28, 40):
                circ(ic, x, y, 1.8, "#222")

    @app("ksudoku")
    def _(ic):
        shadow(ic); grid(ic, 8, 8, 48, 48, 3, 3, "#ffffff", "#333")
        for (i, j, n, c) in ((0, 0, "5", "#222"), (1, 1, "3", "#2a5ad0"), (2, 0, "8", "#222"), (0, 2, "1", "#2a5ad0"), (2, 2, "9", "#222")):
            txt(ic, 16 + i * 16, 21 + j * 16, n, 12, c)

    @app("ktuberling")
    def _(ic):
        shadow(ic); ell(ic, 32, 34, 20, 22, ic.rgrad("#e0b070", "#9a6a30"), "#5a3a10", 2)
        for (x, y) in ((24, 30), (40, 30)):
            ell(ic, x, y, 4.5, 5.5, "#fff", "#333", 1.2); circ(ic, x + 1, y + 1, 2, "#222")
        ell(ic, 32, 38, 3, 2.5, "#e07a6a", "#7a3a2a", 1)
        ic.path("M24 46 Q32 52 40 46", "none", "#7a2020", 2.4)

    @app("kubrick")
    def _(ic):
        shadow(ic)
        n = 2
        P = lambda a, b: (8 + 24 * a / n - 0 * b, 20 - 12 * a / n + 12 * b / n)
        cols_top = ["#ffffff", "#ffcc00", "#e04040", "#ffffff"]
        cols_l = ["#40c040", "#4070e0", "#40c040", "#f08020"]
        cols_r = ["#e04040", "#4070e0", "#ffcc00", "#f08020"]
        def face(pts, col):
            quad(ic, pts, col, 1.6)
        for a in range(2):
            for b in range(2):
                face([(8 + 12 * a + 12 * b, 20 - 6 * a + 6 * b), (20 + 12 * a + 12 * b, 14 - 6 * a + 6 * b),
                      (32 + 12 * a + 12 * b, 20 - 6 * a + 6 * b), (20 + 12 * a + 12 * b, 26 - 6 * a + 6 * b)], cols_top[a * 2 + b])
                face([(8 + 12 * a, 20 + 6 * a + 14 * b), (20 + 12 * a, 26 + 6 * a + 14 * b),
                      (20 + 12 * a, 40 + 6 * a + 14 * b), (8 + 12 * a, 34 + 6 * a + 14 * b)], cols_l[a * 2 + b])
                face([(32 + 12 * a, 32 - 6 * a + 14 * b), (44 + 12 * a, 26 - 6 * a + 14 * b),
                      (44 + 12 * a, 40 - 6 * a + 14 * b), (32 + 12 * a, 46 - 6 * a + 14 * b)], cols_r[a * 2 + b])

    @app("lskat")
    def _(ic):
        shadow(ic, 32, 56, 26, 3); ell(ic, 32, 40, 28, 14, ic.rgrad("#5ab05a", "#1f6a2a"), "#0f3a12", 2)
        card(ic, 14, 14, 22, 30, -12, "♦", "#d02020"); card(ic, 28, 14, 22, 30, 12, "K", "#222")

    @app("palapeli")
    def _(ic):
        shadow(ic)
        d = ("M10 14 H24 q-2 -8 6 -8 t6 8 H50 V26 q8 -2 8 6 t-8 6 V50 H36 q2 8 -6 8 t-6 -8 H10 V38 q-8 2 -8 -6 t8 -6 Z")
        ic.path(d, ic.grad("#7ac0f0", "#2a6ab0", 0, 0, 1, 1), "#123a6a", 2.2)
        ic.path("M18 40 L28 28 L34 36 L40 30 L46 40 Z", "#3a9a3a", "#1a5a1a", 1); circ(ic, 38, 20, 3, "#ffd040")

    @app("picmi")
    def _(ic):
        shadow(ic); fills = {(1, 0): "#333", (2, 0): "#333", (0, 1): "#333", (3, 1): "#333", (1, 2): "#333", (2, 2): "#333", (1, 3): "#333", (2, 3): "#333"}
        grid(ic, 18, 18, 38, 38, 4, 4, "#ffffff", "#555", fills)
        for i, n in enumerate(("1", "2", "2", "1")):
            txt(ic, 22.7 + i * 9.5, 15, n, 8, "#2a5ad0")
            txt(ic, 13, 25 + i * 9.5, ("2", "1 1", "2", "2")[i], 7, "#2a5ad0")

    @app("skladnik")
    def _(ic):
        shadow(ic, 32, 56, 26, 3)
        box3d(ic, ic.grad("#d8a060", "#a06a2a"), "#e8c090", "#7a4a1a", 8, 32, 20, 18, 8)
        box3d(ic, ic.grad("#d8a060", "#a06a2a"), "#e8c090", "#7a4a1a", 30, 36, 20, 16, 8)
        ic.path("M14 41 L22 49 M22 41 L14 49 M36 44 L44 50 M44 44 L36 50", "none", "#5a3a10", 1.6)
        arrow(ic, "r", 40, 18, 1.0, "#3fae2f")

    # ---- graphics / multimedia ----
    @app("kolourpaint")
    def _(ic):
        shadow(ic); ic.path("M8 34 C8 14 34 6 50 14 C60 20 56 32 48 32 C40 32 42 42 36 48 C28 58 8 52 8 34 Z",
                            ic.grad("#f6e0b8", "#c9a066", 0, 0, 1, 1), "#6a4a20", 2)
        for cx, cy, col in ((18, 28, "#e03030"), (26, 18, "#ffcb00"), (38, 16, "#30a030"), (18, 40, "#3060e0")):
            circ(ic, cx, cy, 4, col, "#333", 1)
        ic.path("M30 50 L54 14 L58 17 L36 52 Z", ic.grad("#ffe066", "#c08000", 0, 0, 1, 0), "#5a3a00", 1.4)

    @app("okular")
    def _(ic):
        page(ic); text_lines(ic, n=7); magnifier(ic, 36, 38, 9)

    @app("kruler")
    def _(ic):
        shadow(ic); quad(ic, [(4, 40), (44, 8), (60, 24), (20, 56)], "#f0d060")
        for i in range(1, 10):
            x, y = 4 + i * 4.4, 40 - i * 3.5
            ln = 6 if i % 2 == 0 else 3.5
            ic.path("M%g %g l%g %g" % (x, y, ln * 0.7, ln * 0.7), "none", "#5a4a10", 1.2)

    @app("kcolorchooser")
    def _(ic):
        shadow(ic)
        cols = ["#e03030", "#f09020", "#f0e020", "#40c040", "#30b0e0", "#3050e0", "#a040d0", "#e040a0"]
        for i, c in enumerate(cols):
            a1, a2 = math.radians(i * 45), math.radians(i * 45 + 45)
            ic.path("M32 30 L%g %g A22 22 0 0 1 %g %g Z" % (32 + 22 * math.cos(a1), 30 + 22 * math.sin(a1),
                                                           32 + 22 * math.cos(a2), 30 + 22 * math.sin(a2)), c, dk(c), 1)
        circ(ic, 32, 30, 22, "none", "#333", 2); circ(ic, 32, 30, 7, "#fff", "#333", 1.4)
        ic.path("M44 52 L56 40 L60 44 L48 56 Z", "#ddd", "#333", 1.6)

    @app("kimagemapeditor")
    def _(ic):
        ns["ICONS"]["image-x-generic"][2](ic)
        ic.path("M16 22 L34 18 L40 34 L22 40 Z", "#ffffff", "#e03030", 2, 'fill-opacity="0.25" stroke-dasharray="3 2"')

    @app("skanlite", "scanner")
    def _(ic):
        shadow(ic, 32, 54, 28, 4)
        box3d(ic, ic.grad("#e0e0e0", "#9a9a9a"), ic.grad("#6aa0d0", "#2a5a90"), "#7a7a7a", 6, 34, 44, 14, 14)
        ic.path("M10 33 L52 33", "none", "#9ff", 2)

    @app("skanpage")
    def _(ic):
        shadow(ic, 32, 54, 28, 4)
        box3d(ic, ic.grad("#e0e0e0", "#9a9a9a"), ic.grad("#6aa0d0", "#2a5a90"), "#7a7a7a", 6, 40, 44, 12, 14)
        ic.path("M18 6 L42 4 L46 36 L22 38 Z", "#fff", "#555", 1.6); text_lines(ic, 24, 42, 12, 6, 4, "#999")

    @app("kamoso")
    def _(ic):
        shadow(ic, 32, 58, 16, 3)
        circ(ic, 32, 26, 20, ic.rgrad("#ffffff", "#9a9a9a"), "#333", 2); circ(ic, 32, 26, 10, ic.rgrad("#7ab0f0", "#0a1a40"), "#111", 2)
        circ(ic, 28, 22, 3, "#fff"); circ(ic, 46, 12, 2.2, "#e03030")
        ic.path("M24 46 L22 56 H42 L40 46", "#666", "#222", 1.6)

    @app("koko")
    def _(ic):
        shadow(ic)
        ic.raw('<rect x="8" y="12" width="36" height="30" fill="#fff" stroke="#555" stroke-width="1.6" transform="rotate(-10 26 27)"/>')
        ic.raw('<rect x="18" y="18" width="38" height="32" fill="#fff" stroke="#444" stroke-width="1.8" transform="rotate(6 37 34)"/>')
        ic.raw('<g transform="rotate(6 37 34)"><rect x="21" y="21" width="32" height="22" fill="%s"/>'
               '<path d="M21 43 L31 31 L38 38 L44 32 L53 43 Z" fill="#3a9a3a"/><circle cx="47" cy="26" r="3" fill="#ffd040"/></g>'
               % ic.grad("#a7d8ff", "#e9f6ff"))

    @app("kontrast")
    def _(ic):
        shadow(ic); circ(ic, 32, 30, 24, "#fff", "#222", 2.2)
        ic.path("M32 6 A24 24 0 0 1 32 54 Z", "#222")
        txt(ic, 24, 37, "A", 18, "#222"); txt(ic, 40, 37, "a", 18, "#fff")

    @app("arianna")
    def _(ic):
        openbook(ic, cover="#c04060")

    @app("plasma-camera")
    def _(ic):
        ns["ICONS"]["accessories-screenshot"][2](ic)

    @app("kcachegrind")
    def _(ic):
        shadow(ic); plate(ic, "#ffffff", 6, 8, 48, 44)
        for i, (w, c) in enumerate(((40, "#e04040"), (30, "#f08020"), (22, "#f0c020"), (12, "#40c040"), (18, "#40a0e0"))):
            ic.raw('<rect x="12" y="%g" width="%g" height="6" fill="%s" stroke="%s" stroke-width="0.8"/>' % (14 + i * 7.5, w, c, dk(c)))

    @app("massif-visualizer")
    def _(ic):
        shadow(ic); plate(ic, "#ffffff", 6, 8, 48, 44)
        ic.path("M10 50 L10 40 Q20 30 28 34 T46 22 T54 18 L54 48 Z", ic.grad("#90c0f0", "#2a6ab0"), "#123a6a", 1.4)
        ic.path("M10 50 L10 46 Q22 40 30 42 T54 34 L54 48 Z", ic.grad("#f0b070", "#c06a20"), "#6a3a10", 1.2)

    @app("umbrello")
    def _(ic):
        shadow(ic)
        for (x, y) in ((6, 8), (34, 30)):
            ic.raw('<rect x="%g" y="%g" width="24" height="22" fill="#fff8d0" stroke="#5a4a10" stroke-width="1.6"/>' % (x, y))
            ic.path("M%g %g h24 M%g %g h24" % (x, y + 7, x, y + 14), "none", "#5a4a10", 1.2)
        ic.path("M18 30 V44 H34", "none", "#333", 1.8); quad(ic, [(34, 44), (29, 41), (29, 47)], "#fff", 1.2, False, "#333")

    @app("kompare")
    def _(ic):
        shadow(ic)
        ic.path("M4 10 L26 8 L28 52 L6 54 Z", "#fff", "#555", 1.6); ic.path("M36 8 L58 10 L56 54 L34 52 Z", "#fff", "#555", 1.6)
        ic.raw('<rect x="8" y="22" width="16" height="5" fill="#f0a0a0"/><rect x="38" y="22" width="16" height="5" fill="#a0e0a0"/>')
        for y in (14, 32, 40):
            ic.path("M9 %g h14 M39 %g h14" % (y, y), "none", "#999", 1.2)
        ic.path("M24 25 L38 25", "none", "#2a5ad0", 1.8)

    @app("lokalize")
    def _(ic):
        page(ic); globe(ic, 40, 42, 12); txt(ic, 26, 30, "abc", 10, "#555")

    @app("kapptemplate")
    def _(ic):
        page(ic); ic.path("M20 20 h20 v8 h-20 Z M20 32 h10 v14 h-10 Z", "none", "#2a5ad0", 1.4, 'stroke-dasharray="2 2"')
        gear(ic, 42, 44, 9, "#8aa6d6")

    @app("kdevelop")
    def _(ic):
        monitor(ic, "#1e2a3a"); txt(ic, 29, 33, "{ }", 18, "#7ae07a")
        gear(ic, 50, 46, 9, "#8aa6d6")

    @app("kirigami-gallery", "org.kde.kirigami2.gallery")
    def _(ic):
        phone(ic, screen="#f4f4f4")
        for i in range(4):
            ic.raw('<rect x="24" y="%g" width="16" height="6" rx="1" fill="%s"/>' % (14 + i * 9, ["#4a7ad0", "#ccc", "#ccc", "#ffcb00"][i]))

    @app("accessibility-inspector", "org.kde.accessibilityinspector")
    def _(ic):
        shadow(ic); circ(ic, 28, 28, 22, ic.rgrad("#bfe0ff", "#2a6ec2"), "#173d70", 2)
        circ(ic, 28, 15, 3.4, "#fff")
        ic.path("M16 21 H40 M28 21 V34 L21 45 M28 34 L35 45", "none", "#fff", 3)
        magnifier(ic, 46, 44, 7)

    @app("kdebugsettings")
    def _(ic):
        shadow(ic); ell(ic, 28, 34, 11, 15, ic.rgrad("#90e070", "#2a8a20"), "#1a4a10", 2)
        circ(ic, 28, 16, 6, "#2a5a1a", "#1a3a10", 1.6)
        for s in (-1, 1):
            for y in (26, 34, 42):
                ic.path("M%g %g l%g -3" % (28 + s * 11, y, s * 8), "none", "#1a3a10", 2)
        gear(ic, 48, 46, 9, "#8aa6d6")

    @app("ksystemlog", "utilities-log-viewer")
    def _(ic):
        page(ic)
        for i, c in enumerate(("#3a9a3a", "#3a9a3a", "#e0a020", "#3a9a3a", "#d03030", "#3a9a3a", "#3a9a3a")):
            y = 20 + i * 5
            circ(ic, 20, y - 0.4, 1.6, c); ic.path("M24 %g L44 %g" % (y, y - 0.6), "none", "#888", 1.4)

    @app("kjournald", "kjournaldbrowser", "org.kde.kjournaldbrowser")
    def _(ic):
        book(ic, "#4a6a9a"); clockface(ic, 42, 42, 12)

    @app("kbackup")
    def _(ic):
        ns["ICONS"]["drive-harddisk"][2](ic)
        ic.path("M40 10 A10 10 0 1 1 30 20", "none", "#2e8b22", 3.4); quad(ic, [(26, 14), (34, 20), (26, 24)], "#3fae2f", 1)

    @app("kdf")
    def _(ic):
        ns["ICONS"]["drive-harddisk"][2](ic)
        circ(ic, 44, 18, 12, "#40a0e0", "#1a4a80", 1.6); ic.path("M44 18 L44 6 A12 12 0 0 1 55 22 Z", "#e04040", "#600", 1.2)

    @app("filelight")
    def _(ic):
        shadow(ic)
        for (r, segs) in ((24, [("#e04040", 0, 140), ("#40a0e0", 140, 250), ("#40c040", 250, 360)]),
                          (16, [("#f08080", 0, 90), ("#f0b0b0", 90, 140), ("#90c8f0", 140, 250), ("#90e090", 250, 360)])):
            for c, a0, a1 in segs:
                r0, r1 = math.radians(a0 - 90), math.radians(a1 - 90)
                large = 1 if a1 - a0 > 180 else 0
                ic.path("M32 30 L%g %g A%g %g 0 %d 1 %g %g Z" % (32 + r * math.cos(r0), 30 + r * math.sin(r0), r, r, large,
                                                                 32 + r * math.cos(r1), 30 + r * math.sin(r1)), c, "#333", 1.2)
        circ(ic, 32, 30, 8, "#fff", "#333", 1.2)

    @app("partitionmanager")
    def _(ic):
        ns["ICONS"]["drive-harddisk"][2](ic)
        for i, (w, c) in enumerate(((14, "#e04040"), (10, "#40c040"), (16, "#4070e0"))):
            x = 8 + sum((14, 10, 16)[:i])
            ic.raw('<rect x="%g" y="12" width="%g" height="10" fill="%s" stroke="#333" stroke-width="1"/>' % (x, w, c))

    @app("sweeper")
    def _(ic):
        shadow(ic); ic.path("M44 4 L30 34", "none", "#8a5a2a", 3.6)
        quad(ic, [(24, 30), (36, 36), (30, 56), (8, 48)], "#e8c050", 1.8)
        for i in range(4):
            ic.path("M%g %g L%g %g" % (26 + i * 2, 34 + i * 1, 14 + i * 4, 50 + i * 1.5), "none", "#9a7a20", 1)

    @app("kfind")
    def _(ic):
        folder(ic); magnifier(ic, 38, 34, 10)

    @app("isoimagewriter", "org.kde.isoimagewriter")
    def _(ic):
        ns["ICONS"]["media-optical"][2](ic)
        ic.raw('<rect x="38" y="34" width="20" height="12" rx="2" fill="%s" stroke="#1a3a70" stroke-width="1.6"/>' % ic.grad("#7fb2ff", "#2f5fc0"))
        arrow(ic, "r", 32, 40, 0.7)

    @app("k3b")
    def _(ic):
        ns["ICONS"]["media-optical"][2](ic)
        ic.path("M40 20 C34 10 46 6 44 0 C54 8 56 16 50 24 C48 18 44 20 44 26 C40 26 38 24 40 20 Z",
                ic.grad("#ffe040", "#e03010"), "#7a1a00", 1.4)

    @app("keditbookmarks")
    def _(ic):
        book(ic, "#3a6ab0"); ic.path("M36 8 V30 L41 25 L46 30 V8 Z", "#e03030", "#6a0a0a", 1.4)

    @app("kwalletmanager", "kwalletmanager2")
    def _(ic):
        shadow(ic); ic.raw('<rect x="6" y="16" width="50" height="36" rx="6" fill="%s" stroke="#3a2010" stroke-width="2"/>'
                           % ic.grad("#a06a3a", "#5a3010", 0, 0, 1, 1))
        ic.raw('<rect x="34" y="26" width="24" height="16" rx="4" fill="%s" stroke="#3a2010" stroke-width="2"/>' % ic.grad("#c08a5a", "#7a4a20"))
        circ(ic, 42, 34, 3, "#ffd040", "#7a5a00", 1.2)

    @app("kgpg")
    def _(ic):
        shadow(ic); keyshape(ic, 18, 24, "#e8b020", 1.4)
        padlock(ic, 36, 26, 0.9, "#9aa0a8")

    @app("kleopatra")
    def _(ic):
        page(ic); text_lines(ic, n=5)
        circ(ic, 38, 44, 9, ic.rgrad("#ff8a6a", "#c02010"), "#600", 1.6)
        ic.path("M33 51 L30 60 L35 57 L38 61 L39 52 M43 51 L46 60 L41 57", "#c02010", "#600", 1)

    @app("keysmith")
    def _(ic):
        phone(ic); txt(ic, 32, 30, "123", 9, "#fff"); txt(ic, 32, 42, "456", 9, "#fff")
        keyshape(ic, 40, 46, "#e8b020", 0.6)

    @app("keepsecret")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#9aa0b0", "#5a6070"), "#c0c4d0", "#40444f", 8, 20, 40, 32, 10)
        circ(ic, 28, 36, 9, ic.rgrad("#e0e0e0", "#808080"), "#222", 2)
        for a in range(0, 360, 60):
            r = math.radians(a)
            ic.path("M28 36 L%g %g" % (28 + 7 * math.cos(r), 36 + 7 * math.sin(r)), "none", "#333", 1.4)

    @app("khealthcertificate")
    def _(ic):
        page(ic); text_lines(ic, n=3)
        ic.path("M32 50 C20 42 18 34 24 31 C28 29 31 31 32 34 C33 31 36 29 40 31 C46 34 44 42 32 50 Z", "#e04060", "#7a1020", 1.6)
        ic.path("M26 39 l4 4 l8 -8", "none", "#fff", 2.2)

    @app("kmousetool")
    def _(ic):
        shadow(ic); ell(ic, 32, 34, 15, 22, ic.grad("#f4f4f4", "#a8a8a8", 0, 0, 1, 1), "#333", 2)
        ic.path("M17 28 H47 M32 12 V28", "none", "#555", 1.6); ic.path("M32 12 Q36 2 46 4", "none", "#333", 2)
        clockface(ic, 46, 46, 9)

    @app("kmouth")
    def _(ic):
        shadow(ic); bubble(ic, "#f0f0f0", 4, 8, 42, 30)
        ic.path("M14 22 Q25 14 36 22 Q25 32 14 22 Z", "#e05060", "#7a1a20", 1.4)
        waves(ic, 48, 40, 2, "#3a7ad8", 0.9)

    @app("kmag")
    def _(ic):
        shadow(ic); magnifier(ic, 26, 26, 18); txt(ic, 26, 34, "+", 22, "#2a5ad0")

    @app("kteatime")
    def _(ic):
        shadow(ic, 32, 56, 24, 3)
        ic.path("M10 24 H46 V38 C46 50 38 54 28 54 C18 54 10 50 10 38 Z", ic.grad("#ffffff", "#c8d4e8", 0, 0, 1, 0), "#3a4a6a", 2)
        ell(ic, 28, 24, 18, 4, "#a0522d", "#3a4a6a", 1.6)
        ic.path("M46 30 C58 30 58 44 44 44", "none", "#3a4a6a", 3)
        for x in (20, 28, 36):
            ic.path("M%g 18 q-3 -4 0 -8 t0 -8" % x, "none", "#9aa", 1.6)

    @app("ktimer")
    def _(ic):
        shadow(ic); ic.raw('<rect x="28" y="4" width="8" height="6" fill="#888" stroke="#333" stroke-width="1.4"/>')
        clockface(ic, 32, 34, 22, rim="#d04a3a", h=90, m=90)

    @app("kclock")
    def _(ic):
        shadow(ic); clockface(ic, 32, 30, 24)

    @app("kweather")
    def _(ic):
        shadow(ic)
        for a in range(0, 360, 45):
            r = math.radians(a)
            ic.path("M%g %g L%g %g" % (24 + 13 * math.cos(r), 22 + 13 * math.sin(r), 24 + 18 * math.cos(r), 22 + 18 * math.sin(r)),
                    "none", "#f0a000", 2.4)
        ball(ic, 24, 22, 10, "#ffcc20")
        ic.path("M18 50 a8 8 0 0 1 2 -15 a11 11 0 0 1 21 -3 a8 8 0 0 1 9 18 Z", ic.grad("#ffffff", "#c8d4e8"), "#4a5a7a", 2)

    @app("kcharselect", "accessories-character-map")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#ffffff", "#d0d0d0"), "#f4f4f4", "#a0a0a0", 10, 18, 36, 34, 10)
        txt(ic, 28, 45, "Ω", 26, "#2a5ad0")

    @app("kalk")
    def _(ic):
        ns["ICONS"]["accessories-calculator"][2](ic)
        ic.raw('<rect x="40" y="4" width="18" height="12" rx="2" fill="#2a5ad0"/>'); txt(ic, 49, 13.5, "=", 11)

    @app("krecorder")
    def _(ic):
        shadow(ic, 32, 58, 14, 3); mic(ic, 32, 6, 1.4); circ(ic, 50, 12, 5, "#e03030", "#600", 1.2)

    @app("kwave")
    def _(ic):
        shadow(ic); plate(ic, "#102030", 6, 10, 48, 40)
        ic.path("M" + " L".join(
            "%g %g" % (10 + i * 1.5, 30 + math.sin(i * 0.9) * (13 - abs(i - 14) * 0.55)) for i in range(30)), "none", "#40e0a0", 1.6)

    @app("audex")
    def _(ic):
        ns["ICONS"]["media-optical"][2](ic); note(ic, 46, 58, 0.9, "#2a2a8a")

    @app("kmix")
    def _(ic):
        shadow(ic); plate(ic, "#3a3a3a", 6, 8, 48, 46)
        for i, h in enumerate((30, 18, 38, 24)):
            x = 15 + i * 10
            ic.path("M%g 14 L%g 48" % (x, x), "none", "#111", 3)
            ic.raw('<rect x="%g" y="%g" width="9" height="5" rx="1" fill="%s" stroke="#111"/>' % (x - 4.5, 50 - h, ic.grad("#f0f0f0", "#909090")))

    @app("audiotube")
    def _(ic):
        shadow(ic)
        ic.path("M12 34 A20 20 0 0 1 52 34", "none", "#333", 4)
        ic.raw('<rect x="6" y="32" width="12" height="20" rx="4" fill="%s" stroke="#222" stroke-width="2"/>' % ic.grad("#e05050", "#901010"))
        ic.raw('<rect x="46" y="32" width="12" height="20" rx="4" fill="%s" stroke="#222" stroke-width="2"/>' % ic.grad("#e05050", "#901010"))
        note(ic, 28, 40, 0.8, "#2a2a8a")

    @app("plasmatube")
    def _(ic):
        sx, sy, sw, sh = tv(ic, ic.grad("#5aa0ff", "#123a80"))
        quad(ic, [(27, 22), (40, 30), (27, 38)], "#fff", 1.2)

    @app("telly-skout", "org.kde.telly-skout")
    def _(ic):
        tv(ic, ic.grad("#3a4a6a", "#101a30"))
        for i in range(4):
            ic.raw('<rect x="14" y="%g" width="%g" height="4" fill="%s"/>' % (20 + i * 6, (30, 22, 34, 18)[i], ("#ffcb00", "#aac", "#aac", "#aac")[i]))

    @app("kasts")
    def _(ic):
        shadow(ic, 32, 58, 14, 3); mic(ic, 32, 10, 1.2, "#8a6ad0")
        waves(ic, 44, 22, 2, "#8a6ad0", 0.8); ic.raw('<g transform="scale(-1 1) translate(-64 0)">')
        waves(ic, 44, 22, 2, "#8a6ad0", 0.8); ic.raw('</g>')

    @app("kdenlive")
    def _(ic):
        shadow(ic)
        quad(ic, [(6, 26), (56, 22), (58, 52), (8, 56)], "#3a3a3a")
        ic.path("M6 18 L54 8 L56 16 L8 26 Z", "#fff", "#222", 1.6)
        for i in range(5):
            ic.path("M%g %g l5 -1 l-3 8.8 l-5 1 Z" % (14 + i * 9, 23.4 - i * 1.9), "#222")
        for i, (w, c) in enumerate(((20, "#4a90e0"), (14, "#e0a040"), (26, "#60c060"))):
            ic.raw('<rect x="%g" y="%g" width="%g" height="5" fill="%s"/>' % (12 + i * 6, 32 + i * 7, w, c))

    @app("tokodon")
    def _(ic):
        shadow(ic); bubble(ic, "#6a5ad0"); txt(ic, 29, 31, "@", 22, "#fff")

    @app("neochat")
    def _(ic):
        shadow(ic); bubble(ic, "#40b0a0", 4, 6, 38, 26); bubble(ic, "#f0f0f0", 22, 26, 38, 22, False)
        for x in (32, 40, 48):
            circ(ic, x + 3, 37, 2, "#555")

    @app("konversation")
    def _(ic):
        shadow(ic); bubble(ic, "#3a7ad8", 4, 6, 40, 28); bubble(ic, "#f0c040", 24, 26, 36, 22, False)
        txt(ic, 24, 26, "#", 18, "#fff")

    @app("kdeconnect", "kdeconnect", "org.kde.kdeconnect.app", "kdeconnectindicator")
    def _(ic):
        monitor(ic, ic.grad("#5a9de6", "#1f4f9a", 0, 0, 1, 1), 2, 6, 40, 30)
        phone(ic, x=40, y=22, w=20, h=36)
        ic.path("M30 44 q6 6 10 0", "none", "#3fae2f", 2.4)

    @app("krdc")
    def _(ic):
        monitor(ic, ic.grad("#5a9de6", "#1f4f9a", 0, 0, 1, 1)); arrow(ic, "r", 30, 25, 1.0)

    @app("krfb")
    def _(ic):
        monitor(ic, ic.grad("#5a9de6", "#1f4f9a", 0, 0, 1, 1))
        for (d, x, y) in (("l", 16, 25), ("r", 42, 24)):
            arrow(ic, d, x, y, 0.7, "#ffcb00")

    @app("kget")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#e6b779", "#a86f2c"), "#f6d7a6", "#7c5020", 10, 34, 36, 20, 10)
        arrow(ic, "d", 30, 18, 1.6)

    @app("ktorrent")
    def _(ic):
        shadow(ic); globe(ic, 32, 30, 20, "#d8ffd8", "#2a8a3a", "#7ac07a")
        arrow(ic, "d", 24, 30, 0.9, "#2a6ad0"); arrow(ic, "u", 40, 30, 0.9, "#e0a020")

    @app("falkon")
    def _(ic):
        shadow(ic); globe(ic, 30, 30, 21)
        ic.path("M30 50 C40 40 52 36 60 14 C48 22 40 22 30 30 C38 32 36 42 30 50 Z", ic.grad("#ffd060", "#d07010"), "#6a3a00", 1.6)

    @app("angelfish")
    def _(ic):
        sx, sy, sw, sh = phone(ic, screen="#eef4ff"); globe(ic, 32, 30, 9)

    @app("konqueror")
    def _(ic):
        shadow(ic); globe(ic, 28, 28, 20); gear(ic, 46, 44, 12, "#8aa6d6")

    @app("akregator")
    def _(ic):
        page(ic)
        ic.raw('<rect x="20" y="22" width="24" height="24" rx="4" fill="%s" stroke="#7a3a00" stroke-width="1.4"/>' % ic.grad("#ffb050", "#e06a00"))
        circ(ic, 25, 41, 2.2, "#fff"); ic.path("M24 33 a8 8 0 0 1 8 8 M24 27 a14 14 0 0 1 14 14", "none", "#fff", 2.4)

    @app("alligator")
    def _(ic):
        phone(ic, screen=ic.grad("#ffb050", "#e06a00"))
        circ(ic, 26, 40, 2.2, "#fff"); ic.path("M25 32 a8 8 0 0 1 8 8 M25 26 a14 14 0 0 1 14 14", "none", "#fff", 2.4)

    @app("itinerary")
    def _(ic):
        shadow(ic)
        ic.path("M6 20 L54 14 L56 26 a4 4 0 0 0 1 8 L58 46 L10 52 L8 40 a4 4 0 0 0 -1 -8 Z", ic.grad("#7ab8f0", "#2a6ab0"), "#123a6a", 2)
        ic.path("M40 16 L42 48", "none", "#fff", 1.4, 'stroke-dasharray="2 2"')
        plane(ic, 24, 34, 0.55, "#ffffff")

    @app("ktrip")
    def _(ic):
        shadow(ic, 32, 58, 22, 3)
        ic.raw('<rect x="14" y="6" width="36" height="42" rx="7" fill="%s" stroke="#1a3a70" stroke-width="2"/>' % ic.grad("#5a9ae0", "#1f4a9a"))
        ic.raw('<rect x="18" y="12" width="28" height="14" rx="2" fill="#dff"/>')
        circ(ic, 22, 38, 3, "#ffe060", "#333", 1); circ(ic, 42, 38, 3, "#ffe060", "#333", 1)
        ic.path("M20 48 L14 56 M44 48 L50 56", "none", "#333", 2.4)

    @app("kongress")
    def _(ic):
        shadow(ic); ic.path("M24 4 L32 18 L40 4", "none", "#e03030", 3)
        ic.raw('<rect x="14" y="18" width="36" height="40" rx="3" fill="%s" stroke="#333" stroke-width="2"/>' % ic.grad("#ffffff", "#dcdcdc"))
        ic.raw('<rect x="14" y="18" width="36" height="10" fill="#4a7ad0"/>'); person(ic, 32, 44, 0.7)

    @app("qrca")
    def _(ic):
        shadow(ic); ic.raw('<rect x="8" y="8" width="48" height="48" fill="#fff" stroke="#333" stroke-width="2"/>')
        for (x, y) in ((12, 12), (40, 12), (12, 40)):
            ic.raw('<rect x="%g" y="%g" width="12" height="12" fill="none" stroke="#111" stroke-width="2.4"/>'
                   '<rect x="%g" y="%g" width="5" height="5" fill="#111"/>' % (x, y, x + 3.5, y + 3.5))
        import random
        rnd = random.Random(7)
        for i in range(6):
            for j in range(6):
                if rnd.random() < 0.5 and not (i < 2 and j < 2):
                    ic.raw('<rect x="%g" y="%g" width="4" height="4" fill="#111"/>' % (28 + i * 4.4, 28 + j * 4.4))

    @app("kontact")
    def _(ic):
        calendar(ic, "#3a7ad8", 14, 6, 40, 34, ""); envelope(ic, 4, 30, 40, 24)

    @app("korganizer")
    def _(ic):
        calendar(ic, "#3a7ad8")

    @app("merkuro", "org.kde.merkuro.calendar")
    def _(ic):
        calendar(ic, "#7a4ac0", num="")
        ic.path("M22 38 l6 6 l12 -12", "none", "#3fae2f", 3.4)

    @app("calindori")
    def _(ic):
        phone(ic, screen="#ffffff"); ic.raw('<rect x="21" y="10" width="22" height="8" fill="#e05050"/>'); txt(ic, 32, 36, "31", 13, "#333")

    @app("kalarm")
    def _(ic):
        shadow(ic)
        for s in (-1, 1):
            ic.path("M%g 16 a9 9 0 0 1 %g -10" % (32 + s * 14, s * 4), "#ffcb00", "#7a5a00", 1.6)
        clockface(ic, 32, 34, 20, rim="#e0a020")
        ic.path("M18 54 L22 48 M46 54 L42 48", "none", "#333", 3)

    @app("kaddressbook")
    def _(ic):
        book(ic, "#3a8a5a"); ic.raw('<rect x="16" y="18" width="26" height="30" rx="2" fill="#fff" stroke="#333" stroke-width="1"/>')
        person(ic, 29, 34, 0.75)

    @app("zanshin")
    def _(ic):
        page(ic)
        for i in range(4):
            y = 22 + i * 8
            ic.raw('<rect x="18" y="%g" width="6" height="6" fill="#fff" stroke="#555" stroke-width="1.2"/>' % (y - 5))
            ic.path("M28 %g L44 %g" % (y - 2, y - 2.6), "none", "#888", 1.4)
            if i < 2:
                ic.path("M18.5 %g l3 3 l5 -7" % (y - 3), "none", "#2e8b22", 2.2)

    @app("akonadiconsole")
    def _(ic):
        shadow(ic)
        for y in (40, 28, 16):
            ell(ic, 26, y + 8, 18, 6, ic.grad("#7a9ad0", "#3a5a90", 0, 0, 1, 0), "#1a2a50", 1.6)
            ic.raw('<rect x="8" y="%g" width="36" height="8" fill="%s"/>' % (y, ic.grad("#9ab4e0", "#4a6aa0", 0, 0, 1, 0)))
            ell(ic, 26, y, 18, 6, ic.rgrad("#c8d8f8", "#6a8ac0"), "#1a2a50", 1.6)
        ic.raw('<rect x="34" y="34" width="26" height="20" rx="2" fill="#1e1e1e" stroke="#000" stroke-width="1.6"/>')
        ic.path("M38 40 l4 3 l-4 3 M44 48 h6", "none", "#5f5", 1.6)

    def database(ic, x=8, y=12):
        for yy in (y + 24, y + 12, y):
            ell(ic, x + 18, yy + 8, 18, 6, ic.grad("#7a9ad0", "#3a5a90", 0, 0, 1, 0), "#1a2a50", 1.6)
            ic.raw('<rect x="%g" y="%g" width="36" height="8" fill="%s"/>' % (x, yy, ic.grad("#9ab4e0", "#4a6aa0", 0, 0, 1, 0)))
            ell(ic, x + 18, yy, 18, 6, ic.rgrad("#c8d8f8", "#6a8ac0"), "#1a2a50", 1.6)

    @app("akonadi-import-wizard", "akonadiimportwizard", "org.kde.akonadiimportwizard")
    def _(ic):
        shadow(ic); database(ic, 18, 16); arrow(ic, "r", 12, 30, 1.0)

    @app("pim-data-exporter", "pimdataexporter", "org.kde.pimdataexporter")
    def _(ic):
        shadow(ic); database(ic, 6, 16); arrow(ic, "r", 52, 30, 1.0, "#e0a020")

    @app("mbox-importer", "mboximporter", "org.kde.mboximporter")
    def _(ic):
        shadow(ic); envelope(ic, 14, 22, 44, 28); arrow(ic, "r", 10, 36, 0.8)

    @app("pim-sieve-editor", "sieveeditor", "org.kde.sieveeditor")
    def _(ic):
        page(ic); ic.path("M18 18 L46 15 L36 30 L36 42 L30 46 L30 32 Z", ic.grad("#7ac0f0", "#2a6ab0"), "#123a6a", 1.6)

    @app("grantlee-editor", "contactthemeeditor", "headerthemeeditor", "org.kde.contactthemeeditor", "org.kde.headerthemeeditor")
    def _(ic):
        page(ic); text_lines(ic, n=4)
        ic.path("M30 52 L50 30 L55 34 L36 56 Z", ic.grad("#ffe066", "#c08000", 0, 0, 1, 0), "#5a3a00", 1.4)
        ic.path("M50 30 l5 4 l3 -6 Z", "#d04060", "#5a1020", 1)

    @app("plasma-phonebook", "org.kde.phonebook")
    def _(ic):
        phone(ic, screen="#f4f4f4"); person(ic, 32, 32, 0.8)

    @app("plasma-settings", "org.kde.mobile.plasmasettings")
    def _(ic):
        phone(ic, screen="#f4f4f4"); gear(ic, 32, 30, 10, "#8aa6d6")

    @app("qmlkonsole")
    def _(ic):
        phone(ic, screen="#151515"); ic.path("M24 18 l5 3 l-5 3 M30 28 h8", "none", "#3cff3c", 2)

    @app("yakuake")
    def _(ic):
        shadow(ic); ic.raw('<rect x="4" y="4" width="56" height="34" rx="2" fill="#151515" stroke="#000" stroke-width="2"/>')
        ic.path("M10 12 l5 3 l-5 3 M18 20 h10", "none", "#3cff3c", 2.2)
        quad(ic, [(24, 44), (40, 44), (32, 56)], "#e0e0e0", 1.6)

    @app("francis")
    def _(ic):
        shadow(ic); tomato(ic, 32, 34, 22)
        ic.path("M32 20 V34 L42 38", "none", "#fff", 2.4)

    @app("ghostwriter")
    def _(ic):
        page(ic); text_lines(ic, n=6)
        ic.path("M34 54 C38 34 46 18 58 8 C56 22 50 38 38 52 Z", ic.grad("#ffffff", "#b8c8e0", 0, 0, 1, 1), "#4a5a7a", 1.6)
        ic.path("M34 54 L52 18", "none", "#4a5a7a", 1)

    @app("calligrawords", "calligra", "org.kde.calligrawords")
    def _(ic):
        page(ic); text_lines(ic, n=6); badge(ic, "#2a5ad0", label="W")

    @app("calligrasheets", "org.kde.calligrasheets")
    def _(ic):
        ns["ICONS"]["x-office-spreadsheet"][2](ic)

    @app("calligrastage", "org.kde.calligrastage")
    def _(ic):
        ns["ICONS"]["x-office-presentation"][2](ic)

    @app("karbon", "org.kde.karbon")
    def _(ic):
        page(ic); ic.path("M18 46 C22 20 40 20 44 40", "none", "#2a5ad0", 2.4)
        for (x, y) in ((18, 46), (44, 40), (24, 22), (40, 22)):
            ic.raw('<rect x="%g" y="%g" width="5" height="5" fill="#fff" stroke="#e03030" stroke-width="1.4"/>' % (x - 2.5, y - 2.5))

    @app("ark", "utilities-file-archiver")
    def _(ic):
        ns["ICONS"]["package-x-generic"][2](ic)
        ic.raw('<rect x="31" y="27" width="9" height="12" rx="1.5" fill="%s" stroke="#333" stroke-width="1.2"/>' % ic.grad("#f0f0f0", "#909090"))
        for y in (30, 33, 36):
            ic.path("M33 %g h5" % y, "none", "#555", 1)

    @app("kgraphviewer")
    def _(ic):
        page(ic)
        pts = [(31, 18), (22, 32), (40, 32), (22, 46), (40, 46)]
        for a, b in ((0, 1), (0, 2), (1, 3), (2, 4), (1, 4)):
            ic.path("M%g %g L%g %g" % (*pts[a], *pts[b]), "none", "#555", 1.4)
        for p in pts:
            ell(ic, p[0], p[1], 5, 3.4, "#fff8d0", "#5a4a10", 1.2)

    # ------------------------------------------------------------------
    # register
    # ------------------------------------------------------------------
    for name, (fn, extra) in APPS.items():
        if name.endswith("-x"):
            continue
        names = ["org.kde." + name, name]
        nohyph = name.replace("-", "")
        if nohyph != name:
            names += ["org.kde." + nohyph, nohyph]
        for e in extra:
            if e not in names:
                names.append(e)
        ICONS[names[0]] = ("apps", tuple(names), fn)
    return sorted(APPS)
