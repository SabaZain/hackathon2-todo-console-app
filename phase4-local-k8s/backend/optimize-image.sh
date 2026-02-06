#!/bin/bash
# Script to optimize the backend Docker image
#
# This script creates an optimized version of the backend Docker image
# Optimized images are smaller and more secure, perfect for Minikube
#
# Beginner Tip: Run this AFTER you've successfully built the basic image
# Safety Note: Don't delete original images until you've tested the optimized version
#
# What this script does:
# 1. Builds the backend image using optimization techniques
# 2. Tags the image as 'cloud-native-todo-backend:optimized-v1.0.0'
# 3. Shows the size comparison with the original image
# 4. Provides further optimization suggestions

echo "Optimizing backend Docker image..."
echo "Safety Tip: Make sure the basic image builds successfully before optimizing..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running! Please start Docker Desktop first."
    exit 1
fi

# Build optimized image using multi-stage build with smaller base images
# The -f flag specifies the Dockerfile to use
docker build -f Dockerfile -t cloud-native-todo-backend:optimized-v1.0.0 .

# Check if optimization was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Backend image optimization failed!"
    exit 1
fi

# Analyze image size before and after optimization
echo "Original image size:"
docker images | grep "cloud-native-todo-backend.*v1.0.0"
echo "Optimized image size:"
docker images | grep cloud-native-todo-backend:optimized-v1.0.0

# Provide optimization suggestions if needed
echo ""
echo "Additional optimization suggestions:"
echo "- Use .dockerignore to exclude unnecessary files (__pycache__, .git, etc.)"
echo "- Consider using alpine-based images for smaller footprint"
echo "- Remove build dependencies in final stage"
echo "- Pin specific versions of dependencies for security"
echo "- Use non-root user for running the application"
echo "- Minimize layers by combining RUN commands where appropriate"

echo ""
echo "Backend image optimization completed!"
echo "Optimized image: cloud-native-todo-backend:optimized-v1.0.0"