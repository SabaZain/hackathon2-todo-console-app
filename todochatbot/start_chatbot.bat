@echo off
REM Todo Chatbot Backend Setup - Windows Batch Script
REM This script activates the virtual environment and runs the chatbot server

echo Setting up Todo Chatbot backend environment...

REM Activate the virtual environment
echo Activating virtual environment...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found, assuming packages are installed globally
)

REM Verify that we're in the correct directory
cd /d "%~dp0"

REM Run the chatbot server with uvicorn
echo Starting Todo Chatbot server on port 8000...
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

pause