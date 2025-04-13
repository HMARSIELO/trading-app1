import pandas as pd
import requests

def get_coingecko_market_data(symbol, interval=None, limit=100):
    try:
        ids_map = {
            "BTCUSDT": "bitcoin", "ETHUSDT": "ethereum", "BNBUSDT": "binancecoin"
            # أضف ما تحتاجه
        }
        id = ids_map.get(symbol)
        if not id:
            return None

        url = f"https://api.coingecko.com/api/v3/coins/{id}/market_chart"
        res = requests.get(url, params={"vs_currency": "usd", "days": "1", "interval": "minute"}, timeout=10)
        prices = res.json().get("prices")
        if prices:
            df = pd.DataFrame(prices, columns=["timestamp", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms").astype(int) / 10**9
            df["open"] = df["high"] = df["low"] = df["close"]
            df["volume"] = 0.0
            df = df[["timestamp", "open", "high", "low", "close", "volume"]]
            return df
        return None
    except Exception as e:
        print(f"CoinGecko error: {e}")
        return None
