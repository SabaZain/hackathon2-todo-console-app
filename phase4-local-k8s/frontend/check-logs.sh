#!/bin/bash
# Script to check frontend pod logs

echo "Checking frontend pod status..."
kubectl get pods -l app=frontend

echo "Waiting for frontend pod to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s

echo "Checking frontend pod logs..."
kubectl logs -l app=frontend -f

echo "Frontend pod verification completed!"