@echo off
REM Script to run the backend server with proper environment setup

REM Set the DATABASE_URL environment variable
set DATABASE_URL=sqlite:///./test.db

REM Activate the virtual environment and run the server
call backend\venv\Scripts\activate.bat && uvicorn backend.main:app --reload --app-dir .