# Trial Log (every backtest run is recorded here, including failures)

Data: Binance spot USDT 1h candles (proxy for Kraken USD), resampled. Fees are charged on both entry and exit.
Development period: 2021-01-01 → 2023-12-31. Out-of-sample: 2024-01-01 → 2026-10-31, **used once for v2; now consumed.**
Benchmark numbers come from `tools/benchmarks.py` (each buy pays the same 0.8% fee).

| # | Date | Version | Period | Fee/side | Trades | Net result ($5k start) | Max drawdown (wallet) | Outcome |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-11-25 | v1 (4h) | Dev | 0.8% | 312 | +32% | 52% | **Rejected.** Fees ≈ $4.7k; meme stop bug (trailing from entry) |
| 2 | 2026-11-25 | v2 (daily) | Dev | 0.8% | 79 | +389% | 52% | Passed to OOS. **Concentrated:** one SOL trade (+486%) produced most of the profit |
| 3 | 2026-11-25 | v2 | **OOS** | 0.8% | 102 | +70.5% (CAGR 20.7%), Sharpe 0.77 | 34% | See below |
| 4 | 2026-11-25 | v2 | **OOS** | 1.2% (stress) | 102 | +53.9% (CAGR 16.5%), Sharpe 0.65 | 37% | Survives the cost stress |

## Out-of-sample comparison (2024-01 → 2026-10)
| | Total | CAGR | Max drawdown | Sharpe |
|---|---|---|---|---|
| **TrendTwoSleeve v2** | **+70.5%** | **+20.7%** | **−34%** | **0.77** |
| Buy & hold BTC | +75.6% | +22.0% | −53% | 0.66 |
| Buy & hold ETH | −4.1% | −1.5% | −68% | 0.31 |
| 50/50 BTC/ETH | +35.8% | +11.4% | −59% | 0.47 |
| Equal-weight BTC/ETH/SOL/XRP | +39.3% | +12.4% | −64% | 0.49 |
| Cash | 0% | 0% | 0% | — |

**Interpretation.** In the out-of-sample period, v2 made about the same money as simply holding BTC, with roughly a third smaller worst-case loss. It beat ETH, the 50/50 mix and the equal-weight basket. The meme sleeve contributed modestly (PEPE, PENGU and BONK were positive; SHIB and DOGE were slightly negative). The core BTC/ETH trades lost money; one XRP trade (+331%) carried the result.

**Statistical caution.** The p-value is 0.39, so the result is not statistically significant. Results depend on a few large trades. All gains would be short-term and taxed as ordinary income, while buy-and-hold BTC would mostly qualify for long-term rates. **After tax, buy-and-hold BTC was likely as good or better over this window.** The genuine, demonstrated benefit is smaller drawdowns, not higher returns.
