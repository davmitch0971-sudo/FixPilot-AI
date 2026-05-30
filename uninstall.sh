#!/data/data/com.termux/files/usr/bin/bash
set -e

APP_DIR="$HOME/streamline-ai-project/FixPilot-AI"
BIN_LINK="$PREFIX/bin/fixpilot"

echo "[*] Uninstalling FixPilot-AI ULTRA..."

rm -f "$BIN_LINK"
rm -rf "$APP_DIR"

echo "[+] Uninstall complete."
