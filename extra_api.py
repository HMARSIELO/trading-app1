# extra_api.py
import requests
import pandas as pd

def get_coinbase_market_data(symbol: str, interval: str, limit: int = 100):
    """
    جلب بيانات الشموع من Coinbase Pro.
    يقوم بتحويل رمز العملة (مثل BTCUSDT) إلى الصيغة (BTC-USD).
    يحدد granularity بناءً على الفريم.
    """
    coinbase_symbol = symbol.replace("USDT", "-USD")

    # تعيين granularity بناء على الفريم (مثال مبسط)
    if interval == "1m":
        granularity = 60
    elif interval == "5m":
        granularity = 300
    elif interval == "15m":
        granularity = 900
    elif interval == "1h":
        granularity = 3600
    elif interval == "4h":
        granularity = 14400
    else:
        granularity = 86400  # نفترض يومي

    url = f"https://api.pro.coinbase.com/products/{coinbase_symbol}/candles?granularity={granularity}&limit={limit}"
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        # صيغة Coinbase: [time, low, high, open, close, volume]
        df = pd.DataFrame(data, columns=["timestamp", "low", "high", "open", "close", "volume"])
        # إعادة ترتيب الأعمدة للصيغة الموحدة
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"Error retrieving data from Coinbase for {symbol}: {e}")
        return None
