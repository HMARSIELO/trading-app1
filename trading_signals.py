import pandas as pd
import numpy as np
from unified_collector import get_combined_market_data
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger,
    calculate_liquidity, calculate_pivot_points
)
from risk_management import calculate_entry_exit
from logger import logger
from coingecko_api import get_top_symbols

from machine_learning import load_trade_data, train_model, predict_signal  # 👈 دمج التعلم الآلي

def evaluate_coin(symbol: str, interval: str = "1m"):
    df, source = get_combined_market_data(symbol, interval, limit=100)
    if df is None or df.empty:
        logger.error(f"[{symbol}] No data found for interval {interval}")
        return None

    logger.info(f"[{symbol}] Data source used: {source}")
    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]

    try:
        rsi = calculate_rsi(df)
        macd, signal_line, _ = calculate_macd(df)
        upper, middle, lower = calculate_bollinger(df)
        liquidity = calculate_liquidity(df)
        pivot, s1, r1, s2, r2 = calculate_pivot_points(df)

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

        # 👇 التعلم الآلي
        trade_data = load_trade_data()
        model = train_model(trade_data)
        if model:
            atr_like = df['close'].pct_change().rolling(14).std().iloc[-1]  # تقدير تقريبي للـ ATR
            features = [latest_rsi, latest_macd, atr_like, latest_upper - latest_lower, liquidity]
            ml_signal = predict_signal(model, features)
            if ml_signal == 1:
                logger.info(f"[{symbol}] ML Signal: BUY (overrides rule-based)")
                return "BUY"
            else:
                logger.info(f"[{symbol}] ML Signal: HOLD (overrides rule-based)")
                return "HOLD"

        # fallback على القواعد العادية في حال لم يكن هناك نموذج
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
    symbols = get_top_symbols()
    for symbol in symbols:
        final, detail, votes = evaluate_coin_multi_timeframe(symbol, ["1m", "5m", "1h"])
        print(f"\nFinal signal for {symbol}: {final}")
        print("Details:", detail)
        print("Votes:", votes)
