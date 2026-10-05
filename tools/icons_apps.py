"""Haiku-style function icons for common third-party applications (original artwork, MIT).

These icons deliberately do NOT reproduce the applications' logos or trademarks.
Each one shows what the program does (browser, image editor, media player, …) in
the Haiku icon language and is installed under the application's icon names so it
replaces the logo in menus and task bars. Browsers etc. are told apart by colour
and a neutral initial, not by brand marks.

Loaded by build_icons.py after icons_gear.register() (needs its helpers in ns["H"]).
"""
import math


def register(ns):
    H = ns["H"]
    ICONS, tint, shadow, page, text_lines, badge, globe, box3d, monitor, gear, folder = (
        ns["ICONS"], ns["tint"], ns["shadow"], ns["page"], ns["text_lines"], ns["badge"], ns["globe"],
        ns["box3d"], ns["monitor"], ns["gear"], ns["folder"])
    dk, txt, circ, ball, ell, quad, plate = H["dk"], H["txt"], H["circ"], H["ball"], H["ell"], H["quad"], H["plate"]
    bubble, phone, magnifier, envelope, note, arrow, padlock, keyshape = (
        H["bubble"], H["phone"], H["magnifier"], H["envelope"], H["note"], H["arrow"], H["padlock"], H["keyshape"])
    calendar, mic, waves, person, database, speaker, tv, clockface = (
        H["calendar"], H["mic"], H["waves"], H["person"], H["database"], H["speaker"], H["tv"], H["clockface"])
    fn_of = lambda name: ICONS[name][2]

    APPS = []

    def app(*names):
        def deco(fn):
            APPS.append((names, fn))
            return fn
        return deco

    # ------------------------------------------------------------------
    # shared compositions
    # ------------------------------------------------------------------
    def browser(ic, accent, letter):
        """application window with a tab strip and a globe; accent colour + initial tell browsers apart"""
        shadow(ic, 32, 59, 27, 3.5)
        quad(ic, [(3, 9), (59, 5), (61, 51), (5, 55)], "#e8e8e8")
        quad(ic, [(3, 9), (59, 5), (59.8, 16), (3.8, 20)], accent)
        ic.path("M8 10 L28 8.6 L29 15 L9 16.4 Z", "#fff", dk(accent), 1)
        ic.path("M7 21 L57 17.5 L58.6 49 L8.6 52.5 Z", "#ffffff", "#888", 1)
        globe(ic, 28, 35, 13)
        circ(ic, 49, 46, 11, ic.rgrad(tint(accent, 0.35), accent), dk(accent), 1.8)
        txt(ic, 49, 51, letter, 13, "#fff")

    def ide(ic, accent, label):
        monitor(ic, "#1e2430")
        ic.path("M12 18 l10 -1 M12 23 l16 -1.2 M15 28 l12 -0.9 M15 33 l8 -0.6", "none", accent, 1.8)
        txt(ic, 37, 34, "{ }", 12, "#e0e0e0")
        ic.raw('<rect x="38" y="44" width="22" height="12" rx="2" fill="%s" stroke="%s" stroke-width="1.4"/>'
               % (ic.grad(tint(accent, 0.4), accent), dk(accent)))
        txt(ic, 49, 53, label, 7.5, "#fff")

    def doc(ic, kind, col):
        page(ic)
        if kind == "text":
            text_lines(ic, n=7)
        elif kind == "sheet":
            for i in range(6):
                ic.path("M19 %g L46 %g" % (21 + i * 5, 20.2 + i * 5), "none", "#9a9a9a", 1)
            for x in (27, 36):
                ic.path("M%g 19 L%g 46" % (x, x + 0.4), "none", "#9a9a9a", 1)
        elif kind == "slide":
            ic.path("M20 22 L44 19.5 L45 36 L21 38.5 Z", ic.grad(tint(col, 0.4), col), dk(col), 1.2)
        elif kind == "draw":
            circ(ic, 26, 28, 7, "#f0c040", "#7a5a00", 1.4)
            quad(ic, [(30, 32), (44, 30), (40, 44)], "#4a90e0", 1.2)
        elif kind == "db":
            database(ic, 20, 18)
            return
        elif kind == "math":
            txt(ic, 31, 40, "√x", 16, "#444")
        ic.path("M30 40 L54 37 L56 54 L32 58 Z", ic.grad(tint(col, 0.45), col), dk(col), 1.6)

    def cloud(ic, x=6, y=14, s=1.0, col="#ffffff", stroke="#4a5a7a"):
        ic.path("M%g %g a%g %g 0 0 1 %g %g a%g %g 0 0 1 %g %g a%g %g 0 0 1 %g %g Z"
                % (x + 10 * s, y + 30 * s, 10 * s, 10 * s, 4 * s, -19 * s, 13 * s, 13 * s, 24 * s, -4 * s,
                   10 * s, 10 * s, 10 * s, 23 * s), ic.grad(col, tint(col, 1.12)), stroke, 2)

    def sync_arrows(ic, cx, cy, r, col="#2e8b22"):
        ic.path("M%g %g A%g %g 0 0 1 %g %g" % (cx - r, cy, r, r, cx + r * 0.7, cy - r * 0.7), "none", col, 3)
        quad(ic, [(cx + r * 0.7 + 4, cy - r * 0.7 - 4), (cx + r * 0.7 + 3, cy - r * 0.7 + 5), (cx + r * 0.7 - 5, cy - r * 0.7 + 1)], col, 1)
        ic.path("M%g %g A%g %g 0 0 1 %g %g" % (cx + r, cy, r, r, cx - r * 0.7, cy + r * 0.7), "none", col, 3)
        quad(ic, [(cx - r * 0.7 - 4, cy + r * 0.7 + 4), (cx - r * 0.7 - 3, cy + r * 0.7 - 5), (cx - r * 0.7 + 5, cy + r * 0.7 - 1)], col, 1)

    def gamepad(ic, col="#6a6a7a", y=0):
        ic.path("M8 %g C8 %g 18 %g 24 %g L40 %g C46 %g 56 %g 56 %g C56 %g 50 %g 44 %g L20 %g C14 %g 8 %g 8 %g Z"
                % (30 + y, 20 + y, 18 + y, 22 + y, 22 + y, 18 + y, 20 + y, 30 + y, 42 + y, 48 + y, 42 + y, 42 + y,
                   48 + y, 42 + y, 30 + y), ic.grad(tint(col, 0.4), col, 0, 0, 1, 1), dk(col), 2)
        ic.path("M16 %g h8 M20 %g v8" % (31 + y, 27 + y), "none", "#222", 2.6)
        circ(ic, 42, 29 + y, 2.4, "#e03030"); circ(ic, 47, 34 + y, 2.4, "#3060e0")

    # ------------------------------------------------------------------
    # web browsers
    # ------------------------------------------------------------------
    @app("firefox", "org.mozilla.firefox", "firefox-esr", "firefox-developer-edition", "firefox-nightly")
    def _(ic): browser(ic, "#e8701a", "F")

    @app("chromium", "chromium-browser", "org.chromium.Chromium")
    def _(ic): browser(ic, "#3a7ad8", "C")

    @app("google-chrome", "com.google.Chrome", "google-chrome-stable", "google-chrome-beta")
    def _(ic): browser(ic, "#3aa04a", "G")

    @app("brave-browser", "brave-desktop", "brave", "com.brave.Browser")
    def _(ic): browser(ic, "#d84a2a", "B")

    @app("vivaldi", "vivaldi-stable", "com.vivaldi.Vivaldi")
    def _(ic): browser(ic, "#c0303a", "V")

    @app("opera", "com.opera.Opera")
    def _(ic): browser(ic, "#a01a2a", "O")

    @app("librewolf", "io.gitlab.librewolf-community")
    def _(ic): browser(ic, "#2a6ab0", "L")

    @app("microsoft-edge", "microsoft-edge-stable", "com.microsoft.Edge")
    def _(ic): browser(ic, "#1a9aa0", "E")

    @app("torbrowser", "tor-browser", "torbrowser-launcher", "org.torproject.torbrowser-launcher")
    def _(ic): browser(ic, "#7a4ab0", "T")

    # ------------------------------------------------------------------
    # graphics
    # ------------------------------------------------------------------
    @app("gimp", "org.gimp.GIMP", "gimp-2.10", "gimp-3.0")
    def _(ic):
        fn_of("image-x-generic")(ic)
        ic.path("M28 58 L52 22 L58 26 L34 60 Z", ic.grad("#ffe066", "#c08000", 0, 0, 1, 0), "#5a3a00", 1.4)
        ic.path("M52 22 L58 26 L61 20 L56 16 Z", "#555", "#222", 1.2)

    @app("inkscape", "org.inkscape.Inkscape")
    def _(ic):
        page(ic)
        ic.path("M18 48 C20 22 44 18 46 40", "none", "#2a5ad0", 2.6)
        ic.path("M18 48 L28 26 M46 40 L40 18", "none", "#888", 1)
        for (x, y) in ((18, 48), (46, 40)):
            ic.raw('<rect x="%g" y="%g" width="5" height="5" fill="#fff" stroke="#2a5ad0" stroke-width="1.4"/>' % (x - 2.5, y - 2.5))
        for (x, y) in ((28, 26), (40, 18)):
            circ(ic, x, y, 2.4, "#e03030")
        ic.path("M40 50 L54 30 L58 33 L44 53 L39 55 Z", ic.grad("#f0f0f0", "#a0a0a0", 0, 0, 1, 0), "#333", 1.4)

    @app("krita", "org.kde.krita")
    def _(ic):
        shadow(ic); quad(ic, [(6, 14), (52, 8), (56, 50), (10, 56)], "#ffffff")
        ic.path("M12 44 C20 28 30 40 38 22 C42 14 48 18 46 26", "none", "#d03070", 4)
        ic.path("M12 48 C24 40 30 50 44 36", "none", "#2a8ad0", 3)
        ic.path("M36 60 L58 18 L62 21 L42 62 Z", ic.grad("#c08a5a", "#6a3a10", 0, 0, 1, 0), "#3a1a00", 1.4)
        ic.path("M58 18 L62 21 L63 13 Z", "#d03070", "#5a1030", 1)

    @app("darktable", "org.darktable.Darktable")
    def _(ic):
        shadow(ic, 32, 57, 24, 3.5)
        ic.path("M6 20 L22 18 L26 12 L38 11 L42 16 L56 15 L58 48 L8 52 Z", ic.grad("#7a7a7a", "#2c2c2c", 0, 0, 1, 1), "#111", 2)
        circ(ic, 32, 34, 11, ic.rgrad("#ffcc80", "#6a3a10"), "#111", 2)
        for a in range(0, 360, 60):
            r = math.radians(a)
            ic.path("M32 34 L%g %g" % (32 + 8 * math.cos(r), 34 + 8 * math.sin(r)), "none", "#3a2a10", 1)

    @app("blender", "org.blender.Blender")
    def _(ic):
        shadow(ic)
        F = [(14, 24), (32, 14), (50, 24), (32, 34)]
        ic.path("M14 24 L32 34 L32 54 L14 44 Z", ic.grad("#f0a040", "#b06010"), "#5a2a00", 1.6)
        ic.path("M50 24 L32 34 L32 54 L50 44 Z", ic.grad("#d08030", "#8a4a10"), "#5a2a00", 1.6)
        quad(ic, F, "#ffd090", 1.6)
        for p in F + [(14, 44), (32, 54), (50, 44)]:
            circ(ic, p[0], p[1], 2.2, "#fff", "#2a5ad0", 1.2)

    # ------------------------------------------------------------------
    # multimedia
    # ------------------------------------------------------------------
    @app("vlc", "org.videolan.VLC")
    def _(ic):
        tv(ic, ic.grad("#f0a050", "#a04a10"))
        ic.path("M26 22 L40 30 L26 38 Z", "#fff", "#333", 1.2)

    @app("mpv", "io.mpv.Mpv")
    def _(ic):
        shadow(ic); circ(ic, 32, 30, 24, ic.rgrad("#a080e0", "#3a1a7a"), "#1a0a40", 2)
        quad(ic, [(25, 18), (44, 30), (25, 42)], "#ffffff", 1.4, False, "#333")

    @app("spotify", "spotify-client", "com.spotify.Client", "spotify-launcher")
    def _(ic):
        shadow(ic, 32, 58, 22, 3)
        speaker(ic, 6, 30, 1.4); waves(ic, 30, 30, 3, "#7a4ad0", 1.0)
        note(ic, 46, 56, 0.8, "#7a4ad0")

    @app("com.obsproject.Studio", "obs", "obs-studio")
    def _(ic):
        tv(ic, "#1e2430")
        circ(ic, 24, 30, 7, ic.rgrad("#ff8080", "#c01010"), "#600", 1.6)
        txt(ic, 41, 34, "REC", 9, "#ff6060")

    @app("audacity", "org.audacityteam.Audacity")
    def _(ic):
        shadow(ic); plate(ic, "#f4f4f4", 6, 10, 48, 40)
        ic.path("M10 30 " + " ".join("L%g %g" % (10 + i * 1.5, 30 + math.sin(i * 1.1) * (12 - abs(i - 15) * 0.7)) for i in range(30)),
                "none", "#2a5ad0", 1.6)
        ic.path("M38 46 L56 58 M38 58 L56 46", "none", "#555", 2)
        circ(ic, 37, 45, 3, "none", "#333", 1.8); circ(ic, 37, 59, 3, "none", "#333", 1.8)

    @app("kodi", "tv.kodi.Kodi")
    def _(ic):
        tv(ic, ic.grad("#5ab0e0", "#104a7a"))
        for i, c in enumerate(("#ffcb00", "#ffffff", "#ffffff")):
            ic.raw('<rect x="%g" y="22" width="9" height="16" rx="1" fill="%s"/>' % (16 + i * 12, c))

    @app("handbrake", "fr.handbrake.ghb", "ghb")
    def _(ic):
        fn_of("video-x-generic")(ic)
        gear(ic, 48, 46, 10, "#f0a020")

    # ------------------------------------------------------------------
    # office
    # ------------------------------------------------------------------
    for names, kind, col in (
            (("libreoffice-writer", "org.libreoffice.LibreOffice.writer", "libreoffice6.0-writer", "libreoffice-fresh-writer"), "text", "#2a64c8"),
            (("libreoffice-calc", "org.libreoffice.LibreOffice.calc"), "sheet", "#2e9a3c"),
            (("libreoffice-impress", "org.libreoffice.LibreOffice.impress"), "slide", "#d9661a"),
            (("libreoffice-draw", "org.libreoffice.LibreOffice.draw"), "draw", "#c8a010"),
            (("libreoffice-base", "org.libreoffice.LibreOffice.base"), "db", "#8a3ab0"),
            (("libreoffice-math", "org.libreoffice.LibreOffice.math"), "math", "#555555")):
        APPS.append((names, (lambda kind, col: (lambda ic: doc(ic, kind, col)))(kind, col)))

    @app("libreoffice-startcenter", "org.libreoffice.LibreOffice", "libreoffice-main", "libreoffice")
    def _(ic):
        shadow(ic)
        for i, col in enumerate(("#d9661a", "#2e9a3c", "#2a64c8")):
            x, y = 8 + i * 8, 18 - i * 5
            ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 3, x + 28, y, x + 30, y + 36, x + 2, y + 39), "#fff", "#555", 1.6)
            ic.path("M%g %g L%g %g L%g %g L%g %g Z" % (x, y + 3, x + 28, y, x + 28.6, y + 8, x + 0.6, y + 11),
                    ic.grad(tint(col, 0.4), col), dk(col), 1.2)

    @app("onlyoffice-desktopeditors", "org.onlyoffice.desktopeditors", "onlyoffice", "ONLYOFFICE")
    def _(ic):
        shadow(ic, 32, 56, 24, 3.5)
        for i, col in enumerate(("#2a64c8", "#2e9a3c", "#d9661a")):
            y = 40 - i * 10
            quad(ic, [(8, y), (32, y - 10), (56, y), (32, y + 10)], col, 1.6)
        txt(ic, 32, 23, "DOC", 7, "#fff")

    # ------------------------------------------------------------------
    # communication
    # ------------------------------------------------------------------
    @app("thunderbird", "org.mozilla.Thunderbird", "net.thunderbird.Thunderbird", "thunderbird-esr")
    def _(ic):
        calendar(ic, "#3a7ad8", 22, 4, 34, 30, ""); envelope(ic, 4, 26, 44, 28)
        txt(ic, 39, 28, "@", 11, "#3a7ad8")

    @app("signal-desktop", "org.signal.Signal", "signal")
    def _(ic):
        shadow(ic); bubble(ic, "#3a6ad8", 6, 8, 46, 34)
        padlock(ic, 21, 13, 0.75, "#ffffff")

    @app("telegram", "telegram-desktop", "org.telegram.desktop", "telegramdesktop")
    def _(ic):
        shadow(ic); bubble(ic, "#40a8e0", 6, 8, 46, 34)
        envelope(ic, 16, 16, 26, 16)

    @app("discord", "com.discordapp.Discord", "discord-canary", "vesktop", "dev.vencord.Vesktop")
    def _(ic):
        shadow(ic); bubble(ic, "#6a6ad8", 4, 14, 44, 30)
        ic.path("M14 30 A12 12 0 0 1 38 30", "none", "#fff", 3)
        ic.raw('<rect x="11" y="28" width="6" height="9" rx="2" fill="#fff"/><rect x="35" y="28" width="6" height="9" rx="2" fill="#fff"/>')
        ic.raw('<rect x="40" y="4" width="20" height="14" rx="4" fill="%s" stroke="#3a3a4a" stroke-width="1.4"/>' % ic.grad("#c0c0d0", "#7a7a8a"))

    @app("element-desktop", "im.riot.Riot", "element", "io.element.Element")
    def _(ic):
        shadow(ic); bubble(ic, "#2aa070", 4, 6, 40, 28); bubble(ic, "#f0f0f0", 22, 26, 38, 22, False)
        txt(ic, 24, 26, "[ ]", 12, "#fff")

    @app("Zoom", "zoom", "us.zoom.Zoom", "zoom-videocall")
    def _(ic):
        shadow(ic)
        ic.raw('<rect x="6" y="18" width="36" height="28" rx="6" fill="%s" stroke="#1a3a80" stroke-width="2"/>' % ic.grad("#7ab0f0", "#2a5ad0"))
        quad(ic, [(42, 28), (58, 20), (58, 44), (42, 36)], "#2a5ad0", 1.8)
        person(ic, 24, 34, 0.6, "#ffffff")

    @app("teams", "teams-for-linux", "com.github.IsmaelMartinez.teams_for_linux", "microsoft-teams")
    def _(ic):
        shadow(ic)
        person(ic, 22, 34, 0.8, "#7a6ad0"); person(ic, 40, 30, 0.9, "#5a4ab0")
        bubble(ic, "#ffffff", 34, 4, 26, 16, False)

    # ------------------------------------------------------------------
    # development
    # ------------------------------------------------------------------
    @app("vscode", "visual-studio-code", "com.visualstudio.code", "code", "code-oss", "com.visualstudio.code.oss",
         "visual-studio-code-bin")
    def _(ic): ide(ic, "#2a7ad8", "code")

    @app("vscodium", "com.vscodium.codium", "codium")
    def _(ic): ide(ic, "#2aa0a0", "OSS")

    @app("intellij-idea-community", "intellij-idea-ultimate-edition", "idea", "jetbrains-idea", "jetbrains-idea-ce",
         "com.jetbrains.IntelliJ-IDEA-Community", "com.jetbrains.IntelliJ-IDEA-Ultimate")
    def _(ic): ide(ic, "#c04a7a", "Java")

    @app("pycharm", "pycharm-community", "pycharm-professional", "jetbrains-pycharm", "jetbrains-pycharm-ce",
         "com.jetbrains.PyCharm-Community", "com.jetbrains.PyCharm-Professional")
    def _(ic): ide(ic, "#3a9a4a", "Py")

    @app("webstorm", "jetbrains-webstorm", "com.jetbrains.WebStorm")
    def _(ic): ide(ic, "#2a8ad0", "JS")

    @app("clion", "jetbrains-clion", "com.jetbrains.CLion")
    def _(ic): ide(ic, "#2ab090", "C++")

    @app("goland", "jetbrains-goland", "com.jetbrains.GoLand")
    def _(ic): ide(ic, "#7a5ad0", "Go")

    @app("rider", "jetbrains-rider", "com.jetbrains.Rider")
    def _(ic): ide(ic, "#d0702a", "C#")

    @app("jetbrains-toolbox")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#7a7a8a", "#3a3a4a"), "#9a9aaa", "#2a2a3a", 8, 26, 40, 24, 12)
        gear(ic, 26, 22, 8, "#e0a020"); txt(ic, 28, 44, "{ }", 10, "#fff")

    @app("github-desktop", "io.github.shiftey.Desktop", "github-desktop-bin")
    def _(ic):
        shadow(ic); plate(ic, "#2a2a32", 6, 8, 48, 44)
        ic.path("M20 16 V48 M20 38 C20 30 42 32 42 22", "none", "#e8e8e8", 2.6)
        for (x, y) in ((20, 16), (20, 48), (42, 20)):
            circ(ic, x, y, 4, "#ffcb00", "#7a5a00", 1.4)

    @app("docker-desktop", "docker", "com.docker.DockerDesktop")
    def _(ic):
        shadow(ic, 32, 56, 26, 3.5)
        for i, col in enumerate(("#2a7ad8", "#e0a020", "#3a9a4a")):
            x, y = 6 + (i % 2) * 22, 34 - (i // 2) * 16
            box3d(ic, ic.grad(tint(col, 0.4), col), tint(col, 0.5), dk(col, 1.2), x, y, 22, 14, 8)
            for k in range(4):
                ic.path("M%g %g v10" % (x + 4 + k * 5, y + 2), "none", dk(col, 1.25), 1.2)

    # ------------------------------------------------------------------
    # games
    # ------------------------------------------------------------------
    @app("steam", "com.valvesoftware.Steam", "steam-native", "steam-runtime")
    def _(ic):
        shadow(ic, 32, 58, 26, 3)
        for i, col in enumerate(("#3a7ad8", "#d84a3a", "#3a9a4a", "#e0a020")):
            ic.raw('<rect x="%g" y="8" width="11" height="26" rx="1" fill="%s" stroke="%s" stroke-width="1.4"/>'
                   % (8 + i * 12, ic.grad(tint(col, 0.4), col, 0, 0, 1, 0), dk(col)))
        gamepad(ic, "#5a6070", 14)

    @app("lutris", "net.lutris.Lutris")
    def _(ic):
        shadow(ic, 32, 56, 18, 4)
        ell(ic, 32, 50, 18, 6, ic.grad("#7a7a8a", "#3a3a4a"), "#1a1a2a", 2)
        ic.path("M32 48 L40 18", "none", "#333", 4); ball(ic, 41, 16, 7, "#e05a2a")
        circ(ic, 22, 48, 3, "#e03030", "#600", 1)

    @app("heroic", "com.heroicgameslauncher.hgl", "heroic-games-launcher")
    def _(ic):
        shadow(ic, 32, 58, 16, 3)
        ic.path("M18 8 H46 V20 C46 32 38 38 32 38 C26 38 18 32 18 20 Z", ic.grad("#ffe070", "#c08a00", 0, 0, 1, 0), "#6a4a00", 2)
        ic.path("M18 12 H10 C10 22 14 26 20 26 M46 12 H54 C54 22 50 26 44 26", "none", "#c08a00", 2.4)
        ic.raw('<rect x="28" y="38" width="8" height="10" fill="#c08a00" stroke="#6a4a00" stroke-width="1.4"/>'
               '<rect x="20" y="48" width="24" height="8" rx="1" fill="#6a4a2a" stroke="#3a2a10" stroke-width="1.4"/>')

    @app("bottles", "com.usebottles.bottles")
    def _(ic):
        shadow(ic, 32, 58, 14, 3)
        ic.path("M27 6 H37 V18 C46 22 46 28 46 34 V54 H18 V34 C18 28 18 22 27 18 Z", ic.grad("#a0d8ff", "#3a8ad0", 0, 0, 1, 0), "#1a4a7a", 2)
        ic.raw('<rect x="18" y="34" width="28" height="12" fill="#e0a020" stroke="#6a4a00" stroke-width="1.2"/>')

    # ------------------------------------------------------------------
    # system & tools
    # ------------------------------------------------------------------
    @app("gparted")
    def _(ic):
        fn_of("drive-harddisk")(ic)
        circ(ic, 44, 18, 12, "#3a9a4a", "#1a4a1a", 1.6)
        ic.path("M44 18 L44 6 A12 12 0 0 1 54 24 Z", "#e0a020", "#6a4a00", 1.2)
        ic.path("M44 18 L54 24 A12 12 0 0 1 36 27 Z", "#3a7ad8", "#1a3a70", 1.2)

    @app("keepassxc", "org.keepassxc.KeePassXC", "keepassxc-locked", "keepassxc-unlocked")
    def _(ic):
        page(ic)
        for i in range(4):
            y = 20 + i * 7
            txt(ic, 23, y + 3, "***", 7, "#555")
            ic.path("M30 %g h14" % (y + 0.4), "none", "#aaa", 1.2)
        padlock(ic, 34, 32, 0.9, "#3a9a4a")

    @app("bitwarden", "com.bitwarden.desktop", "bitwarden-desktop")
    def _(ic):
        shadow(ic); padlock(ic, 12, 6, 1.8, "#3a6ad8")
        txt(ic, 32, 51, "* * *", 10, "#fff")

    @app("Nextcloud", "nextcloud", "com.nextcloud.desktopclient.nextcloud", "nextcloud-desktop")
    def _(ic):
        shadow(ic); cloud(ic, 4, 14, 1.0, "#ffffff", "#2a5a9a")
        sync_arrows(ic, 29, 33, 8, "#2a6ad0")

    @app("syncthing", "syncthing-gtk", "syncthingtray", "me.kozec.syncthingtk")
    def _(ic):
        shadow(ic)
        for (x, y, col) in ((4, 8, "#ffc21a"), (32, 28, "#7ab8f0")):
            ic.path("M%g %g l8 -3 l3 2 l15 -4 l2 20 l-26 6 Z" % (x, y + 6), ic.grad(tint(col, 0.5), col, 0, 0, 0.3, 1), dk(col), 1.8)
        sync_arrows(ic, 32, 30, 9, "#2e8b22")

    @app("timeshift")
    def _(ic):
        fn_of("drive-harddisk")(ic)
        clockface(ic, 42, 20, 13, rim="#3a9a4a", h=-90, m=0)
        ic.path("M24 18 A18 18 0 0 1 30 8", "none", "#2e8b22", 3)
        quad(ic, [(30, 3), (34, 10), (26, 11)], "#3fae2f", 1)

    @app("com.github.tchx84.Flatseal", "flatseal")
    def _(ic):
        fn_of("package-x-generic")(ic)
        circ(ic, 44, 22, 11, ic.rgrad("#ff8a6a", "#c02010"), "#600", 1.6)
        ic.path("M38 22 l4 4 l8 -8", "none", "#fff", 2.6)

    @app("transmission", "transmission-qt", "transmission-gtk", "com.transmissionbt.Transmission", "transmission-remote-gtk")
    def _(ic):
        shadow(ic); circ(ic, 32, 30, 24, ic.rgrad("#ffd0a0", "#d06010"), "#6a2a00", 2)
        arrow(ic, "d", 32, 30, 1.6, "#ffffff")

    @app("qbittorrent", "org.qbittorrent.qBittorrent")
    def _(ic):
        shadow(ic); circ(ic, 32, 30, 24, ic.rgrad("#bfe0ff", "#2a6ec2"), "#173d70", 2)
        arrow(ic, "d", 25, 30, 1.0, "#ffffff"); arrow(ic, "u", 39, 30, 1.0, "#ffcb00")

    @app("virtualbox", "org.virtualbox.VirtualBox", "virt-manager", "org.virt_manager.virt-manager", "gnome-boxes",
         "org.gnome.Boxes")
    def _(ic):
        shadow(ic); box3d(ic, ic.grad("#7aa0d8", "#2a5aa0"), "#a8c4ec", "#1a3a70", 8, 26, 40, 26, 12)
        ic.raw('<rect x="13" y="30" width="30" height="18" fill="#1e2430" stroke="#000" stroke-width="1"/>')
        ic.path("M16 35 l4 3 l-4 3 M23 43 h8", "none", "#5f5", 1.6)

    # ------------------------------------------------------------------
    # register (only names not already taken by the core / KDE Gear sets)
    # ------------------------------------------------------------------
    taken = set()
    for cat, names, fn in ICONS.values():
        taken.update(names)
    added = []
    for names, fn in APPS:
        names = tuple(n for n in names if n not in taken)
        if not names:
            continue
        taken.update(names)
        ICONS[names[0]] = ("apps", names, fn)
        added.append(names[0])
    return added
