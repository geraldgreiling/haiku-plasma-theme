// SPDX-License-Identifier: MIT
#include "haikustyle.h"
#include <QStylePlugin>

class HaikuStylePlugin : public QStylePlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID QStyleFactoryInterface_iid FILE "haiku.json")
public:
    QStyle *create(const QString &key) override
    {
        if (key.compare(QLatin1String("haiku"), Qt::CaseInsensitive) == 0)
            return new HaikuStyle;
        return nullptr;
    }
};

#include "haikustyleplugin.moc"
