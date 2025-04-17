import logging
import time
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from trading_signals import evaluate_coin_multi_timeframe, symbols
from telegram_bot import send_message
from config import UPDATE_INTERVAL_SECONDS
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger,
    calculate_liquidity, calculate_atr
)
from db import SessionLocal, AnalysisResult
from unified_collector import get_combined_market_data

logging.basicConfig(level=logging.INFO)

# دالة لتقسيم القائمة إلى دفعات
def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def scheduled_task():
    coins = symbols
    if not coins:
        logging.error("❌ لم يتم استرجاع قائمة العملات.")
        return

    intervals = ["1m", "5m", "1h", "4h", "1d"]
    weights = {"1m": 1, "5m": 2, "1h": 3, "4h": 4, "1d": 5}

    batch_size = 20  # عدد العملات في كل دفعة
    for batch in chunk_list(coins, batch_size):
        logging.info(f"🚀 بدء تحليل دفعة جديدة: {batch}")
        for coin in batch:
            try:
                final_signal, details, votes = evaluate_coin_multi_timeframe(coin, intervals, weights)
                if final_signal in ["BUY", "SELL"]:
                    df, source = get_combined_market_data(coin, interval="1h", symbols=coins)
                    if df is not None and not df.empty:
                        df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
                        latest = df.iloc[-1]
                        entry_price = latest['close']

                        # المؤشرات الفنية
                        rsi = calculate_rsi(df)
                        macd, signal_line, _ = calculate_macd(df)
                        bb_upper, _, bb_lower = calculate_bollinger(df)
                        liquidity = calculate_liquidity(df)
                        atr = calculate_atr(df)

                        stop_loss = entry_price - atr * 1.5 if final_signal == "BUY" else entry_price + atr * 1.5
                        take_profit = entry_price + atr * 2 if final_signal == "BUY" else entry_price - atr * 2

                        msg = (
                            f"📢 إشارة {final_signal} لـ {coin}\n"
                            f"📊 المصدر: {source}\n"
                            f"الفريمات: {intervals}\n"
                            f"التفاصيل: {details}\n"
                            f"الدخول: {entry_price:.2f}\n"
                            f"وقف الخسارة: {stop_loss:.2f}\n"
                            f"جني الأرباح: {take_profit:.2f}\n"
                            f"الأوزان: {votes}"
                        )

                        logging.info(msg)
                        send_message(msg)

                        db = SessionLocal()
                        result = AnalysisResult(
                            symbol=coin,
                            rsi=rsi.iloc[-1] if not rsi.empty else None,
                            macd=macd.iloc[-1] if not macd.empty else None,
                            macd_signal=signal_line.iloc[-1] if not signal_line.empty else None,
                            bb_upper=bb_upper.iloc[-1] if not bb_upper.empty else None,
                            bb_lower=bb_lower.iloc[-1] if not bb_lower.empty else None,
                            liquidity=liquidity,
                            atr=atr,
                            signal=1 if final_signal == "BUY" else -1,
                            source=source,
                            timestamp=datetime.utcnow()
                        )
                        db.add(result)
                        db.commit()
                        db.close()
            except Exception as e:
                logging.error(f"⚠️ خطأ أثناء معالجة {coin}: {e}")

        logging.info("⏸️ راحة قصيرة قبل الدفعة التالية...")
        time.sleep(3)

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_task, "interval", seconds=UPDATE_INTERVAL_SECONDS)
    scheduler.start()

if __name__ == "__main__":
    start_scheduler()
