# سنجرب استخدام ids_map وsymbol_map للتحقق من أن جميع الرموز موجودة ولها قيم صالحة.

# القوائم المحدّثة من CoinGecko و Coinbase
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

# قائمة الرموز الكاملة التي سيتم التحقق منها
symbols = list(ids_map.keys())

# الدالة التي تختبر صلاحية الرموز في كلا القاموسين
def test_symbols(symbols, ids_map, symbol_map):
    missing_in_ids = []
    missing_in_symbols = []
    for symbol in symbols:
        if symbol not in ids_map:
            missing_in_ids.append(symbol)
        if symbol not in symbol_map:
            missing_in_symbols.append(symbol)
    return missing_in_ids, missing_in_symbols

# تجربة الرموز
missing_in_ids, missing_in_symbol_map = test_symbols(symbols, ids_map, symbol_map)
missing_in_ids, missing_in_symbol_map

