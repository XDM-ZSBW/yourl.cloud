@echo off
REM Restart script for URL API Server
REM Author: Yourl-Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo 🚀 Restarting URL API Server...

REM Kill any existing Python processes on port 80
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :80') do (
    echo Stopping process %%a on port 80...
    taskkill /PID %%a /F >nul 2>&1
)

REM Wait a moment for processes to stop
timeout /t 2 /nobreak >nul

REM Start the application
echo Starting URL API Server...
python app.py

pause
