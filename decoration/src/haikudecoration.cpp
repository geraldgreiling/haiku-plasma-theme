// SPDX-License-Identifier: MIT
// Haiku/BeOS style window decoration for KWin (KDecoration3, Plasma >= 6.3).
//
// The title "tab" is only as wide as the buttons plus the caption, exactly
// like Haiku's default decorator. The area to the right of the tab stays
// transparent.

#include "haikudecoration.h"
#include "haikupainter.h"

#include <KDecoration3/DecorationSettings>
#include <KPluginFactory>

#include <QFontMetricsF>
#include <QPainter>
#include <QSettings>
#include <QStandardPaths>
#include <QTimer>

K_PLUGIN_FACTORY_WITH_JSON(HaikuDecorationFactory, "haiku.json", registerPlugin<Haiku::Decoration>();
                           registerPlugin<Haiku::Button>();)

namespace Haiku
{
using KDecoration3::ColorGroup;
using KDecoration3::ColorRole;
using KDecoration3::DecorationButtonType;

static constexpr qreal kPad = 5;  // space between tab edge and buttons
static constexpr qreal kGap = 7;  // space between buttons and caption

Decoration::Decoration(QObject *parent, const QVariantList &args)
    : KDecoration3::Decoration(parent, args)
{
}

Decoration::~Decoration() = default;

QFont Decoration::titleFont() const
{
    QFont f = settings()->font();
    f.setBold(true);
    return f;
}

qreal Decoration::tabHeight() const
{
    return qRound(QFontMetricsF(titleFont()).height()) + 8;
}

qreal Decoration::buttonSize() const
{
    return qRound(tabHeight() * 0.62);
}

qreal Decoration::borderWidth() const
{
    using KDecoration3::BorderSize;
    switch (settings()->borderSize()) {
    case BorderSize::None:
    case BorderSize::NoSides: return 0;
    case BorderSize::Tiny: return 3;
    case BorderSize::Normal: return 5;
    case BorderSize::Large: return 7;
    case BorderSize::VeryLarge: return 9;
    case BorderSize::Huge: return 11;
    case BorderSize::VeryHuge: return 13;
    case BorderSize::Oversized: return 17;
    }
    return 5;
}

// KWin ignores the colour scheme's [WM] section as soon as the scheme defines a
// [Colors:Header] set and then returns the (grey) header background for both
// TitleBar and Frame. Haiku's tab is always yellow, so the decoration uses its
// own colours. They can be changed in ~/.config/haikudecorationrc:
//
//   [Colors]
//   ActiveTab=255,203,0      InactiveTab=232,232,232
//   ActiveFrame=224,224,224  InactiveFrame=232,232,232
//   ActiveText=0,0,0         InactiveText=80,80,80
//   UseColorScheme=false     (true = take the colours from KWin's palette)
static QColor readColor(const QSettings &cfg, const QString &key, const QColor &def)
{
    const QVariant v = cfg.value(key);
    if (!v.isValid())
        return def;
    QStringList parts = v.toStringList();
    if (parts.size() == 1)
        parts = parts.first().split(QLatin1Char(','));
    if (parts.size() < 3) {
        const QColor named(parts.value(0).trimmed());
        return named.isValid() ? named : def;
    }
    return QColor(parts[0].trimmed().toInt(), parts[1].trimmed().toInt(), parts[2].trimmed().toInt());
}

void Decoration::loadColors()
{
    const QString path = QStandardPaths::writableLocation(QStandardPaths::GenericConfigLocation)
        + QStringLiteral("/haikudecorationrc");
    QSettings cfg(path, QSettings::IniFormat);
    cfg.beginGroup(QStringLiteral("Colors"));
    m_useColorScheme = cfg.value(QStringLiteral("UseColorScheme"), false).toBool();
    m_activeTab = readColor(cfg, QStringLiteral("ActiveTab"), QColor(255, 203, 0));
    m_inactiveTab = readColor(cfg, QStringLiteral("InactiveTab"), QColor(232, 232, 232));
    m_activeFrame = readColor(cfg, QStringLiteral("ActiveFrame"), QColor(224, 224, 224));
    m_inactiveFrame = readColor(cfg, QStringLiteral("InactiveFrame"), QColor(232, 232, 232));
    m_activeText = readColor(cfg, QStringLiteral("ActiveText"), QColor(0, 0, 0));
    m_inactiveText = readColor(cfg, QStringLiteral("InactiveText"), QColor(80, 80, 80));
}

QColor Decoration::tabColor() const
{
    const auto w = window();
    if (m_useColorScheme)
        return w->color(w->isActive() ? ColorGroup::Active : ColorGroup::Inactive, ColorRole::TitleBar);
    return w->isActive() ? m_activeTab : m_inactiveTab;
}

QColor Decoration::frameColor() const
{
    const auto w = window();
    if (m_useColorScheme)
        return w->color(w->isActive() ? ColorGroup::Active : ColorGroup::Inactive, ColorRole::Frame);
    return w->isActive() ? m_activeFrame : m_inactiveFrame;
}

QColor Decoration::textColor() const
{
    const auto w = window();
    if (m_useColorScheme)
        return w->color(w->isActive() ? ColorGroup::Active : ColorGroup::Inactive, ColorRole::Foreground);
    return w->isActive() ? m_activeText : m_inactiveText;
}

bool Decoration::init()
{
    setOpaque(false);
    loadColors();

    m_leftButtons = new KDecoration3::DecorationButtonGroup(KDecoration3::DecorationButtonGroup::Position::Left, this,
                                                            &Button::create);
    m_rightButtons = new KDecoration3::DecorationButtonGroup(KDecoration3::DecorationButtonGroup::Position::Right, this,
                                                             &Button::create);

    auto s = settings();
    auto delayed = [this]() { QTimer::singleShot(0, this, &Decoration::updateLayout); };
    connect(s.get(), &KDecoration3::DecorationSettings::reconfigured, this, [this]() {
        loadColors();
        update();
    });
    connect(s.get(), &KDecoration3::DecorationSettings::borderSizeChanged, this, &Decoration::updateLayout);
    connect(s.get(), &KDecoration3::DecorationSettings::fontChanged, this, &Decoration::updateLayout);
    connect(s.get(), &KDecoration3::DecorationSettings::reconfigured, this, delayed);
    connect(s.get(), &KDecoration3::DecorationSettings::decorationButtonsLeftChanged, this, delayed);
    connect(s.get(), &KDecoration3::DecorationSettings::decorationButtonsRightChanged, this, delayed);

    const auto w = window();
    connect(w, &KDecoration3::DecoratedWindow::captionChanged, this, &Decoration::updateLayout);
    connect(w, &KDecoration3::DecoratedWindow::widthChanged, this, &Decoration::updateLayout);
    connect(w, &KDecoration3::DecoratedWindow::maximizedChanged, this, &Decoration::updateLayout);
    connect(w, &KDecoration3::DecoratedWindow::shadedChanged, this, &Decoration::updateLayout);
    connect(w, &KDecoration3::DecoratedWindow::activeChanged, this, [this]() { update(); });
    connect(w, &KDecoration3::DecoratedWindow::paletteChanged, this, [this]() { update(); });

    updateLayout();
    return true;
}

void Decoration::updateLayout()
{
    if (!m_leftButtons || !m_rightButtons)
        return;
    const auto w = window();
    const bool maximized = w->isMaximized();
    const qreal B = maximized ? 0 : borderWidth();
    const qreal T = tabHeight();
    const qreal bs = buttonSize();

    setBorders(QMarginsF(B, T + B, B, B));
    const qreal extra = maximized ? 0 : qMax<qreal>(0, 4 - B);
    setResizeOnlyBorders(QMarginsF(extra, 0, extra, extra));

    for (auto *b : m_leftButtons->buttons())
        b->setGeometry(QRectF(QPointF(0, 0), QSizeF(bs, bs)));
    for (auto *b : m_rightButtons->buttons())
        b->setGeometry(QRectF(QPointF(0, 0), QSizeF(bs, bs)));
    m_leftButtons->setSpacing(4);
    m_rightButtons->setSpacing(4);

    const qreal leftW = m_leftButtons->geometry().width();
    const qreal rightW = m_rightButtons->geometry().width();
    const QFontMetricsF fm(titleFont());
    const qreal captionW = fm.horizontalAdvance(w->caption()) + 2;

    const qreal outerW = w->width() + 2 * B;
    const qreal minW = qMin(outerW, kPad * 2 + leftW + rightW + (leftW > 0 ? kGap : 0) + (rightW > 0 ? kGap : 0) + 24);
    const qreal wanted = kPad + leftW + (leftW > 0 ? kGap : 0) + captionW + (rightW > 0 ? kGap : 0) + rightW + kPad;
    m_tabWidth = qBound(minW, wanted, outerW);

    setTitleBar(QRectF(0, 0, m_tabWidth, T));
    m_leftButtons->setPos(QPointF(kPad, qRound((T - bs) / 2)));
    m_rightButtons->setPos(QPointF(m_tabWidth - kPad - rightW, qRound((T - bs) / 2)));

    const qreal tl = kPad + leftW + (leftW > 0 ? kGap : 0);
    const qreal tr = m_tabWidth - kPad - rightW - (rightW > 0 ? kGap : 0);
    m_titleRect = QRectF(tl, 0, qMax<qreal>(0, tr - tl), T);
    update();
}

void Decoration::paint(QPainter *painter, const QRectF &repaintRegion)
{
    const auto w = window();
    const bool active = w->isActive();
    const qreal T = tabHeight();
    const qreal B = borderLeft();
    const QRectF all = rect();

    painter->save();
    if (!w->isShaded() || B > 0) {
        const QRectF frameRect(all.left(), all.top() + T, all.width(), all.height() - T);
        HaikuDeco::paintFrame(painter, frameRect, B, frameColor(), active);
    }
    HaikuDeco::paintTab(painter, QRectF(0, 0, m_tabWidth, T), tabColor(), active);
    HaikuDeco::paintTitle(painter, m_titleRect, w->caption(), titleFont(), textColor());
    painter->restore();

    m_leftButtons->paint(painter, repaintRegion);
    m_rightButtons->paint(painter, repaintRegion);
}

// ---------------------------------------------------------------------------

Button::Button(KDecoration3::DecorationButtonType type, Decoration *decoration, QObject *parent)
    : KDecoration3::DecorationButton(type, decoration, parent)
{
    const qreal bs = decoration->buttonSize();
    setGeometry(QRectF(QPointF(0, 0), QSizeF(bs, bs)));
}

Button::Button(QObject *parent, const QVariantList &args)
    : Button(args.at(0).value<DecorationButtonType>(), args.at(1).value<Decoration *>(), parent)
{
}

KDecoration3::DecorationButton *Button::create(DecorationButtonType type, KDecoration3::Decoration *decoration,
                                               QObject *parent)
{
    auto *d = qobject_cast<Decoration *>(decoration);
    if (!d)
        return nullptr;
    auto *b = new Button(type, d, parent);
    const auto w = d->window();
    switch (type) {
    case DecorationButtonType::Close:
        b->setVisible(w->isCloseable());
        QObject::connect(w, &KDecoration3::DecoratedWindow::closeableChanged, b, &Button::setVisible);
        break;
    case DecorationButtonType::Maximize:
        b->setVisible(w->isMaximizeable());
        QObject::connect(w, &KDecoration3::DecoratedWindow::maximizeableChanged, b, &Button::setVisible);
        break;
    case DecorationButtonType::Minimize:
        b->setVisible(w->isMinimizeable());
        QObject::connect(w, &KDecoration3::DecoratedWindow::minimizeableChanged, b, &Button::setVisible);
        break;
    case DecorationButtonType::ContextHelp:
        b->setVisible(w->providesContextHelp());
        QObject::connect(w, &KDecoration3::DecoratedWindow::providesContextHelpChanged, b, &Button::setVisible);
        break;
    case DecorationButtonType::Shade:
        b->setVisible(w->isShadeable());
        QObject::connect(w, &KDecoration3::DecoratedWindow::shadeableChanged, b, &Button::setVisible);
        break;
    case DecorationButtonType::Menu:
        QObject::connect(w, &KDecoration3::DecoratedWindow::iconChanged, b, [b]() { b->update(); });
        break;
    default:
        break;
    }
    return b;
}

void Button::paint(QPainter *painter, const QRectF &repaintRegion)
{
    Q_UNUSED(repaintRegion)
    auto *d = qobject_cast<Decoration *>(decoration());
    if (!d || !isVisible())
        return;
    using HaikuDeco::Glyph;
    Glyph g = Glyph::Generic;
    switch (type()) {
    case DecorationButtonType::Close: g = Glyph::Close; break;
    case DecorationButtonType::Maximize: g = Glyph::Zoom; break;
    case DecorationButtonType::Minimize: g = Glyph::Minimize; break;
    case DecorationButtonType::Menu: g = Glyph::Menu; break;
    case DecorationButtonType::OnAllDesktops: g = Glyph::OnAllDesktops; break;
    case DecorationButtonType::KeepAbove: g = Glyph::KeepAbove; break;
    case DecorationButtonType::KeepBelow: g = Glyph::KeepBelow; break;
    case DecorationButtonType::Shade: g = Glyph::Shade; break;
    case DecorationButtonType::ContextHelp: g = Glyph::ContextHelp; break;
    case DecorationButtonType::Spacer: return;
    default: break;
    }
    const QRectF r = geometry();
    if (g == Glyph::Menu) {
        d->window()->icon().paint(painter, r.toRect());
        return;
    }
    HaikuDeco::paintButton(painter, r, d->tabColor(), g, isPressed(), isHovered(), isChecked(), d->window()->isActive());
}
}

#include "haikudecoration.moc"
