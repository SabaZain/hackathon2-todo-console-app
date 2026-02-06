#!/bin/bash

# Phase 4 Deployment Assistant Script
# This script guides you through the Cloud Native Todo Chatbot deployment process

echo "==========================================="
echo "Cloud Native Todo Chatbot - Phase 4 Deployment"
echo "==========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Step 1: Prerequisites Check
echo "Step 1: Prerequisites Check"
echo "---------------------------"
echo "Checking if required tools are installed..."

DOCKER_INSTALLED=$(command_exists docker && echo "YES" || echo "NO")
KUBECTL_INSTALLED=$(command_exists kubectl && echo "YES" || echo "NO")
MINIKUBE_INSTALLED=$(command_exists minikube && echo "YES" || echo "NO")
HELM_INSTALLED=$(command_exists helm && echo "YES" || echo "NO")

echo "Docker: $DOCKER_INSTALLED"
echo "kubectl: $KUBECTL_INSTALLED"
echo "Minikube: $MINIKUBE_INSTALLED"
echo "Helm: $HELM_INSTALLED"

if [[ $DOCKER_INSTALLED == "NO" ]] || [[ $KUBECTL_INSTALLED == "NO" ]] || [[ $MINIKUBE_INSTALLED == "NO" ]] || [[ $HELM_INSTALLED == "NO" ]]; then
    echo ""
    echo "❌ Some prerequisites are missing!"
    echo "Please install all required tools before continuing."
    echo "Run 'powershell -File setup-prerequisites.ps1' to help with installation."
    exit 1
fi

echo "✅ All prerequisites are installed!"
echo ""

read -p "Press Enter to continue to Step 2: Navigate to Phase 4 Folder..."

# Step 2: Navigate to Phase 4 Folder
echo "Step 2: Navigate to Phase 4 Folder"
echo "-----------------------------------"
echo "This is where all Phase 4 files are located."

cd phase4-local-k8s || { echo "❌ Phase 4 folder not found!"; exit 1; }
CURRENT_DIR=$(pwd)
echo "✅ Successfully navigated to: $CURRENT_DIR"

read -p "Press Enter to continue to Step 3: Build Docker Images..."

# Step 3: Build Docker Images
echo ""
echo "Step 3: Build Docker Images"
echo "-----------------------------"
echo "Docker images package your application code and dependencies for deployment."
echo "Building backend image first (dependency for frontend)..."

cd backend
if [[ -f "build-image.sh" ]]; then
    chmod +x build-image.sh
    echo "Running: ./build-image.sh"
    ./build-image.sh
    BUILD_BACKEND_STATUS=$?
else
    echo "❌ build-image.sh not found in backend directory!"
    BUILD_BACKEND_STATUS=1
fi

if [[ $BUILD_BACKEND_STATUS -eq 0 ]]; then
    echo "✅ Backend image built successfully!"
else
    echo "❌ Backend image build failed!"
    exit 1
fi

read -p "Was the backend build successful? (Press Enter to continue)..."

cd ../frontend
if [[ -f "build-image.sh" ]]; then
    chmod +x build-image.sh
    echo "Running: ./build-image.sh"
    ./build-image.sh
    BUILD_FRONTEND_STATUS=$?
else
    echo "❌ build-image.sh not found in frontend directory!"
    BUILD_FRONTEND_STATUS=1
fi

if [[ $BUILD_FRONTEND_STATUS -eq 0 ]]; then
    echo "✅ Frontend image built successfully!"
else
    echo "❌ Frontend image build failed!"
    exit 1
fi

read -p "Was the frontend build successful? (Press Enter to continue)..."

# Step 4: Optimize Docker Images
echo ""
echo "Step 4: Optimize Docker Images"
echo "------------------------------"
echo "Optimization reduces image size and improves deployment speed."

cd ../backend
if [[ -f "optimize-image.sh" ]]; then
    chmod +x optimize-image.sh
    echo "Running: ./optimize-image.sh"
    ./optimize-image.sh
    OPTIMIZE_BACKEND_STATUS=$?
else
    echo "❌ optimize-image.sh not found in backend directory!"
    OPTIMIZE_BACKEND_STATUS=1
fi

if [[ $OPTIMIZE_BACKEND_STATUS -eq 0 ]]; then
    echo "✅ Backend image optimized successfully!"
else
    echo "❌ Backend image optimization failed!"
    exit 1
fi

cd ../frontend
if [[ -f "optimize-image.sh" ]]; then
    chmod +x optimize-image.sh
    echo "Running: ./optimize-image.sh"
    ./optimize-image.sh
    OPTIMIZE_FRONTEND_STATUS=$?
else
    echo "❌ optimize-image.sh not found in frontend directory!"
    OPTIMIZE_FRONTEND_STATUS=1
fi

if [[ $OPTIMIZE_FRONTEND_STATUS -eq 0 ]]; then
    echo "✅ Frontend image optimized successfully!"
else
    echo "❌ Frontend image optimization failed!"
    exit 1
fi

read -p "Press Enter to continue to Step 5: Start Minikube Cluster..."

# Step 5: Start Minikube Cluster
echo ""
echo "Step 5: Start Minikube Cluster"
echo "------------------------------"
echo "Minikube runs a local Kubernetes cluster on your machine."

echo "Starting Minikube with 4 CPUs, 8GB memory, and 20GB disk..."
minikube start --cpus=4 --memory=8192 --disk-size=20g
MINIKUBE_START_STATUS=$?

if [[ $MINIKUBE_START_STATUS -eq 0 ]]; then
    echo "✅ Minikube started successfully!"
else
    echo "❌ Failed to start Minikube!"
    exit 1
fi

read -p "Is Minikube running successfully? (Press Enter to continue)..."

# Step 6: Deploy Backend Service
echo ""
echo "Step 6: Deploy Backend Service"
echo "--------------------------------"
echo "The backend provides the main API for the application."

cd ../backend
if [[ -f "backend-deployment.yaml" ]]; then
    echo "Applying backend deployment..."
    kubectl apply -f backend-deployment.yaml
    DEPLOY_BACKEND_STATUS=$?

    if [[ $DEPLOY_BACKEND_STATUS -eq 0 ]]; then
        echo "Waiting for backend deployment to be available..."
        kubectl wait --for=condition=available deployment/backend-deployment --timeout=300s
        WAIT_BACKEND_STATUS=$?

        if [[ $WAIT_BACKEND_STATUS -eq 0 ]]; then
            echo "✅ Backend service deployed and available!"
        else
            echo "❌ Backend deployment timed out or failed!"
            exit 1
        fi
    else
        echo "❌ Failed to apply backend deployment!"
        exit 1
    fi
else
    echo "❌ backend-deployment.yaml not found!"
    exit 1
fi

read -p "Press Enter to continue to deploy frontend service..."

# Step 7: Deploy Frontend Service
echo ""
echo "Step 7: Deploy Frontend Service"
echo "--------------------------------"
echo "The frontend is the user interface that connects to the backend."

cd ../frontend
if [[ -f "frontend-deployment.yaml" ]]; then
    echo "Applying frontend deployment..."
    kubectl apply -f frontend-deployment.yaml
    DEPLOY_FRONTEND_STATUS=$?

    if [[ $DEPLOY_FRONTEND_STATUS -eq 0 ]]; then
        echo "Waiting for frontend deployment to be available..."
        kubectl wait --for=condition=available deployment/frontend-deployment --timeout=300s
        WAIT_FRONTEND_STATUS=$?

        if [[ $WAIT_FRONTEND_STATUS -eq 0 ]]; then
            echo "✅ Frontend service deployed and available!"
        else
            echo "❌ Frontend deployment timed out or failed!"
            exit 1
        fi
    else
        echo "❌ Failed to apply frontend deployment!"
        exit 1
    fi
else
    echo "❌ frontend-deployment.yaml not found!"
    exit 1
fi

read -p "Are both services running? (Press Enter to continue)..."

# Step 8: Validate Deployment
echo ""
echo "Step 8: Validate Deployment"
echo "-----------------------------"
echo "Running comprehensive validation checks..."

cd ..
if [[ -f "validate-deployment.sh" ]]; then
    chmod +x validate-deployment.sh
    echo "Running validation script..."
    ./validate-deployment.sh
    VALIDATION_STATUS=$?

    if [[ $VALIDATION_STATUS -eq 0 ]]; then
        echo "✅ All validation checks passed!"
    else
        echo "⚠️  Some validation checks had issues (non-critical)."
    fi
else
    echo "Validating manually..."
    echo "Checking pods:"
    kubectl get pods

    echo "Checking services:"
    kubectl get services

    echo "Checking deployments:"
    kubectl get deployments
fi

read -p "Did all critical checks pass? (Press Enter to continue)..."

# Step 9: Optional Scaling
echo ""
echo "Step 9: Optional Scaling"
echo "------------------------"
echo "Scaling increases the number of service instances for better performance."

SCALE_CHOICE=""
while [[ "$SCALE_CHOICE" != "y" && "$SCALE_CHOICE" != "n" ]]; do
    read -p "Would you like to scale services? (y/n): " SCALE_CHOICE
done

if [[ "$SCALE_CHOICE" == "y" ]]; then
    cd ..
    if [[ -f "scale-backend.sh" ]]; then
        chmod +x scale-backend.sh
        ./scale-backend.sh
        echo "✅ Backend scaled!"
    fi

    if [[ -f "scale-frontend.sh" ]]; then
        chmod +x scale-frontend.sh
        ./scale-frontend.sh
        echo "✅ Frontend scaled!"
    fi

    if [[ -f "scaled-services-validation.sh" ]]; then
        chmod +x scaled-services-validation.sh
        ./scaled-services-validation.sh
        echo "✅ Scaled services validated!"
    fi

    read -p "Press Enter after confirming scaling worked..."
fi

# Step 10: Optional Helm Deployment
echo ""
echo "Step 10: Optional Helm Deployment"
echo "-----------------------------------"
echo "Helm simplifies Kubernetes application management with packages called charts."

HELM_CHOICE=""
while [[ "$HELM_CHOICE" != "y" && "$HELM_CHOICE" != "n" ]]; do
    read -p "Would you like to deploy using Helm? (y/n): " HELM_CHOICE
done

if [[ "$HELM_CHOICE" == "y" ]]; then
    cd helm-charts
    if [[ -f "install-backend.sh" ]]; then
        chmod +x install-backend.sh
        ./install-backend.sh
        echo "✅ Helm backend release installed!"
    fi

    if [[ -f "install-frontend.sh" ]]; then
        chmod +x install-frontend.sh
        ./install-frontend.sh
        echo "✅ Helm frontend release installed!"
    fi

    if [[ -f "verify-releases.sh" ]]; then
        chmod +x verify-releases.sh
        ./verify-releases.sh
        echo "✅ Helm releases verified!"
    fi

    read -p "Press Enter after confirming Helm deployment..."
fi

# Step 11: Final Summary & External Access
echo ""
echo "Step 11: Final Summary & External Access"
echo "-----------------------------------------"
echo "Getting final status and access information..."

echo "Current pods and services:"
kubectl get pods,svc

echo ""
echo "Getting frontend service URL:"
minikube service frontend-service --url

echo ""
echo "🎉 Deployment Complete!"
echo "======================="
echo ""
echo "Your Cloud Native Todo Chatbot is now running!"
echo ""
echo "To access the frontend:"
echo "1. Copy the URL from above (should look like http://x.x.x.x:port)"
echo "2. Open it in your browser"
echo ""
echo "To check logs:"
echo "- Backend: kubectl logs -l app=backend"
echo "- Frontend: kubectl logs -l app=frontend"
echo ""
echo "To check current status anytime:"
echo "- kubectl get pods,svc"
echo "- kubectl get deployments"
echo ""
echo "For troubleshooting:"
echo "- Check the Phase 4 documentation in the phase4-local-k8s directory"
echo "- Use the various validation scripts provided"
echo "- Run 'minikube dashboard' for visual interface"

read -p "Do you see the frontend running successfully? (Press Enter to finish)..."