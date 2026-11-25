# Current Status

**Phase:** Fast path. Strategy v2 is built and backtested; waiting on the cloud server for paper trading.
**Last updated:** 2026-11-25 (paused mid-deployment)
**Live trading:** DISABLED (`dry_run: true`) · **Paper trading:** smoke-tested OK on live Kraken data; not yet running 24/7 · **Capital at risk:** $0

## Done
- Phase 0 assessment (`docs/ASSESSMENT.md`). Its custom-build recommendation is superseded by D7 (Freqtrade + Kraken).
- Freqtrade 2026.10 installed; strategy `user_data/strategies/TrendTwoSleeve.py` (v2)
- Price history 2020 → Oct 2026 for 10 coins (`tools/fetch_history.py`)
- Backtests + benchmarks: see `docs/TRIAL_LOG.md`
- Docker deployment file, secrets template, paper-mode smoke test passed

## Deployment progress (paused 2026-11-25 at the owner's request)
- [x] GitHub private repo: btcornellier-hub/crypto-quant-platform (code pushed)
- [x] Telegram bot created (`@btc_trend_paper_bot`); token re-issued after accidental exposure; stored by the owner, not in chat
- [x] Tailscale account (Google sign-in) on phone + desktop
- [x] DigitalOcean account created
- [ ] **Resume here:** create droplet (Ubuntu 24.04, Basic $12/mo, NYC, password auth, backups on, hostname `crypto-bot`), then follow `docs/DEPLOY.md` step E
- Owner uses Windows desktop + iPhone; walk through each screen

## Next
- Deploy to the server; run paper trading ≥30 days; weekly review against BTC buy-and-hold
- Prepare the live-pilot checklist: Kraken account, trade-only API key with IP restriction, `stoploss_on_exchange`

## Known limitations
- Backtests used Binance USDT prices as a proxy for Kraken USD prices
- Results depend on a handful of very large trades; not statistically significant (p ≈ 0.4)
- After-tax comparison not yet modeled (all strategy gains are short-term)
- The out-of-sample period is now used up; paper and live trading are the only fresh evidence
