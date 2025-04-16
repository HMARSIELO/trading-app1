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
