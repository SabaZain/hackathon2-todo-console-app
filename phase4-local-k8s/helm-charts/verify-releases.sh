#!/bin/bash
# Script to verify both Helm releases are functioning correctly

echo "Verifying Helm releases..."

# Check the status of the backend release
echo "Checking backend release status:"
helm status backend-release

# Check the status of the frontend release
echo "Checking frontend release status:"
helm status frontend-release

# List all Helm releases
echo "Listing all Helm releases:"
helm list

# Check pods created by Helm releases
echo "Checking pods created by Helm releases:"
kubectl get pods -l release=backend-release
kubectl get pods -l release=frontend-release

echo "Helm releases verification completed!"