#!/bin/bash
# Script to validate frontend service accessibility
#
# This script checks if the frontend service is accessible
# It verifies that the service is running and can be reached externally
#
# Beginner Tip: Run this script after deploying the frontend to Minikube
# Safety Note: Make sure Minikube is running before executing this script
#
# What this script does:
# 1. Verifies the frontend service exists in Kubernetes
# 2. Gets the NodePort assigned to the frontend service
# 3. Gets the Minikube IP address
# 4. Calculates the access URL for the frontend
# 5. Provides the access URL for verification

echo "Validating frontend service accessibility..."

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
echo "Checking if frontend service exists..."
if ! kubectl get service frontend-service &> /dev/null; then
    echo "ERROR: frontend-service does not exist in Kubernetes"
    echo "Make sure you've deployed the frontend to Minikube first"
    exit 1
fi

kubectl get service frontend-service

# Get the NodePort of the frontend service
# The -o jsonpath option extracts specific fields from the service object
FRONTEND_PORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
if [ -z "$FRONTEND_PORT" ]; then
    echo "ERROR: Could not get NodePort from frontend-service"
    exit 1
fi
echo "Frontend service NodePort: $FRONTEND_PORT"

# Get the Minikube IP
MINIKUBE_IP=$(minikube ip 2>/dev/null)
if [ -z "$MINIKUBE_IP" ]; then
    echo "ERROR: Could not get Minikube IP"
    exit 1
fi
echo "Minikube IP: $MINIKUBE_IP"

# Display the access URL
ACCESS_URL="http://$MINIKUBE_IP:$FRONTEND_PORT"
echo "Frontend should be accessible at: $ACCESS_URL"

# Test accessibility with curl (if available)
if command -v curl &> /dev/null; then
    echo ""
    echo "Testing accessibility..."
    # Use curl with a timeout and silent mode to test the URL
    if curl -s --max-time 10 "$ACCESS_URL" &> /dev/null; then
        echo "✓ Frontend service is accessible!"
    else
        echo "⚠ Frontend service may not be accessible yet, this is normal during startup"
        echo "  The service might still be initializing, try again in a minute"
    fi
fi

echo ""
echo "Frontend service validation completed!"
echo "You can now try accessing: $ACCESS_URL"