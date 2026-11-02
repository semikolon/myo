#!/bin/bash
# Builds ~/Applications/MyoBridge.app: a wrapper that runs myo-bridge from this
# project's venv under its own name, so macOS asks once "MyoBridge would like to
# use Bluetooth" and the bridge can run in the background (a LaunchAgent opens it).
# A Bluetooth program started from an app that declares no Bluetooth use is killed
# by macOS, which is why it cannot simply run from a shell or launchd.
set -euo pipefail

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
APP="$HOME/Applications/MyoBridge.app"

cd "$PROJECT"
uv sync -q

rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS"

cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key><string>MyoBridge</string>
    <key>CFBundleDisplayName</key><string>MyoBridge</string>
    <key>CFBundleIdentifier</key><string>com.fredrikbranstrom.myo-bridge</string>
    <key>CFBundleExecutable</key><string>MyoBridge</string>
    <key>CFBundlePackageType</key><string>APPL</string>
    <key>CFBundleVersion</key><string>1</string>
    <key>LSUIElement</key><true/>
    <key>NSBluetoothAlwaysUsageDescription</key>
    <string>MyoBridge connects to your Myo armband to read its gestures and make it vibrate.</string>
</dict>
</plist>
PLIST

# A compiled launcher, not a script: it must stay the running process so that
# macOS attributes Bluetooth use to MyoBridge (scripts/launcher.c explains why).
PYTHON="$(cd "$PROJECT/.venv/bin" && pwd)/python"
clang -O2 -Wall -DPYTHON_PATH="\"$PYTHON\"" -o "$APP/Contents/MacOS/MyoBridge" "$PROJECT/scripts/launcher.c"

codesign --force --sign - "$APP"
echo "built $APP"
