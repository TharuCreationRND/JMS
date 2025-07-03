@echo off

:: Step 1: Start Django server on port 8002 in a new window
start "Django Server" cmd /k "python manage.py runserver 8002"

:: Step 2: Start Telegram Bot in another new window
start "Telegram Bot" cmd /k "python manage.py run_telegram_bot"

:: Step 3: Wait a few seconds, then start ngrok for port 8002
timeout /t 5 > nul
start "ngrok" cmd /k "ngrok http 8002"
