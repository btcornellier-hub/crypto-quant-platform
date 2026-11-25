# Deploying the bot (paper trading)

About 45–60 minutes, done once. Keep your password manager open.

## A. GitHub (stores the code)
1. Connect GitHub to Claude: https://claude.ai/connect-github
2. On github.com, click **New repository**. Name it `crypto-quant-platform`, choose **Private**, and **don't** add a README.
3. Tell Claude the repository's address (e.g. `yourname/crypto-quant-platform`). Claude pushes the code.

## B. Telegram bot (alerts on your phone)
1. In Telegram, open **@BotFather** and send `/newbot`. Pick any name and a username ending in `bot`.
2. BotFather replies with a **token**. Save it in your password manager. **Do not paste it into Claude.**

## C. Tailscale (private access to the dashboard)
1. Sign up at tailscale.com (the free plan is enough) and install the Tailscale app on your phone. Sign in.

## D. DigitalOcean server
1. Sign up at digitalocean.com and turn on two-factor authentication.
2. Click **Create → Droplets**:
   - Region: New York or San Francisco
   - Image: **Ubuntu 24.04 (LTS) x64**
   - Size: **Basic → Regular → 2 GB RAM / 1 CPU** (≈$12/mo)
   - Authentication: **Password**. Generate a strong one in your password manager.
   - Enable **Backups** (≈$2.40/mo)
   - Hostname: `crypto-bot`
3. When it's ready, open the droplet and click **Console** (top-right). A black terminal window opens.

## E. Run the setup (paste into the Console)
**E1.** Paste this and press Enter. It creates a read-only key so the server can download your code:
```bash
apt-get update && apt-get install -y git && ssh-keygen -t ed25519 -N "" -f /root/.ssh/deploy_key -C crypto-bot && cat /root/.ssh/deploy_key.pub
```
**E2.** Copy the line it prints, which starts with `ssh-ed25519`. (This is a *public* key and is safe to share.) On GitHub, open your repository → **Settings → Deploy keys → Add deploy key**. Paste it, title it `server`, and leave "Allow write access" **unchecked**.

**E3.** Paste this, replacing `YOURNAME` with your GitHub username:
```bash
git clone -c core.sshCommand="ssh -i /root/.ssh/deploy_key -o StrictHostKeyChecking=accept-new" git@github.com:YOURNAME/crypto-quant-platform.git /opt/crypto-quant-platform && bash /opt/crypto-quant-platform/scripts/server-setup.sh
```
**E4.** Follow the prompts:
- A Tailscale login link appears. Open it and approve.
- Paste the Telegram token when asked. Nothing shows as you paste; that's normal.
- Send your bot a message in Telegram.
- **Save the dashboard password** it shows you.

**E5.** At the end, it prints a dashboard address. Open it on your phone, with Tailscale switched on. Also send `/status` to your bot in Telegram.

## Everyday use
- Telegram commands: `/status` (open trades), `/profit` (results), `/daily` (by day), `/balance`, **`/stopentry`** (stop opening new trades), `/stop` (stop the bot)
- Health check from the Console: `bash /opt/crypto-quant-platform/scripts/status.sh`
