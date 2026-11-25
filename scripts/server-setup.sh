#!/usr/bin/env bash
# One-time setup of the trading server (Ubuntu 24.04 on DigitalOcean). Run as root:
#   bash /opt/crypto-quant-platform/scripts/server-setup.sh
# Safe to re-run. Starts the bot in PAPER mode only.
set -euo pipefail
REPO=/opt/crypto-quant-platform
PRIV="$REPO/user_data/config.private.json"
say() { printf '\n\033[1;36m==> %s\033[0m\n' "$*"; }

[ "$(id -u)" -eq 0 ] || { echo "Please run as root."; exit 1; }
[ -d "$REPO/.git" ] || { echo "Repository not found at $REPO"; exit 1; }

say "1/7 Updating the operating system and installing tools"
export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get upgrade -y
apt-get install -y docker.io docker-compose-v2 ufw fail2ban unattended-upgrades jq curl openssl
dpkg-reconfigure -f noninteractive unattended-upgrades
systemctl enable --now docker

say "2/7 Limiting Docker log size"
cat > /etc/docker/daemon.json <<'J'
{"log-driver": "json-file", "log-opts": {"max-size": "10m", "max-file": "5"}}
J
systemctl restart docker

say "3/7 Firewall: block everything incoming except SSH (rate-limited) and the private Tailscale network"
sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config
systemctl reload ssh || true
ufw default deny incoming
ufw default allow outgoing
ufw limit 22/tcp
ufw allow in on tailscale0
ufw --force enable

say "4/7 Installing Tailscale (private access from your phone)"
command -v tailscale >/dev/null || curl -fsSL https://tailscale.com/install.sh | sh
if ! tailscale status >/dev/null 2>&1; then
  echo "A login link will appear below. Open it, sign in to Tailscale, then come back here."
  tailscale up
fi

say "5/7 Private settings (Telegram + dashboard login). These stay on this server only."
if [ ! -f "$PRIV" ]; then
  read -rsp "Paste your Telegram bot token (from @BotFather; input is hidden), then press Enter: " TG_TOKEN; echo
  echo "Now open Telegram, find your new bot, and send it any message (e.g. 'hi')."
  read -rp "Press Enter after you've sent the message... " _
  CHAT_ID=$(curl -fsS "https://api.telegram.org/bot${TG_TOKEN}/getUpdates" | jq -r '.result[-1].message.chat.id // empty')
  [ -n "$CHAT_ID" ] || { echo "Couldn't find your message. Send the bot a message and re-run this script."; exit 1; }
  DASH_USER=owner
  DASH_PASS=$(openssl rand -base64 18 | tr -d '/+=')
  jq -n --arg t "$TG_TOKEN" --arg c "$CHAT_ID" --arg u "$DASH_USER" --arg p "$DASH_PASS" \
        --arg j "$(openssl rand -hex 32)" --arg w "$(openssl rand -hex 32)" '{
    exchange: {name: "kraken", key: "", secret: ""},
    telegram: {enabled: true, token: $t, chat_id: $c,
               notification_settings: {entry: "on", exit: "on", entry_fill: "off", exit_fill: "off",
                                       protection_trigger_global: "on", warning: "on", status: "on"}},
    api_server: {enabled: true, listen_ip_address: "0.0.0.0", listen_port: 8080, verbosity: "error",
                 enable_openapi: false, jwt_secret_key: $j, ws_token: $w, CORS_origins: [],
                 username: $u, password: $p}}' > "$PRIV"
  chmod 600 "$PRIV"
  echo "Dashboard username: $DASH_USER"
  echo "Dashboard password: $DASH_PASS"
  echo ">>> Save this password in your password manager NOW. It will not be shown again. <<<"
  read -rp "Press Enter once it's saved... " _
else
  echo "Private settings already exist; leaving them unchanged."
fi

say "6/7 Starting the bot (PAPER TRADING)"
grep -q '"dry_run": true' "$REPO/user_data/config.json" || { echo "SAFETY STOP: dry_run is not true."; exit 1; }
mkdir -p "$REPO/user_data/logs"
chown -R 1000:1000 "$REPO/user_data"
cd "$REPO" && docker compose pull && docker compose up -d

say "7/7 Publishing the dashboard on your private Tailscale network only"
tailscale serve --bg 8080
HOST=$(tailscale status --json | jq -r '.Self.DNSName' | sed 's/\.$//')
echo
echo "DONE. Paper trading is running."
echo "Dashboard (works only on devices signed in to your Tailscale): https://$HOST"
echo "Telegram: send /status, /profit or /daily to your bot."
