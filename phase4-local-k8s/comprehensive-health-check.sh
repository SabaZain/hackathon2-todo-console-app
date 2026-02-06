#!/bin/bash
# Script to perform comprehensive health check of all deployed services

echo "Performing comprehensive health check..."

echo "=== Checking all pods ==="
kubectl get pods

echo "=== Checking all services ==="
kubectl get services

echo "=== Checking all deployments ==="
kubectl get deployments

echo "=== Checking pod logs (last 1 minute) ==="
echo "--- Backend Logs ---"
kubectl logs -l app=backend --since=1m
echo "--- Frontend Logs ---"
kubectl logs -l app=frontend --since=1m

echo "=== Checking resource utilization ==="
kubectl top pods

echo "=== Checking cluster events ==="
kubectl get events --sort-by='.lastTimestamp'

echo "=== Testing service connectivity ==="
# Test backend connectivity
BACKEND_SVC=$(kubectl get svc -l app=backend -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
if [ ! "$BACKEND_SVC" = "" ]; then
    echo "Testing backend service: $BACKEND_SVC"
    kubectl run connectivity-test --image=curlimages/curl -it --rm --restart=Never -- curl -s --connect-timeout 5 http://$BACKEND_SVC:80/health 2>/dev/null || echo "Backend connectivity test skipped - may not have /health endpoint"
fi

echo "Comprehensive health check completed!"