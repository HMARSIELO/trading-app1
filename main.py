from flask import Flask, render_template, request, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import scheduled_task  # أو أي ملف آخر يحتوي على الدالة
import os
import logging

app = Flask(__name__)
app.secret_key = "secret_key"  # استبدلها بمفتاح حقيقي في الإنتاج
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', seconds=300)  # كل 5 دقائق
scheduler.start()

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

@app.route('/')
def login_page():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "admin" and password == "admin123":
        session['logged_in'] = True
        return redirect(url_for('analysis'))
    return "اسم المستخدم أو كلمة المرور غير صحيحة"

@app.route('/analysis')
def analysis():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    try:
        with open("signals.log", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["لم يتم توليد إشارات حتى الآن."]
    return "<br>".join(lines[-50:])  # آخر 50 سطر

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
