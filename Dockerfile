# استخدم صورة Python الرسمية
FROM python:3.10-slim

# تثبيت بعض الأدوات الأساسية
RUN apt-get update && apt-get install -y build-essential libffi-dev libssl-dev curl git

# إعداد مجلد التطبيق
WORKDIR /app

# نسخ الملفات
COPY . /app

# تثبيت المتطلبات
RUN pip install --upgrade pip
# نسخ ملفات المتطلبات
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --timeout 3000 -r requirements.txt



CMD ["python", "main.py"]
