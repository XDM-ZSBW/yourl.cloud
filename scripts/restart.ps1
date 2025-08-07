# Restart script for URL API Server
# Author: Yourl Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

Write-Host "🚀 Restarting URL API Server..." -ForegroundColor Green

# Kill any existing Python processes on port 8080 (Cloud Run default)
$processes = Get-NetTCPConnection -LocalPort 8080 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($processes) {
    Write-Host "Stopping processes on port 8080..." -ForegroundColor Yellow
    foreach ($processId in $processes) {
        try {
            Stop-Process -Id $processId -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process $processId" -ForegroundColor Yellow
        } catch {
            Write-Host "Could not stop process $processId" -ForegroundColor Red
        }
    }
}

# Wait a moment for processes to stop
Start-Sleep -Seconds 2

# Start the application using production WSGI server
Write-Host "Starting URL API Server with Gunicorn WSGI server..." -ForegroundColor Green
python start.py
