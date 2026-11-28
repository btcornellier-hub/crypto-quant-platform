# Current Status

**Phase:** Paper trading (started 2026-11-28)
**Last updated:** 2026-11-28 
**Live trading:** DISABLED (`dry_run: true`) · **Paper trading:** running 24/7 since 2026-11-28 · **Capital at risk:** $0

## Done
- Phase 0 assessment (`docs/ASSESSMENT.md`). Its custom-build recommendation is superseded by D7 (Freqtrade + Kraken).
- Freqtrade 2026.10 installed; strategy `user_data/strategies/TrendTwoSleeve.py` (v2)
- Price history 2020 → Oct 2026 for 10 coins (`tools/fetch_history.py`)
- Backtests + benchmarks: see `docs/TRIAL_LOG.md`
- Docker deployment file, secrets template, paper-mode smoke test passed

## Paper trading: LIVE since 2026-11-28
- Bot `TrendTwoSleeve v2` running in Docker on DigitalOcean `crypto-bot` (dry run, $5,000 simulated, live Kraken prices)
- Telegram `@btc_trend_paper_bot` responding (`/status` OK on 2026-11-28)
- Earliest live-pilot review: **2026-12-28** (≥30 days), only with explicit owner approval (D10)
- [ ] Confirm dashboard is published (`tailscale serve --bg 8080`) after enabling Serve in the Tailscale admin
- [ ] Rotate the dashboard password (`scripts/reset-dashboard-password.sh`); the first one appeared in a screenshot
- Console tips: `bind 'set enable-bracketed-paste off'` in each new console; never press Ctrl+C to copy

## Next
- Deploy to the server; run paper trading ≥30 days; weekly review against BTC buy-and-hold
- Prepare the live-pilot checklist: Kraken account, trade-only API key with IP restriction, `stoploss_on_exchange`

## Known limitations
- Backtests used Binance USDT prices as a proxy for Kraken USD prices
- Results depend on a handful of very large trades; not statistically significant (p ≈ 0.4)
- After-tax comparison not yet modeled (all strategy gains are short-term)
- The out-of-sample period is now used up; paper and live trading are the only fresh evidence
