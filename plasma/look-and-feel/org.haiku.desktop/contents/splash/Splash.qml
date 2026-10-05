// SPDX-License-Identifier: MIT
// Haiku-style boot splash: a row of icons that light up one after another.
import QtQuick
import org.kde.kirigami as Kirigami

Rectangle {
    id: root
    color: "#336698"          // Haiku desktop blue
    property int stage        // set by ksplashqml (1 … 6)

    readonly property real iconSize: Kirigami.Units.gridUnit * 3
    readonly property int count: 7

    onStageChanged: {
        if (stage === 1)
            fadeIn.start()
        if (stage === 6)
            fadeOut.start()
    }

    Rectangle {
        id: box
        anchors.centerIn: parent
        width: row.width + Kirigami.Units.gridUnit * 2
        height: row.height + Kirigami.Units.gridUnit * 2
        color: "#d8d8d8"
        border.color: "#7b7b7b"
        border.width: 1
        opacity: 0

        // bevel
        Rectangle { x: 1; y: 1; width: parent.width - 2; height: 1; color: "white" }
        Rectangle { x: 1; y: 1; width: 1; height: parent.height - 2; color: "white" }
        Rectangle { x: 1; y: parent.height - 2; width: parent.width - 2; height: 1; color: "#b8b8b8" }
        Rectangle { x: parent.width - 2; y: 1; width: 1; height: parent.height - 2; color: "#b8b8b8" }

        Row {
            id: row
            anchors.centerIn: parent
            spacing: Kirigami.Units.gridUnit
            Repeater {
                model: root.count
                Image {
                    source: "images/stage" + (index + 1) + ".png"
                    width: root.iconSize
                    height: root.iconSize
                    sourceSize.width: 128
                    sourceSize.height: 128
                    smooth: true
                    // ksplash reports stages 1..6; the last icon lights at stage 6
                    readonly property bool lit: root.stage >= Math.min(index + 1, 6) && (index < 6 || root.stage >= 6)
                    opacity: lit ? 1.0 : 0.18
                    Behavior on opacity { NumberAnimation { duration: 250 } }
                }
            }
        }
    }

    NumberAnimation { id: fadeIn; target: box; property: "opacity"; from: 0; to: 1; duration: 300 }
    NumberAnimation { id: fadeOut; target: box; property: "opacity"; to: 0; duration: 600; easing.type: Easing.InQuad }
}
