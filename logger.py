import logging

# إعداد التسجيل (logger)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# تنسيق السجلات
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# مخرج السجل إلى الشاشة
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# التأكد من عدم تكرار الـ handler
if not logger.hasHandlers():
    logger.addHandler(console_handler)
