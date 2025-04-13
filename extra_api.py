import pandas as pd
import requests

def get_coinbase_market_data(symbol, interval, limit=100):
    try:
        pair = symbol.replace("USDT", "-USD")
        granularity = {"1m": 60, "5m": 300, "15m": 900, "1h": 3600}.get(interval, 3600)
        url = f"https://api.pro.coinbase.com/products/{pair}/candles?granularity={granularity}"
        res = requests.get(url, timeout=10)
        data = res.json()
        if isinstance(data, list):
            df = pd.DataFrame(data, columns=["timestamp", "low", "high", "open", "close", "volume"])
            df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
            return df[::-1]
        return None
    except Exception as e:
        print(f"Coinbase error: {e}")
        return None
