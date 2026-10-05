// Renders store screenshots for the Plasma style and the Aurorae decoration.
//   storepreviews <repo-root> <out-dir>
#include <QDir>
#include <QGuiApplication>
#include <QImage>
#include <QPainter>
#include <QSvgRenderer>

static void frame(QPainter &p, QSvgRenderer &r, const QString &pre, const QRectF &R)
{
    auto e = [&](const QString &n) { return pre.isEmpty() ? n : pre + "-" + n; };
    auto b = [&](const QString &n) { return r.boundsOnElement(e(n)); };
    const qreal l = b("left").width(), t = b("top").height(), rr = b("right").width(), bb = b("bottom").height();
    auto d = [&](const QString &n, const QRectF &x) { r.render(&p, e(n), x); };
    d("topleft", {R.left(), R.top(), l, t});
    d("top", {R.left() + l, R.top(), R.width() - l - rr, t});
    d("topright", {R.right() - rr, R.top(), rr, t});
    d("left", {R.left(), R.top() + t, l, R.height() - t - bb});
    d("center", {R.left() + l, R.top() + t, R.width() - l - rr, R.height() - t - bb});
    d("right", {R.right() - rr, R.top() + t, rr, R.height() - t - bb});
    d("bottomleft", {R.left(), R.bottom() - bb, l, bb});
    d("bottom", {R.left() + l, R.bottom() - bb, R.width() - l - rr, bb});
    d("bottomright", {R.right() - rr, R.bottom() - bb, rr, bb});
}

static void icon(QPainter &p, const QString &root, const QString &name, const QRectF &r)
{
    QSvgRenderer s(root + "/icons/Haiku/scalable/" + name + ".svg");
    s.render(&p, r);
}

static void plasmaStyle(const QString &root, const QString &out)
{
    const QString th = root + "/plasma/desktoptheme/haiku/";
    QImage img(1200, 700, QImage::Format_ARGB32);
    img.fill(QColor(51, 102, 152));
    QPainter p(&img);
    p.setRenderHint(QPainter::Antialiasing);
    QFont f;
    f.setPixelSize(14);
    p.setFont(f);

    // panel
    QSvgRenderer panel(th + "widgets/panel-background.svg"), tasks(th + "widgets/tasks.svg");
    frame(p, panel, "", QRectF(0, 0, 1200, 40));
    icon(p, root, "places/start-here", QRectF(8, 6, 28, 28));
    struct T { const char *pre, *label, *ic; } ts[] = {{"focus", "Dolphin", "apps/system-file-manager"},
                                                        {"normal", "Konsole", "apps/utilities-terminal"},
                                                        {"hover", "Kate", "apps/accessories-text-editor"},
                                                        {"attention", "Mail", "apps/internet-mail"}};
    int x = 46;
    for (auto &t : ts) {
        frame(p, tasks, t.pre, QRectF(x, 4, 190, 32));
        icon(p, root, t.ic, QRectF(x + 6, 8, 24, 24));
        p.setPen(Qt::black);
        p.drawText(QRectF(x + 36, 4, 150, 32), Qt::AlignVCenter, t.label);
        x += 196;
    }
    p.drawText(QRectF(1100, 0, 90, 40), Qt::AlignCenter, "12:00");

    // popup dialog (like a menu / launcher)
    QSvgRenderer dlg(th + "dialogs/background.svg"), vi(th + "widgets/viewitem.svg"),
        head(th + "widgets/plasmoidheading.svg");
    QRectF d(8, 44, 330, 400);
    frame(p, dlg, "", d);
    frame(p, head, "header", QRectF(d.left() + 6, d.top() + 6, d.width() - 12, 44));
    p.drawText(QRectF(d.left() + 18, d.top() + 6, 300, 44), Qt::AlignVCenter, "Applications");
    const char *apps[][2] = {{"apps/system-file-manager", "File Manager"}, {"apps/utilities-terminal", "Terminal"},
                             {"apps/web-browser", "Web Browser"}, {"apps/accessories-text-editor", "Text Editor"},
                             {"apps/preferences-system", "System Settings"}, {"apps/accessories-calculator", "Calculator"},
                             {"apps/multimedia-audio-player", "Music Player"}, {"apps/image-viewer", "Image Viewer"}};
    for (int i = 0; i < 8; ++i) {
        QRectF row(d.left() + 8, d.top() + 58 + i * 40, d.width() - 16, 38);
        if (i == 1)
            frame(p, vi, "selected", row);
        else if (i == 3)
            frame(p, vi, "hover", row);
        icon(p, root, apps[i][0], QRectF(row.left() + 8, row.top() + 5, 28, 28));
        p.drawText(row.adjusted(46, 0, 0, 0), Qt::AlignVCenter, apps[i][1]);
    }

    // tooltip
    QSvgRenderer tip(th + "widgets/tooltip.svg");
    frame(p, tip, "", QRectF(250, 48, 210, 56));
    p.drawText(QRectF(262, 48, 190, 30), Qt::AlignVCenter, "Konsole");
    QFont sf = f;
    sf.setPixelSize(12);
    p.setFont(sf);
    p.drawText(QRectF(262, 72, 190, 26), Qt::AlignVCenter, "~/Projects – zsh");
    p.setFont(f);

    // desktop widget with controls
    QSvgRenderer bg(th + "widgets/background.svg"), btn(th + "widgets/button.svg"), le(th + "widgets/lineedit.svg"),
        fr(th + "widgets/frame.svg");
    QRectF w(560, 140, 380, 300);
    frame(p, bg, "", w);
    frame(p, head, "header", QRectF(w.left() + 8, w.top() + 8, w.width() - 16, 40));
    p.drawText(QRectF(w.left() + 20, w.top() + 8, 300, 40), Qt::AlignVCenter, "Notes");
    frame(p, le, "base", QRectF(w.left() + 20, w.top() + 64, w.width() - 40, 32));
    p.drawText(QRectF(w.left() + 30, w.top() + 64, 300, 32), Qt::AlignVCenter, "Search…");
    frame(p, le, "base", QRectF(w.left() + 20, w.top() + 106, w.width() - 40, 32));
    frame(p, le, "focus", QRectF(w.left() + 20, w.top() + 106, w.width() - 40, 32));
    p.drawText(QRectF(w.left() + 30, w.top() + 106, 300, 32), Qt::AlignVCenter, "Focused field");
    frame(p, fr, "sunken", QRectF(w.left() + 20, w.top() + 150, w.width() - 40, 70));
    p.drawText(QRectF(w.left() + 30, w.top() + 150, 320, 70), Qt::AlignVCenter | Qt::TextWordWrap,
               "Grey bevelled panels, pale yellow tooltips and the blue Haiku desktop.");
    const char *bl[] = {"normal", "hover", "pressed"};
    const char *bt[] = {"OK", "Hover", "Pressed"};
    for (int i = 0; i < 3; ++i) {
        QRectF b(w.left() + 20 + i * 116, w.bottom() - 54, 108, 34);
        frame(p, btn, bl[i], b);
        p.drawText(b, Qt::AlignCenter, bt[i]);
    }
    p.end();
    img.save(out + "/preview-plasma-style.png");
}

static void auroraeWindow(QPainter &p, const QString &dir, QPointF at, QSizeF client, const QString &title, bool active)
{
    QSvgRenderer deco(dir + "/decoration.svg");
    const qreal T = 22, B = 5;
    QRectF outer(at.x(), at.y(), client.width() + 2 * B, client.height() + T + 2 * B);
    p.fillRect(outer.adjusted(B, T + B, -B, -B), Qt::white);
    frame(p, deco, active ? "decoration" : "decoration-inactive", outer);
    auto button = [&](const QString &name, qreal x) {
        QSvgRenderer b(dir + "/" + name + ".svg");
        b.render(&p, active ? "active-center" : "inactive-center", QRectF(x, at.y() + 4, 14, 14));
    };
    button("close", at.x() + 7);
    QFont f;
    f.setPixelSize(13);
    f.setBold(true);
    p.setFont(f);
    p.setPen(active ? Qt::black : QColor(80, 80, 80));
    p.drawText(QRectF(at.x() + 31, at.y(), 300, T), Qt::AlignVCenter, title);
    button("minimize", outer.right() - 7 - 14 - 4 - 14);
    button("maximize", outer.right() - 7 - 14);
}

static void aurorae(const QString &root, const QString &out)
{
    const QString dir = root + "/aurorae/themes/Haiku";
    QImage img(900, 520, QImage::Format_ARGB32);
    img.fill(QColor(51, 102, 152));
    QPainter p(&img);
    auroraeWindow(p, dir, {40, 40}, {460, 260}, "Inactive window", false);
    auroraeWindow(p, dir, {300, 170}, {540, 290}, "Haiku (Aurorae) – active window", true);
    p.end();
    img.save(out + "/preview-aurorae.png");
}

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    const QString root = argv[1], out = argv[2];
    QDir().mkpath(out);
    plasmaStyle(root, out);
    aurorae(root, out);
    return 0;
}
