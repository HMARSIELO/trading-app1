import pandas as pd
import pandas_ta as ta


def calculate_rsi(df, period=14):
    if df is None or df.empty or len(df) < period:
        return pd.Series()
    return ta.rsi(df['close'], length=period)


def calculate_macd(df):
    if df is None or df.empty or len(df) < 35:
        return pd.Series(), pd.Series(), pd.Series()
    macd_result = ta.macd(df['close'], fast=12, slow=26, signal=9)
    return (
        macd_result['MACD_12_26_9'],
        macd_result['MACDs_12_26_9'],
        macd_result['MACDh_12_26_9']
    )


def calculate_bollinger(df, period=20):
    if df is None or df.empty or len(df) < period:
        return pd.Series(), pd.Series(), pd.Series()
    bbands = ta.bbands(df['close'], length=period)
    return (
        bbands['BBU_20_2.0'],
        bbands['BBM_20_2.0'],
        bbands['BBL_20_2.0']
    )


def calculate_liquidity(df, period=20):
    if df is None or df.empty or len(df) < period:
        return 0
    avg_volume = df['volume'].tail(period).mean()
    return avg_volume


def calculate_pivot_points(df):
    if df is None or df.empty:
        return 0, 0, 0, 0, 0
    latest = df.iloc[-1]
    high = latest['high']
    low = latest['low']
    close = latest['close']

    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    s1 = 2 * pivot - high
    r2 = pivot + (r1 - s1)
    s2 = pivot - (r1 - s1)
    return pivot, s1, r1, s2, r2


def calculate_atr(df, period=14):
    if df is None or df.empty or len(df) < period:
        return None
    atr_series = ta.atr(high=df['high'], low=df['low'], close=df['close'], length=period)
    return atr_series.iloc[-1] if atr_series is not None else None
