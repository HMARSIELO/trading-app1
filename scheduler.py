import logging
import requests
from apscheduler.schedulers.blocking import BlockingScheduler

from trading_signals import evaluate_coin_multi_timeframe
from telegram_bot import send_message
from config import UPDATE_INTERVAL_SECONDS
from binance_api import get_market_data
from indicators import calculate_atr
import logging
from numpy import NaN as npNaN


logging.basicConfig(level=logging.DEBUG)


def get_top_150_coins():
    """
    دالة لجلب أفضل 150 زوج تداول ينتهي بـ USDT 
    بناءً على حجم التداول (quoteVolume) خلال 24 ساعة.
    """
    url = "https://api.binance.com/api/v3/ticker/24hr"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        logging.error(f"فشل جلب بيانات 24hr: {e}")
        return []
    
    # تصفية الأزواج التي تنتهي بـ USDT فقط (يمكن تعديل الفلترة حسب الحاجة)
    usdt_pairs = [ticker for ticker in data if ticker.get('symbol', '').endswith("USDT")]
    
    # فرز الأزواج بناءً على حجم التداول (quoteVolume) بشكل تنازلي
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x.get('quoteVolume', 0)), reverse=True)
    
    # اختيار أول 150 زوج
    top_150 = [pair['symbol'] for pair in sorted_pairs[:150]]
    return top_150

def scheduled_task():
    # استبدال القائمة الثابتة للقيم بقائمة أفضل 150 عملة
    coins = get_top_150_coins()
    if not coins:
        logging.error("لم يتم استرجاع قائمة العملات.")
        return

    # الفريمات والوزن لكل فريم
    intervals = ["1m", "5m", "1h"]
    weights = {"1m": 1, "5m": 2, "1h": 3}

    for coin in coins:
        try:
            final_signal, details, votes = evaluate_coin_multi_timeframe(coin, intervals, weights)
            if final_signal in ["BUY", "SELL"]:
                # جلب بيانات فريم 1h لحساب مستويات الدخول والخروج
                df = get_market_data(coin, interval="1h", limit=100)
                if df is not None and not df.empty:
                    df.columns = ["timestamp", "open", "high", "low", "close", "volume"]
                    latest = df.iloc[-1]
                    entry_price = latest['close']
                    atr_value = calculate_atr(df, period=14)

                    # حساب وقف الخسارة وجني الأرباح بناءً على قيمة ATR
                    if atr_value is not None:
                        stop_loss = entry_price - atr_value * 1.5 if final_signal == "BUY" else entry_price + atr_value * 1.5
                        take_profit = entry_price + atr_value * 2 if final_signal == "BUY" else entry_price - atr_value * 2
                    else:
                        stop_loss = entry_price - 1
                        take_profit = entry_price + 1

                    msg = (f"إشارة {final_signal} لـ {coin}\n"
                           f"الفريمات: {intervals}\n"
                           f"التفاصيل: {details}\n"
                           f"الدخول: {entry_price:.2f}\n"
                           f"وقف الخسارة: {stop_loss:.2f}\n"
                           f"جني الأرباح: {take_profit:.2f}\n"
                           f"الأوزان: {votes}")

                    logging.info(msg)
                    send_message(msg)

        except Exception as e:
            logging.error(f"Error processing {coin}: {e}")

def start_scheduler():
    scheduler = BlockingScheduler()
    scheduler.add_job(scheduled_task, "interval", seconds=UPDATE_INTERVAL_SECONDS)
    scheduler.start()


if __name__ == "__main__":
    start_scheduler()
