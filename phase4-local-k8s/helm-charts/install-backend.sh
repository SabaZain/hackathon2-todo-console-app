#!/bin/bash
# Script to install the backend Helm release

echo "Installing backend Helm release..."

# Add the current directory to Helm repo
helm install backend-release ./backend

echo "Backend Helm release installed successfully!"