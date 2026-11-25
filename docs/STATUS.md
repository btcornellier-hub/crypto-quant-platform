# Current Status

**Phase:** Fast path. Strategy v2 is built and backtested; waiting on the cloud server for paper trading.
**Last updated:** 2026-11-25
**Live trading:** DISABLED (`dry_run: true`) · **Paper trading:** smoke-tested OK on live Kraken data; not yet running 24/7 · **Capital at risk:** $0

## Done
- Phase 0 assessment (`docs/ASSESSMENT.md`). Its custom-build recommendation is superseded by D7 (Freqtrade + Kraken).
- Freqtrade 2026.10 installed; strategy `user_data/strategies/TrendTwoSleeve.py` (v2)
- Price history 2020 → Oct 2026 for 10 coins (`tools/fetch_history.py`)
- Backtests + benchmarks: see `docs/TRIAL_LOG.md`
- Docker deployment file, secrets template, paper-mode smoke test passed

## Blocked on owner
1. GitHub private repo (to save the code off this temporary workspace)
2. DigitalOcean account (≈$12/mo server) — for 24/7 paper trading
3. Telegram bot token (created on your phone via @BotFather), entered **on the server**, never in chat
4. Tailscale account (private phone access to the dashboard)
5. Decision D9 (start paper trading)

## Next
- Deploy to the server; run paper trading ≥30 days; weekly review against BTC buy-and-hold
- Prepare the live-pilot checklist: Kraken account, trade-only API key with IP restriction, `stoploss_on_exchange`

## Known limitations
- Backtests used Binance USDT prices as a proxy for Kraken USD prices
- Results depend on a handful of very large trades; not statistically significant (p ≈ 0.4)
- After-tax comparison not yet modeled (all strategy gains are short-term)
- The out-of-sample period is now used up; paper and live trading are the only fresh evidence
