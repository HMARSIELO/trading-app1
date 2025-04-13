from binance_api import get_market_data
from extra_api import get_coinbase_market_data
from coingecko_api import get_coingecko_market_data

def get_combined_market_data(symbol, interval, limit=150):
    for fetch in [get_market_data, get_coinbase_market_data, get_coingecko_market_data]:
        df = fetch(symbol, interval, limit)
        if df is not None and not df.empty:
            return df
    return None
