import time
from extra_api import get_coinbase_market_data
from coingecko_api import get_top_symbols
from logger import logger

def get_combined_market_data(symbol, interval, symbols):
    sources = [
        (get_coinbase_market_data, "Coinbase"),
        (get_top_symbols, "CoinGecko"),
    ]

    for fetch_func, name in sources:
        logger.info(f"🔍 تجربة المصدر: {name} لـ {symbol}")
        df = fetch_func(symbol, interval, symbols)
        if df is not None and not df.empty:
            logger.info(f"✅ تم استخدام المصدر {name} لـ {symbol}")
            return df, name
        else:
            logger.warning(f"❌ فشل المصدر {name} لـ {symbol}")
    logger.error(f"🚫 جميع المحاولات فشلت لجلب {symbol}")
    return None, "None"

def chunk_list(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]

def process_symbols_in_batches(symbols, interval, batch_size=20, sleep_between_batches=3):
    all_results = []

    for batch in chunk_list(symbols, batch_size):
        logger.info(f"📦 بدء دفعة جديدة: {batch}")
        for symbol in batch:
            try:
                df, source = get_combined_market_data(symbol, interval, symbols)
                if df is not None:
                    all_results.append((symbol, df, source))
            except Exception as e:
                logger.error(f"⚠️ خطأ أثناء معالجة {symbol}: {e}")

        # راحة قصيرة بين الدفعات
        time.sleep(sleep_between_batches)

    return all_results
