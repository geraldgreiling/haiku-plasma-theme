// Composes a full desktop preview (panel + decorated window with widget gallery).
#include "haikupainter.h"
#include <QFontMetricsF>
#include <QGuiApplication>
#include <QImage>
#include <QPainter>
#include <QSvgRenderer>
using namespace HaikuDeco;

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    // argv: out client.png iconsdir
    QImage client(argv[2]);
    const QString icons = argv[3];
    QImage img(1280, 800, QImage::Format_ARGB32);
    img.fill(QColor(51, 102, 152));
    QPainter p(&img);
    p.setRenderHint(QPainter::Antialiasing);
    // desktop icons
    QFont lf; lf.setPointSizeF(9);
    p.setFont(lf);
    int y = 60;
    for (auto n : {"devices/drive-harddisk|BeFS", "places/user-home|Home", "places/user-trash|Trash"}) {
        QString s(n); auto parts = s.split('|');
        QSvgRenderer r(icons + "/scalable/" + parts[0] + ".svg");
        r.render(&p, QRectF(1190, y, 48, 48));
        p.setPen(Qt::white);
        p.drawText(QRectF(1150, y + 50, 128, 18), Qt::AlignCenter, parts[1]);
        y += 90;
    }
    // panel (Deskbar at top)
    QRect bar(0, 0, 1280, 30);
    p.setRenderHint(QPainter::Antialiasing, false);
    p.fillRect(bar, QColor(216, 216, 216));
    p.setPen(QColor(255, 255, 255)); p.drawLine(0, 0, 1279, 0);
    p.setPen(QColor(124, 124, 124)); p.drawLine(0, 29, 1279, 29);
    QSvgRenderer leaf(icons + "/scalable/places/start-here.svg");
    p.setRenderHint(QPainter::Antialiasing);
    leaf.render(&p, QRectF(6, 3, 24, 24));
    auto task = [&](int x, const QString &t, const QString &icon, bool active) {
        QRect r(x, 3, 180, 24);
        p.setRenderHint(QPainter::Antialiasing, false);
        p.fillRect(r, active ? QColor(232, 232, 232) : QColor(240, 240, 240));
        p.setPen(active ? QColor(152, 152, 152) : QColor(184, 184, 184));
        p.drawRect(r.adjusted(0, 0, -1, -1));
        p.setPen(active ? QColor(184, 184, 184) : Qt::white);
        p.drawLine(r.left() + 1, r.top() + 1, r.right() - 1, r.top() + 1);
        p.setRenderHint(QPainter::Antialiasing);
        QSvgRenderer ic(icons + "/scalable/" + icon + ".svg");
        ic.render(&p, QRectF(x + 4, 5, 20, 20));
        p.setPen(Qt::black);
        p.drawText(QRect(x + 28, 3, 148, 24), Qt::AlignVCenter, t);
    };
    task(40, "Haiku Gallery", "apps/preferences-system", true);
    task(224, "Home", "apps/system-file-manager", false);
    task(408, "Terminal", "apps/utilities-terminal", false);
    p.setPen(Qt::black);
    p.drawText(QRect(1180, 0, 90, 30), Qt::AlignCenter, "12:00");

    // window
    const qreal B = 5;
    QFont f; f.setPointSizeF(10); f.setBold(true);
    QFontMetricsF fm(f);
    const qreal T = qRound(fm.height()) + 8, bs = qRound(T * 0.62);
    const QString title = "Haiku Gallery";
    QPointF at(120, 90);
    const QColor tab(255, 203, 0), frame(224, 224, 224);
    const qreal tw = 5 + bs + 7 + fm.horizontalAdvance(title) + 2 + 7 + bs + 4 + bs + 5;
    QRectF outer(at.x(), at.y() + T, client.width() + 2 * B, client.height() + 2 * B);
    p.drawImage(QPointF(outer.left() + B, outer.top() + B), client);
    paintFrame(&p, outer, B, frame, true);
    paintTab(&p, QRectF(at.x(), at.y(), tw, T), tab, true);
    const qreal by = at.y() + qRound((T - bs) / 2);
    paintButton(&p, QRectF(at.x() + 5, by, bs, bs), tab, Glyph::Close, false, false, false, true);
    paintTitle(&p, QRectF(at.x() + 5 + bs + 7, at.y(), fm.horizontalAdvance(title) + 2, T), title, f, Qt::black);
    paintButton(&p, QRectF(at.x() + tw - 5 - bs - 4 - bs, by, bs, bs), tab, Glyph::Minimize, false, false, false, true);
    paintButton(&p, QRectF(at.x() + tw - 5 - bs, by, bs, bs), tab, Glyph::Zoom, false, false, false, true);
    p.end();
    img.save(argv[1]);
    return 0;
}
