from extra_api import get_coinbase_market_data
from coingecko_api import get_top_symbols

def get_combined_market_data(symbol, interval, limit=150):
    sources = [
        (get_coinbase_market_data, "Coinbase"),
        (get_top_symbols, "CoinGecko"),
    ]
    
    for fetch_func, name in sources:
        df = fetch_func(symbol, interval, limit)
        if df is not None and not df.empty:
            return df, name
    return None, "None"
