// Standalone preview of the Haiku decoration painting (no KWin needed).
#include "haikupainter.h"
#include <QFontMetricsF>
#include <QGuiApplication>
#include <QImage>
#include <QPainter>

using namespace HaikuDeco;

static void window(QPainter &p, QPointF at, QSizeF client, const QString &title, bool active)
{
    const qreal B = 5;
    QFont f; f.setPointSizeF(10); f.setBold(true);
    QFontMetricsF fm(f);
    const qreal T = qRound(fm.height()) + 8;
    const qreal bs = qRound(T * 0.62);
    const QColor tab = active ? QColor(255, 203, 0) : QColor(232, 232, 232);
    const QColor frame = active ? QColor(224, 224, 224) : QColor(232, 232, 232);
    const qreal pad = 5, gap = 7;
    const qreal tw = pad + bs + gap + fm.horizontalAdvance(title) + gap + bs + gap + bs + pad;
    QRectF outer(at.x(), at.y() + T, client.width() + 2 * B, client.height() + 2 * B);
    QRectF tabR(at.x(), at.y(), tw, T);
    p.fillRect(outer.adjusted(B, B, -B, -B), QColor(255, 255, 255));
    paintFrame(&p, outer, B, frame, active);
    paintTab(&p, tabR, tab, active);
    const qreal by = at.y() + (T - bs) / 2;
    paintButton(&p, QRectF(at.x() + pad, by, bs, bs), tab, Glyph::Close, false, false, false, active);
    paintTitle(&p, QRectF(at.x() + pad + bs + gap, at.y(), fm.horizontalAdvance(title) + 2, T), title, f,
               active ? Qt::black : QColor(80, 80, 80));
    paintButton(&p, QRectF(tabR.right() - pad - bs - gap - bs, by, bs, bs), tab, Glyph::Minimize, false, false, false, active);
    paintButton(&p, QRectF(tabR.right() - pad - bs, by, bs, bs), tab, Glyph::Zoom, false, false, false, active);
}

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);
    QImage img(640, 400, QImage::Format_ARGB32);
    img.fill(QColor(51, 102, 152));
    QPainter p(&img);
    window(p, {30, 30}, {360, 200}, "Tracker – /boot/home", false);
    window(p, {200, 130}, {400, 220}, "StyledEdit", true);
    p.end();
    img.save(argc > 1 ? argv[1] : "deco.png");
    return 0;
}
