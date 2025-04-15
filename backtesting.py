import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from indicators import (
    calculate_rsi, calculate_macd, calculate_bollinger,
    calculate_liquidity, calculate_pivot_points
)

def load_historical_data(file_path: str) -> pd.DataFrame:
    """
    تحميل البيانات التاريخية من ملف CSV وتحويلها إلى DataFrame.
    يُفترض أن يحتوي الملف على عمود 'close' لأسعار الإغلاق.
    """
    df = pd.read_csv(file_path)
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    return df

def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    تطبيق الاستراتيجية على البيانات التاريخية باستخدام جميع المؤشرات المتاحة.
    """
    df['RSI'] = calculate_rsi(df, period=14)
    macd, macd_signal = calculate_macd(df)
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['BB_upper'], df['BB_lower'] = calculate_bollinger(df)

    df['Liquidity'] = calculate_liquidity(df)
    df['Pivot'], df['S1'], df['R1'], df['S2'], df['R2'] = calculate_pivot_points(df)

    df['ATR_like'] = df['close'].pct_change().rolling(14).std()

    df['Signal'] = np.where(
        (df['RSI'] < 30) &
        (df['MACD'] > df['MACD_signal']) &
        (df['close'] < df['BB_lower']) &
        (df['Liquidity'] > 0),
        "BUY", "HOLD"
    )

    return df

def simulate_trades(df: pd.DataFrame, initial_balance: float = 1000.0):
    """
    محاكاة تداولات بسيطة بناءً على إشارات الاستراتيجية.
    """
    balance = initial_balance
    balance_history = []
    position = 0
    entry_price = 0

    for index, row in df.iterrows():
        signal = row['Signal']
        price = row['close']

        if signal == "BUY" and position == 0:
            entry_price = price
            position = 1
            print(f"شراء عند {price} في index {index}")
        elif position == 1 and price >= entry_price * 1.03:
            profit = (price - entry_price)
            balance += profit
            position = 0
            print(f"بيع عند {price} في index {index}، ربح: {profit:.2f}")
        balance_history.append(balance)

    df['Balance'] = balance_history
    return df, balance

def plot_results(df: pd.DataFrame):
    """
    عرض النتائج: رسم بياني للرصيد عبر الزمن.
    """
    plt.figure(figsize=(12,6))
    plt.plot(df['Balance'], label='Balance')
    plt.title("محاكاة أداء الاستراتيجية")
    plt.xlabel("عدد الفترات")
    plt.ylabel("الرصيد")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    file_path = "historical_data.csv"  # تأكد من وجود هذا الملف
    try:
        data = load_historical_data(file_path)
    except Exception as e:
        print(f"خطأ في تحميل البيانات: {e}")
        exit(1)

    data = apply_strategy(data)
    data, final_balance = simulate_trades(data, initial_balance=1000.0)
    print(f"الرصيد النهائي: {final_balance:.2f}")
    plot_results(data)
