#!/bin/bash
# Script to validate backend service accessibility
#
# This script checks if the backend service is accessible within the cluster
# It verifies that the service is running and responding to requests
#
# Beginner Tip: Run this script after deploying the backend to Minikube
# Safety Note: Make sure Minikube is running before executing this script
#
# What this script does:
# 1. Verifies the backend service exists in Kubernetes
# 2. Gets the internal cluster IP for the backend service
# 3. Tests connectivity to the backend from within the cluster
# 4. Reports whether the service is accessible

echo "Validating backend service accessibility..."

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "ERROR: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo "ERROR: Minikube is not running! Please start Minikube first."
    exit 1
fi

# Check if the service exists
echo "Checking if backend service exists..."
if ! kubectl get service backend-service &> /dev/null; then
    echo "ERROR: backend-service does not exist in Kubernetes"
    echo "Make sure you've deployed the backend to Minikube first"
    exit 1
fi

kubectl get service backend-service

# Get the cluster IP of the backend service
# The -o jsonpath option extracts specific fields from the service object
BACKEND_IP=$(kubectl get service backend-service -o jsonpath='{.spec.clusterIP}' 2>/dev/null)
if [ -z "$BACKEND_IP" ]; then
    echo "ERROR: Could not get cluster IP from backend-service"
    exit 1
fi
echo "Backend service IP: $BACKEND_IP"

# Check if the service is reachable from within the cluster
echo ""
echo "Testing connectivity from within the cluster..."
echo "Creating temporary test pod to check backend accessibility..."

# Use kubectl run to create a temporary pod with curl to test the backend
# The --rm flag removes the pod after completion
# The -it flag runs the pod interactively
kubectl run test-pod --image=curlimages/curl -it --rm --restart=Never -- curl -s http://$BACKEND_IP:80/health

# Check the exit status of the previous command
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Backend service is accessible from within the cluster!"
else
    echo ""
    echo "⚠ Backend service connectivity test failed"
    echo "  This might be because:"
    echo "  - The service is still starting up"
    echo "  - The health endpoint might be different (/health might not exist)"
    echo "  - Network policies might be blocking the connection"
    echo "  - Try checking pod logs with: kubectl logs -l app=backend"
fi

echo ""
echo "Backend service validation completed!"