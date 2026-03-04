#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Nyarch Linux

"""Main application entry point for Nyarch Tour QT"""

import os
import sys
import signal
from importlib import resources

from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtCore import QUrl, QCoreApplication
from PySide6.QtQml import QQmlApplicationEngine

from nyarchtourqt.pages_model import PagesModel  # noqa: F401
from nyarchtourqt.utils import Utils  # noqa: F401


def run() -> int:
    """Initializes and manages the application execution"""

    # Set application metadata
    QCoreApplication.setApplicationName("Nyarch Tour")
    QCoreApplication.setOrganizationName("Nyarch Linux")
    QCoreApplication.setOrganizationDomain("nyarchlinux.moe")
    QCoreApplication.setApplicationVersion("0.1.0")

    # Use native KDE styling
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "org.kde.desktop")

    app = QGuiApplication(sys.argv)
    app.setDesktopFileName("moe.nyarchlinux.tourqt")
    app.setWindowIcon(QIcon.fromTheme("moe.nyarchlinux.tourqt"))

    engine = QQmlApplicationEngine()

    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Expose models to QML
    pages_model = PagesModel()
    engine.rootContext().setContextProperty("pagesModel", pages_model)

    utils = Utils()
    engine.rootContext().setContextProperty("utils", utils)

    # Set pictures path for QML
    pkg_files = resources.files("nyarchtourqt")
    pictures_path = str(pkg_files.joinpath("pictures"))
    engine.rootContext().setContextProperty("picturesPath", f"file://{pictures_path}")

    # Load main QML
    main_qml = pkg_files.joinpath("qml/main.qml")
    engine.load(QUrl.fromLocalFile(str(main_qml)))

    if not engine.rootObjects():
        return 1

    return app.exec()


def main() -> None:
    raise SystemExit(run())
