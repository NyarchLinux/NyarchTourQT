#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Nyarch Linux

"""Pages data model for QML consumption"""

from PySide6.QtCore import QAbstractListModel, Qt, QModelIndex, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "moe.nyarchlinux.tourqt"
QML_IMPORT_MAJOR_VERSION = 1


# Button structure:
# {
#     "label": "Button text",
#     "icon": None or "icon-name",
#     "style": None or "suggested-action",
#     "command": "command to run"
# }

# Page structure:
# {
#     "icon": "screenshot-filename",
#     "title": "Page Title",
#     "body": "Description text",
#     "condition": function returning bool (optional),
#     "buttons": [list of buttons]
# }

# Raw pages data - will be filtered based on conditions
_RAW_PAGES = [
    {
        "icon": "nyarch-logo",
        "title": "Welcome to Nyarch Plasma",
        "body": "Nyarch Linux is an Arch Linux-based OS that aims to create the best possible experience for weebs.",
        "buttons": [
            {
                "label": "Open Website",
                "icon": None,
                "style": "suggested-action",
                "command": "xdg-open https://nyarchlinux.moe"
            }
        ]
    },
    {
        "icon": "material_you_screenshot",
        "title": "Material You",
        "body": "Choose any waifu as your wallpaper! The desktop and application themes automatically adjust their colors to make you feel at home. This is achieved by a modified version of the Material You Gnome extension.",
        "buttons": [
            {
                "label": "Open Settings",
                "icon": None,
                "style": "suggested-action",
                "command": "systemsettings kcm_wallpaper"
            }
        ]
    },
    {
        "icon": "catgirldownloader-screenshots",
        "title": "Catgirl Downloader",
        "body": "This application satisfies one of the most important needs a weeb has: getting random pictures of cute cat girls whenever you want!",
        "buttons": [
            {
                "label": "Open Catgirl Downloader",
                "icon": None,
                "style": "suggested-action",
                "command": "catgirldownloaderqt"
            }
        ]
    },
    {
        "icon": "komikku-screenshots",
        "title": "Read manga with Komikku",
        "body": "Komikku is an amazing open source application for reading manga from the internet.",
        "buttons": [
            {
                "label": "Project page",
                "icon": None,
                "style": None,
                "command": "xdg-open https://valos.gitlab.io/Komikku/"
            },
            {
                "label": "Open Komikku",
                "icon": None,
                "style": "suggested-action",
                "command": "komikku"
            }
        ]
    },
    {
        "icon": "software-screenshots",
        "title": "Need other apps?",
        "body": "Download your favorite applications from an extensive catalog of applications with Discover.",
        "buttons": [
            {
                "label": "Open Discover",
                "icon": None,
                "style": "suggested-action",
                "command": "plasma-discover"
            }
        ]
    },
    {
        "icon": "nyarchwizard-screenshots",
        "title": "Need suggestions?",
        "body": "Nyarch Wizard will suggest some software to get you started with Nyarch Linux.",
        "buttons": [
            {
                "label": "Open Nyarch Wizard",
                "icon": None,
                "style": "suggested-action",
                "command": "nyarchwizardqt"
            }
        ]
    },
    {
        "icon": "terminal-screenshots",
        "title": "I use Nyarch, btw",
        "body": "We have included nyaofetch to let everyone know that you are using Nyarch Linux, and nyay to download packages from the Arch User Repository and Arch Linux repositories.",
        "buttons": [
            {
                "label": "Run in terminal",
                "icon": None,
                "style": "suggested-action",
                "command": "konsole -e nekofetch"
            }
        ]
    },
    {
        "icon": "nyarchscripts-screenshots",
        "title": "Check out Nyarch Scripts",
        "body": "Nyarch Scripts offers some interesting and common terminal commands and scripts that can be executed with one click.",
        "buttons": [
            {
                "label": "Run Nyarch Scripts",
                "icon": None,
                "style": "suggested-action",
                "command": "nyarchscriptqt"
            }
        ]
    },
    {
        "icon": "nyarchupdater-screenshots",
        "title": "Keep your system up to date",
        "body": "Nyarch Updater helps you to keep your system up to date and install Nyarch Linux updates.",
        "buttons": [
            {
                "label": "Run Nyarch Updater",
                "icon": None,
                "style": "suggested-action",
                "command": "nyarchupdaterqt"
            }
        ]
    },
    {
        "icon": "nyarchassistant-screenshots",
        "title": "Your dream waifu at your command",
        "body": "The Nyarch Assistant is a powerful AI assistant that can help you with your system, roleplay and much more thanks to extensions and customizations.",
        "buttons": [
            {
                "label": "Run Nyarch Assistant",
                "icon": None,
                "style": "suggested-action",
                "command": "nyarchassistant"
            }
        ]
    },
    {
        "icon": "timeshift-screenshots",
        "title": "Take a Time Leap",
        "body": "With timeshift you can create snapshots (backups) of your system instantly and restore them in milliseconds.",
        "buttons": [
            {
                "label": "Open Timeshift",
                "icon": None,
                "style": "suggested-action",
                "command": "pkexec timeshift-gtk"
            }
        ]
    },
    {
        "icon": "gnome-screenshot",
        "title": "Discover more about your desktop",
        "body": "Run Plasma Welcome to learn more about desktop customization",
        "buttons": [
            {
                "label": "Start Tour",
                "icon": None,
                "style": "suggested-action",
                "command": "plasma-welcome"
            }
        ]
    },
]


def _check_btrfs():
    """Check if root filesystem is BTRFS"""
    import subprocess
    try:
        script = """if [ "$(findmnt -n -o FSTYPE /)" == "btrfs" ]; then
          echo 1
        else
          echo 0
        fi
        """
        result = subprocess.check_output(
            ["flatpak-spawn", "--host", "bash", "-c", script]
        ).decode("utf-8").strip()
        return result == "1"
    except Exception:
        return False


def _filter_pages():
    """Filter pages based on conditions"""
    filtered = []
    for page in _RAW_PAGES:
        # Timeshift page (index 17) only shown on BTRFS
        if page["icon"] == "timeshift-screenshots" and not _check_btrfs():
            continue
        filtered.append(page)
    return filtered


@QmlElement
class PagesModel(QAbstractListModel):
    """Model exposing page data to QML"""

    # Define roles
    TitleRole = Qt.UserRole + 1
    BodyRole = Qt.UserRole + 2
    IconRole = Qt.UserRole + 3
    ButtonsRole = Qt.UserRole + 4

    def __init__(self, parent=None):
        super().__init__(parent)
        self._pages = _filter_pages()

    def rowCount(self, parent=QModelIndex()):
        return len(self._pages)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or index.row() >= len(self._pages):
            return None

        page = self._pages[index.row()]

        if role == self.TitleRole:
            return page.get("title", "")
        elif role == self.BodyRole:
            return page.get("body", "")
        elif role == self.IconRole:
            return page.get("icon", "")
        elif role == self.ButtonsRole:
            return page.get("buttons", [])

        return None

    def roleNames(self):
        return {
            self.TitleRole: b"title",
            self.BodyRole: b"body",
            self.IconRole: b"icon",
            self.ButtonsRole: b"buttons",
        }

    @Slot(int, result=list)
    def getButtons(self, index):
        """Get buttons for a specific page index"""
        if 0 <= index < len(self._pages):
            return self._pages[index].get("buttons", [])
        return []

    @Slot(result=int)
    def pageCount(self):
        """Return the total number of pages"""
        return len(self._pages)

    @Slot(int, result=str)
    def getPageTitle(self, index):
        """Get title for a specific page"""
        if 0 <= index < len(self._pages):
            return self._pages[index].get("title", "")
        return ""

    @Slot(int, result=str)
    def getPageIcon(self, index):
        """Get icon for a specific page"""
        if 0 <= index < len(self._pages):
            return self._pages[index].get("icon", "")
        return ""

    @Slot(int, result=str)
    def getPageBody(self, index):
        """Get body text for a specific page"""
        if 0 <= index < len(self._pages):
            return self._pages[index].get("body", "")
        return ""
