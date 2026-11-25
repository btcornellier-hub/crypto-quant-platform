"""
TrendTwoSleeve v2: daily, low-turnover trend following with two capital sleeves.

Version history (each version is pre-specified; parameters are fixed before the run; see docs/TRIAL_LOG.md)
  v1 (trial 1): 4h candles. Rejected: 312 trades in 3 yrs; fees ≈ capital; meme stop bug.
  v2 (trial 2): daily candles, Turtle-style breakout/exit, wider stops sized for daily volatility.

Core sleeve (~75% of capital): BTC, ETH, SOL, XRP at 18.75% of the wallet each.
Meme sleeve (≤25% of capital): DOGE, PEPE, SHIB, BONK, PENGU, TRUMP at 8% each, max 3 open (24%).

Entry (daily close):
  * close above its 100-day EMA                       (established uptrend)
  * close above the prior 20-day high                 (fresh breakout)
  * memes also: volume > 1.5x its 20-day average, and BTC above its own 100-day EMA
Exit:
  * close below the prior 10-day low                  (trend broken; classic Turtle exit)
  * Core: hard stop -20% from entry
  * Meme: hard stop -20% from entry; sell HALF at +40%; then trail the rest 20% below the peak;
          losing meme trades are closed after 21 days
Account guardrails (built-in Freqtrade protections): cooldown after exits, pause after a run of
stop-losses, and pause ALL new entries if the account falls >15% within a week.
"""
from datetime import datetime, timedelta
from typing import Optional

import talib.abstract as ta
from pandas import DataFrame

from freqtrade.persistence import Trade
from freqtrade.strategy import IStrategy, informative, stoploss_from_open

CORE = {"BTC/USD", "ETH/USD", "SOL/USD", "XRP/USD"}
MEMES = {"DOGE/USD", "PEPE/USD", "SHIB/USD", "BONK/USD", "PENGU/USD", "TRUMP/USD"}

CORE_STAKE_PCT = 0.1875
MEME_STAKE_PCT = 0.08
MAX_MEME_TRADES = 3
MEME_TAKE_PROFIT = 0.40
MEME_TRAIL = 0.20
MEME_STOP = -0.20
CORE_STOP = -0.20
MEME_MAX_DAYS_LOSING = 21


class TrendTwoSleeve(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = "1d"
    can_short = False
    stoploss = CORE_STOP            # absolute floor for every trade
    use_custom_stoploss = True
    minimal_roi = {"0": 100}        # disabled; exits are rule-based
    position_adjustment_enable = True
    max_entry_position_adjustment = 0
    startup_candle_count = 120
    process_only_new_candles = True
    use_exit_signal = True

    @property
    def protections(self):
        return [
            {"method": "CooldownPeriod", "stop_duration_candles": 1},
            {"method": "StoplossGuard", "lookback_period_candles": 7, "trade_limit": 3,
             "stop_duration_candles": 3, "only_per_pair": False},
            {"method": "MaxDrawdown", "lookback_period_candles": 7, "trade_limit": 2,
             "stop_duration_candles": 7, "max_allowed_drawdown": 0.15},
        ]

    @informative("1d", "BTC/USD")
    def populate_indicators_btc(self, df: DataFrame, metadata: dict) -> DataFrame:
        df["ema100"] = ta.EMA(df, timeperiod=100)
        df["bull"] = (df["close"] > df["ema100"]).astype(int)
        return df

    def populate_indicators(self, df: DataFrame, metadata: dict) -> DataFrame:
        df["ema100"] = ta.EMA(df, timeperiod=100)
        df["hh20"] = df["high"].rolling(20).max().shift(1)   # prior candles only: no look-ahead
        df["ll10"] = df["low"].rolling(10).min().shift(1)
        df["vol_avg"] = df["volume"].rolling(20).mean().shift(1)
        return df

    def populate_entry_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        sig = (df["close"] > df["ema100"]) & (df["close"] > df["hh20"])
        if metadata["pair"] in MEMES:
            sig &= (df["volume"] > 1.5 * df["vol_avg"]) & (df["btc_usd_bull_1d"] == 1)
        df.loc[sig & (df["volume"] > 0), "enter_long"] = 1
        return df

    def populate_exit_trend(self, df: DataFrame, metadata: dict) -> DataFrame:
        df.loc[df["close"] < df["ll10"], "exit_long"] = 1
        return df

    # ---- position sizing & sleeve caps -------------------------------------------------
    def custom_stake_amount(self, pair, current_time, current_rate, proposed_stake, min_stake,
                            max_stake, leverage, entry_tag, side, **kwargs) -> float:
        total = self.wallets.get_total_stake_amount()
        pct = MEME_STAKE_PCT if pair in MEMES else CORE_STAKE_PCT
        return min(total * pct, max_stake)

    def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force, current_time,
                            entry_tag, side, **kwargs) -> bool:
        if pair in MEMES:
            open_memes = sum(1 for t in Trade.get_trades_proxy(is_open=True) if t.pair in MEMES)
            return open_memes < MAX_MEME_TRADES
        return True

    # ---- meme exits: take half at target, trail the rest, hard stop, time stop -----------
    def adjust_trade_position(self, trade: Trade, current_time, current_rate, current_profit,
                              min_stake, max_stake, current_entry_rate, current_exit_rate,
                              current_entry_profit, current_exit_profit, **kwargs):
        if trade.pair in MEMES and trade.nr_of_successful_exits == 0 \
                and current_profit >= MEME_TAKE_PROFIT:
            return -(trade.stake_amount / 2), "take_half_profit"
        return None

    def custom_stoploss(self, pair, trade: Trade, current_time, current_rate, current_profit,
                        after_fill, **kwargs) -> Optional[float]:
        if pair not in MEMES:
            return None                                   # core uses the fixed -20% floor
        if trade.nr_of_successful_exits > 0 or current_profit >= MEME_TAKE_PROFIT:
            return -MEME_TRAIL                            # trail 20% below price; only ratchets up
        # fixed stop measured from the ENTRY price (v1 bug: it trailed from the start)
        return stoploss_from_open(MEME_STOP, current_profit, is_short=trade.is_short,
                                  leverage=trade.leverage)

    def custom_exit(self, pair, trade: Trade, current_time: datetime, current_rate,
                    current_profit, **kwargs):
        if pair in MEMES and current_profit < 0 and \
                current_time - trade.open_date_utc > timedelta(days=MEME_MAX_DAYS_LOSING):
            return "meme_time_stop"
        return None
