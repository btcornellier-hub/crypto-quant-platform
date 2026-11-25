# Instructions for AI assistants working on this repository

## Owner context
The owner is a business owner (MBA, financially literate). They are not a software engineer or professional trader. Explain things in business terms, give step-by-step instructions, and challenge optimism. Do not flatter.

## Resume procedure
1. Read `docs/STATUS.md`, then `docs/DECISION_LOG.md`, then the relevant sections of `docs/ASSESSMENT.md`.
2. Update `docs/STATUS.md` and `docs/DECISION_LOG.md` at the end of every working session.

## Non-negotiable rules
- Never fabricate market data, backtest results or expected returns. Label every illustrative number as such.
- Never ask for, or accept, exchange credentials in chat. Secrets live only on the server, outside Git.
- Live trading stays disabled unless the owner has given explicit, logged approval for a specific strategy version and capital limit.
- No leverage, derivatives or short selling without a new logged owner decision.
- LLMs never place orders, change risk limits or edit production strategy parameters.
- Strategy parameters are frozen per version. Any change creates a new version and restarts validation.
- The risk gate is independent of strategies. Strategies produce targets; only the risk gate approves orders.
- Every backtest run is recorded in the trial registry. The locked holdout is opened once per strategy version.
- Compare every strategy against BTC buy-and-hold, ETH buy-and-hold, 50/50 BTC/ETH, monthly DCA and cash, after costs (and estimated taxes).
- If evidence favors passive investing, say so plainly.
