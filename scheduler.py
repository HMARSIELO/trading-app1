import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from trading_signals import evaluate_coin_multi_timeframe
from telegram_bot import send_message
from config import UPDATE_INTERVAL_SECONDS
from indicators import calculate_atr
from unified_collector import get_combined_market_data
from coingecko_api import get_top_symbols
from db import SessionLocal, AnalysisResult
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def scheduled_task():
    coins = get_top_symbols(limit=30)
    if not coins:
        logging.error("لم يتم استرجاع قائمة العملات.")
        return

    intervals = ["1m", "5m", "1h"]
    weights = {"1m": 1, "5m": 2, "1h": 3}

    for coin in coins:
        try:
            final_signal, details, votes = evaluate_coin_multi_timeframe(coin, intervals, weights)
            if final_signal in ["BUY", "SELL"]:
                df, source = get_combined_market_data(coin, interval="1h", limit=100)
                if df is not None and not df.empty:
                    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
                    latest = df.iloc[-1]
                    entry_price = latest['close']
                    atr_value = calculate_atr(df, period=14)

                    if atr_value is not None:
                        stop_loss = entry_price - atr_value * 1.5 if final_signal == "BUY" else entry_price + atr_value * 1.5
                        take_profit = entry_price + atr_value * 2 if final_signal == "BUY" else entry_price - atr_value * 2
                    else:
                        stop_loss = entry_price - 1
                        take_profit = entry_price + 1

                    msg = (f"📢 إشارة {final_signal} لـ {coin}\n"
                           f"📊 المصدر: {source}\n"
                           f"الفريمات: {intervals}\n"
                           f"التفاصيل: {details}\n"
                           f"الدخول: {entry_price:.2f}\n"
                           f"وقف الخسارة: {stop_loss:.2f}\n"
                           f"جني الأرباح: {take_profit:.2f}\n"
                           f"الأوزان: {votes}")

                    logging.info(msg)
                    send_message(msg)

                    # ✅ تخزين النتيجة في قاعدة البيانات
                    db = SessionLocal()
                    result = AnalysisResult(
                        symbol=coin,
                        rsi=None,
                        macd=None,
                        signal=1 if final_signal == "BUY" else -1,
                        source=source,
                        timestamp=datetime.utcnow()
                    )
                    db.add(result)
                    db.commit()
                    db.close()

        except Exception as e:
            logging.error(f"Error processing {coin}: {e}")

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_task, "interval", seconds=UPDATE_INTERVAL_SECONDS)
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
