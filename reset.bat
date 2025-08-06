@echo off
REM yourl.cloud Reset Script (Windows)
REM Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

echo yourl.cloud - Reset Script
echo ==========================
echo Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
echo Timestamp: %date% %time%
echo.

echo Resetting yourl.cloud to clean state...
echo.

REM Clear any cached data
if exist ".cache" (
    echo Clearing cache directory...
    rmdir /s /q ".cache"
)

REM Reset git status (if needed)
if exist ".git" (
    echo Checking git status...
    git status --porcelain
    echo.
)

REM Show current files
echo Current project files:
dir /b *.html *.md *.sh *.bat reset status 2>nul
echo.

echo Reset complete. Essential files maintained:
echo - index.html
echo - README.md
echo - reset.sh
echo - reset.bat
echo - reset
echo - status
echo.
echo For more information: https://github.com/XDM-ZSBW/yourl.cloud

pause
