@echo off
echo Killing processes on ports 3000, 3001, 3002, 3003...

REM Find and kill processes on port 3000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3000') do (
    echo Killing process with PID %%a
    taskkill /f /pid %%a
)

REM Find and kill processes on port 3001
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3001') do (
    echo Killing process with PID %%a
    taskkill /f /pid %%a
)

REM Find and kill processes on port 3002
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3002') do (
    echo Killing process with PID %%a
    taskkill /f /pid %%a
)

REM Find and kill processes on port 3003
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :3003') do (
    echo Killing process with PID %%a
    taskkill /f /pid %%a
)

echo Removing .next directory...
cd /d D:\hackathontwo\fullstackwebapp\frontend
if exist .next rmdir /s /q .next

echo Starting frontend on port 3000...
npm run dev