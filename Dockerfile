# استخدم صورة Python الرسمية كقاعدة
FROM python:3.9-slim

# تعيين متغير البيئة لمنع إنشاء ملفات .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# تعيين متغير البيئة لضمان إخراج سلس في التيرمينال
ENV PYTHONUNBUFFERED 1

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات
COPY requirements.in .

# تثبيت pip-tools لإدارة الإصدارات
RUN pip install pip-tools

# توليد requirements.txt مع الإصدارات
RUN pip-compile requirements.in

# نسخ باقي ملفات المشروع إلى الحاوية
COPY . .

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt


# تحديد الأمر الافتراضي لتشغيل التطبيق
CMD ["python", "main.py"]
