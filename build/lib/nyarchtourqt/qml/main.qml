// SPDX-License-Identifier: GPL-3.0-or-later
// SPDX-FileCopyrightText: 2024 Nyarch Linux

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as Controls
import org.kde.kirigami as Kirigami

Kirigami.ApplicationWindow {
    id: root

    title: qsTr("Nyarch Tour")

    minimumWidth: Kirigami.Units.gridUnit * 30
    minimumHeight: Kirigami.Units.gridUnit * 35
    width: Kirigami.Units.gridUnit * 35
    height: Kirigami.Units.gridUnit * 40

    // Track current page for exit confirmation
    property int currentPageIndex: 0
    property bool quitConfirmed: false

    // Custom header
    header: Controls.ToolBar {
        id: toolbar

        RowLayout {
            anchors.fill: parent
            spacing: Kirigami.Units.smallSpacing

            // Previous button
            Controls.ToolButton {
                id: prevButton
                icon.name: "go-previous"
                enabled: swipeView.currentIndex > 0
                opacity: enabled ? 1.0 : 0.3
                onClicked: swipeView.currentIndex--

                Controls.ToolTip.visible: hovered
                Controls.ToolTip.text: qsTr("Previous")
            }

            Item { Layout.fillWidth: true }

            // Page indicator
            Controls.PageIndicator {
                id: pageIndicator
                count: swipeView.count
                currentIndex: swipeView.currentIndex
                interactive: true
                onCurrentIndexChanged: {
                    if (currentIndex !== swipeView.currentIndex) {
                        swipeView.currentIndex = currentIndex
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // Next button
            Controls.ToolButton {
                id: nextButton
                icon.name: "go-next"
                enabled: swipeView.currentIndex < swipeView.count - 1
                opacity: enabled ? 1.0 : 0.3
                onClicked: swipeView.currentIndex++

                Controls.ToolTip.visible: hovered
                Controls.ToolTip.text: qsTr("Next")
            }

            // Menu button
            Controls.ToolButton {
                icon.name: "application-menu"
                onClicked: optionMenu.popup()

                Controls.Menu {
                    id: optionMenu

                    Controls.MenuItem {
                        text: qsTr("About Nyarch Tour")
                        icon.name: "help-about"
                        onTriggered: aboutDialog.open()
                    }

                    Controls.MenuItem {
                        text: qsTr("Quit")
                        icon.name: "application-exit"
                        onTriggered: confirmQuit()
                    }
                }
            }
        }
    }

    // Main content - SwipeView for carousel navigation
    Controls.SwipeView {
        id: swipeView
        anchors.fill: parent
        clip: true

        onCurrentIndexChanged: {
            root.currentPageIndex = currentIndex
        }

        Repeater {
            model: pagesModel

            Loader {
                active: Controls.SwipeView.isCurrentItem || Controls.SwipeView.isNextItem || Controls.SwipeView.isPreviousItem

                sourceComponent: TourPage {
                    pageTitle: model.title
                    pageIcon: model.icon
                    pageBody: model.body
                    pageButtons: model.buttons
                }
            }
        }
    }

    // Exit confirmation dialog
    Kirigami.Dialog {
        id: exitDialog
        title: qsTr("Confirm Exit")
        standardButtons: Kirigami.Dialog.NoButton

        ColumnLayout {
            spacing: Kirigami.Units.largeSpacing
            Layout.preferredWidth: Kirigami.Units.gridUnit * 25

            Controls.Label {
                text: qsTr("Nyarch Tour will guide you through all the Nyarch Linux features.\nAre you sure you want to exit?")
                wrapMode: Text.WordWrap
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
            }

            RowLayout {
                Layout.alignment: Qt.AlignHCenter
                spacing: Kirigami.Units.largeSpacing

                Controls.Button {
                    text: qsTr("Cancel")
                    onClicked: exitDialog.close()
                }

                Controls.Button {
                    text: qsTr("Exit")
                    icon.name: "application-exit"
                    onClicked: requestQuit()
                }
            }
        }
    }

    // About Dialog
    Kirigami.Dialog {
        id: aboutDialog
        title: qsTr("About Nyarch Tour")
        standardButtons: Kirigami.Dialog.Close
        preferredWidth: Kirigami.Units.gridUnit * 20

        ColumnLayout {
            spacing: Kirigami.Units.largeSpacing

            Kirigami.Heading {
                text: qsTr("Nyarch Tour")
                level: 1
                Layout.alignment: Qt.AlignHCenter
            }

            Controls.Label {
                text: qsTr("Version 0.1.0")
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.7
            }

            Controls.Label {
                text: qsTr("A tour application for Nyarch Linux to help you discover all the features.")
                wrapMode: Text.WordWrap
                horizontalAlignment: Text.AlignHCenter
                Layout.fillWidth: true
            }

            Controls.Label {
                text: qsTr("Built with Kirigami for KDE Plasma")
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.7
            }

            Controls.Label {
                text: "© 2024 Nyarch Linux"
                Layout.alignment: Qt.AlignHCenter
                opacity: 0.5
            }
        }
    }

    // Keyboard navigation
    Shortcut {
        sequence: "Left"
        onActivated: if (swipeView.currentIndex > 0) swipeView.currentIndex--
    }

    Shortcut {
        sequence: "Right"
        onActivated: if (swipeView.currentIndex < swipeView.count - 1) swipeView.currentIndex++
    }

    Shortcut {
        sequence: StandardKey.Quit
        onActivated: confirmQuit()
    }

    // Confirm quit function
    function confirmQuit() {
        // Only show confirmation if on page 8 or earlier (index 7 or less)
        if (currentPageIndex <= 7) {
            exitDialog.open()
        } else {
            requestQuit()
        }
    }

    function requestQuit() {
        quitConfirmed = true
        Qt.quit()
    }

    // Handle window close request
    onClosing: function(closeEvent) {
        if (quitConfirmed) {
            closeEvent.accepted = true
            return
        }

        if (currentPageIndex <= 7) {
            closeEvent.accepted = false
            exitDialog.open()
        }
    }
}
