# Phase 4: Cloud Native Todo Chatbot Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Cloud Native Todo Chatbot to a local Minikube cluster using Docker, Kubernetes, and optionally Helm.

## Prerequisites
- Docker Desktop running
- Minikube installed and configured
- kubectl installed and configured
- kubectl-ai installed for natural language Kubernetes interactions
- Helm installed (for Helm deployment option)

## Deployment Options

### Option 1: Direct Kubernetes Deployment (Recommended for Beginners)

#### 1. Start Minikube
```bash
minikube start --cpus=4 --memory=8192 --disk-size=20g
```

#### 2. Build Docker Images
Navigate to the frontend and backend directories and build the images:

```bash
# For frontend
cd phase4-local-k8s/frontend
./build-image.sh

# For backend
cd ../backend
./build-image.sh
```

#### 3. Deploy Services to Minikube
```bash
# Deploy backend first (it's a dependency for frontend)
kubectl apply -f ../backend/backend-deployment.yaml

# Wait for backend to be ready
kubectl wait --for=condition=available deployment/backend-deployment --timeout=300s

# Deploy frontend
kubectl apply -f ../frontend/frontend-deployment.yaml

# Wait for frontend to be ready
kubectl wait --for=condition=available deployment/frontend-deployment --timeout=300s
```

#### 4. Access the Application
```bash
# Get the frontend NodePort
kubectl get service frontend-service

# Get Minikube IP
minikube ip

# Access the application at http://<minikube-ip>:<frontend-nodeport>
```

### Option 2: Helm-Based Deployment

#### 1. Install Helm Releases
```bash
# Install backend release
helm install backend-release ./helm-charts/backend

# Install frontend release
helm install frontend-release ./helm-charts/frontend
```

#### 2. Verify Installation
```bash
# Check release status
helm status backend-release
helm status frontend-release
```

## Validation Commands
Use these scripts to validate your deployment:

```bash
# Check pod logs
./frontend/check-logs.sh
./backend/check-logs.sh

# Validate inter-service communication
./check-inter-service-communication.sh

# Full validation
./full-validation.sh
```

## Scaling Services
To scale your services:

```bash
# Scale backend
./scale-backend.sh

# Scale frontend
./scale-frontend.sh

# Validate scaled services
./scaled-services-validation.sh
```

## Troubleshooting

### Common Issues
1. **Images not found**: Make sure to build the Docker images before deploying
2. **Services not accessible**: Check that NodePort services are properly configured
3. **Inter-service communication failing**: Verify that service names match in environment variables

### Useful Commands
```bash
# Check all pods
kubectl get pods

# Check pod logs
kubectl logs -l app=<app-name>

# Check services
kubectl get services

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

## Lessons Learned
- Always deploy backend services first as they are often dependencies for frontend services
- Use resource limits to prevent individual pods from consuming excessive resources in Minikube
- Implement proper health checks to ensure service readiness before traffic routing
- Consider using InitContainers for dependency checks before starting main containers
- Proper labeling helps with debugging and management