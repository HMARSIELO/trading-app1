import pandas_ta as ta
def calculate_entry_exit(entry_price: float, atr_value: float, signal: str):
    """
    يحسب مستويات الدخول ووقف الخسارة وجني الأرباح بناءً على الإشارة و ATR.
    """
    if atr_value is None or entry_price is None or signal not in ["BUY", "SELL"]:
        return entry_price, entry_price  # fallback

    if signal == "BUY":
        stop_loss = entry_price - atr_value * 1.5
        take_profit = entry_price + atr_value * 2
    elif signal == "SELL":
        stop_loss = entry_price + atr_value * 1.5
        take_profit = entry_price - atr_value * 2
    else:
        stop_loss = entry_price
        take_profit = entry_price

    return stop_loss, take_profit
