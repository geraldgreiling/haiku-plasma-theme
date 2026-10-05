// SPDX-License-Identifier: MIT
// Haiku R1 look-alike widget style for Qt 6 / KDE Plasma 6.
#pragma once

#include <QProxyStyle>

class HaikuStyle : public QProxyStyle
{
    Q_OBJECT
public:
    HaikuStyle();

    void drawPrimitive(PrimitiveElement pe, const QStyleOption *opt, QPainter *p,
                       const QWidget *w = nullptr) const override;
    void drawControl(ControlElement ce, const QStyleOption *opt, QPainter *p,
                     const QWidget *w = nullptr) const override;
    void drawComplexControl(ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p,
                            const QWidget *w = nullptr) const override;
    QRect subControlRect(ComplexControl cc, const QStyleOptionComplex *opt, SubControl sc,
                         const QWidget *w = nullptr) const override;
    int pixelMetric(PixelMetric pm, const QStyleOption *opt = nullptr,
                    const QWidget *w = nullptr) const override;
    int styleHint(StyleHint sh, const QStyleOption *opt = nullptr, const QWidget *w = nullptr,
                  QStyleHintReturn *ret = nullptr) const override;
    QPalette standardPalette() const override;
    void polish(QWidget *w) override;
    void unpolish(QWidget *w) override;
    void unpolish(QApplication *app) override { QProxyStyle::unpolish(app); }
    void polish(QPalette &pal) override { QProxyStyle::polish(pal); }
    void polish(QApplication *app) override { QProxyStyle::polish(app); }

    // Shared painting helpers (also used by the gallery test)
    static QColor tint(const QColor &c, qreal t);
    static void paintButton(QPainter *p, const QRectF &r, const QPalette &pal, bool enabled,
                            bool pressed, bool hover, bool focus, bool isDefault, qreal radius = 3.0);
    static void paintTextFrame(QPainter *p, const QRectF &r, const QPalette &pal, bool enabled,
                               bool focus, bool fill);
    static void paintArrow(QPainter *p, const QRectF &r, Qt::ArrowType dir, const QColor &c);
};
