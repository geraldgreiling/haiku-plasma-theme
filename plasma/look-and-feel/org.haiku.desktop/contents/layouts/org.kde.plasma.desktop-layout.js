// Haiku-like desktop: plain "Haiku blue" desktop and a Deskbar-style panel
// along the top edge (leaf menu – window list – tray – clock).

var desktopsArray = desktopsForActivity(currentActivity());
for (var j = 0; j < desktopsArray.length; j++) {
    var d = desktopsArray[j];
    d.wallpaperPlugin = "org.kde.color";
    d.currentConfigGroup = ["Wallpaper", "org.kde.color", "General"];
    d.writeConfig("Color", "51,102,152");
}

var panel = new Panel;
panel.location = "top";
panel.height = Math.round(gridUnit * 1.8);
try { panel.floating = false; } catch (e) {}
try { panel.hiding = "none"; } catch (e) {}

var kickoff = panel.addWidget("org.kde.plasma.kickoff");
kickoff.currentConfigGroup = ["General"];
kickoff.writeConfig("icon", "start-here");
kickoff.writeConfig("menuLabel", "");

var tasks = panel.addWidget("org.kde.plasma.taskmanager");
tasks.currentConfigGroup = ["General"];
tasks.writeConfig("showOnlyCurrentDesktop", "false");
tasks.writeConfig("maxStripes", "1");
tasks.writeConfig("groupingStrategy", "0");

panel.addWidget("org.kde.plasma.marginsseparator");
panel.addWidget("org.kde.plasma.systemtray");

var clock = panel.addWidget("org.kde.plasma.digitalclock");
clock.currentConfigGroup = ["Appearance"];
clock.writeConfig("showDate", "false");

// Haiku window behaviour: close button left, (minimise +) zoom right,
// double-click on the tab minimises the window.
try {
    var kwin = ConfigFile("kwinrc");
    kwin.group = "org.kde.kdecoration2";
    kwin.writeEntry("ButtonsOnLeft", "X");
    kwin.writeEntry("ButtonsOnRight", "IA");
    var win = ConfigFile("kwinrc");
    win.group = "Windows";
    win.writeEntry("TitlebarDoubleClickCommand", "Minimize");
} catch (e) {}
