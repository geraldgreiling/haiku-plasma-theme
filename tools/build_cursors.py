#!/usr/bin/env python3
"""Generates the 'Haiku' Xcursor theme (original artwork, MIT).

Needs: rsvg-convert, xcursorgen. Usage: build_cursors.py <outdir>
"""
import math
import os
import shutil
import subprocess
import sys
import tempfile

OUT = sys.argv[1] if len(sys.argv) > 1 else "cursors/Haiku-Cursors"
SIZES = [24, 32, 48, 64]
BLACK, WHITE = "#000000", "#ffffff"


def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32">%s</svg>' % body)


def outlined(d, fill=BLACK, outline=WHITE, w=1.6, transform=""):
    t = ' transform="%s"' % transform if transform else ""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%g" stroke-linejoin="round"%s/>'
            '<path d="%s" fill="%s"%s/>' % (d, outline, outline, w * 2, t, d, fill, t))


ARROW_D = "M4 3 L4 24.5 L9.2 19.8 L13 28.5 L16.6 27 L12.8 18.6 L19.8 18.6 Z"


def arrow():
    return outlined(ARROW_D)


HAND_D = ("M11 16 L11 5.2 C11 2.6 14.6 2.6 14.6 5.2 L14.6 12.6 C14.6 10.9 18 10.9 18 12.9 "
          "C18 11.3 21.4 11.3 21.4 13.4 C21.4 11.9 24.8 11.9 24.8 14.4 L24.8 21 C24.8 25.3 22.2 28.4 18.2 28.4 "
          "L15.4 28.4 C12.6 28.4 11.1 27 9.5 24.8 L5.6 19.4 C4.4 17.6 7 15.4 8.8 17.2 Z")


def hand():
    return (outlined(HAND_D, WHITE, BLACK, 0.9) +
            '<path d="M14.6 12.6 L14.6 17 M18 12.9 L18 17 M21.4 13.4 L21.4 17.2" stroke="#000" stroke-width="1" fill="none"/>')


OPEN_D = ("M9 17 L6.2 11.5 C5.2 9.6 7.8 8.2 9 10 L11.2 14 L10 6.5 C9.7 4.4 12.8 4 13.1 6.2 L14.2 13 "
          "L14.4 4.6 C14.4 2.4 17.6 2.4 17.6 4.6 L17.6 13 L19.2 5.8 C19.6 3.8 22.6 4.4 22.2 6.4 L20.8 14.2 "
          "L23.2 9.8 C24.2 8 26.8 9.2 25.8 11.2 L22.4 20.6 C21.2 25.4 18.6 28.4 15 28.4 C11.6 28.4 9.8 25.6 9 22 Z")
CLOSED_D = ("M8.6 15.6 C8.4 12.8 11.4 12.4 11.8 14.4 C11.8 11.6 15 11.4 15.2 13.6 C15.4 11.2 18.6 11.2 18.8 13.6 "
            "C19.2 11.6 22.4 11.8 22.4 14.4 C22.6 12.8 25.4 13 25.4 15.4 L25.4 20 C25.4 25 22.4 28.4 17.6 28.4 "
            "L15.6 28.4 C11.4 28.4 8.8 25 8.6 21 Z")


def ibeam():
    d = "M11 4 L13.5 4 C14.8 4 15.6 4.8 16 5.6 C16.4 4.8 17.2 4 18.5 4 L21 4 M16 5.6 L16 26.4 M11 28 L13.5 28 C14.8 28 15.6 27.2 16 26.4 C16.4 27.2 17.2 28 18.5 28 L21 28 M13 16 L19 16"
    return ('<path d="%s" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            '<path d="%s" fill="none" stroke="#000" stroke-width="1.8" stroke-linecap="round"/>' % (d, d))


def double_arrow(angle):
    d = "M16 2.5 L22 9 L18.2 9 L18.2 23 L22 23 L16 29.5 L10 23 L13.8 23 L13.8 9 L10 9 Z"
    return outlined(d, transform="rotate(%g 16 16)" % angle)


def split(angle):
    d = ("M16 2.5 L21.5 8.5 L18 8.5 L18 13 L28 13 L28 19 L18 19 L18 23.5 L21.5 23.5 L16 29.5 L10.5 23.5 L14 23.5 "
         "L14 19 L4 19 L4 13 L14 13 L14 8.5 L10.5 8.5 Z")
    return outlined(d, transform="rotate(%g 16 16)" % angle)


def fleur():
    d = ("M16 2 L21 7.5 L17.6 7.5 L17.6 14.4 L24.5 14.4 L24.5 11 L30 16 L24.5 21 L24.5 17.6 L17.6 17.6 L17.6 24.5 "
         "L21 24.5 L16 30 L11 24.5 L14.4 24.5 L14.4 17.6 L7.5 17.6 L7.5 21 L2 16 L7.5 11 L7.5 14.4 L14.4 14.4 "
         "L14.4 7.5 L11 7.5 Z")
    return outlined(d)


def crosshair():
    d = "M16 3 L16 13 M16 19 L16 29 M3 16 L13 16 M19 16 L29 16"
    return ('<path d="%s" stroke="#fff" stroke-width="4" stroke-linecap="round"/>'
            '<path d="%s" stroke="#000" stroke-width="1.6" stroke-linecap="round"/>'
            '<circle cx="16" cy="16" r="1.2" fill="#000" stroke="#fff" stroke-width="0.8"/>' % (d, d))


def up_arrow():
    return outlined("M16 3 L26 14 L19.5 14 L19.5 29 L12.5 29 L12.5 14 L6 14 Z")


def forbidden():
    return ('<circle cx="16" cy="16" r="11" fill="none" stroke="#fff" stroke-width="7"/>'
            '<circle cx="16" cy="16" r="11" fill="none" stroke="#d01010" stroke-width="3.6"/>'
            '<path d="M8.2 23.8 L23.8 8.2" stroke="#fff" stroke-width="7"/>'
            '<path d="M8.6 23.4 L23.4 8.6" stroke="#d01010" stroke-width="3.6"/>')


def pencil():
    d = "M4 28 L6 21 L22 5 L27 10 L11 26 Z"
    return (outlined(d, "#ffcb00", BLACK, 0.9) +
            '<path d="M4 28 L6 21 L11 26 Z" fill="#000"/><path d="M19 8 L24 13" stroke="#000" stroke-width="1"/>')


def badge(content_svg, x=17, y=17, color="#ffcb00"):
    return ('<rect x="%g" y="%g" width="13" height="13" rx="2" fill="%s" stroke="#000" stroke-width="1.2"/>%s'
            % (x, y, color, content_svg))


def spinner(phase, cx=16, cy=16, r=11, small=False):
    """Haiku-ish busy indicator: ring of 8 dots, highlight rotating"""
    out = []
    n = 8
    rr = r * 0.85
    dot = 2.6 if not small else 1.7
    for i in range(n):
        a = 2 * math.pi * i / n - math.pi / 2
        k = (i - phase) % n
        col = ["#ffcb00", "#f0b000", "#c8a040", "#909090", "#a8a8a8", "#bcbcbc", "#cccccc", "#dcdcdc"][k]
        x, y = cx + rr * math.cos(a), cy + rr * math.sin(a)
        out.append('<circle cx="%.2f" cy="%.2f" r="%g" fill="%s" stroke="#000" stroke-width="%g"/>'
                   % (x, y, dot, col, 0.9 if not small else 0.7))
    bg = ('<circle cx="%g" cy="%g" r="%g" fill="#fff" fill-opacity="0.85" stroke="#000" stroke-width="1"/>'
          % (cx, cy, r + dot + 0.6))
    return bg + "".join(out)


CURSORS = {
    # name: (frames(list of svg bodies), hotspot, aliases, frame delay ms)
    "left_ptr": ([arrow()], (4, 3), ["default", "arrow", "top_left_arrow", "left_arrow", "right_ptr", "draft_large", "draft_small"]),
    "hand2": ([hand()], (12.8, 3), ["hand1", "pointer", "pointing_hand", "9d800788f1b08800ae810202380a0822",
                                   "e29285e634086352946a0e7090d73106"]),
    "xterm": ([ibeam()], (16, 16), ["text", "ibeam", "vertical-text"]),
    "crosshair": ([crosshair()], (16, 16), ["cross", "tcross", "cross_reverse", "diamond_cross", "cell", "color-picker"]),
    "fleur": ([fleur()], (16, 16), ["move", "size_all", "all-scroll", "4498f0e0c1937ffe01fd06f973665830",
                                   "9081237383d90e509aa00f00170e968f"]),
    "size_ver": ([double_arrow(0)], (16, 16), ["ns-resize", "n-resize", "s-resize", "v_double_arrow", "sb_v_double_arrow",
                                              "top_side", "bottom_side", "00008160000006810000408080010102",
                                              "2870a09082c103050810ffdffffe0204"]),
    "size_hor": ([double_arrow(90)], (16, 16), ["ew-resize", "e-resize", "w-resize", "h_double_arrow", "sb_h_double_arrow",
                                               "left_side", "right_side", "028006030e0e7ebffc7f7070c0600140",
                                               "14fef782d02440884392942c11205230"]),
    "size_fdiag": ([double_arrow(-45)], (16, 16), ["nwse-resize", "nw-resize", "se-resize", "top_left_corner",
                                                  "bottom_right_corner", "bd_double_arrow", "c7088f0f3e6c8088236ef8e1e3e70000"]),
    "size_bdiag": ([double_arrow(45)], (16, 16), ["nesw-resize", "ne-resize", "sw-resize", "top_right_corner",
                                                 "bottom_left_corner", "fd_double_arrow", "fcf1c3c7cd4491d801f1e1c78f100000"]),
    "split_v": ([split(0)], (16, 16), ["row-resize", "sb_v_double_arrow2"]),
    "split_h": ([split(90)], (16, 16), ["col-resize"]),
    "up_arrow": ([up_arrow()], (16, 3), ["center_ptr", "sb_up_arrow"]),
    "not-allowed": ([forbidden()], (16, 16), ["forbidden", "circle", "crossed_circle", "no-drop", "dnd-no-drop",
                                             "03b6e0fcb3499374a867c041f52298f0"]),
    "openhand": ([outlined(OPEN_D, WHITE, BLACK, 0.9)], (16, 12), ["grab", "9141b49c8149039304290b508d208c40", "all_scroll_hand"]),
    "closedhand": ([outlined(CLOSED_D, WHITE, BLACK, 0.9)], (16, 16), ["grabbing", "dnd-move", "dnd-none",
                                                                     "fcf21c00b30f7e3f83fe0dfd12e71cff"]),
    "help": ([arrow() + badge('<text x="23.5" y="27.8" font-family="sans-serif" font-weight="bold" font-size="11" '
                              'text-anchor="middle" fill="#000">?</text>', color="#7fb6ff")], (4, 3),
             ["question_arrow", "whats_this", "left_ptr_help", "dnd-ask", "d9ce0ab605698f320427677b458ad60b",
              "5c6cd98b3f3ebcb1f9c7f1c204630408"]),
    "copy": ([arrow() + badge('<path d="M23.5 19.5 L23.5 27.5 M19.5 23.5 L27.5 23.5" stroke="#000" stroke-width="2"/>',
                              color="#7ed46e")], (4, 3),
             ["dnd-copy", "1081e37283d90000800003c07f3ef6bf", "6407b0e94181790501fd1e167b474872"]),
    "alias": ([arrow() + badge('<path d="M20 27 C20 21 22 20.5 26 20.5 M23.5 18.2 L26.5 20.5 L23.5 22.8" fill="none" '
                               'stroke="#000" stroke-width="1.8"/>', color="#ffffff")], (4, 3),
              ["link", "dnd-link", "3085a0e285430894940527032f8b26df", "640fb0e74195791501fd1ed57b41487f"]),
    "pencil": ([pencil()], (4, 28), []),
    "watch": ([spinner(i) for i in range(8)], (16, 16), ["wait"], 90),
    "left_ptr_watch": ([arrow() + spinner(i, 23.5, 23.5, 5.2, True) for i in range(8)], (4, 3),
                       ["progress", "half-busy", "08e8e1c95fe2fc01f976f1e063a24ccd", "3ecb610c1bf2410f44200f48c40d3599"], 90),
}


def main():
    if not shutil.which("xcursorgen") or not shutil.which("rsvg-convert"):
        sys.exit("needs xcursorgen and rsvg-convert")
    cdir = os.path.join(OUT, "cursors")
    os.makedirs(cdir, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for name, spec in CURSORS.items():
        frames, (hx, hy), aliases = spec[0], spec[1], spec[2]
        delay = spec[3] if len(spec) > 3 else None
        cfg = []
        for fi, body in enumerate(frames):
            sp = os.path.join(tmp, "%s_%d.svg" % (name, fi))
            with open(sp, "w") as f:
                f.write(svg(body))
            for s in SIZES:
                png = os.path.join(tmp, "%s_%d_%d.png" % (name, fi, s))
                subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), sp, "-o", png], check=True)
                line = "%d %d %d %s" % (s, round(hx * s / 32), round(hy * s / 32), png)
                if delay:
                    line += " %d" % delay
                cfg.append(line)
        cp = os.path.join(tmp, name + ".cfg")
        with open(cp, "w") as f:
            f.write("\n".join(cfg) + "\n")
        subprocess.run(["xcursorgen", cp, os.path.join(cdir, name)], check=True)
        for a in aliases:
            link = os.path.join(cdir, a)
            if os.path.lexists(link):
                os.remove(link)
            os.symlink(name, link)
    with open(os.path.join(OUT, "index.theme"), "w") as f:
        f.write("[Icon Theme]\nName=Haiku Cursors\nComment=Haiku/BeOS inspired cursors\nInherits=breeze_cursors\n")
    print("cursors:", len(CURSORS), "base cursors written to", cdir, "tmp:", tmp)


if __name__ == "__main__":
    main()
