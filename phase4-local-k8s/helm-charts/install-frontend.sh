#!/bin/bash
# Script to install the frontend Helm release

echo "Installing frontend Helm release..."

# Add the current directory to Helm repo
helm install frontend-release ./frontend

echo "Frontend Helm release installed successfully!"