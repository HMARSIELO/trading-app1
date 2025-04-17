# CoinGecko ID mapping
ids_map = {
    "BTCUSDT": "bitcoin",
    "ETHUSDT": "ethereum",
    "BNBUSDT": "binancecoin",
    "SOLUSDT": "solana",
    "XRPUSDT": "ripple",
    "DOGEUSDT": "dogecoin",
    "ADAUSDT": "cardano",
    "AVAXUSDT": "avalanche-2",
    "TONUSDT": "toncoin",
    "DOTUSDT": "polkadot",
    "TRXUSDT": "tron",
    "LINKUSDT": "chainlink",
    "MATICUSDT": "matic-network",
    "SHIBUSDT": "shiba-inu",
    "BCHUSDT": "bitcoin-cash",
    "LTCUSDT": "litecoin",
    "NEARUSDT": "near",
    "ICPUSDT": "internet-computer",
    "UNIUSDT": "uniswap",
    "APTUSDT": "aptos",
    "ETCUSDT": "ethereum-classic",
    "STXUSDT": "stacks",
    "IMXUSDT": "immutable-x",
    "INJUSDT": "injective-protocol",
    "FILUSDT": "filecoin",
    "HBARUSDT": "hedera-hashgraph",
    "ARBUSDT": "arbitrum",
    "OPUSDT": "optimism",
    "RUNEUSDT": "thorchain",
    "VETUSDT": "vechain"
}

# Coinbase pair mapping
symbol_map = {
    "BTCUSDT": "BTC-USD",
    "ETHUSDT": "ETH-USD",
    "BNBUSDT": "BNB-USD",
    "SOLUSDT": "SOL-USD",
    "XRPUSDT": "XRP-USD",
    "DOGEUSDT": "DOGE-USD",
    "ADAUSDT": "ADA-USD",
    "AVAXUSDT": "AVAX-USD",
    "TONUSDT": "TON-USD",
    "DOTUSDT": "DOT-USD",
    "TRXUSDT": "TRX-USD",
    "LINKUSDT": "LINK-USD",
    "MATICUSDT": "MATIC-USD",
    "SHIBUSDT": "SHIB-USD",
    "BCHUSDT": "BCH-USD",
    "LTCUSDT": "LTC-USD",
    "NEARUSDT": "NEAR-USD",
    "ICPUSDT": "ICP-USD",
    "UNIUSDT": "UNI-USD",
    "APTUSDT": "APT-USD",
    "ETCUSDT": "ETC-USD",
    "STXUSDT": "STX-USD",
    "IMXUSDT": "IMX-USD",
    "INJUSDT": "INJ-USD",
    "FILUSDT": "FIL-USD",
    "HBARUSDT": "HBAR-USD",
    "ARBUSDT": "ARB-USD",
    "OPUSDT": "OP-USD",
    "RUNEUSDT": "RUNE-USD",
    "VETUSDT": "VET-USD"
}

# دالة موحدة للحصول على معرف CoinGecko ورمز Coinbase
def get_coin_ids(symbol):
    if symbol not in ids_map or symbol not in symbol_map:
        print(f"⚠️ الرمز {symbol} غير موجود في الخرائط.")
        return None
    return {
        "coingecko_id": ids_map[symbol],
        "coinbase_symbol": symbol_map[symbol]
    }

# مثال على الاستخدام:
# coin_info = get_coin_ids("BTCUSDT")
# if coin_info:
#     print(coin_info["coingecko_id"])     # bitcoin
#     print(coin_info["coinbase_symbol"])  # BTC-USD
