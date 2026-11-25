# Decision Log

Every material decision is recorded here: date, decision, rationale, and who approved it. Changes to risk limits, capital, live trading or strategy versions **require the owner's explicit approval**.

## Open decisions (awaiting owner)

| ID | Question | Recommendation | Owner answer |
|---|---|---|---|
| D1 | Should we build a custom thin Python platform rather than use Freqtrade/Hummingbot? | Custom thin platform on established libraries (ASSESSMENT §3) | _pending_ |
| D2 | Should the primary objective be "beat BTC/ETH buy-and-hold and cash on a risk-adjusted, after-cost, after-tax basis; else recommend passive"? | Yes (§1) | _pending_ |
| D3 | Should the initial trading universe be BTC-USD and ETH-USD only? | Yes; altcoins only after the core passes (§7) | _pending_ |
| D4 | Should Coinbase Advanced be the primary exchange, with Kraken as an optional second data source and backup? | Yes, pending the actual fee tier and your state of residence | _pending_ |
| D5 | Should the data split be: development to end of 2022, validation 2023 to mid-2025, locked holdout from mid-2025 onward? | Yes (§8.1) | _pending_ |
| D6 | Are the proposed initial hard risk limits (§9) acceptable as a starting point for paper trading? | Yes; finalized before Phase 4 | _pending_ |

## Decided

| Date | ID | Decision | Rationale | Approved by |
|---|---|---|---|---|
| 2026-11-25 | P1 | No leverage, derivatives or short selling before live deployment | Owner requirement | Owner (project brief) |
| 2026-11-25 | P2 | Real-money trading disabled by default; two-key enablement | Owner requirement / capital preservation | Owner (project brief) |
| 2026-11-25 | P3 | No LLM authority over orders, risk limits or production strategies | Owner requirement | Owner (project brief) |
| 2026-11-25 | P4 | Exchange API keys: view + trade only; withdrawals and transfers disabled; never shared in chat | Security | Owner (project brief) |
