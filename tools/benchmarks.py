"""Buy-and-hold benchmarks from the same daily data used in backtests.
Each buy pays the same 0.8% fee as the strategy; holdings are valued at the close."""
import sys
import pandas as pd
from pathlib import Path

D = Path(__file__).resolve().parents[1] / "user_data" / "data" / "kraken"
FEE = 0.008

def closes(pair):
    s = pd.read_feather(D / f"{pair.replace('/', '_')}-1d.feather").set_index("date")["close"]
    return s

def stats(equity, label):
    ret = equity.iloc[-1] / equity.iloc[0] - 1
    dd = (equity / equity.cummax() - 1).min()
    days = (equity.index[-1] - equity.index[0]).days
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (365 / days) - 1
    daily = equity.pct_change().dropna()
    sharpe = daily.mean() / daily.std() * (365 ** 0.5)
    print(f"{label:34s} total {ret:+8.1%}  CAGR {cagr:+7.1%}  max drawdown {dd:7.1%}  Sharpe {sharpe:5.2f}")

def run(start, end):
    print(f"\n--- {start} to {end} (start $5,000) ---")
    px = {p: closes(p).loc[start:end] for p in ["BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD"]}
    for p in ["BTC/USD", "ETH/USD"]:
        stats(5000 * (1 - FEE) * px[p] / px[p].iloc[0], f"Buy & hold {p[:3]}")
    mix = sum(2500 * (1 - FEE) * px[p] / px[p].iloc[0] for p in ["BTC/USD", "ETH/USD"])
    stats(mix, "50/50 BTC/ETH (never rebalanced)")
    core = sum(1250 * (1 - FEE) * px[p] / px[p].iloc[0] for p in px)
    stats(core, "Equal-weight BTC/ETH/SOL/XRP")
    # monthly dollar-cost averaging into BTC: $5,000 split over the first 12 months
    btc = px["BTC/USD"]; buys = btc.resample("MS").first().iloc[:12]
    units = pd.Series(0.0, index=btc.index); cash = pd.Series(5000.0, index=btc.index)
    for dt, price in buys.items():
        units.loc[dt:] += (5000 / 12) * (1 - FEE) / price; cash.loc[dt:] -= 5000 / 12
    stats(units * btc + cash, "DCA into BTC over first 12 months")
    print(f"{'Cash (0% interest assumed)':34s} total    +0.0%")

if __name__ == "__main__":
    run("2021-01-01", "2023-12-31")
    run("2024-01-01", "2026-10-31")
