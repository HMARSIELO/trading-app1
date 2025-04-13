import pandas as pd
import numpy as np
from unified_collector import get_combined_market_data
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger,
    calculate_liquidity, calculate_pivot_points
)
from risk_management import calculate_entry_exit
from logger import logger  # استخدام logger المخصص

def evaluate_coin(symbol: str, interval: str = "1m"):
    df = get_combined_market_data(symbol, interval, limit=100)
    if df is None or df.empty:
        logger.error(f"[{symbol}] No data found for interval {interval}")
        return None

    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]

    try:
        # حساب المؤشرات
        rsi = calculate_rsi(df)
        macd, signal_line, _ = calculate_macd(df)
        upper, middle, lower = calculate_bollinger(df)
        liquidity = calculate_liquidity(df)
        pivot, s1, r1, s2, r2 = calculate_pivot_points(df)

        # استخراج القيم الأخيرة
        latest_price = df['close'].iloc[-1]
        if len(rsi) == 0 or len(macd) == 0 or len(signal_line) == 0:
            logger.warning(f"[{symbol}] Indicator arrays are empty.")
            return "HOLD"

        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_upper = upper.iloc[-1]
        latest_lower = lower.iloc[-1]

        logger.debug(f"[{symbol}] Indicators: RSI={latest_rsi}, MACD={latest_macd}, Signal={latest_signal}")

        if latest_rsi < 30 and latest_macd > latest_signal and latest_price < latest_lower and liquidity > 0:
            return "BUY"
        elif latest_rsi > 70 and latest_macd < latest_signal and latest_price > latest_upper and liquidity > 0:
            return "SELL"
        else:
            return "HOLD"
    except Exception as e:
        logger.error(f"[{symbol}] Error while calculating indicators: {e}")
        return None


def evaluate_coin_multi_timeframe(symbol: str, intervals: list, weights: dict = None):
    if weights is None:
        weights = {"1m": 1, "5m": 2, "15m": 3, "1h": 4, "4h": 5}

    votes = {"BUY": 0, "SELL": 0, "HOLD": 0}
    details = {}

    for interval in intervals:
        logger.info(f"Processing {symbol} on interval {interval}")
        signal = evaluate_coin(symbol, interval)
        details[interval] = signal or "HOLD"
        votes[details[interval]] += weights.get(interval, 1)

    final = max(votes, key=votes.get)
    return final, details, votes


if __name__ == "__main__":
    symbol = "BTCUSDT"
    final, detail, votes = evaluate_coin_multi_timeframe(symbol, ["1m", "5m", "1h"])
    print(f"Final signal for {symbol}: {final}")
    print("Details:", detail)
    print("Votes:", votes)
