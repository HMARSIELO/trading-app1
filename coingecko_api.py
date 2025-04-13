import pandas as pd
import requests

def get_coingecko_market_data(symbol, interval=None, limit=100):
    try:
        ids_map = {
            "BTCUSDT": "bitcoin", "ETHUSDT": "ethereum", "BNBUSDT": "binancecoin"
            # أضف المزيد حسب الحاجة
        }
        id = ids_map.get(symbol)
        if not id:
            print(f"CoinGecko mapping missing for symbol: {symbol}")
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

def get_top_symbols(limit=30):
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets"
        params = {
            "vs_currency": "usd",
            "order": "market_cap_desc",
            "per_page": limit,
            "page": 1,
            "sparkline": False
        }
        res = requests.get(url, params=params, timeout=10)
        coins = res.json()

        symbols = []
        for coin in coins:
            symbol = coin['symbol'].upper()
            symbols.append(f"{symbol}USDT")
        return symbols
    except Exception as e:
        print(f"CoinGecko Top Symbols Error: {e}")
        return []
