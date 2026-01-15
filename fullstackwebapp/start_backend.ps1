# Phase II Backend Setup - PowerShell Script
# This script activates the virtual environment and runs the backend server

Write-Host "Setting up Phase II backend environment..." -ForegroundColor Green

# Set the DATABASE_URL environment variable for the session
$env:DATABASE_URL = "sqlite:///./test.db"
Write-Host "DATABASE_URL set to: $env:DATABASE_URL" -ForegroundColor Yellow

# Change to the correct directory
Set-Location $PSScriptRoot

# Activate the virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& backend\venv\Scripts\Activate.ps1

# Run the backend server with uvicorn
Write-Host "Starting backend server..." -ForegroundColor Green
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000