import pandas as pd
from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET

client = Client(api_key=BINANCE_API_KEY, api_secret=BINANCE_API_SECRET)

def get_market_data(symbol, interval, limit=100):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(klines, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "trades",
            "taker_base", "taker_quote", "ignore"
        ])
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"Binance error: {e}")
        return None

def get_all_binance_symbols():
    try:
        info = client.get_exchange_info()
        return [s['symbol'] for s in info['symbols'] if s['symbol'].endswith("USDT")]
    except Exception as e:
        print(f"Binance symbol error: {e}")
        return []
