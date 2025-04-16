import pandas as pd
import requests
from symbol_mapper import symbol_map
from logger import logger

def get_coinbase_market_data(symbol, interval, symbols):
    try:
        logger.info(f"📡 محاولة جلب بيانات {symbol} من Coinbase")
        pair = symbol_map.get(symbol, symbol.replace("USDT", "-USD"))
        granularity = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}.get(interval, 3600)
        url = f"https://api.pro.coinbase.com/products/{pair}/candles?granularity={granularity}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if isinstance(data, list):
            logger.info(f"✅ تم جلب بيانات {symbol} من Coinbase بنجاح")
            df = pd.DataFrame(data, columns=["timestamp", "low", "high", "open", "close", "volume"])
            df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
            return df[::-1]
        logger.warning(f"⚠️ Coinbase أعاد استجابة غير متوقعة لـ {symbol}")
        return None
    except Exception as e:
        logger.error(f"❌ Coinbase فشل في جلب {symbol}: {e}")
        return None
