#!/data/data/com.termux/files/usr/bin/bash
set -e

APP_DIR="$HOME/streamline-ai-project/FixPilot-AI"
BIN_LINK="$PREFIX/bin/fixpilot"

echo "[*] Installing FixPilot-AI ULTRA..."

mkdir -p "$APP_DIR"

# Copy main script
cp "$(dirname "$0")/fixpilot.py" "$APP_DIR/fixpilot.py"
chmod +x "$APP_DIR/fixpilot.py"

# Version file
if [ -f "$(dirname "$0")/version.txt" ]; then
  cp "$(dirname "$0")/version.txt" "$APP_DIR/version.txt"
fi

# Symlink
rm -f "$BIN_LINK"
ln -s "$APP_DIR/fixpilot.py" "$BIN_LINK"

echo "[+] Install complete."
echo "Run:  fixpilot diagnose"
