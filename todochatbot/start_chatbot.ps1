# Todo Chatbot Backend Setup - PowerShell Script
# This script activates the virtual environment and runs the chatbot server

Write-Host "Setting up Todo Chatbot backend environment..." -ForegroundColor Green

# Change to the correct directory
Set-Location $PSScriptRoot

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
if (Test-Path ".venv\Scripts\Activate.ps1") {
    & .venv\Scripts\Activate.ps1
} else {
    Write-Host "Warning: Virtual environment not found, assuming packages are installed globally" -ForegroundColor Yellow
}

# Run the chatbot server with uvicorn
Write-Host "Starting Todo Chatbot server on port 8000..." -ForegroundColor Green
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000