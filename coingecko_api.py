# coingecko_api.py
import requests
import pandas as pd

def get_coingecko_market_data(symbol: str):
    """
    جلب بيانات السوق لأي عملة من CoinGecko.
    """
    url = f"https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": symbol.lower(),
        "order": "market_cap_desc",
        "per_page": 1,
        "page": 1,
        "sparkline": False
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data:
            return pd.DataFrame(data)
        return None
    except Exception as e:
        print(f"Error retrieving data from CoinGecko for {symbol}: {e}")
        return None
