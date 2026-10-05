// SPDX-License-Identifier: MIT
// Pure-Qt painting routines for the Haiku window decoration.
// Kept free of KDecoration types so they can be previewed/tested standalone.
#pragma once

#include <QColor>
#include <QFont>
#include <QRectF>
#include <QString>

class QPainter;

namespace HaikuDeco
{
enum class Glyph {
    Close,     // plain bevelled square (Haiku style)
    Zoom,      // two overlapping squares
    Minimize,
    Menu,
    OnAllDesktops,
    KeepAbove,
    KeepBelow,
    Shade,
    ContextHelp,
    Generic,
};

QColor tint(const QColor &c, qreal t);

// outer = complete frame rectangle (below the tab), border = frame width in px
void paintFrame(QPainter *p, const QRectF &outer, qreal border, const QColor &frame, bool active);
// tab rectangle; its bottom edge touches the frame
void paintTab(QPainter *p, const QRectF &tab, const QColor &tabColor, bool active);
void paintTitle(QPainter *p, const QRectF &r, const QString &text, const QFont &font, const QColor &color);
void paintButton(QPainter *p, const QRectF &r, const QColor &tabColor, Glyph g, bool pressed, bool hovered,
                 bool checked, bool active);
}
