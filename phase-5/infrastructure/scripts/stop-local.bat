@echo off
REM Phase 5 - Stop Local Services Script (Windows)
REM This script stops all Phase 5 services

echo ========================================
echo Phase 5 - Stopping Services
echo ========================================
echo.

REM Navigate to docker directory
cd /d "%~dp0\..\docker"

echo Stopping all services...
docker-compose down

echo.
echo [OK] All services stopped
echo.
echo To remove volumes (data will be lost):
echo   docker-compose down -v
echo.
echo To remove volumes and images:
echo   scripts\clean.bat
echo.
pause
