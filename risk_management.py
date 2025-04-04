# risk_management.py
import pandas as pd
import talib

from indicators import calculate_atr

def calculate_trade_size_advanced(account_balance: float, risk_percentage: float,
                                  entry_price: float, data: pd.DataFrame) -> float:
    """
    حساب حجم الصفقة باستخدام ATR لتحديد وقف الخسارة.
    """
    atr_value = calculate_atr(data, period=14)
    if atr_value is None:
        raise ValueError("ATR calculation failed or no data available.")

    # نفترض أننا في صفقة شراء؛ وقف الخسارة تحت سعر الدخول بمقدار ATR
    stop_loss_price = entry_price - atr_value
    stop_loss_distance = abs(entry_price - stop_loss_price)
    if stop_loss_distance == 0:
        raise ValueError("Stop loss distance must be > 0.")

    risk_amount = account_balance * risk_percentage
    trade_size = risk_amount / stop_loss_distance
    return trade_size

if __name__ == "__main__":
    # مثال تجريبي
    data = pd.DataFrame({
        'high':  [101, 102, 103, 104, 105],
        'low':   [95,  96,  97,  98,  99],
        'close': [100, 101, 102, 103, 104],
        'volume':[10,  12,  15,  11,  20]
    })
    balance = 1000.0
    risk_perc = 0.02
    entry = 102.0
    size = calculate_trade_size_advanced(balance, risk_perc, entry, data)
    print(f"Trade size: {size:.4f} units")
