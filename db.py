# db.py
import os
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

# يمكنك تغيير نوع القاعدة لاحقًا (مثل PostgreSQL) بتغيير هذا الرابط
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

Base = declarative_base()
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

class AnalysisResult(Base):
    __tablename__ = 'analysis_results'

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)

    # المؤشرات الفنية
    rsi = Column(Float, nullable=True)
    macd = Column(Float, nullable=True)
    macd_signal = Column(Float, nullable=True)
    bb_upper = Column(Float, nullable=True)
    bb_lower = Column(Float, nullable=True)
    liquidity = Column(Float, nullable=True)
    atr = Column(Float, nullable=True)

    # معلومات الإشارة
    signal = Column(Integer)  # 1 = BUY, -1 = SELL
    source = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# إنشاء الجداول عند تشغيل السكربت
Base.metadata.create_all(engine)
