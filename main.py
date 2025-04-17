from flask import Flask, render_template, request, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import scheduled_task
from db import SessionLocal, AnalysisResult
import os
import logging
from trading_signals import symbols

app = Flask(__name__)
app.secret_key = "secret_key"

# إعداد وتحسين الجدولة
scheduler = BackgroundScheduler()
scheduler.add_job(
    scheduled_task,
    'interval',
    seconds=600,
    max_instances=1,           # لا تكرر التنفيذ إذا لم تنته المهمة السابقة
    misfire_grace_time=60      # يعطي فرصة 60 ثانية في حال حصل تأخير
)
scheduler.start()

# تفعيل نظام السجلات
logging.basicConfig(level=logging.INFO)

@app.route('/')
def login_page():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username == "HMARSIELO" and password == "Hassan#99":
        session['logged_in'] = True
        return redirect(url_for('analysis'))
    return "اسم المستخدم أو كلمة المرور غير صحيحة"

@app.route('/analysis')
def analysis():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    db = SessionLocal()
    with SessionLocal() as db:
        results = (
            db.query(AnalysisResult)
            .filter(AnalysisResult.symbol.in_(symbols))
            .order_by(AnalysisResult.timestamp.desc())
            .all()
        )

    return render_template("analysis.html", results=results)

def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))
