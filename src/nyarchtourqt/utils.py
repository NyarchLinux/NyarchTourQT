#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2024 Nyarch Linux

"""Utility functions for Nyarch Tour QT"""

import subprocess
import shlex
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement
import os 

QML_IMPORT_NAME = "moe.nyarchlinux.tourqt"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class Utils(QObject):
    """Utility class providing helper functions to QML"""

    def __init__(self, parent=None):
        super().__init__(parent)

    def is_flatpak(self) -> bool:
        """
        Check if we are in a flatpak

        Returns:
            bool: True if we are in a flatpak
        """
        if os.getenv("container"):
            return True
        return False

    def get_spawn_command(self) -> list:
        """
        Get the spawn command to run commands on the user system

        Returns:
            list: space diveded command  
        """
        if self.is_flatpak():
            return ["flatpak-spawn", "--host"]
        else:
            return []
    
    @Slot(str)
    def run_command(self, command: str) -> None:
        """Execute a command on the host system via flatpak-spawn"""
        try:
            subprocess.Popen(self.get_spawn_command() + shlex.split(command))
        except Exception as e:
            print(f"Error running command '{command}': {e}")

    @Slot(result=bool)
    def check_btrfs(self) -> bool:
        """Check if the root filesystem is BTRFS"""
        try:
            script = """if [ "$(findmnt -n -o FSTYPE /)" == "btrfs" ]; then
              echo 1
            else
              echo 0
            fi
            """
            result = subprocess.check_output(
                self.get_spawn_command() + ["bash", "-c", script]
            ).decode("utf-8").strip()
            return result == "1"
        except Exception as e:
            print(f"Error checking BTRFS: {e}")
            return False

    @Slot(str)
    def open_url(self, url: str) -> None:
        """Open a URL using xdg-open"""
        self.run_command(f"xdg-open {url}")
