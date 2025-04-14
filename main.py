from flask import Flask, render_template, request, redirect, url_for, session
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import scheduled_task
from db import SessionLocal, AnalysisResult
import os
import logging

app = Flask(__name__)
app.secret_key = "secret_key"
scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_task, 'interval', seconds=300)
scheduler.start()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

@app.route('/')
def login_page():
    return render_template("index.html")

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
    results = db.query(AnalysisResult).order_by(AnalysisResult.timestamp.desc()).limit(50).all()
    db.close()

    html = "<h2>آخر 50 تحليل</h2><table border='1'><tr><th>العملة</th><th>RSI</th><th>MACD</th><th>Signal</th><th>المصدر</th><th>الوقت</th></tr>"
    for r in results:
        html += f"<tr><td>{r.symbol}</td><td>{r.rsi if r.rsi else '-'}</td><td>{r.macd if r.macd else '-'}</td><td>{'BUY' if r.signal == 1 else 'SELL'}</td><td>{r.source}</td><td>{r.timestamp}</td></tr>"
    html += "</table>"
    return html

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
