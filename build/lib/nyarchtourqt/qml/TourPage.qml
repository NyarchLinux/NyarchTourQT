// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 Nyarch Linux

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ScrollablePage {
    id: tourPage

    property string pageTitle: ""
    property string pageIcon: ""
    property string pageBody: ""
    property var pageButtons: []

    title: pageTitle

    ColumnLayout {
        anchors.centerIn: parent
        width: Math.min(parent.width - Kirigami.Units.gridUnit * 2, Kirigami.Units.gridUnit * 36)

        spacing: Kirigami.Units.gridUnit

        // Page content
        ColumnLayout {
            Layout.fillWidth: true
            spacing: Kirigami.Units.gridUnit

            // Screenshot image
            Image {
                id: screenshotImage
                source: picturesPath + "/" + pageIcon + ".png"
                Layout.preferredWidth: Kirigami.Units.gridUnit * 26
                Layout.preferredHeight: Kirigami.Units.gridUnit * 16
                Layout.alignment: Qt.AlignHCenter
                fillMode: Image.PreserveAspectFit
                mipmap: true
                smooth: true
                sourceSize.width: 1200
                sourceSize.height: 740

                // Error handling - show placeholder if image not found
                onStatusChanged: {
                    if (status === Image.Error) {
                        console.log("Failed to load image: " + source)
                    }
                }
            }

            // Title
            Kirigami.Heading {
                text: pageTitle
                level: 1
                Layout.alignment: Qt.AlignHCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                Layout.maximumWidth: Kirigami.Units.gridUnit * 32
            }

            // Description
            Controls.Label {
                text: pageBody
                Layout.alignment: Qt.AlignHCenter
                horizontalAlignment: Text.AlignHCenter
                wrapMode: Text.WordWrap
                Layout.maximumWidth: Kirigami.Units.gridUnit * 32
                opacity: 0.8
                font.pointSize: Kirigami.Theme.defaultFont.pointSize + 1
            }

            // Buttons row
            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                Layout.topMargin: Kirigami.Units.gridUnit
                spacing: Kirigami.Units.largeSpacing
                visible: pageButtons.length > 0

                Repeater {
                    model: pageButtons

                    delegate: Controls.Button {
                        text: modelData.label
                        icon.name: modelData.icon || ""

                        // Apply style based on button configuration
                        highlighted: modelData.style === "suggested-action"
                        font.pointSize: Kirigami.Theme.defaultFont.pointSize + 1

                        onClicked: {
                            utils.run_command(modelData.command)
                        }
                    }
                }
            }
        }
    }
}
