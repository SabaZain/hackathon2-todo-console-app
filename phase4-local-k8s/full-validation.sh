#!/bin/bash
# Comprehensive validation script for the entire application

echo "Starting comprehensive application validation..."

echo "Step 1: Checking all pods status..."
kubectl get pods

echo "Step 2: Checking all services..."
kubectl get services

echo "Step 3: Getting Minikube IP and NodePorts..."
MINIKUBE_IP=$(minikube ip)
FRONTEND_PORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}')

echo "Minikube IP: $MINIKUBE_IP"
echo "Frontend NodePort: $FRONTEND_PORT"
echo "Frontend should be accessible at: http://$MINIKUBE_IP:$FRONTEND_PORT"

echo "Step 4: Testing backend service connectivity..."
BACKEND_IP=$(kubectl get service backend-service -o jsonpath='{.spec.clusterIP}')
echo "Backend ClusterIP: $BACKEND_IP"

# Test if backend is responding
kubectl run test-backend --image=curlimages/curl -it --rm --restart=Never -- curl -s http://$BACKEND_IP:80/health

echo "Step 5: Waiting for all deployments to be ready..."
kubectl wait --for=condition=available deployment/frontend-deployment --timeout=300s
kubectl wait --for=condition=available deployment/backend-deployment --timeout=300s

echo "Step 6: Displaying final status..."
echo "=== FRONTEND DEPLOYMENT ==="
kubectl describe deployment frontend-deployment
echo ""
echo "=== BACKEND DEPLOYMENT ==="
kubectl describe deployment backend-deployment
echo ""
echo "=== SERVICES ==="
kubectl describe service frontend-service
kubectl describe service backend-service

echo ""
echo "Application validation completed!"
echo "Access the application at: http://$MINIKUBE_IP:$FRONTEND_PORT"