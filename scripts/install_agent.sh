#!/bin/bash
# Builds MyoBridge.app and (re)loads the LaunchAgent that keeps the bridge running.
set -euo pipefail
PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
LABEL=com.fredrikbranstrom.myo-bridge
DEST="$HOME/Library/LaunchAgents/$LABEL.plist"

bash "$PROJECT/scripts/build_app.sh"
mkdir -p "$HOME/.local/state/myo-bridge"
cp "$PROJECT/scripts/$LABEL.plist" "$DEST"
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$DEST"
echo "loaded $LABEL"
