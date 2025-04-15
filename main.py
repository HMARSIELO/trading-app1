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
    results = db.query(AnalysisResult).order_by(AnalysisResult.timestamp.desc()).limit(50).all()
    db.close()

    return render_template("analysis.html", results=results)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login_page'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
