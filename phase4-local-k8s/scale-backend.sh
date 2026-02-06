#!/bin/bash
# Script to test scaling of backend service to multiple replicas

echo "Scaling backend service to 3 replicas..."

# Scale the backend deployment to 3 replicas
kubectl scale deployment backend-deployment --replicas=3

# Wait for all pods to be ready
echo "Waiting for backend pods to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s

# Check the status of the scaled deployment
echo "Backend deployment status:"
kubectl get deployment backend-deployment

# List all backend pods
echo "Backend pods:"
kubectl get pods -l app=backend

echo "Backend scaling completed!"