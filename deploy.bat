@echo off
REM yourl.cloud - Google Cloud Deployment Script (Windows)
REM ====================================================
REM 
REM Yourl-Cloud Inc. - AI-Friendly Service Hub
REM Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

setlocal enabledelayedexpansion

REM Configuration
set PROJECT_ID=yourl-cloud-inc
set REGION=us-central1
set SERVICE_NAME=yourl-cloud
set SESSION_ID=f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo.
echo 🚀 Yourl-Cloud Inc. - Google Cloud Deployment
echo =============================================
echo Session ID: %SESSION_ID%
echo Project ID: %PROJECT_ID%
echo Region: %REGION%
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK is not installed.
    echo Please install it from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Check if user is authenticated
gcloud auth list --filter=status:ACTIVE --format="value(account)" | findstr /r "." >nul
if %errorlevel% neq 0 (
    echo ⚠️  Not authenticated with Google Cloud.
    echo Please run: gcloud auth login
    pause
    exit /b 1
)

REM Set the project
echo 📋 Setting project to %PROJECT_ID%...
gcloud config set project %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

REM Build and deploy
echo 🏗️  Building and deploying to Google App Engine...
gcloud app deploy app.yaml --quiet

REM Get the deployed URL
echo 🌐 Getting deployment URL...
for /f "tokens=*" %%i in ('gcloud app browse --no-launch-browser') do set DEPLOYED_URL=%%i

echo.
echo ✅ Deployment successful!
echo 🌍 Your application is available at: %DEPLOYED_URL%

REM Show status
echo 📊 Checking application status...
gcloud app describe

echo.
echo 🎉 Yourl-Cloud Inc. is now live on Google Cloud!
echo 📝 Next steps:
echo   1. Set up custom domain (optional)
echo   2. Configure SSL certificates
echo   3. Set up monitoring and logging
echo   4. Configure CI/CD pipeline
echo.
echo 🔗 Useful commands:
echo   - View logs: gcloud app logs tail -s default
echo   - Check status: gcloud app describe
echo   - Open app: gcloud app browse
echo.

pause
