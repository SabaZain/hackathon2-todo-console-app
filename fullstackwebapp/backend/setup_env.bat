@echo off
REM Script to activate virtual environment and set environment variables for backend

REM Set the DATABASE_URL environment variable
set DATABASE_URL=sqlite:///./test.db

REM Activate the virtual environment
call backend\venv\Scripts\activate.bat

echo Virtual environment activated and DATABASE_URL set to %DATABASE_URL%
echo You can now run the backend with: uvicorn backend.main:app --reload