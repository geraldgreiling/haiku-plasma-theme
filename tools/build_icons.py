#!/usr/bin/env python3
"""Generates the 'Haiku' icon theme core set (original artwork, MIT).

Style: slight 3/4 perspective, saturated vertical/diagonal gradients and a dark
outline in a darker shade of the fill colour – the visual language of Haiku's
vector icons. Everything not covered here is inherited from Breeze.
"""
import os
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "icons/Haiku"
_gid = [0]


def tint(c, t):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    v = [int(c[i:i + 2], 16) for i in (0, 2, 4)]
    f = (lambda x: 255 - (255 - x) * t) if t < 1 else (lambda x: x * (2 - t))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(f(x)))) for x in v)


class Icon:
    def __init__(self):
        self.defs, self.body = [], []

    def grad(self, c1, c2, x1=0, y1=0, x2=0, y2=1, stops=None):
        _gid[0] += 1
        gid = "g%d" % _gid[0]
        st = stops or [(0, c1), (1, c2)]
        s = "".join('<stop offset="%g" stop-color="%s"/>' % (o, c) for o, c in st)
        self.defs.append('<linearGradient id="%s" x1="%g" y1="%g" x2="%g" y2="%g">%s</linearGradient>'
                         % (gid, x1, y1, x2, y2, s))
        return "url(#%s)" % gid

    def rgrad(self, c1, c2, cx=0.35, cy=0.3, r=0.75):
        _gid[0] += 1
        gid = "g%d" % _gid[0]
        self.defs.append('<radialGradient id="%s" cx="%g" cy="%g" r="%g"><stop offset="0" stop-color="%s"/>'
                         '<stop offset="1" stop-color="%s"/></radialGradient>' % (gid, cx, cy, r, c1, c2))
        return "url(#%s)" % gid

    def path(self, d, fill, stroke=None, sw=2.0, extra=""):
        st = ' stroke="%s" stroke-width="%g" stroke-linejoin="round" stroke-linecap="round"' % (stroke, sw) if stroke else ""
        self.body.append('<path d="%s" fill="%s"%s %s/>' % (d, fill, st, extra))

    def raw(self, s):
        self.body.append(s)

    def svg(self):
        return ('<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64">'
                '<defs>%s</defs>%s</svg>\n' % ("".join(self.defs), "".join(self.body)))


# ----------------------------------------------------------------------------
# base shapes
# ----------------------------------------------------------------------------
def shadow(ic, cx=32, cy=58, rx=24, ry=4):
    ic.raw('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#000" opacity="0.18"/>' % (cx, cy, rx, ry))


def folder(ic, col="#ffc21a"):
    dark = tint(col, 1.55)
    shadow(ic, 33, 57, 25, 4)
    # back plate with tab
    ic.path("M6 20 L22 14 L28 18 L52 10 L56 44 L12 54 Z", ic.grad(tint(col, 1.15), tint(col, 1.3)), dark)
    # paper sheet
    ic.path("M12 22 L50 13 L52 40 L15 49 Z", "#fdfdf8", tint("#d0d0c0", 1.2), 1.2)
    # front flap (perspective)
    ic.path("M4 30 L46 20 L60 46 L14 56 Z", ic.grad(tint(col, 0.55), col, 0, 0, 0.3, 1), dark)
    ic.path("M7 31 L45 22", "none", tint(col, 0.2), 1.2)


def folder_emblem(ic, kind):
    # emblems are drawn on the front flap (centre ~ (33,40))
    if kind == "home":
        ic.path("M24 42 L33 34 L42 40 L40 49 L27 51 Z", "#ffffff", "#7a4a00", 1.6)
        ic.path("M31 50 L31 44 L36 43 L36 49", "#c0392b", "#7a4a00", 1.2)
    elif kind == "desktop":
        ic.path("M23 38 L42 34 L43 45 L24 49 Z", ic.grad("#7fb2e6", "#2f6aa8"), "#1c3d63", 1.6)
    elif kind == "documents":
        ic.path("M26 35 L38 33 L40 48 L28 50 Z", "#ffffff", "#555", 1.4)
        for y in (38, 41, 44):
            ic.path("M29 %g L37 %g" % (y, y - 1.6), "none", "#888", 1)
    elif kind == "download":
        ic.path("M30 33 L36 32 L36 40 L41 39 L34 48 L26 42 L30 41 Z", ic.grad("#7ad36b", "#2e8b22"), "#1d5a15", 1.5)
    elif kind == "music":
        ic.path("M30 47 a3.5 3 -10 1 1 -1 -1 L30 35 L40 33 L40 44 a3.5 3 -10 1 1 -1 -1 L39 37 L31 38.6 Z",
                "#3a3a80", "#1a1a40", 1)
    elif kind == "pictures":
        ic.path("M24 37 L42 34 L43 47 L25 50 Z", "#bfe3ff", "#355", 1.4)
        ic.path("M25 49 L31 41 L35 45 L38 42 L42.6 46.5 Z", "#4c9a3a")
        ic.raw('<circle cx="38" cy="38" r="2" fill="#ffd400"/>')
    elif kind == "videos":
        ic.path("M24 37 L42 34 L43 47 L25 50 Z", "#333", "#111", 1.4)
        ic.path("M31 38.5 L37 41 L31.6 45.4 Z", "#fff")
    elif kind == "templates":
        ic.path("M26 36 L39 34 L40 48 L27 50 Z", "none", "#7a4a00", 1.4, 'stroke-dasharray="2 2"')
    elif kind == "public":
        ic.raw('<circle cx="29" cy="41" r="3.5" fill="#3b7dd8" stroke="#1d3f6e" stroke-width="1.2"/>')
        ic.raw('<circle cx="38" cy="39" r="3.5" fill="#d84f3b" stroke="#6e1d1d" stroke-width="1.2"/>')
    elif kind == "network":
        ic.raw('<circle cx="33" cy="41" r="6" fill="%s" stroke="#1d3f6e" stroke-width="1.4"/>' % ic.rgrad("#bfe0ff", "#2a6ec2"))
        ic.path("M27 41 L39 41 M33 35 C30 38 30 44 33 47 M33 35 C36 38 36 44 33 47", "none", "#1d3f6e", 1)


def page(ic, col="#ffffff", fold=True):
    shadow(ic, 33, 59, 20, 3)
    d = "M14 8 L40 5 L52 16 L52 57 L16 60 Z"
    ic.path(d, ic.grad("#ffffff", tint(col, 1.06), 0, 0, 1, 1) if col == "#ffffff" else ic.grad(tint(col, .3), col, 0, 0, 1, 1),
            "#5b5b5b", 1.8)
    if fold:
        ic.path("M40 5 L41 15 L52 16 Z", ic.grad("#e8e8e8", "#bdbdbd", 0, 0, 1, 1), "#5b5b5b", 1.5)


def text_lines(ic, x0=19, x1=44, y0=22, n=8, step=4, col="#8a8a8a"):
    for i in range(n):
        y = y0 + i * step
        ic.path("M%g %g L%g %g" % (x0, y, x1 - (6 if i % 4 == 3 else 0), y - 0.6), "none", col, 1.4)


def badge(ic, col, kind=None, label=None):
    """coloured type badge in the lower right corner of a page"""
    ic.path("M30 40 L54 37 L56 54 L32 58 Z", ic.grad(tint(col, .45), col), tint(col, 1.5), 1.6)
    if label:
        ic.raw('<text x="43" y="52" font-family="sans-serif" font-weight="bold" font-size="9" fill="#fff" '
               'text-anchor="middle" transform="rotate(-7 43 50)">%s</text>' % label)


def globe(ic, cx=32, cy=32, r=22, c1="#c8e6ff", c2="#2468c0", land="#3fa34d"):
    ic.raw('<circle cx="%g" cy="%g" r="%g" fill="%s" stroke="%s" stroke-width="2"/>' % (cx, cy, r, ic.rgrad(c1, c2), tint(c2, 1.5)))
    s = r / 22.0
    def P(x, y):
        return "%g %g" % (cx + x * s, cy + y * s)
    ic.path("M%s C%s %s %s C%s %s %s C%s %s %s Z" % (P(-14, -10), P(-8, -18), P(4, -16), P(2, -8),
                                                   P(0, -2), P(-6, 2), P(-8, 8), P(-14, 6), P(-18, 0), P(-14, -10)),
            land, tint(land, 1.4), 1.2)
    ic.path("M%s C%s %s %s C%s %s %s Z" % (P(6, 4), P(14, 0), P(18, 6), P(14, 14), P(10, 18), P(4, 12), P(6, 4)),
            land, tint(land, 1.4), 1.2)
    ic.raw('<ellipse cx="%g" cy="%g" rx="%g" ry="%g" fill="#fff" opacity="0.35"/>' % (cx - 7 * s, cy - 10 * s, 9 * s, 5 * s))


def box3d(ic, front, top, side, x=8, y=22, w=40, h=26, d=10):
    """iso box: front face rect skewed slightly, top and right side"""
    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y, x + d, y - d * 0.6, x + w + d, y - d * 0.6, x + w, y), top, tint("#808080", 1.6), 1.8)
    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x + w, y, x + w + d, y - d * 0.6, x + w + d, y + h - d * 0.6, x + w, y + h), side, tint("#808080", 1.6), 1.8)
    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y, x + w, y, x + w, y + h, x, y + h), front, tint("#808080", 1.6), 1.8)


def monitor(ic, screen_fill, x=6, y=8, w=46, h=34):
    shadow(ic, 32, 58, 22, 3.5)
    ic.path("M24 46 L40 46 L44 56 L20 56 Z", ic.grad("#d8d8d8", "#8c8c8c"), "#4a4a4a", 1.6)
    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 2, x + w, y, x + w + 4, y + h, x + 2, y + h + 4),
            ic.grad("#f0f0f0", "#a8a8a8", 0, 0, 1, 1), "#4a4a4a", 2)
    ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x + 4, y + 5.5, x + w - 3, y + 4, x + w, y + h - 3, x + 5.5, y + h),
            screen_fill, "#303030", 1.4)


def cylinder_trash(ic, full=False):
    shadow(ic, 32, 58, 20, 4)
    body = ic.grad("#f2f2f2", "#8e8e8e", 0, 0, 1, 0, [(0, "#9a9a9a"), (0.35, "#f4f4f4"), (1, "#7b7b7b")])
    ic.path("M14 18 L50 18 L46 56 Q32 61 18 56 Z", body, "#404040", 2)
    for x0, x1 in ((22, 23), (32, 32), (42, 41)):
        ic.path("M%g 24 L%g 53" % (x0, x1), "none", "#6b6b6b", 1.6)
    ic.raw('<ellipse cx="32" cy="18" rx="19" ry="5" fill="%s" stroke="#404040" stroke-width="2"/>' % ic.grad("#ffffff", "#a0a0a0"))
    ic.raw('<ellipse cx="32" cy="18" rx="14" ry="3" fill="#5a5a5a"/>')
    if full:
        ic.path("M17 19 C16 6 28 6 32 12 C36 4 50 6 47 19 C40 22 24 22 17 19 Z", "#fff", "#555", 1.4)
        ic.path("M24 12 L30 16 M38 10 L42 15 M34 17 L40 18", "none", "#999", 1.2)


def gear(ic, cx, cy, r, col):
    import math
    pts = []
    teeth = 8
    for i in range(teeth * 2):
        a = math.pi * 2 * i / (teeth * 2)
        rr = r if i % 2 == 0 else r * 0.78
        a1, a2 = a - math.pi / (teeth * 2) * 0.6, a + math.pi / (teeth * 2) * 0.6
        pts.append("%g %g" % (cx + rr * math.cos(a1), cy + rr * math.sin(a1)))
        pts.append("%g %g" % (cx + rr * math.cos(a2), cy + rr * math.sin(a2)))
    ic.path("M" + " L".join(pts) + " Z", ic.rgrad(tint(col, .3), col), tint(col, 1.55), 1.8)
    ic.raw('<circle cx="%g" cy="%g" r="%g" fill="#d8d8d8" stroke="%s" stroke-width="1.6"/>' % (cx, cy, r * 0.32, tint(col, 1.55)))


# ----------------------------------------------------------------------------
# icon definitions
# ----------------------------------------------------------------------------
ICONS = {}


def icon(cat, *names):
    def deco(fn):
        ICONS[names[0]] = (cat, names, fn)
        return fn
    return deco


@icon("places", "folder", "inode-directory", "folder-open", "folder-blue", "folder-yellow")
def i_folder(ic):
    folder(ic)


for _kind, _names in {
    "home": ("user-home", "folder-home"),
    "desktop": ("user-desktop", "folder-desktop"),
    "documents": ("folder-documents",),
    "download": ("folder-download", "folder-downloads"),
    "music": ("folder-music", "folder-sound"),
    "pictures": ("folder-pictures", "folder-images"),
    "videos": ("folder-videos", "folder-video"),
    "templates": ("folder-templates",),
    "public": ("folder-publicshare", "folder-public"),
    "network": ("folder-network", "folder-remote"),
}.items():
    def _mk(kind):
        def fn(ic):
            folder(ic)
            folder_emblem(ic, kind)
        return fn
    ICONS[_names[0]] = ("places", _names, _mk(_kind))


@icon("places", "user-trash", "trashcan_empty")
def i_trash(ic):
    cylinder_trash(ic)


@icon("places", "user-trash-full", "trashcan_full")
def i_trash_full(ic):
    cylinder_trash(ic, True)


@icon("places", "network-workgroup", "network-server", "folder-network-symbolic-x")
def i_network(ic):
    shadow(ic)
    globe(ic, 32, 30, 22)


@icon("devices", "drive-harddisk", "drive-harddisk-root", "drive-harddisk-system")
def i_hdd(ic):
    shadow(ic, 34, 56, 24, 3.5)
    box3d(ic, ic.grad("#e4e4e4", "#9a9a9a"), ic.grad("#ffffff", "#cfcfcf"), ic.grad("#b0b0b0", "#7a7a7a"), 5, 28, 44, 24, 14)
    ic.path("M10 44 L36 44", "none", "#666", 1.4)
    ic.raw('<circle cx="43" cy="44" r="2.3" fill="#39d439" stroke="#145214" stroke-width="1"/>')


@icon("devices", "drive-removable-media", "drive-removable-media-usb", "media-flash")
def i_usb(ic):
    shadow(ic, 34, 56, 20, 3)
    box3d(ic, ic.grad("#7fb2ff", "#2f5fc0"), ic.grad("#bcd6ff", "#7fa6e6"), ic.grad("#3a64b8", "#203f80"), 8, 32, 38, 20, 12)
    ic.path("M14 32 L19 22 L33 22 L28 32 Z", "#d0d0d0", "#555", 1.4)
    ic.raw('<circle cx="40" cy="42" r="1.8" fill="#ffcc00"/>')


@icon("devices", "media-optical", "drive-optical", "media-optical-cd", "media-optical-dvd")
def i_optical(ic):
    shadow(ic, 32, 56, 22, 3.5)
    ic.raw('<ellipse cx="32" cy="34" rx="26" ry="20" fill="%s" stroke="#555" stroke-width="2"/>'
           % ic.grad("#e6e6ff", "#ffd6f0", 0, 0, 1, 1, [(0, "#d8f0ff"), (0.3, "#ffe7ba"), (0.55, "#f6c8ff"), (0.8, "#c7ffd8"), (1, "#bcd0ff")]))
    ic.raw('<ellipse cx="32" cy="34" rx="7" ry="5.4" fill="#f4f4f4" stroke="#777" stroke-width="1.5"/>')
    ic.raw('<ellipse cx="32" cy="34" rx="2.6" ry="2" fill="#444"/>')


@icon("devices", "computer", "computer-laptop", "system")
def i_computer(ic):
    monitor(ic, ic.grad("#5a9de6", "#1f4f9a", 0, 0, 1, 1))
    ic.path("M14 18 L28 15", "none", "#ffffff", 1.4, 'opacity="0.6"')


@icon("places", "start-here", "start-here-kde", "start-here-kde-plasma", "start-here-symbolic-x",
      "distributor-logo")
def i_start(ic):
    # a generic green leaf (Deskbar "leaf menu" idea, not the Haiku logo)
    shadow(ic, 32, 57, 18, 3)
    ic.path("M12 52 C10 30 24 10 54 8 C54 34 40 52 12 52 Z", ic.grad("#b8f07a", "#2f8f1f", 0, 0, 1, 1), "#1b5a12", 2.2)
    ic.path("M14 50 C24 38 34 26 48 14", "none", "#1b5a12", 1.8)
    for (a, b, c, d) in ((24, 38, 22, 28), (30, 31, 30, 22), (36, 25, 38, 17), (28, 34, 38, 36), (35, 27, 44, 28)):
        ic.path("M%g %g L%g %g" % (a, b, c, d), "none", "#2b7a1d", 1.3)
    ic.path("M12 52 L8 58", "none", "#1b5a12", 2.4)


# --- mime types ---------------------------------------------------------------
@icon("mimetypes", "text-plain", "text-x-generic", "text-x-readme", "text-x-log")
def i_text(ic):
    page(ic)
    text_lines(ic)


@icon("mimetypes", "unknown", "application-octet-stream", "application-x-zerosize")
def i_unknown(ic):
    page(ic)
    ic.raw('<text x="33" y="45" font-family="sans-serif" font-weight="bold" font-size="24" fill="#9a9a9a" '
           'text-anchor="middle">?</text>')


@icon("mimetypes", "text-html", "application-xhtml+xml", "text-xml")
def i_html(ic):
    page(ic)
    text_lines(ic, n=4)
    globe(ic, 42, 46, 11)


@icon("mimetypes", "application-x-executable", "application-x-sharedlib", "application-x-desktop",
      "application-x-appimage")
def i_exec(ic):
    shadow(ic, 33, 57, 22, 3.5)
    # Haiku style "application" diamond
    ic.path("M32 8 L58 30 L32 54 L6 30 Z", ic.grad("#9fd0ff", "#2e6fc6", 0, 0, 1, 1), "#173d70", 2.2)
    ic.path("M32 15 L50 30 L32 47 L14 30 Z", "none", "#d8ecff", 1.4, 'opacity="0.7"')
    gear(ic, 32, 31, 9, "#f0b400")


@icon("mimetypes", "application-x-shellscript", "text-x-script", "text-x-python", "application-x-perl",
      "text-x-csrc", "text-x-c++src", "text-x-chdr", "application-javascript", "text-x-makefile")
def i_script(ic):
    page(ic)
    ic.path("M19 23 L44 20 L46 44 L21 47 Z", "#1e1e1e", "#000", 1.2)
    ic.path("M23 29 L28 32 L23.6 35.4 M30 37 L37 36", "none", "#3cff3c", 1.8)
    badge(ic, "#3a9a3a", label="SH")


@icon("mimetypes", "image-x-generic", "image-png", "image-jpeg", "image-svg+xml", "image-gif", "image-bmp",
      "image-webp", "image-tiff")
def i_image(ic):
    shadow(ic, 33, 57, 22, 3.5)
    ic.path("M8 12 L54 8 L58 50 L12 56 Z", ic.grad("#fff", "#d9d9d9", 0, 0, 1, 1), "#4d4d4d", 2)
    ic.path("M13 17 L50 13.5 L53.5 46 L16 50.5 Z", ic.grad("#a7d8ff", "#e9f6ff"), "#355a7a", 1.2)
    ic.path("M16 50.5 L28 32 L36 42 L42 35 L53.5 46 Z", ic.grad("#7ccd5a", "#2f7d22"), "#1d5214", 1.2)
    ic.raw('<circle cx="43" cy="23" r="4" fill="%s" stroke="#a87000" stroke-width="1"/>' % ic.rgrad("#fff6b0", "#ffc400"))


@icon("mimetypes", "audio-x-generic", "audio-mpeg", "audio-x-wav", "audio-flac", "audio-ogg", "audio-x-mpegurl")
def i_audio(ic):
    page(ic)
    ic.path("M24 50 a5 4 -10 1 1 -1.5 -1.4 L22.5 26 L42 22 L42 44 a5 4 -10 1 1 -1.5 -1.4 L40.5 30 L24 33.4 Z",
            ic.grad("#7a7af0", "#25258a"), "#14144a", 1.4)


@icon("mimetypes", "video-x-generic", "video-mp4", "video-x-matroska", "video-webm", "video-quicktime")
def i_video(ic):
    shadow(ic, 33, 57, 22, 3.5)
    ic.path("M6 14 L56 10 L58 50 L8 54 Z", "#2b2b2b", "#000", 2)
    for i in range(6):
        x = 10 + i * 8
        ic.path("M%g %g l4 -0.3 l0 3 l-4 0.3 Z" % (x, 13.5 - i * 0.3), "#ddd")
        ic.path("M%g %g l4 -0.3 l0 3 l-4 0.3 Z" % (x + 1, 49 - i * 0.3), "#ddd")
    ic.path("M12 19 L52 16 L53.5 45 L13.5 48 Z", ic.grad("#5aa0ff", "#123a80", 0, 0, 1, 1))
    ic.path("M28 25 L40 31 L29 39 Z", "#fff", "#333", 1)


@icon("mimetypes", "application-pdf", "application-postscript", "image-vnd.djvu")
def i_pdf(ic):
    page(ic)
    text_lines(ic, n=4)
    badge(ic, "#d03020", label="PDF")


@icon("mimetypes", "package-x-generic", "application-x-archive", "application-zip", "application-x-tar",
      "application-x-compressed-tar", "application-x-7z-compressed", "application-x-rar",
      "application-x-bzip-compressed-tar", "application-x-xz-compressed-tar", "application-gzip")
def i_package(ic):
    shadow(ic, 34, 57, 24, 3.5)
    box3d(ic, ic.grad("#e6b779", "#a86f2c"), ic.grad("#f6d7a6", "#d9a868"), ic.grad("#b07a3a", "#7c5020"), 8, 26, 38, 26, 12)
    ic.path("M24 26 L34 18.8 L40 18.8 L30 26 Z", "#f4f0e0", "#7c5020", 1.2)
    ic.path("M24 26 L30 26 L30 52 L24 52 Z", "#f4f0e0", "#7c5020", 1.2)


@icon("mimetypes", "x-office-document", "application-vnd.oasis.opendocument.text", "application-msword",
      "application-vnd.openxmlformats-officedocument.wordprocessingml.document", "application-rtf")
def i_doc(ic):
    page(ic)
    text_lines(ic, n=6)
    badge(ic, "#2f62c8", label="DOC")


@icon("mimetypes", "x-office-spreadsheet", "application-vnd.oasis.opendocument.spreadsheet",
      "application-vnd.ms-excel", "application-vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text-csv")
def i_sheet(ic):
    page(ic)
    for i in range(6):
        y = 21 + i * 5
        ic.path("M19 %g L46 %g" % (y, y - 0.8), "none", "#9a9a9a", 1)
    for x in (27, 36):
        ic.path("M%g 19 L%g 46" % (x, x + 0.4), "none", "#9a9a9a", 1)
    badge(ic, "#2e9a3c", label="XLS")


@icon("mimetypes", "x-office-presentation", "application-vnd.oasis.opendocument.presentation",
      "application-vnd.ms-powerpoint", "application-vnd.openxmlformats-officedocument.presentationml.presentation")
def i_pres(ic):
    page(ic)
    ic.path("M20 22 L44 19.5 L45 36 L21 38.5 Z", ic.grad("#ffd27a", "#e8891a"), "#8a5010", 1.2)
    badge(ic, "#d9661a", label="PPT")


# --- applications -------------------------------------------------------------
@icon("apps", "system-file-manager", "org.kde.dolphin", "dolphin", "file-manager")
def i_fm(ic):
    folder(ic, "#ffc21a")
    ic.raw('<circle cx="40" cy="38" r="8" fill="%s" stroke="#333" stroke-width="2.2"/>' % ic.rgrad("#ffffff", "#9ad0ff"))
    ic.path("M45.5 44 L54 52", "none", "#333", 4)


@icon("apps", "utilities-terminal", "org.kde.konsole", "konsole", "terminal", "Terminal")
def i_term(ic):
    monitor(ic, "#151515")
    ic.path("M14 18 L21 22 L15 26.5 M23 29 L32 28", "none", "#38ff38", 2.4)


@icon("apps", "web-browser", "internet-web-browser", "applications-internet")
def i_web(ic):
    shadow(ic)
    globe(ic, 30, 30, 21, "#ffe9a8", "#e07a10", "#3f8fd3")
    ic.path("M40 44 L56 40 L50 56 Z", ic.grad("#ff6a5a", "#b01a10"), "#600", 1.6)


@icon("apps", "preferences-system", "systemsettings", "preferences-desktop", "applications-system",
      "preferences-other")
def i_settings(ic):
    shadow(ic, 32, 57, 20, 3.5)
    gear(ic, 26, 26, 17, "#8aa6d6")
    gear(ic, 44, 42, 12, "#f0b400")


@icon("apps", "accessories-text-editor", "org.kde.kate", "org.kde.kwrite", "kate", "kwrite", "text-editor")
def i_editor(ic):
    page(ic)
    text_lines(ic, n=7)
    ic.path("M30 52 L50 24 L56 28 L36 56 L29 58 Z", ic.grad("#ffe066", "#e6a800", 0, 0, 1, 0), "#6a4a00", 1.6)
    ic.path("M50 24 L56 28 L58 25 L52 21 Z", "#ff8aa0", "#6a4a00", 1.4)
    ic.path("M30 52 L36 56 L29 58 Z", "#333")


@icon("apps", "accessories-calculator", "org.kde.kcalc", "kcalc", "calc")
def i_calc(ic):
    shadow(ic, 32, 58, 18, 3)
    ic.path("M14 6 L46 4 L50 56 L18 59 Z", ic.grad("#d0d0d0", "#7e7e7e", 0, 0, 1, 1), "#3a3a3a", 2)
    ic.path("M19 10 L44 8.6 L45 19 L20 20.5 Z", "#b9d6a0", "#344a28", 1.4)
    for r in range(4):
        for c in range(3):
            x, y = 20 + c * 8.4 + r * 0.2, 25 + r * 7.6 - c * 0.5
            ic.path("M%g %g l6 -0.4 l0.4 5 l-6 0.4 Z" % (x, y), "#f2f2f2" if c < 2 else "#ffb030", "#444", 1)


@icon("apps", "internet-mail", "mail-client", "org.kde.kmail2", "kmail", "thunderbird-x")
def i_mail(ic):
    shadow(ic, 32, 56, 24, 3.5)
    ic.path("M6 18 L54 12 L58 46 L10 52 Z", ic.grad("#ffffff", "#d6d6d6", 0, 0, 1, 1), "#4a4a4a", 2)
    ic.path("M6 18 L33 36 L54 12", "none", "#4a4a4a", 1.8)
    ic.path("M44 17 L52 16 L53 24 L45 25 Z", "#d04040", "#701010", 1.2)


@icon("apps", "multimedia-video-player", "org.kde.dragonplayer", "vlc-x", "applications-multimedia",
      "org.kde.haruna")
def i_vplayer(ic):
    i_video(ic)


@icon("apps", "multimedia-audio-player", "org.kde.elisa", "elisa", "juk")
def i_aplayer(ic):
    shadow(ic, 32, 57, 20, 3.5)
    ic.path("M12 10 L46 6 L52 54 L18 58 Z", ic.grad("#5d5d5d", "#2a2a2a", 0, 0, 1, 1), "#000", 2)
    ic.raw('<ellipse cx="32" cy="38" rx="11" ry="12" fill="%s" stroke="#000" stroke-width="1.8"/>' % ic.rgrad("#bdbdbd", "#3a3a3a"))
    ic.raw('<ellipse cx="32" cy="38" rx="4" ry="4.3" fill="#111"/>')
    ic.raw('<ellipse cx="29" cy="18" rx="5" ry="5" fill="%s" stroke="#000" stroke-width="1.4"/>' % ic.rgrad("#bdbdbd", "#3a3a3a"))


@icon("apps", "image-viewer", "org.kde.gwenview", "gwenview", "eog-x")
def i_iviewer(ic):
    i_image(ic)
    ic.raw('<circle cx="44" cy="44" r="8" fill="%s" fill-opacity="0.7" stroke="#333" stroke-width="2.2"/>' % ic.rgrad("#ffffff", "#9ad0ff"))
    ic.path("M49.5 50 L57 57", "none", "#333", 4)


@icon("apps", "utilities-system-monitor", "org.kde.plasma-systemmonitor", "ksysguard", "system-monitor")
def i_sysmon(ic):
    monitor(ic, "#0c1a0c")
    ic.path("M12 32 L18 30 L22 22 L27 34 L32 18 L37 30 L41 26 L48 27", "none", "#39ff5a", 1.8)


@icon("apps", "system-software-install", "org.kde.discover", "plasmadiscover", "system-software-update",
      "applications-other")
def i_install(ic):
    i_package(ic)
    ic.path("M44 6 L52 5 L52.4 15 L58 14.4 L49 25 L39 16 L45 15.4 Z", ic.grad("#7ad36b", "#2e8b22"), "#1d5a15", 1.6)


@icon("apps", "help-browser", "help-about", "org.kde.khelpcenter", "khelpcenter", "help-contents")
def i_help(ic):
    shadow(ic)
    ic.raw('<circle cx="32" cy="30" r="22" fill="%s" stroke="#173d70" stroke-width="2.2"/>' % ic.rgrad("#bfe0ff", "#2a6ec2"))
    ic.raw('<text x="32" y="41" font-family="sans-serif" font-weight="bold" font-size="30" fill="#fff" '
           'stroke="#173d70" stroke-width="1" text-anchor="middle">?</text>')


@icon("apps", "accessories-screenshot", "org.kde.spectacle", "spectacle", "applets-screenshooter")
def i_shot(ic):
    shadow(ic, 32, 57, 24, 3.5)
    ic.path("M6 20 L22 18 L26 12 L38 11 L42 16 L56 15 L58 48 L8 52 Z", ic.grad("#9a9a9a", "#3c3c3c", 0, 0, 1, 1), "#111", 2)
    ic.raw('<circle cx="32" cy="34" r="11" fill="%s" stroke="#111" stroke-width="2"/>' % ic.rgrad("#9ad0ff", "#123a80"))
    ic.raw('<circle cx="28" cy="30" r="3" fill="#fff" opacity="0.7"/>')


@icon("apps", "preferences-desktop-theme", "preferences-desktop-color", "preferences-desktop-wallpaper",
      "preferences-desktop-theme-global")
def i_theme(ic):
    shadow(ic, 32, 57, 22, 3.5)
    ic.path("M8 30 C8 12 32 4 48 12 C60 18 58 32 50 34 C42 36 44 44 40 50 C34 58 8 52 8 30 Z",
            ic.grad("#f6e0b8", "#c9a066", 0, 0, 1, 1), "#6a4a20", 2)
    for cx, cy, col in ((20, 26, "#e03030"), (30, 16, "#ffcb00"), (42, 18, "#30a030"), (20, 40, "#3060e0")):
        ic.raw('<circle cx="%g" cy="%g" r="4.5" fill="%s" stroke="#333" stroke-width="1"/>' % (cx, cy, col))


@icon("apps", "applications-games", "input-gaming")
def i_games(ic):
    shadow(ic, 32, 56, 24, 3)
    ic.path("M8 30 C8 20 18 18 24 22 L40 22 C46 18 56 20 56 30 C56 42 50 48 44 42 L20 42 C14 48 8 42 8 30 Z",
            ic.grad("#c8c8c8", "#6a6a6a", 0, 0, 1, 1), "#2a2a2a", 2)
    ic.path("M16 31 L24 31 M20 27 L20 35", "none", "#222", 2.6)
    ic.raw('<circle cx="42" cy="29" r="2.5" fill="#e03030"/><circle cx="47" cy="34" r="2.5" fill="#3060e0"/>')


# ----------------------------------------------------------------------------
def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import icons_gear
    icons_gear.register(globals())
    import icons_apps
    icons_apps.register(globals())
    cats = {}
    for key, (cat, names, fn) in ICONS.items():
        _gid[0] = 0
        ic = Icon()
        fn(ic)
        d = os.path.join(OUT, "scalable", cat)
        os.makedirs(d, exist_ok=True)
        main_file = os.path.join(d, names[0] + ".svg")
        with open(main_file, "w") as f:
            f.write(ic.svg())
        for alias in names[1:]:
            if alias.endswith("-x"):
                continue  # placeholder names that are intentionally not installed
            link = os.path.join(d, alias + ".svg")
            if os.path.lexists(link):
                os.remove(link)
            os.symlink(names[0] + ".svg", link)
        cats.setdefault(cat, 0)
        cats[cat] += 1
    dirs = ["scalable/%s" % c for c in sorted(cats)]
    with open(os.path.join(OUT, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=Haiku\nComment=Haiku/BeOS inspired icon core set (falls back to Breeze)\n"
                "Inherits=breeze,hicolor\nExample=folder\nDisplayDepth=32\nDirectories=%s\n\n" % ",".join(dirs))
        ctx = {"places": "Places", "devices": "Devices", "mimetypes": "MimeTypes", "apps": "Applications"}
        for c in sorted(cats):
            f.write("[scalable/%s]\nSize=64\nMinSize=16\nMaxSize=512\nType=Scalable\nContext=%s\n\n" % (c, ctx[c]))
    print("icons:", sum(cats.values()), "originals", cats)


if __name__ == "__main__":
    main()
