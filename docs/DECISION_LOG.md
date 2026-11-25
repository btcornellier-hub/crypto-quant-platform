# Decision Log

Every material decision is recorded here: date, decision, rationale, and who approved it. Changes to risk limits, capital, live trading or strategy versions **require the owner's explicit approval**.

## Open decisions (awaiting owner)

| ID | Question | Recommendation | Owner answer |
|---|---|---|---|
| D1 | ~~Custom platform vs framework~~ | — | **Superseded by D7** |
| D2 | Should the primary objective be "beat BTC/ETH buy-and-hold and cash on a risk-adjusted, after-cost, after-tax basis; else recommend passive"? | Yes (§1) | _pending_ |
| D3 | ~~BTC/ETH-only universe~~ | — | **Superseded by D8** |
| D4 | ~~Coinbase as primary exchange~~ | — | **Superseded by D7 (Kraken)** |
| D5 | ~~Three-way data split~~ | — | **Superseded:** fast path uses dev 2021–2023 / out-of-sample 2024–Oct 2026 (see TRIAL_LOG) |
| D10 | Should we go live with $250–500 after 30 clean paper days? | Decide after the paper results | _pending_ |

## Decided

| Date | ID | Decision | Rationale | Approved by |
|---|---|---|---|---|
| 2026-11-25 | P1 | No leverage, derivatives or short selling before live deployment | Owner requirement | Owner (project brief) |
| 2026-11-25 | P2 | Real-money trading disabled by default; two-key enablement | Owner requirement / capital preservation | Owner (project brief) |
| 2026-11-25 | P3 | No LLM authority over orders, risk limits or production strategies | Owner requirement | Owner (project brief) |
| 2026-11-25 | P4 | Exchange API keys: view + trade only; withdrawals and transfers disabled; never shared in chat | Security | Owner (project brief) |
| 2026-11-25 | D7 | **Fast path:** use Freqtrade 2026.10 (established open-source bot) on **Kraken**. Coinbase is not supported by Freqtrade (verified in its source code). | Owner wants a viable system now without reinventing the wheel | Owner |
| 2026-11-25 | D8 | Two sleeves: core (BTC/ETH/SOL/XRP, ~75%) plus a **meme sleeve capped at 25%** (DOGE, PEPE, SHIB, BONK, PENGU, TRUMP; exchange-listed only; max 3 positions) | Owner request; cap limits damage from meme crashes | Owner |
| 2026-11-25 | D2 | Primary yardstick: beat BTC/ETH buy-and-hold and cash after costs; recommend passive investing if not | Owner proceeded on this basis | Owner (implicit) |
| 2026-11-25 | — | Owner resides in **Florida**; Kraken excludes only ME and NY | Exchange eligibility | Owner |
| 2026-11-25 | — | Paper-trading period shortened to ≥30 days (from 90) for the fast path; live pilot capped at $250–500 | Owner timeline; the small pilot is the real test | Owner |
| 2026-11-25 | D9 | Start ≥30-day paper trading of TrendTwoSleeve v2 ($5,000 simulated) on a DigitalOcean server | Owner said "yes, let's start" | Owner |
