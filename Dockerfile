# استخدام صورة Python الرسمية
FROM python:3.9-slim

# إعداد متغيرات البيئة
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# تثبيت المتطلبات الأساسية للنظام
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    gcc \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    libtool \
    autoconf \
    pkg-config \
    libglib2.0-dev \
    libsm6 \
    libxext6 \
    libxrender-dev

# تحميل و بناء مكتبة TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xvzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# إعداد مجلد العمل
WORKDIR /app

# نسخ متطلبات المشروع
COPY requirements.in .

# تثبيت pip-tools
RUN pip install pip-tools

# إنشاء ملف requirements.txt
RUN pip-compile requirements.in

# نسخ ملفات المشروع
COPY . .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# الأمر الإفتراضي لتشغيل التطبيق
CMD ["python", "main.py"]