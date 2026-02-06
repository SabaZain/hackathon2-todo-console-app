#!/bin/bash
# Script to build the frontend Docker image
#
# This script builds a Docker image for the frontend Next.js application
# It uses the Dockerfile in the current directory to create the image
#
# Beginner Tip: Always run this script from the frontend directory
# Safety Note: Make sure Docker Desktop is running before executing this script
#
# What this script does:
# 1. Creates a Docker image tagged as 'cloud-native-todo-frontend:v1.0.0'
# 2. Uses the Dockerfile in the current directory as build instructions
# 3. Outputs the image to your local Docker registry

echo "Building frontend Docker image..."
echo "Make sure Docker Desktop is running before proceeding..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running! Please start Docker Desktop first."
    exit 1
fi

# Build the frontend image with appropriate tag
# The '.' tells Docker to use the current directory for the build context
docker build -t cloud-native-todo-frontend:v1.0.0 .

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "Frontend image built successfully!"
    echo "Image name: cloud-native-todo-frontend:v1.0.0"
    echo "You can now use this image for deployment to Minikube"
else
    echo "ERROR: Frontend image build failed!"
    exit 1
fi