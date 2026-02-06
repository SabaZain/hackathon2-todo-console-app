#!/bin/bash
# Script to check backend pod logs

echo "Checking backend pod status..."
kubectl get pods -l app=backend

echo "Waiting for backend pod to be ready..."
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s

echo "Checking backend pod logs..."
kubectl logs -l app=backend -f

echo "Backend pod verification completed!"