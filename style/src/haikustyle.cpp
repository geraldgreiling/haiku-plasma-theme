// SPDX-License-Identifier: MIT
// Haiku R1 look-alike widget style for Qt 6 / KDE Plasma 6.
//
// Built as a QProxyStyle on top of Fusion: everything that is not drawn
// explicitly here falls back to Fusion, so unusual widgets never break.

#include "haikustyle.h"

#include <QAbstractButton>
#include <QAbstractItemView>
#include <QAbstractSpinBox>
#include <QApplication>
#include <QCheckBox>
#include <QComboBox>
#include <QHeaderView>
#include <QLinearGradient>
#include <QPainter>
#include <QPainterPath>
#include <QPushButton>
#include <QRadialGradient>
#include <QRadioButton>
#include <QScrollBar>
#include <QSlider>
#include <QStyleFactory>
#include <QStyleOption>
#include <QTabBar>
#include <QToolButton>

namespace
{
// Haiku interface colours (InterfaceDefs.cpp defaults)
const QColor kNavigation(0, 0, 229);   // B_NAVIGATION_BASE_COLOR – keyboard focus
const QColor kMark(46, 76, 186);       // check marks / radio dots
const QColor kFill(102, 152, 203);     // B_CONTROL_HIGHLIGHT_COLOR – slider fill
const QColor kBar(50, 150, 255);       // BStatusBar default bar colour

struct PainterSaver {
    explicit PainterSaver(QPainter *p) : m_p(p) { m_p->save(); }
    ~PainterSaver() { m_p->restore(); }
    QPainter *m_p;
};

bool isEnabled(const QStyleOption *opt) { return opt->state & QStyle::State_Enabled; }
bool isHover(const QStyleOption *opt) { return (opt->state & QStyle::State_MouseOver) && isEnabled(opt); }

QRectF half(const QRect &r) { return QRectF(r).adjusted(0.5, 0.5, -0.5, -0.5); }
} // namespace

HaikuStyle::HaikuStyle()
    : QProxyStyle(QStyleFactory::create(QStringLiteral("Fusion")))
{
    setObjectName(QStringLiteral("Haiku"));
}

// Haiku's tint_color(): t < 1 lightens (0 = white), t > 1 darkens (2 = black)
QColor HaikuStyle::tint(const QColor &c, qreal t)
{
    auto f = [t](int v) {
        int r = (t < 1.0) ? int(255 - (255 - v) * t) : int(v * (2.0 - t));
        return qBound(0, r, 255);
    };
    return QColor(f(c.red()), f(c.green()), f(c.blue()), c.alpha());
}

void HaikuStyle::paintButton(QPainter *p, const QRectF &rect, const QPalette &pal, bool enabled,
                             bool pressed, bool hover, bool focus, bool isDefault, qreal radius)
{
    PainterSaver s(p);
    p->setRenderHint(QPainter::Antialiasing, true);
    QColor base = pal.color(QPalette::Button);
    if (!enabled)
        base = tint(base, 0.6);

    QRectF r = rect.adjusted(0.5, 0.5, -0.5, -0.5);
    if (isDefault) {
        // Haiku draws an additional frame around the default button
        QPainterPath outer;
        outer.addRoundedRect(r, radius + 1, radius + 1);
        p->fillPath(outer, tint(base, 1.12));
        p->setPen(QPen(tint(base, enabled ? 1.45 : 1.2), 1));
        p->drawPath(outer);
        r.adjust(2, 2, -2, -2);
    }

    QLinearGradient g(r.topLeft(), r.bottomLeft());
    if (pressed) {
        g.setColorAt(0, tint(base, 1.18));
        g.setColorAt(1, tint(base, 1.06));
    } else {
        g.setColorAt(0, tint(base, hover ? 0.15 : 0.35));
        g.setColorAt(0.5, tint(base, hover ? 0.45 : 0.7));
        g.setColorAt(1, tint(base, hover ? 0.95 : 1.04));
    }
    QPainterPath path;
    path.addRoundedRect(r, radius, radius);
    p->fillPath(path, g);

    // inner bevel
    if (!pressed && r.width() > 6 && r.height() > 6) {
        p->setPen(QPen(QColor(255, 255, 255, enabled ? 210 : 120), 1));
        p->drawLine(QPointF(r.left() + radius, r.top() + 1), QPointF(r.right() - radius, r.top() + 1));
        p->drawLine(QPointF(r.left() + 1, r.top() + radius), QPointF(r.left() + 1, r.bottom() - radius));
        p->setPen(QPen(QColor(0, 0, 0, enabled ? 28 : 12), 1));
        p->drawLine(QPointF(r.left() + radius, r.bottom() - 1), QPointF(r.right() - radius, r.bottom() - 1));
        p->drawLine(QPointF(r.right() - 1, r.top() + radius), QPointF(r.right() - 1, r.bottom() - radius));
    }

    QColor border = tint(base, enabled ? 1.55 : 1.22);
    p->setBrush(Qt::NoBrush);
    p->setPen(QPen(border, 1));
    p->drawPath(path);
    if (focus && enabled) {
        QPainterPath fp;
        fp.addRoundedRect(r.adjusted(1, 1, -1, -1), qMax(0.0, radius - 1), qMax(0.0, radius - 1));
        p->setPen(QPen(kNavigation, 1));
        p->drawPath(fp);
    }
}

void HaikuStyle::paintTextFrame(QPainter *p, const QRectF &rect, const QPalette &pal, bool enabled,
                                bool focus, bool fill)
{
    PainterSaver s(p);
    p->setRenderHint(QPainter::Antialiasing, false);
    const QRect r = rect.toRect();
    const QColor bg = pal.color(QPalette::Window);
    // outer sunken bevel: dark top/left, white bottom/right
    p->setPen(tint(bg, 1.12));
    p->drawLine(r.topLeft(), r.topRight() - QPoint(1, 0));
    p->drawLine(r.topLeft(), r.bottomLeft() - QPoint(0, 1));
    p->setPen(tint(bg, 0.25));
    p->drawLine(r.bottomLeft(), r.bottomRight());
    p->drawLine(r.topRight(), r.bottomRight());
    // inner border
    QRect in = r.adjusted(1, 1, -1, -1);
    if (fill)
        p->fillRect(in.adjusted(1, 1, 0, 0), enabled ? pal.color(QPalette::Base) : tint(bg, 0.6));
    p->setPen(focus && enabled ? kNavigation : tint(bg, enabled ? 1.45 : 1.2));
    p->setBrush(Qt::NoBrush);
    p->drawRect(in.adjusted(0, 0, -1, -1));
}

void HaikuStyle::paintArrow(QPainter *p, const QRectF &r, Qt::ArrowType dir, const QColor &c)
{
    PainterSaver s(p);
    p->setRenderHint(QPainter::Antialiasing, true);
    const qreal sz = qMax(3.0, qMin(r.width(), r.height()) * 0.55);
    const QPointF ct = r.center();
    QPolygonF poly;
    const qreal h = sz / 2.0;
    switch (dir) {
    case Qt::UpArrow:
        poly << QPointF(ct.x() - sz * 0.6, ct.y() + h * 0.6) << QPointF(ct.x() + sz * 0.6, ct.y() + h * 0.6)
             << QPointF(ct.x(), ct.y() - h * 0.7);
        break;
    case Qt::DownArrow:
        poly << QPointF(ct.x() - sz * 0.6, ct.y() - h * 0.6) << QPointF(ct.x() + sz * 0.6, ct.y() - h * 0.6)
             << QPointF(ct.x(), ct.y() + h * 0.7);
        break;
    case Qt::LeftArrow:
        poly << QPointF(ct.x() + h * 0.6, ct.y() - sz * 0.6) << QPointF(ct.x() + h * 0.6, ct.y() + sz * 0.6)
             << QPointF(ct.x() - h * 0.7, ct.y());
        break;
    default:
        poly << QPointF(ct.x() - h * 0.6, ct.y() - sz * 0.6) << QPointF(ct.x() - h * 0.6, ct.y() + sz * 0.6)
             << QPointF(ct.x() + h * 0.7, ct.y());
        break;
    }
    p->setPen(Qt::NoPen);
    p->setBrush(c);
    p->drawPolygon(poly);
}

// ---------------------------------------------------------------------------
// local drawing helpers
// ---------------------------------------------------------------------------
static void paintCheck(QPainter *p, const QStyleOption *opt, bool on, bool tristate)
{
    PainterSaver s(p);
    p->setRenderHint(QPainter::Antialiasing, true);
    const QPalette &pal = opt->palette;
    const bool en = isEnabled(opt);
    const int side = qMin(opt->rect.width(), opt->rect.height());
    QRectF r(0, 0, side, side);
    r.moveCenter(QRectF(opt->rect).center());
    r.adjust(0.5, 0.5, -0.5, -0.5);
    QColor base = en ? pal.color(QPalette::Base) : HaikuStyle::tint(pal.color(QPalette::Window), 0.6);
    QLinearGradient g(r.topLeft(), r.bottomLeft());
    if (opt->state & QStyle::State_Sunken) {
        g.setColorAt(0, HaikuStyle::tint(base, 1.2));
        g.setColorAt(1, HaikuStyle::tint(base, 1.08));
    } else {
        g.setColorAt(0, HaikuStyle::tint(base, 1.08));
        g.setColorAt(1, base);
    }
    p->setBrush(g);
    QColor border = HaikuStyle::tint(pal.color(QPalette::Window), en ? 1.55 : 1.25);
    if ((opt->state & QStyle::State_HasFocus) && en)
        border = kNavigation;
    p->setPen(QPen(border, 1));
    p->drawRoundedRect(r, 1.5, 1.5);
    QColor mark = en ? kMark : HaikuStyle::tint(pal.color(QPalette::Window), 1.3);
    if (tristate) {
        p->setPen(QPen(mark, 2, Qt::SolidLine, Qt::RoundCap));
        p->drawLine(QPointF(r.left() + 3.5, r.center().y()), QPointF(r.right() - 3.5, r.center().y()));
    } else if (on) {
        // Haiku draws a cross as check mark
        p->setPen(QPen(mark, 2, Qt::SolidLine, Qt::RoundCap));
        const QRectF m = r.adjusted(3.5, 3.5, -3.5, -3.5);
        p->drawLine(m.topLeft(), m.bottomRight());
        p->drawLine(m.topRight(), m.bottomLeft());
    }
}

static void paintRadio(QPainter *p, const QStyleOption *opt)
{
    PainterSaver s(p);
    p->setRenderHint(QPainter::Antialiasing, true);
    const QPalette &pal = opt->palette;
    const bool en = isEnabled(opt);
    const int side = qMin(opt->rect.width(), opt->rect.height());
    QRectF r(0, 0, side, side);
    r.moveCenter(QRectF(opt->rect).center());
    r.adjust(0.5, 0.5, -0.5, -0.5);
    QColor base = en ? pal.color(QPalette::Base) : HaikuStyle::tint(pal.color(QPalette::Window), 0.6);
    QLinearGradient g(r.topLeft(), r.bottomLeft());
    const bool sunken = opt->state & QStyle::State_Sunken;
    g.setColorAt(0, HaikuStyle::tint(base, sunken ? 1.25 : 1.1));
    g.setColorAt(1, sunken ? HaikuStyle::tint(base, 1.08) : base);
    p->setBrush(g);
    QColor border = HaikuStyle::tint(pal.color(QPalette::Window), en ? 1.55 : 1.25);
    if ((opt->state & QStyle::State_HasFocus) && en)
        border = kNavigation;
    p->setPen(QPen(border, 1));
    p->drawEllipse(r);
    if (opt->state & QStyle::State_On) {
        QRectF d = r.adjusted(r.width() * 0.27, r.height() * 0.27, -r.width() * 0.27, -r.height() * 0.27);
        QColor mark = en ? kMark : HaikuStyle::tint(pal.color(QPalette::Window), 1.3);
        QRadialGradient rg(d.center() - QPointF(d.width() * 0.2, d.height() * 0.2), d.width() * 0.7);
        rg.setColorAt(0, HaikuStyle::tint(mark, 0.45));
        rg.setColorAt(1, mark);
        p->setPen(Qt::NoPen);
        p->setBrush(rg);
        p->drawEllipse(d);
    }
}

static void paintBarBackground(QPainter *p, const QRect &r, const QPalette &pal, bool bottomLine)
{
    const QColor bg = pal.color(QPalette::Window);
    QLinearGradient g(r.topLeft(), r.bottomLeft());
    g.setColorAt(0, HaikuStyle::tint(bg, 0.45));
    g.setColorAt(1, bg);
    p->fillRect(r, g);
    if (bottomLine) {
        p->setPen(HaikuStyle::tint(bg, 1.35));
        p->drawLine(r.bottomLeft(), r.bottomRight());
    }
}

static void paintGrip(QPainter *p, const QRect &r, Qt::Orientation o, const QColor &bg)
{
    // three short ridges perpendicular to the scroll direction
    const QPoint c = r.center();
    for (int i = -1; i <= 1; ++i) {
        if (o == Qt::Vertical) {
            const int y = c.y() + i * 3;
            p->setPen(HaikuStyle::tint(bg, 1.45));
            p->drawLine(c.x() - 3, y, c.x() + 3, y);
            p->setPen(QColor(255, 255, 255));
            p->drawLine(c.x() - 3, y + 1, c.x() + 3, y + 1);
        } else {
            const int x = c.x() + i * 3;
            p->setPen(HaikuStyle::tint(bg, 1.45));
            p->drawLine(x, c.y() - 3, x, c.y() + 3);
            p->setPen(QColor(255, 255, 255));
            p->drawLine(x + 1, c.y() - 3, x + 1, c.y() + 3);
        }
    }
}

// ---------------------------------------------------------------------------
// primitives
// ---------------------------------------------------------------------------
void HaikuStyle::drawPrimitive(PrimitiveElement pe, const QStyleOption *opt, QPainter *p,
                               const QWidget *w) const
{
    const QPalette &pal = opt->palette;
    const bool en = isEnabled(opt);

    switch (pe) {
    case PE_PanelButtonCommand:
    case PE_PanelButtonBevel: {
        const bool pressed = opt->state & (State_Sunken | State_On);
        paintButton(p, opt->rect, pal, en, pressed, isHover(opt), false, false);
        return;
    }
    case PE_PanelButtonTool: {
        const bool pressed = opt->state & (State_Sunken | State_On);
        if (pressed || isHover(opt) || (opt->state & State_Raised))
            paintButton(p, opt->rect, pal, en, pressed, isHover(opt), false, false, 2.5);
        return;
    }
    case PE_FrameButtonTool:
    case PE_FrameDefaultButton:
    case PE_FrameStatusBarItem:
        return;

    case PE_FrameFocusRect: {
        // Haiku: blue underline below the label of check/radio boxes,
        // nothing on item-view items, a thin blue rectangle elsewhere.
        if (qobject_cast<const QAbstractItemView *>(w))
            return;
        PainterSaver s(p);
        p->setPen(kNavigation);
        if (qobject_cast<const QCheckBox *>(w) || qobject_cast<const QRadioButton *>(w)) {
            const QRect r = opt->rect;
            p->drawLine(r.left(), r.bottom(), r.right(), r.bottom());
        } else {
            p->setBrush(Qt::NoBrush);
            p->drawRect(opt->rect.adjusted(0, 0, -1, -1));
        }
        return;
    }

    case PE_IndicatorCheckBox:
    case PE_IndicatorItemViewItemCheck:
        paintCheck(p, opt, opt->state & State_On, opt->state & State_NoChange);
        return;
    case PE_IndicatorRadioButton:
        paintRadio(p, opt);
        return;

    case PE_IndicatorArrowUp:
    case PE_IndicatorArrowDown:
    case PE_IndicatorArrowLeft:
    case PE_IndicatorArrowRight:
    case PE_IndicatorSpinUp:
    case PE_IndicatorSpinDown: {
        Qt::ArrowType a = Qt::RightArrow;
        if (pe == PE_IndicatorArrowUp || pe == PE_IndicatorSpinUp)
            a = Qt::UpArrow;
        else if (pe == PE_IndicatorArrowDown || pe == PE_IndicatorSpinDown)
            a = Qt::DownArrow;
        else if (pe == PE_IndicatorArrowLeft)
            a = Qt::LeftArrow;
        QColor c = en ? pal.color(QPalette::ButtonText) : tint(pal.color(QPalette::Window), 1.35);
        if (opt->state & State_Selected && !(opt->state & State_Sunken))
            c = pal.color(QPalette::HighlightedText);
        paintArrow(p, opt->rect, a, c);
        return;
    }

    case PE_IndicatorBranch: {
        if (!(opt->state & State_Children))
            return;
        Qt::ArrowType a = (opt->state & State_Open) ? Qt::DownArrow
                                                    : (opt->direction == Qt::RightToLeft ? Qt::LeftArrow : Qt::RightArrow);
        QRect r(0, 0, 12, 12);
        r.moveCenter(opt->rect.center());
        QColor c = (opt->state & State_Selected) ? pal.color(QPalette::HighlightedText)
                                                 : tint(pal.color(QPalette::Window), 1.6);
        paintArrow(p, r, a, c);
        return;
    }

    case PE_PanelLineEdit: {
        const auto *f = qstyleoption_cast<const QStyleOptionFrame *>(opt);
        if (f && f->lineWidth > 0) {
            paintTextFrame(p, opt->rect, pal, en, opt->state & State_HasFocus, true);
        } else {
            p->fillRect(opt->rect, pal.color(QPalette::Base));
        }
        return;
    }
    case PE_FrameLineEdit:
        paintTextFrame(p, opt->rect, pal, en, opt->state & State_HasFocus, false);
        return;

    case PE_Frame: {
        // Dolphin's small status bar overlay ("11 Ordner") sits in the corner of
        // the view and is filled with the window colour, which makes it blend
        // into the places panel. Give it a clearly lighter background and a
        // visible raised edge (left/bottom are clipped away by Dolphin).
        if (w && w->inherits("DolphinStatusBar")) {
            // Dolphin places the overlay at the very left/bottom edge of the
            // view container, i.e. on top of the view's frame. Its own palette
            // is transparent (see polish()), so only this inset box is visible
            // and the overlay stays inside the white view area.
            PainterSaver s(p);
            const QColor base = QApplication::palette().color(QPalette::Window);
            const int fw = proxy()->pixelMetric(PM_DefaultFrameWidth, opt, w);
            QRect box = w->rect().adjusted(0, 0, 0, -fw);
            if (w->layoutDirection() == Qt::RightToLeft)
                box.setRight(box.right() - fw);
            else
                box.setLeft(box.left() + fw);
            p->setClipping(false);
            p->fillRect(box, tint(base, 0.3));
            p->setPen(tint(base, 1.4));
            if (w->layoutDirection() == Qt::RightToLeft) {
                p->drawLine(box.topLeft(), box.topRight());
                p->drawLine(box.topLeft(), box.bottomLeft());
            } else {
                p->drawLine(box.topLeft(), box.topRight());
                p->drawLine(box.topRight(), box.bottomRight());
            }
            p->setPen(QColor(255, 255, 255));
            p->drawLine(box.left() + 1, box.top() + 1, box.right() - 1, box.top() + 1);
            return;
        }
        // scroll views: plain grey frame (no blue focus line)
        const bool focus = false;
        if (opt->state & State_Raised) {
            PainterSaver s(p);
            const QRect r = opt->rect.adjusted(0, 0, -1, -1);
            p->setPen(tint(pal.color(QPalette::Window), 1.4));
            p->drawRect(r);
            p->setPen(QColor(255, 255, 255));
            p->drawLine(r.left() + 1, r.top() + 1, r.right() - 1, r.top() + 1);
            p->drawLine(r.left() + 1, r.top() + 1, r.left() + 1, r.bottom() - 1);
            return;
        }
        paintTextFrame(p, opt->rect, pal, en, focus, false);
        return;
    }

    case PE_FrameGroupBox: {
        // BBox: etched line
        PainterSaver s(p);
        p->setRenderHint(QPainter::Antialiasing, true);
        QRectF r = QRectF(opt->rect).adjusted(0.5, 0.5, -1.5, -1.5);
        p->setBrush(Qt::NoBrush);
        p->setPen(QColor(255, 255, 255));
        p->drawRoundedRect(r.translated(1, 1), 3, 3);
        p->setPen(tint(pal.color(QPalette::Window), 1.3));
        p->drawRoundedRect(r, 3, 3);
        return;
    }

    case PE_FrameTabWidget: {
        PainterSaver s(p);
        const QRect r = opt->rect.adjusted(0, 0, -1, -1);
        p->setPen(tint(pal.color(QPalette::Window), 1.45));
        p->setBrush(Qt::NoBrush);
        p->drawRect(r);
        p->setPen(QColor(255, 255, 255, 220));
        p->drawLine(r.left() + 1, r.top() + 1, r.right() - 1, r.top() + 1);
        p->drawLine(r.left() + 1, r.top() + 1, r.left() + 1, r.bottom() - 1);
        p->setPen(tint(pal.color(QPalette::Window), 1.1));
        p->drawLine(r.left() + 1, r.bottom() - 1, r.right() - 1, r.bottom() - 1);
        p->drawLine(r.right() - 1, r.top() + 1, r.right() - 1, r.bottom() - 1);
        return;
    }
    case PE_FrameTabBarBase: {
        const auto *tbb = qstyleoption_cast<const QStyleOptionTabBarBase *>(opt);
        PainterSaver s(p);
        p->setPen(tint(pal.color(QPalette::Window), 1.45));
        if (tbb && (tbb->shape == QTabBar::RoundedSouth || tbb->shape == QTabBar::TriangularSouth))
            p->drawLine(opt->rect.topLeft(), opt->rect.topRight());
        else
            p->drawLine(opt->rect.bottomLeft(), opt->rect.bottomRight());
        return;
    }

    case PE_PanelMenu:
        p->fillRect(opt->rect, pal.color(QPalette::Window));
        [[fallthrough]];
    case PE_FrameMenu: {
        PainterSaver s(p);
        const QRect r = opt->rect.adjusted(0, 0, -1, -1);
        p->setBrush(Qt::NoBrush);
        p->setPen(tint(pal.color(QPalette::Window), 1.6));
        p->drawRect(r);
        p->setPen(QColor(255, 255, 255));
        p->drawLine(r.left() + 1, r.top() + 1, r.right() - 1, r.top() + 1);
        p->drawLine(r.left() + 1, r.top() + 1, r.left() + 1, r.bottom() - 1);
        p->setPen(tint(pal.color(QPalette::Window), 1.15));
        p->drawLine(r.left() + 1, r.bottom() - 1, r.right() - 1, r.bottom() - 1);
        p->drawLine(r.right() - 1, r.top() + 1, r.right() - 1, r.bottom() - 1);
        return;
    }
    case PE_PanelMenuBar:
        paintBarBackground(p, opt->rect, pal, true);
        return;

    case PE_PanelTipLabel: {
        PainterSaver s(p);
        p->fillRect(opt->rect, pal.color(QPalette::ToolTipBase));
        p->setPen(tint(pal.color(QPalette::ToolTipBase), 1.7));
        p->setBrush(Qt::NoBrush);
        p->drawRect(opt->rect.adjusted(0, 0, -1, -1));
        return;
    }

    case PE_PanelScrollAreaCorner:
        p->fillRect(opt->rect, pal.color(QPalette::Window));
        return;

    default:
        break;
    }
    QProxyStyle::drawPrimitive(pe, opt, p, w);
}

// ---------------------------------------------------------------------------
// controls
// ---------------------------------------------------------------------------
void HaikuStyle::drawControl(ControlElement ce, const QStyleOption *opt, QPainter *p,
                             const QWidget *w) const
{
    const QPalette &pal = opt->palette;
    const bool en = isEnabled(opt);

    switch (ce) {
    case CE_PushButtonBevel: {
        const auto *b = qstyleoption_cast<const QStyleOptionButton *>(opt);
        if (!b)
            break;
        const bool pressed = b->state & (State_Sunken | State_On);
        if ((b->features & QStyleOptionButton::Flat) && !pressed && !isHover(b))
            return;
        const bool isDefault = (b->features & QStyleOptionButton::DefaultButton) && en;
        paintButton(p, b->rect, pal, en, pressed, isHover(b), b->state & State_HasFocus, isDefault);
        if (b->features & QStyleOptionButton::HasMenu) {
            const int ind = proxy()->pixelMetric(PM_MenuButtonIndicator, b, w);
            QRect ar(b->rect.right() - ind - 4, b->rect.top(), ind, b->rect.height());
            ar = visualRect(b->direction, b->rect, ar);
            paintArrow(p, ar, Qt::DownArrow, en ? pal.color(QPalette::ButtonText)
                                                : tint(pal.color(QPalette::Window), 1.35));
        }
        return;
    }

    case CE_MenuBarEmptyArea:
        paintBarBackground(p, opt->rect, pal, true);
        return;

    case CE_MenuBarItem: {
        const auto *mi = qstyleoption_cast<const QStyleOptionMenuItem *>(opt);
        if (!mi)
            break;
        PainterSaver s(p);
        QRect full = mi->rect;
        if (w)
            full = QRect(mi->rect.left(), 0, mi->rect.width(), w->height());
        paintBarBackground(p, full, pal, true);
        const bool active = (mi->state & State_Selected) && (mi->state & (State_Sunken | State_HasFocus | State_Enabled));
        const bool down = mi->state & State_Sunken;
        if (active && down) {
            p->fillRect(mi->rect.adjusted(0, 0, 0, -1), pal.color(QPalette::Highlight));
        } else if (active) {
            p->fillRect(mi->rect.adjusted(0, 0, 0, -1), tint(pal.color(QPalette::Window), 1.1));
        }
        int flags = Qt::AlignCenter | Qt::TextShowMnemonic | Qt::TextDontClip | Qt::TextSingleLine;
        if (!proxy()->styleHint(SH_UnderlineShortcut, mi, w))
            flags |= Qt::TextHideMnemonic;
        proxy()->drawItemText(p, mi->rect, flags, pal, en, mi->text,
                              (active && down) ? QPalette::HighlightedText : QPalette::ButtonText);
        return;
    }

    case CE_ProgressBarGroove:
        paintTextFrame(p, opt->rect, pal, en, false, true);
        return;

    case CE_ProgressBarContents: {
        const auto *pb = qstyleoption_cast<const QStyleOptionProgressBar *>(opt);
        if (!pb)
            break;
        PainterSaver s(p);
        QRect r = pb->rect.adjusted(2, 2, -2, -2);
        const bool horizontal = pb->state & State_Horizontal;
        bool inverted = pb->invertedAppearance;
        if (horizontal && pb->direction == Qt::RightToLeft)
            inverted = !inverted;
        const qint64 range = qint64(pb->maximum) - pb->minimum;
        QRect bar = r;
        const QColor col = en ? kBar : tint(pal.color(QPalette::Window), 1.2);
        if (range <= 0) {
            // busy indicator: striped bar
            p->setClipRect(r);
            p->fillRect(r, tint(col, 0.55));
            p->setPen(Qt::NoPen);
            p->setBrush(tint(col, 0.85));
            p->setRenderHint(QPainter::Antialiasing, true);
            for (int x = r.left() - r.height(); x < r.right() + r.height(); x += 16) {
                QPolygon poly;
                poly << QPoint(x, r.bottom() + 1) << QPoint(x + 8, r.bottom() + 1)
                     << QPoint(x + 8 + r.height(), r.top()) << QPoint(x + r.height(), r.top());
                p->drawPolygon(poly);
            }
            return;
        }
        const qint64 val = qint64(qBound(pb->minimum, pb->progress, pb->maximum)) - pb->minimum;
        if (horizontal) {
            const int len = int(val * r.width() / range);
            bar.setWidth(len);
            if (inverted)
                bar.moveRight(r.right());
        } else {
            const int len = int(val * r.height() / range);
            bar.setHeight(len);
            if (!inverted)
                bar.moveBottom(r.bottom());
        }
        if (bar.width() <= 0 || bar.height() <= 0)
            return;
        QLinearGradient g(bar.topLeft(), horizontal ? bar.bottomLeft() : bar.topRight());
        g.setColorAt(0, tint(col, 0.55));
        g.setColorAt(0.45, col);
        g.setColorAt(1, tint(col, 1.12));
        p->fillRect(bar, g);
        p->setPen(tint(col, 1.35));
        p->setBrush(Qt::NoBrush);
        p->drawRect(bar.adjusted(0, 0, -1, -1));
        return;
    }

    case CE_TabBarTabShape: {
        const auto *tab = qstyleoption_cast<const QStyleOptionTab *>(opt);
        if (!tab)
            break;
        const bool north = tab->shape == QTabBar::RoundedNorth || tab->shape == QTabBar::TriangularNorth;
        const bool south = tab->shape == QTabBar::RoundedSouth || tab->shape == QTabBar::TriangularSouth;
        if (!north && !south)
            break;
        PainterSaver s(p);
        p->setRenderHint(QPainter::Antialiasing, true);
        QRectF r = QRectF(tab->rect);
        if (south) {
            // draw a north tab mirrored vertically
            QTransform t;
            t.translate(0, r.top() + r.bottom() + 1);
            t.scale(1, -1);
            p->setTransform(t, true);
        }
        const bool selected = tab->state & State_Selected;
        if (!selected)
            r.adjust(0, 2, 0, 0);
        r.adjust(0.5, 0.5, -0.5, 0);
        const qreal rad = 4;
        QPainterPath path;
        path.moveTo(r.left(), r.bottom() + 0.5);
        path.lineTo(r.left(), r.top() + rad);
        path.arcTo(QRectF(r.left(), r.top(), 2 * rad, 2 * rad), 180, -90);
        path.lineTo(r.right() - rad, r.top());
        path.arcTo(QRectF(r.right() - 2 * rad, r.top(), 2 * rad, 2 * rad), 90, -90);
        path.lineTo(r.right(), r.bottom() + 0.5);
        const QColor bg = pal.color(QPalette::Window);
        QLinearGradient g(r.topLeft(), r.bottomLeft());
        if (selected) {
            g.setColorAt(0, tint(bg, 0.3));
            g.setColorAt(1, bg);
        } else {
            const bool hov = isHover(tab);
            g.setColorAt(0, tint(bg, hov ? 0.6 : 0.9));
            g.setColorAt(1, tint(bg, hov ? 1.0 : 1.08));
        }
        p->fillPath(path, g);
        p->setPen(QPen(tint(bg, 1.45), 1));
        p->drawPath(path);
        if (selected) {
            p->setPen(QPen(QColor(255, 255, 255, 220), 1));
            p->drawLine(QPointF(r.left() + rad, r.top() + 1), QPointF(r.right() - rad, r.top() + 1));
        } else {
            p->drawLine(QPointF(r.left(), r.bottom()), QPointF(r.right(), r.bottom()));
        }
        return;
    }

    case CE_HeaderSection:
    case CE_HeaderEmptyArea: {
        PainterSaver s(p);
        const QRect r = opt->rect;
        const QColor bg = pal.color(QPalette::Button);
        const bool sunken = opt->state & State_Sunken;
        QLinearGradient g(r.topLeft(), r.bottomLeft());
        g.setColorAt(0, tint(bg, sunken ? 1.1 : 0.4));
        g.setColorAt(1, tint(bg, sunken ? 1.02 : 1.03));
        p->fillRect(r, g);
        p->setPen(tint(bg, 1.45));
        p->drawLine(r.bottomLeft(), r.bottomRight());
        if (ce == CE_HeaderSection) {
            p->setPen(tint(bg, 1.3));
            p->drawLine(r.topRight(), r.bottomRight() - QPoint(0, 1));
            p->setPen(QColor(255, 255, 255));
            p->drawLine(r.topLeft(), r.bottomLeft() - QPoint(0, 1));
        }
        return;
    }

    case CE_Splitter: {
        PainterSaver s(p);
        p->setRenderHint(QPainter::Antialiasing, true);
        const QPointF c = QRectF(opt->rect).center();
        const bool horiz = opt->state & State_Horizontal;
        for (int i = -2; i <= 2; ++i) {
            QPointF d = horiz ? QPointF(c.x(), c.y() + i * 4) : QPointF(c.x() + i * 4, c.y());
            p->setPen(Qt::NoPen);
            p->setBrush(QColor(255, 255, 255));
            p->drawEllipse(d + QPointF(0.6, 0.6), 1.1, 1.1);
            p->setBrush(tint(pal.color(QPalette::Window), 1.5));
            p->drawEllipse(d, 1.1, 1.1);
        }
        return;
    }

    case CE_ShapedFrame: {
        const auto *f = qstyleoption_cast<const QStyleOptionFrame *>(opt);
        if (f && f->frameShape == QFrame::StyledPanel) {
            proxy()->drawPrimitive(PE_Frame, opt, p, w);
            return;
        }
        break;
    }

    default:
        break;
    }
    QProxyStyle::drawControl(ce, opt, p, w);
}

// ---------------------------------------------------------------------------
// complex controls
// ---------------------------------------------------------------------------
void HaikuStyle::drawComplexControl(ComplexControl cc, const QStyleOptionComplex *opt, QPainter *p,
                                    const QWidget *w) const
{
    const QPalette &pal = opt->palette;
    const bool en = isEnabled(opt);

    switch (cc) {
    case CC_ScrollBar: {
        const auto *sb = qstyleoption_cast<const QStyleOptionSlider *>(opt);
        if (!sb)
            break;
        PainterSaver s(p);
        const bool horiz = sb->orientation == Qt::Horizontal;
        const QColor bg = pal.color(QPalette::Window);
        const bool scrollable = sb->maximum > sb->minimum && en;
        const QRect r = sb->rect;
        // trough
        p->fillRect(r, scrollable ? tint(bg, 1.12) : tint(bg, 0.8));
        if (scrollable) {
            p->setPen(tint(bg, 1.28));
            if (horiz)
                p->drawLine(r.left(), r.top() + 1, r.right(), r.top() + 1);
            else
                p->drawLine(r.left() + 1, r.top(), r.left() + 1, r.bottom());
        }
        p->setPen(tint(bg, 1.5));
        p->setBrush(Qt::NoBrush);
        p->drawRect(r.adjusted(0, 0, -1, -1));

        auto subRect = [&](SubControl sc) { return proxy()->subControlRect(CC_ScrollBar, sb, sc, w); };
        auto active = [&](SubControl sc) { return (sb->activeSubControls & sc) && (sb->state & State_Sunken); };
        auto hovered = [&](SubControl sc) { return (sb->activeSubControls & sc) && (sb->state & State_MouseOver); };

        const QColor arrowCol = scrollable ? pal.color(QPalette::ButtonText) : tint(bg, 1.3);
        if (sb->subControls & SC_ScrollBarSubLine) {
            const QRect a = subRect(SC_ScrollBarSubLine);
            paintButton(p, a, pal, scrollable, active(SC_ScrollBarSubLine), hovered(SC_ScrollBarSubLine), false, false, 0);
            paintArrow(p, QRectF(a).adjusted(1, 1, -1, -1),
                       horiz ? (sb->direction == Qt::RightToLeft ? Qt::RightArrow : Qt::LeftArrow) : Qt::UpArrow, arrowCol);
        }
        if (sb->subControls & SC_ScrollBarAddLine) {
            const QRect a = subRect(SC_ScrollBarAddLine);
            paintButton(p, a, pal, scrollable, active(SC_ScrollBarAddLine), hovered(SC_ScrollBarAddLine), false, false, 0);
            paintArrow(p, QRectF(a).adjusted(1, 1, -1, -1),
                       horiz ? (sb->direction == Qt::RightToLeft ? Qt::LeftArrow : Qt::RightArrow) : Qt::DownArrow, arrowCol);
        }
        if ((sb->subControls & SC_ScrollBarSlider) && scrollable) {
            const QRect sl = subRect(SC_ScrollBarSlider);
            paintButton(p, sl, pal, true, active(SC_ScrollBarSlider), hovered(SC_ScrollBarSlider), false, false, 0);
            if ((horiz ? sl.width() : sl.height()) > 16)
                paintGrip(p, sl, sb->orientation, pal.color(QPalette::Button));
        }
        return;
    }

    case CC_Slider: {
        const auto *sl = qstyleoption_cast<const QStyleOptionSlider *>(opt);
        if (!sl)
            break;
        PainterSaver s(p);
        p->setRenderHint(QPainter::Antialiasing, true);
        const bool horiz = sl->orientation == Qt::Horizontal;
        const QRect groove = proxy()->subControlRect(CC_Slider, sl, SC_SliderGroove, w);
        const QRect handle = proxy()->subControlRect(CC_Slider, sl, SC_SliderHandle, w);
        const QColor bg = pal.color(QPalette::Window);

        if (sl->subControls & SC_SliderGroove) {
            const qreal th = 6;
            QRectF bar = horiz ? QRectF(groove.left(), groove.center().y() - th / 2 + 0.5, groove.width(), th)
                               : QRectF(groove.center().x() - th / 2 + 0.5, groove.top(), th, groove.height());
            bar.adjust(0.5, 0.5, -0.5, -0.5);
            p->setPen(QPen(tint(bg, 1.5), 1));
            p->setBrush(tint(bg, 1.15));
            p->drawRoundedRect(bar, 3, 3);
            // filled part up to the knob
            QRectF fill = bar;
            const QPointF hc = QRectF(handle).center();
            const bool upside = sl->upsideDown;
            if (horiz) {
                if (!upside)
                    fill.setRight(hc.x());
                else
                    fill.setLeft(hc.x());
            } else {
                if (!upside)
                    fill.setTop(hc.y());
                else
                    fill.setBottom(hc.y());
            }
            const QColor fc = en ? kFill : tint(bg, 1.2);
            QLinearGradient g(fill.topLeft(), horiz ? fill.bottomLeft() : fill.topRight());
            g.setColorAt(0, tint(fc, 0.6));
            g.setColorAt(1, fc);
            p->setPen(QPen(tint(fc, 1.35), 1));
            p->setBrush(g);
            p->drawRoundedRect(fill, 3, 3);
        }

        if ((sl->subControls & SC_SliderTickmarks) && sl->tickPosition != QSlider::NoTicks) {
            p->setRenderHint(QPainter::Antialiasing, false);
            p->setPen(tint(bg, 1.5));
            int interval = sl->tickInterval;
            if (interval <= 0)
                interval = sl->singleStep > 0 ? sl->singleStep : 1;
            const int len = proxy()->pixelMetric(PM_SliderLength, sl, w);
            const int available = (horiz ? groove.width() : groove.height()) - len;
            const int range = sl->maximum - sl->minimum;
            if (range > 0 && range / interval < 200) {
                for (int v = sl->minimum; v <= sl->maximum; v += interval) {
                    const int pos = sliderPositionFromValue(sl->minimum, sl->maximum, v, available, sl->upsideDown) + len / 2;
                    if (horiz) {
                        const int x = groove.left() + pos;
                        if (sl->tickPosition & QSlider::TicksAbove)
                            p->drawLine(x, sl->rect.top(), x, sl->rect.top() + 3);
                        if (sl->tickPosition & QSlider::TicksBelow)
                            p->drawLine(x, sl->rect.bottom() - 3, x, sl->rect.bottom());
                    } else {
                        const int y = groove.top() + pos;
                        if (sl->tickPosition & QSlider::TicksAbove)
                            p->drawLine(sl->rect.left(), y, sl->rect.left() + 3, y);
                        if (sl->tickPosition & QSlider::TicksBelow)
                            p->drawLine(sl->rect.right() - 3, y, sl->rect.right(), y);
                    }
                }
            }
            p->setRenderHint(QPainter::Antialiasing, true);
        }

        if (sl->subControls & SC_SliderHandle) {
            const bool pressed = (sl->activeSubControls & SC_SliderHandle) && (sl->state & State_Sunken);
            const bool hov = (sl->activeSubControls & SC_SliderHandle) && isHover(sl);
            paintButton(p, handle, pal, en, pressed, hov, sl->state & State_HasFocus, false, 2);
            p->setRenderHint(QPainter::Antialiasing, false);
            const QPoint c = handle.center();
            p->setPen(tint(pal.color(QPalette::Button), 1.5));
            if (horiz)
                p->drawLine(c.x(), handle.top() + 4, c.x(), handle.bottom() - 4);
            else
                p->drawLine(handle.left() + 4, c.y(), handle.right() - 4, c.y());
            p->setPen(QColor(255, 255, 255));
            if (horiz)
                p->drawLine(c.x() + 1, handle.top() + 4, c.x() + 1, handle.bottom() - 4);
            else
                p->drawLine(handle.left() + 4, c.y() + 1, handle.right() - 4, c.y() + 1);
        }
        return;
    }

    case CC_ComboBox: {
        const auto *cb = qstyleoption_cast<const QStyleOptionComboBox *>(opt);
        if (!cb)
            break;
        const QRect arrow = proxy()->subControlRect(CC_ComboBox, cb, SC_ComboBoxArrow, w);
        const QColor ac = en ? pal.color(QPalette::ButtonText) : tint(pal.color(QPalette::Window), 1.35);
        if (cb->editable) {
            paintTextFrame(p, cb->rect, pal, en, cb->state & State_HasFocus, true);
            const bool pressed = (cb->activeSubControls & SC_ComboBoxArrow) && (cb->state & State_Sunken);
            paintButton(p, arrow.adjusted(0, 2, -2, -2), pal, en, pressed, isHover(cb), false, false, 2);
            paintArrow(p, arrow.adjusted(0, 2, -2, -2), Qt::DownArrow, ac);
        } else {
            const bool pressed = cb->state & State_On;
            paintButton(p, cb->rect, pal, en, pressed, isHover(cb), cb->state & State_HasFocus, false);
            // Haiku menu fields show a small popup triangle with a divider
            PainterSaver s(p);
            p->setPen(tint(pal.color(QPalette::Button), 1.3));
            const int x = (cb->direction == Qt::RightToLeft) ? arrow.right() + 1 : arrow.left() - 1;
            p->drawLine(x, cb->rect.top() + 4, x, cb->rect.bottom() - 4);
            p->setPen(QColor(255, 255, 255, 200));
            p->drawLine(x + 1, cb->rect.top() + 4, x + 1, cb->rect.bottom() - 4);
            paintArrow(p, arrow, Qt::DownArrow, ac);
        }
        return;
    }

    case CC_SpinBox: {
        const auto *sp = qstyleoption_cast<const QStyleOptionSpinBox *>(opt);
        if (!sp)
            break;
        if (sp->frame)
            paintTextFrame(p, sp->rect, pal, en, sp->state & State_HasFocus, true);
        else
            p->fillRect(sp->rect, pal.color(QPalette::Base));
        if (sp->buttonSymbols == QAbstractSpinBox::NoButtons)
            return;
        const QRect up = proxy()->subControlRect(CC_SpinBox, sp, SC_SpinBoxUp, w);
        const QRect dn = proxy()->subControlRect(CC_SpinBox, sp, SC_SpinBoxDown, w);
        const bool upEn = en && (sp->stepEnabled & QAbstractSpinBox::StepUpEnabled);
        const bool dnEn = en && (sp->stepEnabled & QAbstractSpinBox::StepDownEnabled);
        const bool upPressed = (sp->activeSubControls & SC_SpinBoxUp) && (sp->state & State_Sunken);
        const bool dnPressed = (sp->activeSubControls & SC_SpinBoxDown) && (sp->state & State_Sunken);
        const bool upHov = (sp->activeSubControls & SC_SpinBoxUp) && isHover(sp);
        const bool dnHov = (sp->activeSubControls & SC_SpinBoxDown) && isHover(sp);
        paintButton(p, up, pal, upEn, upPressed, upHov, false, false, 1.5);
        paintButton(p, dn, pal, dnEn, dnPressed, dnHov, false, false, 1.5);
        const QColor dis = tint(pal.color(QPalette::Window), 1.3);
        if (sp->buttonSymbols == QAbstractSpinBox::PlusMinus) {
            PainterSaver s(p);
            auto sign = [&](const QRect &r, bool plus, bool e) {
                p->setPen(QPen(e ? pal.color(QPalette::ButtonText) : dis, 1.5));
                const QPointF c = QRectF(r).center();
                p->drawLine(QPointF(c.x() - 3, c.y()), QPointF(c.x() + 3, c.y()));
                if (plus)
                    p->drawLine(QPointF(c.x(), c.y() - 3), QPointF(c.x(), c.y() + 3));
            };
            sign(up, true, upEn);
            sign(dn, false, dnEn);
        } else {
            paintArrow(p, up, Qt::UpArrow, upEn ? pal.color(QPalette::ButtonText) : dis);
            paintArrow(p, dn, Qt::DownArrow, dnEn ? pal.color(QPalette::ButtonText) : dis);
        }
        return;
    }

    default:
        break;
    }
    QProxyStyle::drawComplexControl(cc, opt, p, w);
}

QRect HaikuStyle::subControlRect(ComplexControl cc, const QStyleOptionComplex *opt, SubControl sc,
                                 const QWidget *w) const
{
    if (cc == CC_ScrollBar) {
        const auto *sb = qstyleoption_cast<const QStyleOptionSlider *>(opt);
        if (!sb)
            return QProxyStyle::subControlRect(cc, opt, sc, w);
        const QRect r = sb->rect;
        const bool horiz = sb->orientation == Qt::Horizontal;
        const int len = horiz ? r.width() : r.height();
        const int extent = horiz ? r.height() : r.width();
        const int bl = qMin(extent, len / 2);
        const int grooveStart = bl;
        const int grooveLen = qMax(0, len - 2 * bl);
        int sliderLen = grooveLen;
        if (sb->maximum > sb->minimum) {
            const qint64 range = qint64(sb->maximum) - sb->minimum;
            sliderLen = int(qint64(grooveLen) * sb->pageStep / (range + sb->pageStep));
            const int minLen = proxy()->pixelMetric(PM_ScrollBarSliderMin, sb, w);
            sliderLen = qBound(qMin(minLen, grooveLen), sliderLen, grooveLen);
        }
        const int sliderStart = grooveStart
            + sliderPositionFromValue(sb->minimum, sb->maximum, sb->sliderPosition, grooveLen - sliderLen, sb->upsideDown);
        int start = 0, length = 0;
        switch (sc) {
        case SC_ScrollBarSubLine: start = 0; length = bl; break;
        case SC_ScrollBarAddLine: start = len - bl; length = bl; break;
        case SC_ScrollBarSubPage: start = grooveStart; length = sliderStart - grooveStart; break;
        case SC_ScrollBarAddPage: start = sliderStart + sliderLen; length = grooveStart + grooveLen - start; break;
        case SC_ScrollBarSlider: start = sliderStart; length = sliderLen; break;
        case SC_ScrollBarGroove: start = grooveStart; length = grooveLen; break;
        default: return QProxyStyle::subControlRect(cc, opt, sc, w);
        }
        QRect res = horiz ? QRect(r.x() + start, r.y(), length, r.height())
                          : QRect(r.x(), r.y() + start, r.width(), length);
        return horiz ? visualRect(sb->direction, r, res) : res;
    }
    return QProxyStyle::subControlRect(cc, opt, sc, w);
}

int HaikuStyle::pixelMetric(PixelMetric pm, const QStyleOption *opt, const QWidget *w) const
{
    switch (pm) {
    case PM_ScrollBarExtent: return 17;
    case PM_ScrollBarSliderMin: return 28;
    case PM_IndicatorWidth:
    case PM_IndicatorHeight:
    case PM_ExclusiveIndicatorWidth:
    case PM_ExclusiveIndicatorHeight: return 14;
    case PM_DefaultFrameWidth:
    case PM_ComboBoxFrameWidth:
    case PM_SpinBoxFrameWidth: return 2;
    case PM_ButtonDefaultIndicator:
    case PM_ButtonShiftHorizontal:
    case PM_ButtonShiftVertical: return 0;
    case PM_SliderThickness: return 20;
    case PM_SliderControlThickness: return 18;
    case PM_SliderLength: return 14;
    case PM_SplitterWidth: return 6;
    case PM_MenuPanelWidth: return 2;
    case PM_MenuHMargin: return 0;
    case PM_MenuVMargin: return 2;
    case PM_MenuBarPanelWidth: return 0;
    case PM_MenuBarItemSpacing: return 0;
    case PM_MenuBarVMargin: return 1;
    case PM_MenuBarHMargin: return 2;
    case PM_ToolTipLabelFrameWidth: return 3;
    case PM_TabBarTabOverlap: return 0;
    case PM_TabBarBaseOverlap: return 1;
    case PM_TabBarTabShiftVertical:
    case PM_TabBarTabShiftHorizontal: return 0;
    default: break;
    }
    return QProxyStyle::pixelMetric(pm, opt, w);
}

int HaikuStyle::styleHint(StyleHint sh, const QStyleOption *opt, const QWidget *w, QStyleHintReturn *ret) const
{
    switch (sh) {
    case SH_ScrollBar_Transient: return false;
    case SH_ScrollBar_MiddleClickAbsolutePosition: return true;
    case SH_ScrollView_FrameOnlyAroundContents: return false;
    case SH_ComboBox_Popup: return true;
    case SH_EtchDisabledText:
    case SH_DitherDisabledText: return false;
    case SH_Menu_Scrollable: return true;
    case SH_MenuBar_MouseTracking:
    case SH_Menu_MouseTracking: return true;
    case SH_TabBar_Alignment: return Qt::AlignLeft;
    case SH_FocusFrame_AboveWidget: return false;
    default: break;
    }
    return QProxyStyle::styleHint(sh, opt, w, ret);
}

QPalette HaikuStyle::standardPalette() const
{
    QPalette pal;
    const QColor panel(216, 216, 216);
    pal.setColor(QPalette::Window, panel);
    pal.setColor(QPalette::WindowText, Qt::black);
    pal.setColor(QPalette::Base, Qt::white);
    pal.setColor(QPalette::AlternateBase, QColor(244, 244, 244));
    pal.setColor(QPalette::Text, Qt::black);
    pal.setColor(QPalette::Button, QColor(232, 232, 232));
    pal.setColor(QPalette::ButtonText, Qt::black);
    pal.setColor(QPalette::BrightText, Qt::white);
    pal.setColor(QPalette::Highlight, QColor(115, 120, 184));
    pal.setColor(QPalette::HighlightedText, Qt::white);
    pal.setColor(QPalette::ToolTipBase, QColor(255, 255, 216));
    pal.setColor(QPalette::ToolTipText, Qt::black);
    pal.setColor(QPalette::Link, kNavigation);
    pal.setColor(QPalette::Light, Qt::white);
    pal.setColor(QPalette::Midlight, QColor(232, 232, 232));
    pal.setColor(QPalette::Mid, QColor(184, 184, 184));
    pal.setColor(QPalette::Dark, QColor(152, 152, 152));
    pal.setColor(QPalette::Shadow, QColor(96, 96, 96));
    pal.setColor(QPalette::PlaceholderText, QColor(128, 128, 128));
    for (auto role : {QPalette::WindowText, QPalette::Text, QPalette::ButtonText})
        pal.setColor(QPalette::Disabled, role, QColor(150, 150, 150));
    pal.setColor(QPalette::Disabled, QPalette::Base, QColor(236, 236, 236));
    return pal;
}

static const char *kLightPaletteProp = "_haiku_light_statusbar";

void HaikuStyle::polish(QWidget *w)
{
    QProxyStyle::polish(w);
    // Dolphin's small status bar overlay: its contents live in a QScrollArea
    // that fills itself with the window colour, so the lighter background has
    // to come from the palette (inherited by all child widgets).
    if (w->inherits("DolphinStatusBar")) {
        // transparent: Dolphin and its child widgets fill with this colour;
        // the visible (lighter, inset) box is painted in PE_Frame.
        QPalette pal = w->palette();
        for (auto g : {QPalette::Active, QPalette::Inactive, QPalette::Disabled})
            pal.setColor(g, QPalette::Window, Qt::transparent);
        w->setPalette(pal);
        w->setProperty(kLightPaletteProp, true);
    }
    if (qobject_cast<QAbstractButton *>(w) || qobject_cast<QComboBox *>(w) || qobject_cast<QScrollBar *>(w)
        || qobject_cast<QSlider *>(w) || qobject_cast<QAbstractSpinBox *>(w) || qobject_cast<QTabBar *>(w)
        || qobject_cast<QHeaderView *>(w)) {
        w->setAttribute(Qt::WA_Hover, true);
    }
}

void HaikuStyle::unpolish(QWidget *w)
{
    if (w->property(kLightPaletteProp).toBool()) {
        w->setPalette(QPalette());
        w->setProperty(kLightPaletteProp, QVariant());
    }
    QProxyStyle::unpolish(w);
}
