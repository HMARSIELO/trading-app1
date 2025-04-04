# binance_api.py
import pandas as pd
from binance.client import Client
from config import BINANCE_API_KEY, BINANCE_API_SECRET
from extra_api import get_coinbase_market_data
from coingecko_api import get_coingecko_market_data

# تهيئة عميل Binance مع مهلة 20 ثانية
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, requests_params={'timeout': 20})

def get_market_data(symbol: str, interval: str, limit: int = 100):
    """
    جلب بيانات السوق من Binance أو Coinbase أو CoinGecko.
    """
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        columns = ["timestamp", "open", "high", "low", "close", "volume",
                   "close_time", "quote_asset_volume", "trades",
                   "taker_base", "taker_quote", "ignore"]
        df = pd.DataFrame(klines, columns=columns)
        df = df[["timestamp", "open", "high", "low", "close", "volume"]].astype(float)
        return df
    except Exception as e:
        print(f"Error retrieving market data for {symbol} from Binance: {e}")
        # تجربة Coinbase كمصدر بديل

      
        # تجربة CoinGecko إذا فشلت جميع المصادر
        df_gecko = get_coingecko_market_data(symbol, interval, limit)
        if df_gecko is not None:
            return df_gecko
    
        df_alt = get_coinbase_market_data(symbol, interval, limit)
        return df_alt  
    
    return None


def get_my_trades(symbol: str):
    """
    جلب بيانات الصفقات المنفذة من حساب Binance.
    """
    try:
        trades = client.get_my_trades(symbol=symbol)
        return trades
    except Exception as e:
        print(f"Error retrieving trades for {symbol}: {e}")
        return None

if __name__ == "__main__":
    symbol = "BTCUSDT"
    data = get_market_data(symbol, interval="1m", limit=10)
    if data is not None:
        print("Binance (or Coinbase) Market Data:")
        print(data.head())
    trades = get_my_trades(symbol)
    if trades:
        print("My Trades (sample):")
        print(trades[:5])
def get_all_binance_symbols():
    """
    جلب جميع أزواج التداول من Binance.
    """
    try:
        exchange_info = client.get_exchange_info()
        symbols = [s["symbol"] for s in exchange_info["symbols"] if s["status"] == "TRADING"]
        return symbols
    except Exception as e:
        print(f"Error retrieving Binance symbols: {e}")
        return []

if __name__ == "__main__":
    symbols = get_all_binance_symbols()[:5]  # تجربة 5 عملات فقط
    for symbol in symbols:
        print(f"Fetching data for {symbol}...")
        data = get_market_data(symbol, interval="1m", limit=10)
        if data is not None:
            print(data.head())