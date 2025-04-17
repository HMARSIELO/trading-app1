import pandas as pd
import numpy as np
from unified_collector import get_combined_market_data
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger,
    calculate_liquidity, calculate_pivot_points
)
from risk_management import calculate_entry_exit
from logger import logger
from machine_learning import load_trade_data, train_model, predict_signal  # 👈 دمج التعلم الآلي

# ✅ متاح للاستيراد من أي ملف آخر
symbols = [
    "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
    "DOGEUSDT", "ADAUSDT", "DOTUSDT","TRXUSDT", "LINKUSDT", "MATICUSDT", "SHIBUSDT", "BCHUSDT",
    "LTCUSDT", "NEARUSDT", "ICPUSDT", "UNIUSDT", "APTUSDT",
    "ETCUSDT", "STXUSDT", "IMXUSDT", "INJUSDT", "FILUSDT",
    "HBARUSDT", "ARBUSDT", "OPUSDT", "RUNEUSDT", "XLMUSDT",
    "ATOMUSDT", "SANDUSDT", "MANAUSDT", "AAVEUSDT", "GRTUSDT",
    "EOSUSDT", "XTZUSDT", "SNXUSDT", "CRVUSDT", "1INCHUSDT",
    "ENJUSDT", "ZILUSDT", "BATUSDT", "CHZUSDT", "KSMUSDT",
    "YFIUSDT", "COMPUSDT", "ZRXUSDT", "ALGOUSDT", "DASHUSDT",
    "FTMUSDT", "GALAUSDT", "DYDXUSDT", "LDOUSDT", "SUSHIUSDT",
    "MINAUSDT", "GMXUSDT", "FLOWUSDT", "RLCUSDT", "OCEANUSDT",
    "ANKRUSDT", "BALUSDT", "CVCUSDT", "KAVAUSDT", "SKLUSDT",
    "CELRUSDT", "CTSIUSDT", "BANDUSDT", "STMXUSDT", "MTLUSDT",
    "NKNUSDT", "RENUSDT", "DGBUSDT", "WRXUSDT", "TWTUSDT",
    "CKBUSDT", "XEMUSDT", "ARDRUSDT", "FUNUSDT", "POWRUSDT",
    "STORJUSDT", "COTIUSDT", "PERLUSDT", "LRCUSDT", "VTHOUSDT",
    "DENTUSDT", "NULSUSDT", "MIRUSDT", "PUNDIXUSDT", "REEFUSDT",
    "BNTUSDT", "SXPUSDT", "TOMOUSDT", "BLZUSDT", "CVCUSDT",
    "FETUSDT", "HOTUSDT", "XVSUSDT", "ZECUSDT", "ZENUSDT"
]



def evaluate_coin(symbol: str, interval: str = "1m"):
    df, source = get_combined_market_data(symbol, interval, symbols)
    if df is None or df.empty:
        logger.error(f"[{symbol}] No data found for interval {interval}")
        return None, None, None

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
            return "HOLD", None, None

        latest_rsi = rsi.iloc[-1]
        latest_macd = macd.iloc[-1]
        latest_signal = signal_line.iloc[-1]
        latest_upper = upper.iloc[-1]
        latest_lower = lower.iloc[-1]

        logger.debug(f"[{symbol}] Indicators: RSI={latest_rsi}, MACD={latest_macd}, Signal={latest_signal}")

        atr_like = df['close'].pct_change().rolling(14).std().iloc[-1]
        entry_price = latest_price

        # 👇 التعلم الآلي
        trade_data = load_trade_data()
        model = train_model(trade_data)
        if model:
            features = [latest_rsi, latest_macd, atr_like, latest_upper - latest_lower, liquidity]
            ml_signal = predict_signal(model, features)
            if ml_signal == 1:
                signal = "BUY"
            else:
                signal = "HOLD"
        else:
            if latest_rsi < 30 and latest_macd > latest_signal and latest_price < latest_lower and liquidity > 0:
                signal = "BUY"
            elif latest_rsi > 70 and latest_macd < latest_signal and latest_price > latest_upper and liquidity > 0:
                signal = "SELL"
            else:
                signal = "HOLD"

        if signal in ["BUY", "SELL"]:
            stop_loss, take_profit = calculate_entry_exit(entry_price, atr_like, signal)
        else:
            stop_loss, take_profit = None, None

        logger.info(f"[{symbol}] Signal: {signal}, SL: {stop_loss}, TP: {take_profit}")
        return signal, stop_loss, take_profit

    except Exception as e:
        logger.error(f"[{symbol}] Error while calculating indicators: {e}")
        return None, None, None


def evaluate_coin_multi_timeframe(symbol: str, intervals: list, weights: dict = None):
    if weights is None:
        weights = {"1m": 1, "5m": 2, "15m": 3, "1h": 4, "4h": 5}

    votes = {"BUY": 0, "SELL": 0, "HOLD": 0}
    details = {}
    last_sl = None
    last_tp = None

    for interval in intervals:
        logger.info(f"Processing {symbol} on interval {interval}")
        signal, sl, tp = evaluate_coin(symbol, interval)
        details[interval] = signal or "HOLD"
        votes[details[interval]] += weights.get(interval, 1)

        if signal in ["BUY", "SELL"]:
            last_sl = sl
            last_tp = tp

    final = max(votes, key=votes.get)
    return final, details, votes, last_sl, last_tp


if __name__ == "__main__":
    for symbol in symbols:
        final, detail, votes, sl, tp = evaluate_coin_multi_timeframe(symbol, ["1m", "5m", "1h", "4h", "1d"])
        print(f"\n✅ Final signal for {symbol}: {final}")
        print("📊 Details:", detail)
        print("📈 Votes:", votes)
        if final in ["BUY", "SELL"]:
            print(f"🎯 Entry SL: {sl:.4f} | TP: {tp:.4f}")
