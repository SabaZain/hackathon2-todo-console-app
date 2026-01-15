@echo off
REM Phase II Backend Setup - Windows Batch Script
REM This script activates the virtual environment and runs the backend server

echo Setting up Phase II backend environment...

REM Set the DATABASE_URL environment variable for the session
set DATABASE_URL=sqlite:///./test.db
echo DATABASE_URL set to %DATABASE_URL%

REM Activate the virtual environment
echo Activating virtual environment...
call backend\venv\Scripts\activate.bat

REM Verify that we're in the correct directory
cd /d "%~dp0"

REM Run the backend server with uvicorn
echo Starting backend server...
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

pause