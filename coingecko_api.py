import pandas as pd
import requests
from symbol_mapper import ids_map
from logger import logger

def get_top_symbols(symbol, interval=None, symbols=None):
    try:
        logger.info(f"📡 محاولة جلب بيانات {symbol} من CoinGecko")
        id = ids_map.get(symbol)
        if not id:
            logger.warning(f"🚫 لا يوجد ID مطابق لـ {symbol} في CoinGecko")
            return None

        url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart"
        res = requests.get(url, params={"vs_currency": "usd", "days": "1", "interval": "minute"}, timeout=10)
        prices = res.json().get("prices")
        if prices:
            logger.info(f"✅ تم جلب بيانات {symbol} من CoinGecko بنجاح")
            df = pd.DataFrame(prices, columns=["timestamp", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").astype(int) / 10**9
            df["open"] = df["high"] = df["low"] = df["close"]
            df["volume"] = 0.0
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]
            return df
        logger.warning(f"⚠️ لم يتم العثور على بيانات {symbol} في CoinGecko")
        return None
    except Exception as e:
        logger.error(f"❌ CoinGecko فشل في جلب {symbol}: {e}")
        return None
