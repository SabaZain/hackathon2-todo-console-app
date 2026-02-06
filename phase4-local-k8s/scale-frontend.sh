#!/bin/bash
# Script to test scaling of frontend service to multiple replicas

echo "Scaling frontend service to 3 replicas..."

# Scale the frontend deployment to 3 replicas
kubectl scale deployment frontend-deployment --replicas=3

# Wait for all pods to be ready
echo "Waiting for frontend pods to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

# Check the status of the scaled deployment
echo "Frontend deployment status:"
kubectl get deployment frontend-deployment

# List all frontend pods
echo "Frontend pods:"
kubectl get pods -l app=frontend

echo "Frontend scaling completed!"