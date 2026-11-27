#!/usr/bin/env bash
# Generates a new dashboard password and restarts the bot. Run as root on the server.
set -euo pipefail
PRIV=/opt/crypto-quant-platform/user_data/config.private.json
[ -f "$PRIV" ] || { echo "Private settings not found; run server-setup.sh first."; exit 1; }
NEW=$(openssl rand -base64 18 | tr -d '/+=')
TMP=$(mktemp)
jq --arg p "$NEW" '.api_server.password = $p' "$PRIV" > "$TMP"
install -m 600 -o 1000 -g 1000 "$TMP" "$PRIV"; rm -f "$TMP"
cd /opt/crypto-quant-platform && docker compose restart freqtrade >/dev/null 2>&1 || true
echo "New dashboard password (username: owner): $NEW"
echo "Save it in your password manager. To copy: highlight it with the mouse, then right-click > Copy."
echo "Do NOT press Ctrl+C in this console; that cancels instead of copying."
