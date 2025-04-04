# main.py
from logger import setup_logging
from scheduler import start_scheduler
from flask import Flask, send_from_directory
def main():
    setup_logging()
    print("بدء تشغيل تطبيق التداول الآلي...")

    start_scheduler()
app = Flask(__name__)

# استضافة الملفات الثابتة (الصورة والصفحة الرئيسية)
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
 
    start_scheduler()
