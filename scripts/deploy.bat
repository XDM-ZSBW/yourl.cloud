@echo off
REM Deployment script for Yourl.Cloud
REM Author: Yourl Cloud Inc.
REM Session: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo 🚀 Deploying Yourl.Cloud to Google Cloud Run...

REM Check if gcloud is installed
where gcloud >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ gcloud CLI not found. Please install Google Cloud SDK first.
    pause
    exit /b 1
)

REM Check if user is authenticated
gcloud auth list --filter=status:ACTIVE --format="value(account)" | findstr . >nul
if %errorlevel% neq 0 (
    echo ❌ Not authenticated with gcloud. Please run 'gcloud auth login' first.
    pause
    exit /b 1
)

REM Get project ID
for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo ❌ No project ID set. Please run 'gcloud config set project YOUR_PROJECT_ID' first.
    pause
    exit /b 1
)

echo 📋 Project ID: %PROJECT_ID%

REM Build and deploy using Cloud Build
echo 🔨 Building and deploying with Cloud Build...
gcloud builds submit --config cloudbuild.yaml

if %errorlevel% equ 0 (
    echo ✅ Deployment successful!
    echo 🌐 Your application should be available at:
    echo    https://yourl-cloud-%PROJECT_ID:~0,8%-uc.a.run.app
    echo.
    echo 🔐 Demo password: yourl2024
    echo 📊 Health check: https://yourl-cloud-%PROJECT_ID:~0,8%-uc.a.run.app/health
) else (
    echo ❌ Deployment failed. Please check the logs above.
)

pause
