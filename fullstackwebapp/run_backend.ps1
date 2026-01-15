# PowerShell script to run the backend server with proper environment setup

# Set the DATABASE_URL environment variable
$env:DATABASE_URL = "sqlite:///./test.db"

# Activate the virtual environment and run the server
& backend\venv\Scripts\Activate.ps1
uvicorn backend.main:app --reload --app-dir .