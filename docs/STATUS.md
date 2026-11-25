# Current Status

**Phase:** 0 — Assessment (awaiting owner decisions)
**Last updated:** 2026-11-25
**Live trading:** DISABLED · **Paper trading:** not started · **Capital at risk:** $0

## Done
- Phase 0 assessment written (`docs/ASSESSMENT.md`)
- Repository skeleton, `.gitignore` (blocks secrets and data files)

## Blocked on owner
- Decisions D1–D6 (`docs/DECISION_LOG.md`)
- Private GitHub repository + connection to Claude Code
- Actual Coinbase maker/taker fee tier (read from the logged-in fee page)
- US state of residence (affects exchange availability)
- Approval for the cloud workspace to reach Coinbase's public market-data API

## Next (Milestone 1: Data & benchmarks)
1. Project structure, Python environment, test harness
2. Coinbase public candle downloader (BTC-USD, ETH-USD; daily + hourly)
3. Data quality checks + report
4. Cost model; backtest engine core with look-ahead protection
5. Benchmark scorecard report; trial registry; locked holdout

## Known limitations / open questions
- Fee figures are from secondary sources and must be verified in-account
- freqtrade.io, help.coinbase.com and exchange APIs were unreachable from the current cloud environment
- Survivorship bias is unavoidable for any altcoin universe; this is mitigated by starting with BTC/ETH only
