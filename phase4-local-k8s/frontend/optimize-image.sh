#!/bin/bash
# Script to optimize the frontend Docker image
#
# This script creates an optimized version of the frontend Docker image
# Optimized images are smaller and more secure, perfect for Minikube
#
# Beginner Tip: Run this AFTER you've successfully built the basic image
# Safety Note: Don't delete original images until you've tested the optimized version
#
# What this script does:
# 1. Builds the frontend image using optimization techniques
# 2. Tags the image as 'cloud-native-todo-frontend:optimized-v1.0.0'
# 3. Shows the size comparison with the original image
# 4. Provides further optimization suggestions

echo "Optimizing frontend Docker image..."
echo "Safety Tip: Make sure the basic image builds successfully before optimizing..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running! Please start Docker Desktop first."
    exit 1
fi

# Build optimized image using multi-stage build with smaller base images
# The -f flag specifies the Dockerfile to use
docker build -f Dockerfile -t cloud-native-todo-frontend:optimized-v1.0.0 .

# Check if optimization was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Frontend image optimization failed!"
    exit 1
fi

# Analyze image size before and after optimization
echo "Original image size:"
docker images | grep "cloud-native-todo-frontend.*v1.0.0"
echo "Optimized image size:"
docker images | grep cloud-native-todo-frontend:optimized-v1.0.0

# Provide optimization suggestions if needed
echo ""
echo "Additional optimization suggestions:"
echo "- Use .dockerignore to exclude unnecessary files (node_modules, .git, etc.)"
echo "- Consider using alpine-based images for smaller footprint"
echo "- Remove build dependencies in final stage"
echo "- Pin specific versions of packages for reproducible builds"
echo "- Use multi-stage builds to separate build and runtime environments"

echo ""
echo "Frontend image optimization completed!"
echo "Optimized image: cloud-native-todo-frontend:optimized-v1.0.0"