# Current Status

**Phase:** Fast path. Strategy v2 is built and backtested; waiting on the cloud server for paper trading.
**Last updated:** 2026-11-27 (paused mid-deployment) 
**Live trading:** DISABLED (`dry_run: true`) · **Paper trading:** smoke-tested OK on live Kraken data; not yet running 24/7 · **Capital at risk:** $0

## Done
- Phase 0 assessment (`docs/ASSESSMENT.md`). Its custom-build recommendation is superseded by D7 (Freqtrade + Kraken).
- Freqtrade 2026.10 installed; strategy `user_data/strategies/TrendTwoSleeve.py` (v2)
- Price history 2020 → Oct 2026 for 10 coins (`tools/fetch_history.py`)
- Backtests + benchmarks: see `docs/TRIAL_LOG.md`
- Docker deployment file, secrets template, paper-mode smoke test passed

## Deployment progress (paused 2026-11-27 at the owner's request)
- [x] GitHub private repo: btcornellier-hub/crypto-quant-platform
- [x] Telegram bot `@btc_trend_paper_bot`; token re-issued after accidental exposure; owner has messaged the bot
- [x] Tailscale on phone + Windows desktop (Google sign-in); **server joined Tailscale**
- [x] DigitalOcean droplet `crypto-bot` (Ubuntu 24.04, Basic 1 vCPU / 2 GB, SFO2, $12/mo), read-only deploy key added to GitHub
- [x] Setup script steps 1–5 completed; `config.private.json` written on the server (token validated)
- [ ] **Resume here:** the script was cancelled (Ctrl+C) before step 6, so the **bot is NOT running yet**. In the DO web console run:
      `git -C /opt/crypto-quant-platform pull && bash /opt/crypto-quant-platform/scripts/server-setup.sh`
- [ ] Then rotate the dashboard password (the first one appeared in a screenshot):
      `bash /opt/crypto-quant-platform/scripts/reset-dashboard-password.sh`
- [ ] Verify: Telegram `/status`, dashboard opens over Tailscale; start the 30-day paper clock
- Console tips: type `bind 'set enable-bracketed-paste off'` after opening a new console if pastes show `^[[200~`; never press Ctrl+C to copy (highlight + right-click)

## Next
- Deploy to the server; run paper trading ≥30 days; weekly review against BTC buy-and-hold
- Prepare the live-pilot checklist: Kraken account, trade-only API key with IP restriction, `stoploss_on_exchange`

## Known limitations
- Backtests used Binance USDT prices as a proxy for Kraken USD prices
- Results depend on a handful of very large trades; not statistically significant (p ≈ 0.4)
- After-tax comparison not yet modeled (all strategy gains are short-term)
- The out-of-sample period is now used up; paper and live trading are the only fresh evidence
