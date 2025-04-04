# trading_signals.py
import pandas as pd
import numpy as np

from binance_api import get_market_data
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger_bands,
    calculate_liquidity, calculate_pivot_points
)

def evaluate_coin(symbol: str, interval: str = "1m"):
    """
    تقييم العملة باستخدام مجموعة من المؤشرات:
      - RSI, MACD, Bollinger Bands, السيولة, نقاط Pivot
    تعيد الدالة إحدى الإشارات: BUY, SELL, HOLD
    """
    df = get_market_data(symbol, interval=interval, limit=100)
    if df is None or df.empty:
        return None

    df = df.copy()
    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]

    # حساب المؤشرات
    rsi = calculate_rsi(df, period=14)
    macd, signal_line, _ = calculate_macd(df)
    upper, middle, lower = calculate_bollinger_bands(df, period=20)
    liquidity = calculate_liquidity(df, period=20)
    pivot, s1, r1, s2, r2 = calculate_pivot_points(df)

    # آخر صف
    latest_rsi = rsi[-1]
    latest_macd = macd[-1]
    latest_signal = signal_line[-1]
    latest_price = df['close'].iloc[-1]
    latest_upper = upper[-1]
    latest_lower = lower[-1]

    # منطق بسيط لإشارة شراء/بيع
    if (latest_rsi < 30
        and latest_macd > latest_signal
        and latest_price < latest_lower
        and liquidity > 0):
        return "BUY"
    elif (latest_rsi > 70
          and latest_macd < latest_signal
          and latest_price > latest_upper
          and liquidity > 0):
        return "SELL"
    else:
        return "HOLD"

def evaluate_coin_multi_timeframe(symbol: str, intervals: list, weights: dict = None):
    """
    تحليل متعدد الأطر الزمنية مع منطق تجميع مرجح (Weighted Aggregation).
    إذا لم يتم تمرير weights، يتم افتراض أوزان بسيطة.
    """
    if weights is None:
        weights = {}
        for interval in intervals:
            if interval == "1m":
                weights[interval] = 1
            elif interval == "5m":
                weights[interval] = 2
            elif interval == "15m":
                weights[interval] = 3
            elif interval == "1h":
                weights[interval] = 4
            elif interval == "4h":
                weights[interval] = 5
            else:
                weights[interval] = 1

    weighted_votes = {"BUY": 0, "SELL": 0, "HOLD": 0}
    details = {}

    for interval in intervals:
        signal = evaluate_coin(symbol, interval=interval)
        if signal is None:
            signal = "HOLD"  # في حال فشل جلب البيانات
        details[interval] = signal

        if signal in weighted_votes:
            weighted_votes[signal] += weights.get(interval, 1)
        else:
            weighted_votes["HOLD"] += weights.get(interval, 1)

    final_signal = max(weighted_votes, key=weighted_votes.get)
    return final_signal, details, weighted_votes

if __name__ == "__main__":
    symbol_test = "BTCUSDT"
    intervals_test = ["1m", "5m", "1h"]
    final_sig, detail_sig, votes_sig = evaluate_coin_multi_timeframe(symbol_test, intervals_test)
    print(f"Final signal for {symbol_test}: {final_sig}")
    print("Details:", detail_sig)
    print("Votes:", votes_sig)
