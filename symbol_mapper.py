# symbol_mapper.py

# CoinGecko ID Map
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
    "MATICUSDT": "polygon",
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
    "XLMUSDT": "stellar",
    "ATOMUSDT": "cosmos",
    "SANDUSDT": "the-sandbox",
    "MANAUSDT": "decentraland",
    "AAVEUSDT": "aave",
    "GRTUSDT": "the-graph",
    "EOSUSDT": "eos",
    "XTZUSDT": "tezos",
    "SNXUSDT": "synthetix-network-token",
    "CRVUSDT": "curve-dao-token",
    "1INCHUSDT": "1inch",
    "ENJUSDT": "enjincoin",
    "ZILUSDT": "zilliqa",
    "BATUSDT": "basic-attention-token",
    "CHZUSDT": "chiliz",
    "KSMUSDT": "kusama",
    "YFIUSDT": "yearn-finance",
    "COMPUSDT": "compound-governance-token",
    "ZRXUSDT": "0x",
    "ALGOUSDT": "algorand",
    "DASHUSDT": "dash"
}

# Coinbase Symbol Map
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
    "XLMUSDT": "XLM-USD",
    "ATOMUSDT": "ATOM-USD",
    "SANDUSDT": "SAND-USD",
    "MANAUSDT": "MANA-USD",
    "AAVEUSDT": "AAVE-USD",
    "GRTUSDT": "GRT-USD",
    "EOSUSDT": "EOS-USD",
    "XTZUSDT": "XTZ-USD",
    "SNXUSDT": "SNX-USD",
    "CRVUSDT": "CRV-USD",
    "1INCHUSDT": "1INCH-USD",
    "ENJUSDT": "ENJ-USD",
    "ZILUSDT": "ZIL-USD",
    "BATUSDT": "BAT-USD",
    "CHZUSDT": "CHZ-USD",
    "KSMUSDT": "KSM-USD",
    "YFIUSDT": "YFI-USD",
    "COMPUSDT": "COMP-USD",
    "ZRXUSDT": "ZRX-USD",
    "ALGOUSDT": "ALGO-USD",
    "DASHUSDT": "DASH-USD"
}

# الرموز الموحدة
symbols = list(ids_map.keys())

# فحص صحة الرموز
def test_symbols(symbols, ids_map, symbol_map):
    missing_in_ids = [s for s in symbols if s not in ids_map]
    missing_in_symbols = [s for s in symbols if s not in symbol_map]
    return missing_in_ids, missing_in_symbols

# التحقق التلقائي عند التشغيل
if __name__ == "__main__":
    missing_ids, missing_symbols = test_symbols(symbols, ids_map, symbol_map)
    if missing_ids or missing_symbols:
        print("❌ رموز مفقودة:")
        if missing_ids:
            print("في ids_map:", missing_ids)
        if missing_symbols:
            print("في symbol_map:", missing_symbols)
    else:
        print("✅ جميع الرموز صحيحة وموجودة.")
