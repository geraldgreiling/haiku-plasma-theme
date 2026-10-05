// SPDX-License-Identifier: MIT
#include "haikupainter.h"

#include <QFontMetricsF>
#include <QLinearGradient>
#include <QPainter>
#include <QPainterPath>
#include <QtMath>

namespace HaikuDeco
{
QColor tint(const QColor &c, qreal t)
{
    auto f = [t](int v) {
        int r = (t < 1.0) ? int(255 - (255 - v) * t) : int(v * (2.0 - t));
        return qBound(0, r, 255);
    };
    return QColor(f(c.red()), f(c.green()), f(c.blue()), c.alpha());
}

static void line(QPainter *p, qreal x1, qreal y1, qreal x2, qreal y2, const QColor &c)
{
    p->setPen(QPen(c, 1));
    p->drawLine(QPointF(x1, y1), QPointF(x2, y2));
}

void paintFrame(QPainter *p, const QRectF &outer, qreal border, const QColor &frame, bool active)
{
    if (border <= 0)
        return;
    p->save();
    p->setRenderHint(QPainter::Antialiasing, false);
    const QColor dark = tint(frame, active ? 1.45 : 1.3);
    const QColor light = tint(frame, 0.25);
    const QColor shade = tint(frame, 1.15);

    // fill the frame ring with the base colour
    QRectF in = outer.adjusted(border, border, -border, -border);
    QPainterPath ring;
    ring.addRect(outer);
    ring.addRect(in);
    ring.setFillRule(Qt::OddEvenFill);
    p->fillPath(ring, frame);

    // pixel-centred coordinates
    const qreal l = outer.left() + 0.5, t = outer.top() + 0.5;
    const qreal r = outer.right() - 0.5, b = outer.bottom() - 0.5;
    // 1) outer dark line
    p->setPen(QPen(dark, 1));
    p->setBrush(Qt::NoBrush);
    p->drawRect(QRectF(l, t, r - l, b - t));
    if (border >= 3) {
        // 2) raised bevel: light top/left, shade bottom/right
        line(p, l + 1, t + 1, r - 1, t + 1, light);
        line(p, l + 1, t + 1, l + 1, b - 1, light);
        line(p, l + 1, b - 1, r - 1, b - 1, shade);
        line(p, r - 1, t + 1, r - 1, b - 1, shade);
        // 3) inner sunken line next to the client
        const qreal il = in.left() - 0.5, it = in.top() - 0.5, ir = in.right() + 0.5, ib = in.bottom() + 0.5;
        line(p, il, it, ir, it, dark);
        line(p, il, it, il, ib, dark);
        line(p, il, ib, ir, ib, light);
        line(p, ir, it, ir, ib, light);
    }
    // resize knob marks in the bottom right corner
    if (border >= 4) {
        const qreal k = 18;
        line(p, r - k, b - border + 1, r - k, b - 1, dark);
        line(p, r - k + 1, b - border + 1, r - k + 1, b - 1, light);
        line(p, r - border + 1, b - k, r - 1, b - k, dark);
        line(p, r - border + 1, b - k + 1, r - 1, b - k + 1, light);
    }
    p->restore();
}

void paintTab(QPainter *p, const QRectF &tab, const QColor &tabColor, bool active)
{
    p->save();
    p->setRenderHint(QPainter::Antialiasing, false);
    QLinearGradient g(tab.topLeft(), tab.bottomLeft());
    g.setColorAt(0, tint(tabColor, active ? 0.45 : 0.6));
    g.setColorAt(1, tabColor);
    p->fillRect(tab, g);
    const QColor dark = active ? tint(tabColor, 1.4) : tint(tabColor, 1.35);
    const QColor light = tint(tabColor, 0.2);
    const qreal l = tab.left() + 0.5, t = tab.top() + 0.5, r = tab.right() - 0.5, b = tab.bottom() + 0.5;
    // outer border (bottom stays open – it merges into the frame)
    line(p, l, b, l, t, dark);
    line(p, l, t, r, t, dark);
    line(p, r, t, r, b, dark);
    // bevel
    line(p, l + 1, t + 1, r - 1, t + 1, light);
    line(p, l + 1, t + 1, l + 1, b, light);
    line(p, r - 1, t + 2, r - 1, b, tint(tabColor, 1.12));
    p->restore();
}

void paintTitle(QPainter *p, const QRectF &r, const QString &text, const QFont &font, const QColor &color)
{
    if (r.width() <= 4)
        return;
    p->save();
    p->setFont(font);
    p->setPen(color);
    QFontMetricsF fm(font);
    const QString el = fm.elidedText(text, Qt::ElideRight, r.width());
    p->drawText(r, Qt::AlignLeft | Qt::AlignVCenter | Qt::TextSingleLine, el);
    p->restore();
}

// bevelled box used by all buttons
static void box(QPainter *p, const QRectF &rr, const QColor &c, bool pressed, bool hovered)
{
    const QRectF r = rr.adjusted(0.5, 0.5, -0.5, -0.5);
    QLinearGradient g(r.topLeft(), r.bottomRight());
    if (pressed) {
        g.setColorAt(0, tint(c, 1.25));
        g.setColorAt(1, tint(c, 0.6));
    } else {
        g.setColorAt(0, tint(c, hovered ? 0.15 : 0.3));
        g.setColorAt(1, tint(c, hovered ? 0.95 : 1.08));
    }
    p->fillRect(r, g);
    p->setPen(QPen(tint(c, 1.5), 1));
    p->setBrush(Qt::NoBrush);
    p->drawRect(r);
    if (!pressed && r.width() > 4) {
        line(p, r.left() + 1, r.top() + 1, r.right() - 1, r.top() + 1, QColor(255, 255, 255, 170));
        line(p, r.left() + 1, r.top() + 1, r.left() + 1, r.bottom() - 1, QColor(255, 255, 255, 170));
    }
}

void paintButton(QPainter *p, const QRectF &rect, const QColor &tabColor, Glyph g, bool pressed, bool hovered,
                 bool checked, bool active)
{
    p->save();
    p->setRenderHint(QPainter::Antialiasing, false);
    const QColor c = active ? tabColor : tint(tabColor, 1.02);
    // keep everything on the pixel grid
    const qreal s = qFloor(qMin(rect.width(), rect.height()));
    QRectF r(qRound(rect.left() + (rect.width() - s) / 2), qRound(rect.top() + (rect.height() - s) / 2), s, s);
    const QColor ink = tint(c, 1.75);

    switch (g) {
    case Glyph::Close:
        box(p, r, c, pressed, hovered);
        break;
    case Glyph::Zoom: {
        // big square bottom-right, small square top-left on top of it
        const qreal big = qRound(s * 0.75), small = qRound(s * 0.5);
        box(p, QRectF(r.right() + 1 - big, r.bottom() + 1 - big, big, big), c, pressed, hovered);
        box(p, QRectF(r.left(), r.top(), small, small), c, pressed, hovered);
        break;
    }
    case Glyph::Minimize: {
        box(p, r, c, pressed, hovered);
        const qreal h = qMax(2.0, qRound(s * 0.2) * 1.0);
        box(p, QRectF(r.left() + 3, r.bottom() - 2 - h, r.width() - 6, h), c, !pressed, false);
        break;
    }
    case Glyph::Menu:
        break; // the window icon is painted by the button itself
    default: {
        box(p, r, c, pressed || checked, hovered);
        p->setRenderHint(QPainter::Antialiasing, true);
        p->setPen(QPen(ink, 1.3));
        p->setBrush(ink);
        const QPointF ct = r.center();
        const qreal q = s * 0.22;
        if (g == Glyph::OnAllDesktops) {
            p->drawEllipse(ct, q * 0.8, q * 0.8);
        } else if (g == Glyph::KeepAbove) {
            p->drawPolygon(QPolygonF({QPointF(ct.x() - q, ct.y() + q * 0.6), QPointF(ct.x() + q, ct.y() + q * 0.6), QPointF(ct.x(), ct.y() - q * 0.8)}));
        } else if (g == Glyph::KeepBelow) {
            p->drawPolygon(QPolygonF({QPointF(ct.x() - q, ct.y() - q * 0.6), QPointF(ct.x() + q, ct.y() - q * 0.6), QPointF(ct.x(), ct.y() + q * 0.8)}));
        } else if (g == Glyph::Shade) {
            p->drawLine(QPointF(ct.x() - q, ct.y() - q * 0.5), QPointF(ct.x() + q, ct.y() - q * 0.5));
        } else if (g == Glyph::ContextHelp) {
            QFont f;
            f.setPixelSize(int(s * 0.7));
            f.setBold(true);
            p->setFont(f);
            p->drawText(r, Qt::AlignCenter, QStringLiteral("?"));
        }
        break;
    }
    }
    p->restore();
}
}
