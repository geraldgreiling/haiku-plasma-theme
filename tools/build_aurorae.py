#!/usr/bin/env python3
"""Generates the Aurorae fallback decoration (full-width yellow title bar)."""
import os, sys, json

OUT = sys.argv[1] if len(sys.argv) > 1 else "aurorae/themes/Haiku"
os.makedirs(OUT, exist_ok=True)
T, B = 22, 5  # title height, border

def tint(c, t):
    f = (lambda v: 255 - (255 - v) * t) if t < 1 else (lambda v: v * (2 - t))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(f(v)))) for v in c)

def deco(prefix, tab, frame):
    top = T + B
    light, dark = tint(tab, .45), tint(tab, 1.4)
    fd, fl, fs = tint(frame, 1.45), tint(frame, .25), tint(frame, 1.15)
    g = f'''<linearGradient id="{prefix}g" x1="0" y1="0" x2="0" y2="{T}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{light}"/><stop offset="1" stop-color="{'#%02x%02x%02x' % tab}"/></linearGradient>'''
    def title(x, w, left=False, right=False):
        s = f'<rect x="{x}" y="0" width="{w}" height="{T}" fill="url(#{prefix}g)"/>'
        s += f'<rect x="{x}" y="0" width="{w}" height="1" fill="{dark}"/><rect x="{x}" y="1" width="{w}" height="1" fill="{tint(tab,.2)}"/>'
        if left: s += f'<rect x="{x}" y="0" width="1" height="{top}" fill="{dark}"/><rect x="{x+1}" y="1" width="1" height="{T-1}" fill="{tint(tab,.2)}"/>'
        if right: s += f'<rect x="{x+w-1}" y="0" width="1" height="{top}" fill="{dark}"/>'
        # frame strip under the tab
        s += f'<rect x="{x}" y="{T}" width="{w}" height="{B}" fill="#%02x%02x%02x"/>' % frame
        s += f'<rect x="{x}" y="{T}" width="{w}" height="1" fill="{fd}"/><rect x="{x}" y="{top-1}" width="{w}" height="1" fill="{fd}"/>'
        if left: s += f'<rect x="{x}" y="{T}" width="1" height="{B}" fill="{fd}"/>'
        if right: s += f'<rect x="{x+w-1}" y="{T}" width="1" height="{B}" fill="{fd}"/>'
        return s
    def side(x, y, w, h, vertical, outer_first):
        fr = '#%02x%02x%02x' % frame
        s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fr}"/>'
        if vertical:
            xo, xi = (x, x + w - 1) if outer_first else (x + w - 1, x)
            s += f'<rect x="{xo}" y="{y}" width="1" height="{h}" fill="{fd}"/><rect x="{xi}" y="{y}" width="1" height="{h}" fill="{fd}"/>'
        else:
            yo, yi = (y + h - 1, y) 
            s += f'<rect x="{x}" y="{yo}" width="{w}" height="1" fill="{fd}"/><rect x="{x}" y="{yi}" width="{w}" height="1" fill="{fl}"/>'
        return s
    p = f'decoration-{prefix}' if prefix else 'decoration'
    parts = []
    X0 = 0 if not prefix else 100
    def grp(name, content): parts.append(f'<g id="{p}-{name}">{content}</g>')
    grp('topleft', title(X0, B, left=True))
    grp('top', title(X0 + 10, 20))
    grp('topright', title(X0 + 35, B, right=True))
    grp('left', side(X0, 40, B, 20, True, True))
    grp('right', side(X0 + 35, 40, B, 20, True, False))
    grp('bottomleft', side(X0, 70, B, B, False, True) + f'<rect x="{X0}" y="70" width="1" height="{B}" fill="{fd}"/>')
    grp('bottom', side(X0 + 10, 70, 20, B, False, True))
    grp('bottomright', side(X0 + 35, 70, B, B, False, True) + f'<rect x="{X0+35+B-1}" y="70" width="1" height="{B}" fill="{fd}"/>')
    grp('center', f'<rect x="{X0+10}" y="40" width="20" height="20" fill="none"/>')
    return g, parts

ga, pa = deco('', (255, 203, 0), (224, 224, 224))
gi, pi = deco('inactive', (232, 232, 232), (232, 232, 232))
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="200" height="100"><defs>{ga}{gi}</defs>{"".join(pa + pi)}</svg>'
open(os.path.join(OUT, 'decoration.svg'), 'w').write(svg)

def button(name, glyph):
    # four states laid out horizontally: active, hover, pressed, inactive, deactivated
    states = [('active', (255, 203, 0), False, False), ('hover', (255, 220, 70), False, True),
              ('pressed', (255, 203, 0), True, False), ('inactive', (232, 232, 232), False, False),
              ('deactivated', (232, 232, 232), False, False)]
    S = 14
    out = []
    for i, (st, c, pressed, _) in enumerate(states):
        x0 = i * 20
        def box(x, y, s):
            a, b = (tint(c, 1.25), tint(c, .6)) if pressed else (tint(c, .3), tint(c, 1.08))
            gid = f'{st}{x}{y}'
            return (f'<linearGradient id="{gid}" x1="{x}" y1="{y}" x2="{x+s}" y2="{y+s}" gradientUnits="userSpaceOnUse">'
                    f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
                    f'<rect x="{x+.5}" y="{y+.5}" width="{s-1}" height="{s-1}" fill="url(#{gid})" stroke="{tint(c,1.5)}"/>')
        g = f'<rect x="{x0}" y="0" width="{S}" height="{S}" fill="none"/>'
        if glyph == 'close':
            g += box(x0, 0, S)
        elif glyph in ('maximize', 'restore'):
            big, small = 10, 7
            g += box(x0 + S - big, S - big, big) + box(x0, 0, small)
        elif glyph == 'minimize':
            g += box(x0, 0, S) + box(x0 + 3, S - 6, S - 6) if False else box(x0, 0, S) + f'<rect x="{x0+3.5}" y="{S-5.5}" width="{S-7}" height="2" fill="none" stroke="{tint(c,1.5)}"/>'
        else:
            g += box(x0, 0, S)
        out.append(f'<g id="{st}-center">{g}</g>')
    open(os.path.join(OUT, f'{name}.svg'), 'w').write(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="100" height="{S}">{"".join(out)}</svg>')

for n in ['close', 'maximize', 'restore', 'minimize', 'alldesktops', 'keepabove', 'keepbelow', 'shade', 'help']:
    button(n, n)

open(os.path.join(OUT, 'Haikurc'), 'w').write(f"""[General]
ActiveTextColor=0,0,0
InactiveTextColor=80,80,80
TitleAlignment=Left
TitleVerticalAlignment=Center
Animation=0
UseTextShadow=false
Shadow=false
DecorationPosition=0

[Layout]
BorderLeft={B}
BorderRight={B}
BorderBottom={B}
TitleEdgeTop=0
TitleEdgeBottom={B}
TitleEdgeLeft=0
TitleEdgeRight=0
TitleBorderLeft=7
TitleBorderRight=7
TitleHeight={T}
ButtonWidth=14
ButtonHeight=14
ButtonSpacing=4
ButtonMarginTop=4
ExplicitButtonSpacer=10
PaddingTop=0
PaddingBottom=0
PaddingLeft=0
PaddingRight=0
""")
meta = {"KPlugin": {"Id": "__aurorae__svg__Haiku", "Name": "Haiku (Aurorae fallback)",
        "Description": "Haiku-like decoration without compiled plugin (full-width title bar)",
        "Authors": [{"Name": "Gerald Greiling"}], "License": "MIT", "Version": "1.0.0"}}
json.dump(meta, open(os.path.join(OUT, 'metadata.json'), 'w'), indent=2)
open(os.path.join(OUT, 'metadata.desktop'), 'w').write("""[Desktop Entry]
Name=Haiku (Aurorae fallback)
Comment=Haiku-like decoration without compiled plugin
X-KDE-PluginInfo-Name=Haiku
X-KDE-PluginInfo-License=MIT
X-KDE-PluginInfo-Version=1.0.0
X-Plasma-API=javascript
X-KDE-ServiceTypes=KWin/Decoration
""")
print("aurorae ok")
