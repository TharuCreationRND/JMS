@echo off

:: Step 1: Start Django server on port 8002 in a new window (with venv activated)
start "Django Server" cmd /k "venv\Scripts\activate && python manage.py runserver 8000"

:: Step 2: Start Telegram Bot in another new window (with venv activated)
start "Telegram Bot" cmd /k "venv\Scripts\activate && python manage.py run_telegram_bot"
