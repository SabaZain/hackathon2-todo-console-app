@echo off
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Phase-4 Render Deployment Test
echo ========================================
echo.

set BACKEND_URL=https://todo-backend-phase4.onrender.com
set FRONTEND_URL=https://todo-frontend-phase4.onrender.com
set PASSED=0
set FAILED=0

echo Testing backend health...
curl -s "%BACKEND_URL%/health" --max-time 10 > temp_response.txt
findstr /C:"healthy" temp_response.txt >nul
if %errorlevel% equ 0 (
    echo [PASS] Backend is healthy
    set /a PASSED+=1
) else (
    echo [FAIL] Backend health check failed
    set /a FAILED+=1
)
echo.

echo Testing frontend...
curl -s -o nul -w "%%{http_code}" "%FRONTEND_URL%" --max-time 10 > temp_status.txt
set /p FRONTEND_STATUS=<temp_status.txt
if "!FRONTEND_STATUS!"=="200" (
    echo [PASS] Frontend loads successfully (HTTP !FRONTEND_STATUS!)
    set /a PASSED+=1
) else (
    echo [FAIL] Frontend returned HTTP !FRONTEND_STATUS!
    set /a FAILED+=1
)
echo.

echo Testing CORS configuration...
curl -s -I -X OPTIONS "%BACKEND_URL%/api/tasks" -H "Origin: %FRONTEND_URL%" -H "Access-Control-Request-Method: GET" --max-time 10 > temp_cors.txt
findstr /I /C:"access-control-allow-origin" temp_cors.txt >nul
if %errorlevel% equ 0 (
    echo [PASS] CORS is configured correctly
    set /a PASSED+=1
) else (
    echo [FAIL] CORS configuration issue
    set /a FAILED+=1
)
echo.

echo Testing backend API endpoints...
curl -s "%BACKEND_URL%/api/health" --max-time 10 > temp_api.txt
findstr /C:"healthy" temp_api.txt >nul
if %errorlevel% equ 0 (
    echo [PASS] Backend API endpoints accessible
    set /a PASSED+=1
) else (
    echo [WARN] Backend /api/health endpoint check inconclusive
    set /a FAILED+=1
)
echo.

echo ========================================
echo   Test Summary
echo ========================================
echo Tests Passed: !PASSED!
echo Tests Failed: !FAILED!
echo.

if !FAILED! equ 0 (
    echo [SUCCESS] All critical tests passed!
    echo.
    echo Next steps:
    echo 1. Visit %FRONTEND_URL% in your browser
    echo 2. Open DevTools Console (F12^) and check for errors
    echo 3. Look for chatbot icon in bottom-right corner
    echo 4. Test user registration and login
    echo 5. Create, update, and delete tasks
    echo 6. Test chatbot functionality
) else (
    echo [ERROR] Some tests failed.
    echo.
    echo Troubleshooting:
    echo 1. Check Render service logs in the dashboard
    echo 2. Verify environment variables are set correctly
    echo 3. Ensure latest code is deployed
    echo 4. Review RENDER_DEPLOYMENT_FIX.md for detailed steps
)

del temp_*.txt 2>nul

echo.
pause
