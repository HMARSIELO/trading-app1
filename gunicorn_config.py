# gunicorn_config.py

timeout = 2000 # المهلة بـ الثواني (5 دقائق)
workers = 1    # عدد الـ workers (يمكن تغييره حسب الحاجة)
bind = "0.0.0.0:8000"
