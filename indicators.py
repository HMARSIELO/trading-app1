# indicators.py
import pandas as pd
import talib
import numpy as np

def calculate_rsi(data: pd.DataFrame, period: int = 14):
    close = data['close'].values.astype(float)
    return talib.RSI(close, timeperiod=period)

def calculate_macd(data: pd.DataFrame, fastperiod=12, slowperiod=26, signalperiod=9):
    close = data['close'].values.astype(float)
    macd, signal, hist = talib.MACD(close, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    return macd, signal, hist

def calculate_bollinger_bands(data: pd.DataFrame, period=20, nbdevup=2, nbdevdn=2):
    close = data['close'].values.astype(float)
    upper, middle, lower = talib.BBANDS(close, timeperiod=period, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return upper, middle, lower

def calculate_atr(data: pd.DataFrame, period=14):
    high = data['high'].values.astype(float)
    low = data['low'].values.astype(float)
    close = data['close'].values.astype(float)
    atr = talib.ATR(high, low, close, timeperiod=period)
    return atr[-1] if len(atr) > 0 else None

def calculate_pivot_points(data: pd.DataFrame):
    last = data.iloc[-1]
    pivot = (last['high'] + last['low'] + last['close']) / 3
    support1 = (2 * pivot) - last['high']
    resistance1 = (2 * pivot) - last['low']
    support2 = pivot - (last['high'] - last['low'])
    resistance2 = pivot + (last['high'] - last['low'])
    return pivot, support1, resistance1, support2, resistance2

def calculate_liquidity(data: pd.DataFrame, period=20):
    if len(data) < period:
        return 0
    rolling_vol = data['volume'].rolling(window=period).mean()
    return rolling_vol.iloc[-1] if rolling_vol.notnull().all() else 0
