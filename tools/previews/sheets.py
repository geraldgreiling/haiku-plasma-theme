#!/usr/bin/env python3
"""Store screenshots for icons, cursors and the colour scheme.
Needs Pillow and rsvg-convert.   sheets.py <repo-root> <out-dir>"""
import configparser, glob, io, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

ROOT, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
BLUE, PANEL = (51, 102, 152), (216, 216, 216)


def font(sz, bold=False):
    for f in (["DejaVuSans-Bold.ttf", "NotoSans-Bold.ttf"] if bold else ["DejaVuSans.ttf", "NotoSans-Regular.ttf"]):
        for d in ("/usr/share/fonts", "/usr/share/fonts/truetype"):
            hits = glob.glob(d + "/**/" + f, recursive=True)
            if hits:
                return ImageFont.truetype(hits[0], sz)
    return ImageFont.load_default()


def svg_png(path_or_data, size):
    if os.path.exists(str(path_or_data)):
        data = subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), path_or_data],
                              capture_output=True, check=True).stdout
    else:
        data = subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size)], input=path_or_data.encode(),
                              capture_output=True, check=True).stdout
    return Image.open(io.BytesIO(data)).convert("RGBA")


# --- icons -----------------------------------------------------------------
files = sorted(f for f in glob.glob(ROOT + "/icons/Haiku/scalable/*/*.svg") if not os.path.islink(f))
cols, cell = 8, 140
rows = (len(files) + cols - 1) // cols
img = Image.new("RGB", (cols * cell, rows * cell + 60), PANEL)
d = ImageDraw.Draw(img)
d.text((20, 18), "Haiku icons – core set (%d originals, falls back to Breeze)" % len(files), fill=(0, 0, 0), font=font(20, True))
f = font(12)
for i, path in enumerate(files):
    x, y = (i % cols) * cell, (i // cols) * cell + 60
    ic = svg_png(path, 72)
    img.paste(ic, (x + (cell - 72) // 2, y + 12), ic)
    name = os.path.basename(path)[:-4]
    if len(name) > 22:
        name = name[:21] + "…"
    w = d.textlength(name, font=f)
    d.text((x + (cell - w) / 2, y + 96), name, fill=(0, 0, 0), font=f)
img.save(OUT + "/preview-icons.png")

# small vs. large rendering
sel = ["places/folder", "places/user-home", "places/user-trash", "devices/drive-harddisk", "apps/utilities-terminal",
       "apps/system-file-manager", "mimetypes/text-plain", "mimetypes/image-x-generic"]
img = Image.new("RGB", (len(sel) * 150, 280), BLUE)
d = ImageDraw.Draw(img)
for i, n in enumerate(sel):
    x = i * 150
    for j, s in enumerate((16, 22, 32)):
        ic = svg_png(ROOT + "/icons/Haiku/scalable/%s.svg" % n, s)
        img.paste(ic, (x + 20 + j * 40, 30 + (32 - s)), ic)
    ic = svg_png(ROOT + "/icons/Haiku/scalable/%s.svg" % n, 128)
    img.paste(ic, (x + 11, 90), ic)
img.save(OUT + "/preview-icons-sizes.png")

# --- cursors ---------------------------------------------------------------
sys.path.insert(0, ROOT + "/tools")
import build_cursors as bc  # noqa: E402
names = ["left_ptr", "hand2", "xterm", "watch", "left_ptr_watch", "help", "copy", "alias", "crosshair", "fleur",
         "size_ver", "size_hor", "size_fdiag", "size_bdiag", "split_h", "split_v", "openhand", "closedhand",
         "not-allowed", "pencil", "up_arrow"]
cols, cell = 7, 130
img = Image.new("RGB", (cols * cell, 3 * cell + 60), BLUE)
d = ImageDraw.Draw(img)
d.text((20, 18), "Haiku Cursors", fill=(255, 255, 255), font=font(20, True))
for i, n in enumerate(names):
    x, y = (i % cols) * cell, (i // cols) * cell + 60
    frames = bc.CURSORS[n][0]
    cur = svg_png(bc.svg(frames[min(2, len(frames) - 1)]), 64)
    img.paste(cur, (x + 33, y + 10), cur)
    w = d.textlength(n, font=f)
    d.text((x + (cell - w) / 2, y + 90), n, fill=(255, 255, 255), font=f)
img.save(OUT + "/preview-cursors.png")

# --- colour scheme -----------------------------------------------------------
cp = configparser.ConfigParser(interpolation=None, strict=False)
cp.optionxform = str
cp.read(ROOT + "/colors/HaikuR1.colors")
def c(sec, key):
    return tuple(int(v) for v in cp[sec][key].split(","))
sw = [("Window", c("Colors:Window", "BackgroundNormal")), ("View", c("Colors:View", "BackgroundNormal")),
      ("Button", c("Colors:Button", "BackgroundNormal")), ("Selection", c("Colors:Selection", "BackgroundNormal")),
      ("Tooltip", c("Colors:Tooltip", "BackgroundNormal")), ("Focus", c("Colors:View", "DecorationFocus")),
      ("Hover", c("Colors:View", "DecorationHover")), ("Title bar", c("WM", "activeBackground")),
      ("Desktop", c("Colors:Complementary", "BackgroundNormal")), ("Link", c("Colors:View", "ForegroundLink")),
      ("Negative", c("Colors:View", "ForegroundNegative")), ("Positive", c("Colors:View", "ForegroundPositive"))]
img = Image.new("RGB", (900, 520), c("Colors:Window", "BackgroundNormal"))
d = ImageDraw.Draw(img)
d.text((24, 18), "Haiku R1 colour scheme", fill=(0, 0, 0), font=font(22, True))
for i, (name, col) in enumerate(sw):
    x, y = 24 + (i % 4) * 214, 70 + (i // 4) * 140
    d.rectangle([x, y, x + 196, y + 80], fill=col, outline=(110, 110, 110))
    d.line([x + 1, y + 1, x + 195, y + 1], fill=(255, 255, 255))
    d.text((x, y + 88), name, fill=(0, 0, 0), font=font(15, True))
    d.text((x, y + 108), "%d, %d, %d" % col, fill=(60, 60, 60), font=font(13))
img.save(OUT + "/preview-colors.png")
print("sheets ok")
