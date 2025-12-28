#!/bin/bash
set -e

INSTALL_DIR="/usr/local/secure-comm"
BIN_DIR="/usr/local/bin"

echo "🔐 Installing secure-comm..."

sudo mkdir -p "$INSTALL_DIR"
sudo cp -r ./* "$INSTALL_DIR"

sudo ln -sf "$INSTALL_DIR/sc" "$BIN_DIR/sc"

echo "✅ secure-comm installed successfully"
echo "👉 Run: sc help"
