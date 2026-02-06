# Phase 4: Cloud Native Todo Chatbot Deployment

Welcome to the Phase 4 deployment guide for the Cloud Native Todo Chatbot! This guide will help you deploy the application to a local Kubernetes cluster using Minikube.

## Prerequisites

Before starting the deployment, you need to install the following tools:

1. **Docker Desktop** - Containerization platform
2. **kubectl** - Kubernetes command-line tool
3. **Minikube** - Local Kubernetes cluster
4. **Helm** - Kubernetes package manager (optional)

## Installation Methods

### Method 1: Automated Setup (Recommended)
Run the PowerShell setup script to install all prerequisites:

```powershell
# From the hackathontwo directory
powershell -File setup-prerequisites.ps1
```

### Method 2: Manual Installation
Install each tool manually:

- **Docker Desktop**: [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop)
- **kubectl**: [https://kubernetes.io/docs/tasks/tools/install-kubectl/](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- **Minikube**: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
- **Helm**: [https://helm.sh/docs/intro/install/](https://helm.sh/docs/intro/install/)

## Deployment Steps

### Step 1: Verify Prerequisites
After installing all tools, verify they're working:

```bash
docker --version
kubectl version --client
minikube version
helm version
```

### Step 2: Run Deployment Script
Choose the appropriate script for your operating system:

**On Windows:**
```cmd
deploy-phase4.bat
```

**On Linux/Mac:**
```bash
chmod +x deploy-phase4.sh
./deploy-phase4.sh
```

### Step 3: Follow the Interactive Guide
The deployment script will guide you through each step:
1. Check prerequisites
2. Navigate to Phase 4 folder
3. Build Docker images
4. Optimize Docker images
5. Start Minikube cluster
6. Deploy backend service
7. Deploy frontend service
8. Validate deployment
9. Optional scaling
10. Optional Helm deployment
11. Final summary and access

## What Gets Deployed

The deployment creates:
- **Backend Service**: FastAPI application (handles business logic)
- **Frontend Service**: Next.js application (user interface)
- **Services**: Kubernetes services for internal and external access
- **Deployments**: Managed sets of pods for each service

## Accessing the Application

After successful deployment, the script will display the URL to access the frontend. It typically looks like:
```
http://<minikube-ip>:<nodeport>
```

## Troubleshooting

### Common Issues:
1. **Docker not running**: Start Docker Desktop before deployment
2. **Insufficient resources**: Ensure Minikube has enough CPU/memory
3. **Image pull errors**: Make sure images were built successfully
4. **Service not accessible**: Check that both backend and frontend are running

### Useful Commands:
```bash
# Check all pods
kubectl get pods

# Check all services
kubectl get svc

# Check logs for backend
kubectl logs -l app=backend

# Check logs for frontend
kubectl logs -l app=frontend

# Open Minikube dashboard
minikube dashboard

# Check deployment status
kubectl get deployments
```

### Reset if Needed:
```bash
# Delete all deployments
kubectl delete all --all

# Stop and start Minikube fresh
minikube stop
minikube start --cpus=4 --memory=8192 --disk-size=20g
```

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐
│   User/Browser  │    │  Minikube        │
│                 │    │  (Local K8s)     │
│  http://url     │◄──►│                  │
└─────────────────┘    ├──────────────────┤
                       │ ┌──────────────┐ │
                       │ │ Frontend     │ │
                       │ │ (Next.js)    │ │
                       │ └──────────────┘ │
                       │       │          │
                       │       ▼          │
                       │ ┌──────────────┐ │
                       │ │ Backend      │ │
                       │ │ (FastAPI)    │ │
                       │ └──────────────┘ │
                       └──────────────────┘
```

## Validation

The deployment includes multiple validation steps:
- Pod health checks
- Service connectivity
- Inter-service communication
- External accessibility

## Scaling

The application supports horizontal scaling:
- Scale backend: `kubectl scale deployment backend-deployment --replicas=3`
- Scale frontend: `kubectl scale deployment frontend-deployment --replicas=3`

## Helm Charts

Optional Helm charts are available in the `helm-charts/` directory for easier management:
- Backend Helm chart
- Frontend Helm chart
- Parameterized configurations

## Files Structure

```
phase4-local-k8s/
├── frontend/                 # Frontend (Next.js) artifacts
│   ├── Dockerfile            # Multi-stage Docker build for frontend
│   ├── build-image.sh        # Build script with comments for beginners
│   ├── optimize-image.sh     # Optimization script with safety notes
│   ├── check-logs.sh         # Log checking script
│   ├── validation.sh         # Validation script with enhanced comments
│   └── frontend-deployment.yaml # Kubernetes deployment for frontend
├── backend/                  # Backend (FastAPI) artifacts
│   ├── Dockerfile            # Multi-stage Docker build for backend
│   ├── build-image.sh        # Build script with comments for beginners
│   ├── optimize-image.sh     # Optimization script with safety notes
│   ├── check-logs.sh         # Log checking script
│   ├── validation.sh         # Validation script with enhanced comments
│   └── backend-deployment.yaml # Kubernetes deployment for backend
├── helm-charts/              # Helm chart definitions
│   ├── backend/              # Backend Helm chart
│   │   ├── Chart.yaml        # Chart metadata
│   │   ├── values.yaml       # Default values
│   │   └── templates/        # Kubernetes resource templates
│   └── frontend/             # Frontend Helm chart
│       ├── Chart.yaml        # Chart metadata
│       ├── values.yaml       # Default values
│       └── templates/        # Kubernetes resource templates
└── scripts/                  # Utility scripts
```

## Support

If you encounter issues:
1. Check the logs using the commands above
2. Review the validation scripts in the frontend and backend directories
3. Consult the detailed documentation in the phase4-local-k8s directory
4. Run the comprehensive health check: `./comprehensive-health-check.sh`

Happy deploying!