# backtesting.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from indicators import calculate_rsi, calculate_macd, calculate_bollinger

def load_historical_data(file_path: str) -> pd.DataFrame:
    """
    تحميل البيانات التاريخية من ملف CSV وتحويلها إلى DataFrame.
    يُفترض أن يحتوي الملف على عمود 'close' لأسعار الإغلاق.
    """
    df = pd.read_csv(file_path)
    # التأكد من تحويل أسعار الإغلاق إلى قيم رقمية
    df['close'] = pd.to_numeric(df['close'], errors='coerce')
    return df

def apply_strategy(df: pd.DataFrame) -> pd.DataFrame:
    """
    تطبيق الاستراتيجية على البيانات التاريخية.
    - حساب المؤشرات الفنية (RSI, MACD, بولينجر باند).
    - توليد إشارة تداول بناءً على منطق بسيط: إشارة "BUY" إذا كان RSI < 30 و MACD > MACD_signal، وإلا "HOLD".
    
    تُضاف الأعمدة 'RSI', 'MACD', 'MACD_signal', 'BB_upper', 'BB_lower', و 'Signal' إلى DataFrame.
    """
    df['RSI'] = calculate_rsi(df, period=14)
    macd, macd_signal = calculate_macd(df)
    df['MACD'] = macd
    df['MACD_signal'] = macd_signal
    df['BB_upper'], df['BB_lower'] = calculate_bollinger(df)
    
    # توليد الإشارات: إذا كان RSI أقل من 30 وMACD أكبر من MACD_signal => "BUY"، وإلا "HOLD"
    df['Signal'] = np.where((df['RSI'] < 30) & (df['MACD'] > df['MACD_signal']), "BUY", "HOLD")
    return df

def simulate_trades(df: pd.DataFrame, initial_balance: float = 1000.0):
    """
    محاكاة تداولات بسيطة بناءً على إشارات الاستراتيجية.
    - نفترض أن كل صفقة شراء تُنفذ بسعر الإغلاق.
    - يتم حساب تغير الرصيد عند كل صفقة شراء.
    - تُرجع النتائج النهائية والرصيد عبر الزمن.
    
    ملاحظة: هذه محاكاة مبسطة جدًا لأغراض الاختبار.
    """
    balance = initial_balance
    balance_history = []
    position = 0  # 0: لا توجد صفقة مفتوحة، 1: صفقة مفتوحة
    entry_price = 0
    
    for index, row in df.iterrows():
        signal = row['Signal']
        price = row['close']
        
        # إذا كانت الإشارة BUY ولم تكن هناك صفقة مفتوحة
        if signal == "BUY" and position == 0:
            entry_price = price
            position = 1
            print(f"شراء عند {price} في index {index}")
        # إذا كانت الصفقة مفتوحة وتغير السعر بشكل إيجابي (مثال: أخذ ربح افتراضي عند ارتفاع السعر بنسبة 3%)
        elif position == 1 and price >= entry_price * 1.03:
            profit = (price - entry_price)
            balance += profit
            position = 0  # إغلاق الصفقة
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

# اختبار الوحدة عند تشغيل الملف مباشرة
if __name__ == "__main__":
    # نفترض وجود ملف بيانات تاريخية باسم 'historical_data.csv'
    # يجب أن يحتوي الملف على عمود 'close' على الأقل.
    file_path = "historical_data.csv"  # قم بتحديث المسار حسب ملفك
    try:
        data = load_historical_data(file_path)
    except Exception as e:
        print(f"خطأ في تحميل البيانات: {e}")
        exit(1)
    
    data = apply_strategy(data)
    data, final_balance = simulate_trades(data, initial_balance=1000.0)
    print(f"الرصيد النهائي: {final_balance:.2f}")
    plot_results(data)
