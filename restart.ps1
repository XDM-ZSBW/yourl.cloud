# Restart script for URL API Server
# Author: Yourl-Cloud Inc.
# Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

Write-Host "🚀 Restarting URL API Server..." -ForegroundColor Green

# Kill any existing Python processes on port 80
$processes = Get-NetTCPConnection -LocalPort 80 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess
if ($processes) {
    Write-Host "Stopping processes on port 80..." -ForegroundColor Yellow
    foreach ($pid in $processes) {
        try {
            Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue
            Write-Host "Stopped process $pid" -ForegroundColor Yellow
        } catch {
            Write-Host "Could not stop process $pid" -ForegroundColor Red
        }
    }
}

# Wait a moment for processes to stop
Start-Sleep -Seconds 2

# Start the application
Write-Host "Starting URL API Server..." -ForegroundColor Green
python app.py
