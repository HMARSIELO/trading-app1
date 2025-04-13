FROM python:3.10

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ المتطلبات
COPY requirements.txt .

# تثبيت الأدوات الأساسية مع تنظيف بعد التثبيت
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    curl \
    git \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# إعداد مجلد التطبيق
COPY . .

# تثبيت مكتبات Python
RUN pip install --default-timeout=3000 -r requirements.txt


# تشغيل التطبيق
CMD ["python", "main.py"]
