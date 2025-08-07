@echo off
REM yourl.cloud - Docker Build Script (Windows)
REM ===========================================
REM 
REM Easy Docker build and run script for Windows
REM Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49

setlocal enabledelayedexpansion

REM Configuration
set IMAGE_NAME=yourl-cloud
set CONTAINER_NAME=yourl-cloud
set PORT=8080

echo 🚀 yourl.cloud Docker Build Script
echo =====================================
echo Session ID: f1d78acb-de07-46e0-bfa7-f5b75e3c0c49
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    exit /b 1
)
echo ✅ Docker is running

REM Get command from first argument
set COMMAND=%1
if "%COMMAND%"=="" set COMMAND=build

if "%COMMAND%"=="build" (
    echo 🔨 Building Docker image...
    docker build -t %IMAGE_NAME% .
    if errorlevel 1 (
        echo ❌ Build failed
        exit /b 1
    )
    echo ✅ Image built successfully
    
) else if "%COMMAND%"=="run" (
    echo 🔄 Stopping existing container...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
    
    echo 🚀 Starting container...
    docker run -d --name %CONTAINER_NAME% -p %PORT%:80 --restart unless-stopped %IMAGE_NAME%
    if errorlevel 1 (
        echo ❌ Failed to start container
        exit /b 1
    )
    echo ✅ Container started successfully
    echo 🌐 Access your application at: http://localhost:%PORT%
    echo 🏥 Health check: http://localhost:%PORT%/health
    echo 📊 Status: http://localhost:%PORT%/status
    
) else if "%COMMAND%"=="start" (
    docker ps --format "table {{.Names}}" | findstr /C:"%CONTAINER_NAME%" >nul
    if errorlevel 1 (
        echo 🚀 Starting container...
        docker run -d --name %CONTAINER_NAME% -p %PORT%:80 --restart unless-stopped %IMAGE_NAME%
        echo ✅ Container started successfully
    ) else (
        echo ✅ Container is already running
    )
    echo 📊 Container status:
    docker ps --filter "name=%CONTAINER_NAME%" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
) else if "%COMMAND%"=="stop" (
    docker ps --format "table {{.Names}}" | findstr /C:"%CONTAINER_NAME%" >nul
    if errorlevel 1 (
        echo ⚠️  Container is not running
    ) else (
        echo 🛑 Stopping container...
        docker stop %CONTAINER_NAME%
        echo ✅ Container stopped
    )
    
) else if "%COMMAND%"=="logs" (
    docker ps --format "table {{.Names}}" | findstr /C:"%CONTAINER_NAME%" >nul
    if errorlevel 1 (
        echo ❌ Container is not running
    ) else (
        echo 📋 Container logs:
        docker logs %CONTAINER_NAME%
    )
    
) else if "%COMMAND%"=="status" (
    echo 📊 Container status:
    docker ps --filter "name=%CONTAINER_NAME%" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    
) else if "%COMMAND%"=="clean" (
    echo 🧹 Cleaning up...
    docker stop %CONTAINER_NAME% >nul 2>&1
    docker rm %CONTAINER_NAME% >nul 2>&1
    docker rmi %IMAGE_NAME% >nul 2>&1
    echo ✅ Cleanup completed
    
) else if "%COMMAND%"=="help" (
    echo Usage: %0 [command]
    echo.
    echo Commands:
    echo   build   - Build the Docker image
    echo   run     - Build and run the container
    echo   start   - Start the container (if not running)
    echo   stop    - Stop the container
    echo   logs    - Show container logs
    echo   status  - Show container status
    echo   clean   - Clean up container and image
    echo   help    - Show this help message
    
) else (
    echo ❌ Unknown command: %COMMAND%
    echo Use '%0 help' for usage information
    exit /b 1
)

endlocal
