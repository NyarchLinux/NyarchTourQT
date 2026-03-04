#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Nyarch Linux

set -e

APP_ID="moe.nyarchlinux.tourqt"
BUILD_DIR="flatpak-build-dir"
REPO_DIR="repo"

echo "Building Nyarch Tour QT flatpak..."

flatpak-builder --force-clean --install-deps-from flathub "$BUILD_DIR" "$APP_ID.json"

if [ "$1" == "--bundle" ]; then
    echo "Creating flatpak bundle..."
    flatpak-builder --repo="$REPO_DIR" --force-clean "$BUILD_DIR" "$APP_ID.json"
    flatpak build-bundle "$REPO_DIR" nyarchtourqt.flatpak "$APP_ID"
    echo "Bundle created: nyarchtourqt.flatpak"
fi

if [ "$1" == "--install" ]; then
    echo "Installing flatpak..."
    flatpak-builder --user --install --force-clean "$BUILD_DIR" "$APP_ID.json"
    echo "Installed! Run with: flatpak run $APP_ID"
fi

if [ "$1" == "--run" ] || [ -z "$1" ]; then
    echo "Running Nyarch Tour QT..."
    flatpak-builder --run "$BUILD_DIR" "$APP_ID.json" nyarchtourqt
fi

echo "Done!"
