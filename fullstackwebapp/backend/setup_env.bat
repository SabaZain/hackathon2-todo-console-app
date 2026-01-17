@echo off
REM Script to activate virtual environment for backend
REM Environment variables should be set externally or via .env file

REM Activate the virtual environment
call venv\Scripts\activate.bat

echo Virtual environment activated
echo Set environment variables before running: set DATABASE_URL=your_db_url_here
echo You can now run the backend with: uvicorn main:app --reload