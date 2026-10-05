// SPDX-License-Identifier: MIT
#pragma once

#include <KDecoration3/DecoratedWindow>
#include <KDecoration3/Decoration>
#include <KDecoration3/DecorationButton>
#include <KDecoration3/DecorationButtonGroup>

#include <QColor>
#include <QVariant>

namespace Haiku
{
class Decoration : public KDecoration3::Decoration
{
    Q_OBJECT
public:
    explicit Decoration(QObject *parent = nullptr, const QVariantList &args = QVariantList());
    ~Decoration() override;

    bool init() override;
    void paint(QPainter *painter, const QRectF &repaintRegion) override;

    qreal tabHeight() const;
    qreal borderWidth() const;
    qreal buttonSize() const;
    QFont titleFont() const;
    QColor tabColor() const;
    QColor frameColor() const;
    QColor textColor() const;

private Q_SLOTS:
    void updateLayout();

private:
    void loadColors();
    bool m_useColorScheme = false;
    QColor m_activeTab, m_inactiveTab, m_activeFrame, m_inactiveFrame, m_activeText, m_inactiveText;
    KDecoration3::DecorationButtonGroup *m_leftButtons = nullptr;
    KDecoration3::DecorationButtonGroup *m_rightButtons = nullptr;
    qreal m_tabWidth = 0;
    QRectF m_titleRect;
};

class Button : public KDecoration3::DecorationButton
{
    Q_OBJECT
public:
    explicit Button(QObject *parent, const QVariantList &args);
    Button(KDecoration3::DecorationButtonType type, Decoration *decoration, QObject *parent = nullptr);
    static KDecoration3::DecorationButton *create(KDecoration3::DecorationButtonType type,
                                                  KDecoration3::Decoration *decoration, QObject *parent);
    void paint(QPainter *painter, const QRectF &repaintRegion) override;
};
}
