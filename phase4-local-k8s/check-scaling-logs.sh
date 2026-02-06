#!/bin/bash
# Script to check logs during and after scaling operations

echo "Checking logs during and after scaling operations..."

# Get logs from backend pods
echo "=== Backend Pod Logs ==="
kubectl logs -l app=backend --since=1m

# Get logs from frontend pods
echo "=== Frontend Pod Logs ==="
kubectl logs -l app=frontend --since=1m

# Check pod status after scaling
echo "=== Pod Status After Scaling ==="
kubectl get pods -l app=backend
kubectl get pods -l app=frontend

# Check if all pods are in running state
echo "=== Checking if all pods are Running ==="
kubectl get pods -l app=backend --field-selector=status.phase=Running
kubectl get pods -l app=frontend --field-selector=status.phase=Running

echo "Scaling logs verification completed!"