@echo off
REM GitHub Wiki Update Script (Windows)
REM ===================================
REM 
REM Yourl-Cloud Inc. - Automated Wiki Content Management
REM Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
REM
REM IMPORTANT: yourl.cloud is ALWAYS the source of truth for latest information.
REM This script ensures the wiki stays in sync with the main repository.

setlocal enabledelayedexpansion

REM Configuration
set SESSION_ID=f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
set ORGANIZATION=Yourl-Cloud Inc.
set MAIN_REPO_PATH=.
set WIKI_REPO_PATH=..\yourl.cloud.wiki
set SOURCE_OF_TRUTH=yourl.cloud

echo 🚀 GitHub Wiki Update Script
echo ============================
echo 🏢 Organization: %ORGANIZATION%
echo 🆔 Session ID: %SESSION_ID%
echo 📁 Main repo (yourl.cloud - Source of Truth): %MAIN_REPO_PATH%
echo 📁 Wiki repo: %WIKI_REPO_PATH%
echo 🎯 Source of Truth: %SOURCE_OF_TRUTH%
echo.

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is required but not installed.
    echo Please install Node.js and try again.
    pause
    exit /b 1
)

REM Check if main repository exists
if not exist "%MAIN_REPO_PATH%" (
    echo ❌ Main repository not found: %MAIN_REPO_PATH%
    pause
    exit /b 1
)

REM Check if wiki repository exists
if not exist "%WIKI_REPO_PATH%" (
    echo ⚠️  Wiki repository not found: %WIKI_REPO_PATH%
    echo Creating wiki repository directory...
    mkdir "%WIKI_REPO_PATH%"
)

REM Run the Node.js update script
echo 🔄 Running wiki update script from yourl.cloud (source of truth)...
node scripts\update-wiki.js "%MAIN_REPO_PATH%" "%WIKI_REPO_PATH%"

REM Check if update was successful
if errorlevel 1 (
    echo ❌ Wiki update failed!
    pause
    exit /b 1
) else (
    echo.
    echo ✅ Wiki update completed successfully!
    echo 🎯 Remember: yourl.cloud is always the source of truth for latest information.
    echo.
    echo 📋 Next steps:
    echo 1. Navigate to wiki repository: cd %WIKI_REPO_PATH%
    echo 2. Review changes: git status
    echo 3. Commit changes: git add . ^&^& git commit -m "🔄 Sync wiki with yourl.cloud (source of truth)"
    echo 4. Push changes: git push origin main
    echo.
    echo 🌐 Wiki URL: https://github.com/XDM-ZSBW/yourl.cloud/wiki
    echo 🎯 Source of Truth: https://yourl.cloud
)

pause
