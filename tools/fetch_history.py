"""Download free historical 1h candles from data.binance.vision and save them
in Freqtrade's format under user_data/data/kraken/ for backtesting.

Binance USDT prices are used as a PROXY for Kraken USD prices (Kraken's API only
serves ~720 recent candles). Live/paper trading always uses real Kraken prices.
"""
import io, sys, zipfile, urllib.request
from pathlib import Path
import pandas as pd

# Kraken pair  ->  Binance symbol
PAIRS = {
    "BTC/USD": "BTCUSDT", "ETH/USD": "ETHUSDT", "SOL/USD": "SOLUSDT", "XRP/USD": "XRPUSDT",
    "DOGE/USD": "DOGEUSDT", "PEPE/USD": "PEPEUSDT", "SHIB/USD": "SHIBUSDT",
    "BONK/USD": "BONKUSDT", "PENGU/USD": "PENGUUSDT", "TRUMP/USD": "TRUMPUSDT",
}
START, END = "2020-01", "2026-10"
OUT = Path(__file__).resolve().parents[1] / "user_data" / "data" / "kraken"
COLS = ["open_time", "open", "high", "low", "close", "volume"]

def month_frame(sym, ym):
    url = f"https://data.binance.vision/data/spot/monthly/klines/{sym}/1h/{sym}-1h-{ym}.zip"
    try:
        raw = urllib.request.urlopen(url, timeout=60).read()
    except Exception:
        return None  # pair not listed yet that month
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        df = pd.read_csv(z.open(z.namelist()[0]), header=None).iloc[:, :6]
    df.columns = COLS
    df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()].astype(float)
    ts = df["open_time"].astype("int64")
    unit = "us" if ts.iloc[0] > 1e14 else "ms"  # Binance switched to microseconds in 2025
    df["date"] = pd.to_datetime(ts, unit=unit, utc=True)
    return df[["date", "open", "high", "low", "close", "volume"]]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    months = pd.period_range(START, END, freq="M").strftime("%Y-%m")
    for pair, sym in PAIRS.items():
        frames = [f for ym in months if (f := month_frame(sym, ym)) is not None]
        if not frames:
            print(f"{pair}: no data"); continue
        df = pd.concat(frames).drop_duplicates("date").sort_values("date").reset_index(drop=True)
        base = pair.replace("/", "_")
        df.to_feather(OUT / f"{base}-1h.feather")
        df4 = (df.set_index("date").resample("4h", label="left", closed="left")
                 .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
                 .dropna().reset_index())
        df4.to_feather(OUT / f"{base}-4h.feather")
        d1 = (df.set_index("date").resample("1D")
                .agg({"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"})
                .dropna().reset_index())
        d1.to_feather(OUT / f"{base}-1d.feather")
        gaps = (df["date"].diff() > pd.Timedelta("1h")).sum()
        print(f"{pair:10s} {df.date.min():%Y-%m-%d} -> {df.date.max():%Y-%m-%d}  rows={len(df):6d}  gaps={gaps}")

if __name__ == "__main__":
    sys.exit(main())
