@echo off
REM Phase 4 Deployment Assistant Script (Windows Batch)
REM This script guides you through the Cloud Native Todo Chatbot deployment process

echo ===========================================
echo Cloud Native Todo Chatbot - Phase 4 Deployment
echo ===========================================
echo.

REM Step 1: Prerequisites Check
echo Step 1: Prerequisites Check
echo ---------------------------
echo Checking if required tools are installed...

where docker >nul 2>nul
if %errorlevel% equ 0 (set DOCKER_INSTALLED=YES) else (set DOCKER_INSTALLED=NO)

where kubectl >nul 2>nul
if %errorlevel% equ 0 (set KUBECTL_INSTALLED=YES) else (set KUBECTL_INSTALLED=NO)

where minikube >nul 2>nul
if %errorlevel% equ 0 (set MINIKUBE_INSTALLED=YES) else (set MINIKUBE_INSTALLED=NO)

where helm >nul 2>nul
if %errorlevel% equ 0 (set HELM_INSTALLED=YES) else (set HELM_INSTALLED=NO)

echo Docker: %DOCKER_INSTALLED%
echo kubectl: %KUBECTL_INSTALLED%
echo Minikube: %MINIKUBE_INSTALLED%
echo Helm: %HELM_INSTALLED%

if "%DOCKER_INSTALLED%"=="NO" goto MISSING_PREREQ
if "%KUBECTL_INSTALLED%"=="NO" goto MISSING_PREREQ
if "%MINIKUBE_INSTALLED%"=="NO" goto MISSING_PREREQ
if "%HELM_INSTALLED%"=="NO" goto MISSING_PREREQ

echo.
echo  All prerequisites are installed!
echo.

pause
echo.
echo Step 2: Navigate to Phase 4 Folder
echo -----------------------------------
echo This is where all Phase 4 files are located.
echo.

cd /d "%~dp0phase4-local-k8s"
if errorlevel 1 (
  echo  Phase 4 folder not found!
  pause
  exit /b 1
)

set CURRENT_DIR=%cd%
echo  Successfully navigated to: %CURRENT_DIR%
echo.

pause
goto STEP3

:MISSING_PREREQ
echo.
echo  Some prerequisites are missing!
echo Please install all required tools before continuing.
echo Run 'powershell -File setup-prerequisites.ps1' to help with installation.
pause
exit /b 1

:STEP3
echo.
echo Step 3: Build Docker Images
echo -----------------------------
echo Docker images package your application code and dependencies for deployment.
echo Building backend image first ^(dependency for frontend^)...
echo.

cd backend
if not exist "build-image.sh" (
  echo  build-image.sh not found in backend directory!
  pause
  exit /b 1
)

call powershell -Command "& './build-image.sh'"
set BUILD_BACKEND_STATUS=%errorlevel%

if %BUILD_BACKEND_STATUS% equ 0 (
  echo  Backend image built successfully!
) else (
  echo  Backend image build failed!
  pause
  exit /b 1
)

echo.
set /p DUMMY="Was the backend build successful? (Press Enter to continue)..."
echo.

cd ..\frontend
if not exist "build-image.sh" (
  echo  build-image.sh not found in frontend directory!
  pause
  exit /b 1
)

call powershell -Command "& './build-image.sh'"
set BUILD_FRONTEND_STATUS=%errorlevel%

if %BUILD_FRONTEND_STATUS% equ 0 (
  echo  Frontend image built successfully!
) else (
  echo  Frontend image build failed!
  pause
  exit /b 1
)

echo.
set /p DUMMY="Was the frontend build successful? (Press Enter to continue)..."
echo.

goto STEP4

:STEP4
echo.
echo Step 4: Optimize Docker Images
echo ------------------------------
echo Optimization reduces image size and improves deployment speed.
echo.

cd ..\backend
if exist "optimize-image.sh" (
  call powershell -Command "& './optimize-image.sh'"
  set OPTIMIZE_BACKEND_STATUS=%errorlevel%

  if %OPTIMIZE_BACKEND_STATUS% equ 0 (
    echo  Backend image optimized successfully!
  ) else (
    echo  Backend image optimization failed!
    pause
    exit /b 1
  )
) else (
  echo Warning: optimize-image.sh not found in backend directory!
)

cd ..\frontend
if exist "optimize-image.sh" (
  call powershell -Command "& './optimize-image.sh'"
  set OPTIMIZE_FRONTEND_STATUS=%errorlevel%

  if %OPTIMIZE_FRONTEND_STATUS% equ 0 (
    echo  Frontend image optimized successfully!
  ) else (
    echo  Frontend image optimization failed!
    pause
    exit /b 1
  )
) else (
  echo Warning: optimize-image.sh not found in frontend directory!
)

echo.
set /p DUMMY="Press Enter to continue to Step 5: Start Minikube Cluster..."
echo.

goto STEP5

:STEP5
echo.
echo Step 5: Start Minikube Cluster
echo ------------------------------
echo Minikube runs a local Kubernetes cluster on your machine.
echo.

echo Starting Minikube with 4 CPUs, 8GB memory, and 20GB disk...
minikube start --cpus=4 --memory=8192 --disk-size=20g
set MINIKUBE_START_STATUS=%errorlevel%

if %MINIKUBE_START_STATUS% equ 0 (
  echo  Minikube started successfully!
) else (
  echo  Failed to start Minikube!
  pause
  exit /b 1
)

echo.
set /p DUMMY="Is Minikube running successfully? (Press Enter to continue)..."
echo.

goto STEP6

:STEP6
echo.
echo Step 6: Deploy Backend Service
echo -------------------------------
echo The backend provides the main API for the application.
echo.

cd ..\backend
if not exist "backend-deployment.yaml" (
  echo  backend-deployment.yaml not found!
  pause
  exit /b 1
)

kubectl apply -f backend-deployment.yaml
set DEPLOY_BACKEND_STATUS=%errorlevel%

if %DEPLOY_BACKEND_STATUS% equ 0 (
  echo Waiting for backend deployment to be available...
  kubectl wait --for=condition=available deployment/backend-deployment --timeout=300s
  set WAIT_BACKEND_STATUS=%errorlevel%

  if %WAIT_BACKEND_STATUS% equ 0 (
    echo  Backend service deployed and available!
  ) else (
    echo  Backend deployment timed out or failed!
    pause
    exit /b 1
  )
) else (
  echo  Failed to apply backend deployment!
  pause
  exit /b 1
)

echo.
set /p DUMMY="Press Enter to continue to deploy frontend service..."
echo.

goto STEP7

:STEP7
echo.
echo Step 7: Deploy Frontend Service
echo -------------------------------
echo The frontend is the user interface that connects to the backend.
echo.

cd ..\frontend
if not exist "frontend-deployment.yaml" (
  echo  frontend-deployment.yaml not found!
  pause
  exit /b 1
)

kubectl apply -f frontend-deployment.yaml
set DEPLOY_FRONTEND_STATUS=%errorlevel%

if %DEPLOY_FRONTEND_STATUS% equ 0 (
  echo Waiting for frontend deployment to be available...
  kubectl wait --for=condition=available deployment/frontend-deployment --timeout=300s
  set WAIT_FRONTEND_STATUS=%errorlevel%

  if %WAIT_FRONTEND_STATUS% equ 0 (
    echo  Frontend service deployed and available!
  ) else (
    echo  Frontend deployment timed out or failed!
    pause
    exit /b 1
  )
) else (
  echo  Failed to apply frontend deployment!
  pause
  exit /b 1
)

echo.
set /p DUMMY="Are both services running? (Press Enter to continue)..."
echo.

goto STEP8

:STEP8
echo.
echo Step 8: Validate Deployment
echo ----------------------------
echo Running comprehensive validation checks.
echo.

cd ..
if exist "validate-deployment.sh" (
  call powershell -Command "& './validate-deployment.sh'"
  set VALIDATION_STATUS=%errorlevel%

  if %VALIDATION_STATUS% equ 0 (
    echo  All validation checks passed!
  ) else (
    echo  Some validation checks had issues ^(non-critical^).
  )
) else (
  echo Validating manually...
  echo Checking pods:
  kubectl get pods

  echo Checking services:
  kubectl get services

  echo Checking deployments:
  kubectl get deployments
)

echo.
set /p DUMMY="Did all critical checks pass? (Press Enter to continue)..."
echo.

goto STEP9

:STEP9
echo.
echo Step 9: Optional Scaling
echo ------------------------
echo Scaling increases the number of service instances for better performance.
echo.

set /p SCALE_CHOICE="Would you like to scale services? (y/n): "
if /i not "%SCALE_CHOICE%"=="y" goto STEP10

cd ..
if exist "scale-backend.sh" (
  call powershell -Command "& './scale-backend.sh'"
  echo  Backend scaled!
)

if exist "scale-frontend.sh" (
  call powershell -Command "& './scale-frontend.sh'"
  echo  Frontend scaled!
)

if exist "scaled-services-validation.sh" (
  call powershell -Command "& './scaled-services-validation.sh'"
  echo  Scaled services validated!
)

echo.
set /p DUMMY="Press Enter after confirming scaling worked..."
echo.

goto STEP10

:STEP10
echo.
echo Step 10: Optional Helm Deployment
echo ----------------------------------
echo Helm simplifies Kubernetes application management with packages called charts.
echo.

set /p HELM_CHOICE="Would you like to deploy using Helm? (y/n): "
if /i not "%HELM_CHOICE%"=="y" goto STEP11

cd helm-charts
if exist "install-backend.sh" (
  call powershell -Command "& './install-backend.sh'"
  echo  Helm backend release installed!
)

if exist "install-frontend.sh" (
  call powershell -Command "& './install-frontend.sh'"
  echo  Helm frontend release installed!
)

if exist "verify-releases.sh" (
  call powershell -Command "& './verify-releases.sh'"
  echo  Helm releases verified!
)

echo.
set /p DUMMY="Press Enter after confirming Helm deployment..."
echo.

goto STEP11

:STEP11
echo.
echo Step 11: Final Summary ^& External Access
echo -----------------------------------------
echo Getting final status and access information.
echo.

echo Current pods and services:
kubectl get pods,svc

echo.
echo Getting frontend service URL:
minikube service frontend-service --url

echo.
echo  Deployment Complete!
echo ========================
echo.
echo Your Cloud Native Todo Chatbot is now running!
echo.
echo To access the frontend:
echo 1. Copy the URL from above ^(should look like http://x.x.x.x:port^)
echo 2. Open it in your browser
echo.
echo To check logs:
echo - Backend: kubectl logs -l app=backend
echo - Frontend: kubectl logs -l app=frontend
echo.
echo To check current status anytime:
echo - kubectl get pods,svc
echo - kubectl get deployments
echo.
echo For troubleshooting:
echo - Check the Phase 4 documentation in the phase4-local-k8s directory
echo - Use the various validation scripts provided
echo - Run 'minikube dashboard' for visual interface
echo.
set /p DUMMY="Do you see the frontend running successfully? (Press Enter to finish)..."
echo.
echo Thank you for using the Phase 4 Deployment Assistant!
pause