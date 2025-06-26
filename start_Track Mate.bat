@echo off
title EcoSri System + Telegram Bot Runner

:: Step 1: Activate virtual environment
call venv\Scripts\activate

:: Step 2: Start Django server in a new window
start "Django Server" cmd /k "python manage.py runserver"

:: Step 3: Start Telegram Bot in another new window
start "Telegram Bot" cmd /k "python manage.py run_telegram_bot"

:: Optional: Message
echo Both Django and Telegram Bot are running in separate windows.
pause
