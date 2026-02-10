@echo off
REM Phase 5 - Local Deployment Script (Windows)
REM This script starts all Phase 5 services using Docker Compose

echo ========================================
echo Phase 5 - Local Deployment
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Error: Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo [OK] Docker is running
echo.

REM Navigate to docker directory
cd /d "%~dp0\..\docker"

REM Check if backend .env exists
if not exist "..\..\backend\.env" (
    echo [WARNING] Backend .env file not found. Creating from .env.example...
    if exist "..\..\backend\.env.example" (
        copy "..\..\backend\.env.example" "..\..\backend\.env"
        echo [OK] Created backend .env file
    ) else (
        echo Error: .env.example not found in backend directory
        exit /b 1
    )
)

echo Starting infrastructure services...
docker-compose up -d postgres redis zookeeper kafka

echo.
echo Waiting for infrastructure to be ready (30 seconds)...
timeout /t 30 /nobreak >nul

echo.
echo Initializing Kafka topics...
docker-compose up kafka-init

echo.
echo Starting Kafka UI...
docker-compose up -d kafka-ui

echo.
echo Running database migrations...
cd /d "%~dp0\..\..\backend"
if not exist "node_modules" (
    echo Installing backend dependencies...
    call npm install
)

echo Generating Prisma client...
call npx prisma generate

echo Running Prisma migrations...
call npx prisma migrate deploy || call npx prisma migrate dev --name init

cd /d "%~dp0\..\docker"

echo.
echo Building and starting application services...
docker-compose up -d --build backend frontend audit-agent reminder-agent recurring-task-agent realtime-sync-agent

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Services:
echo   Frontend:    http://localhost:3000
echo   Backend API: http://localhost:3001
echo   Kafka UI:    http://localhost:8080
echo   PostgreSQL:  localhost:5432
echo   Redis:       localhost:6379
echo.
echo Health Checks:
echo   Backend:     http://localhost:3001/health
echo.
echo View logs:
echo   docker-compose -f infrastructure/docker/docker-compose.yml logs -f
echo.
echo Stop services:
echo   scripts\stop-local.bat
echo.
pause
