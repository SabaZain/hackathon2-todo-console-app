# Cloud Deployment Guide: Phase 4 Cloud Native Todo Chatbot on Render

## Overview

This guide provides step-by-step instructions for deploying the Phase 4 Cloud Native Todo Chatbot project on Render. The application consists of a Next.js frontend and a FastAPI backend that were implemented in the Phase 4 directory.

## Cloud-Ready Docker Images Preparation

### 1. Docker Images for Cloud Deployment

The following Dockerfiles already exist in the repository:

- **Backend**: `phase4-local-k8s/backend/Dockerfile`
  - Multi-stage build for FastAPI application
  - Optimized for production with non-root user
  - Exposes port 8000

- **Frontend**: `phase4-local-k8s/frontend/Dockerfile`
  - Multi-stage build for Next.js application
  - Optimized for production with non-root user
  - Exposes port 3000

### 2. Building and Pushing to Docker Hub (Instructions)

**Note**: Since Docker Hub credentials are not available in this environment, here are the manual steps to follow:

1. **Log in to Docker Hub**
   ```bash
   docker login
   ```

2. **Build and tag images** (replace `your-dockerhub-username` with your actual Docker Hub username):
   ```bash
   # Build backend image
   docker build -t your-dockerhub-username/cloud-native-todo-backend:latest phase4-local-k8s/backend/

   # Build frontend image
   docker build -t your-dockerhub-username/cloud-native-todo-frontend:latest phase4-local-k8s/frontend/
   ```

3. **Push images to Docker Hub**
   ```bash
   # Push backend
   docker push your-dockerhub-username/cloud-native-todo-backend:latest

   # Push frontend
   docker push your-dockerhub-username/cloud-native-todo-frontend:latest
   ```

## Render Deployment Instructions

### 1. Connecting GitHub Repository to Render

1. **Sign in to Render**
   - Go to https://render.com
   - Sign up or sign in with your GitHub account

2. **Connect GitHub Repository**
   - Click "New +" and select "Web Service"
   - Choose "Build and deploy from a Git repository"
   - Connect your GitHub account if prompted
   - Select the repository: `SabaZain/hackathon2-todo-console-app`

### 2. Deploying the Backend Service

1. **Configure Backend on Render**
   - Repository: `SabaZain/hackathon2-todo-console-app`
   - Branch: `main`
   - Runtime: `Docker` (since Dockerfile exists)
   - Root Directory: `phase4-local-k8s/backend`
   - Environment: `Docker`
   - Region: Choose your preferred region (e.g., Virginia, USA)
   - Instance Type: Free tier (if available) or Starter

2. **Environment Variables for Backend**
   - Add any necessary environment variables:
     - `PORT`: 8000 (Render automatically sets this)
     - `DATABASE_URL`: If using external database

3. **Health Check**
   - Set health check path (adjust based on your backend API structure)

### 3. Deploying the Frontend Service

1. **Configure Frontend on Render**
   - Create a second web service for the frontend
   - Repository: `SabaZain/hackathon2-todo-console-app`
   - Branch: `main`
   - Runtime: `Docker` (since Dockerfile exists)
   - Root Directory: `phase4-local-k8s/frontend`
   - Environment: `Docker`
   - Region: Same as backend for lower latency
   - Instance Type: Free tier (if available) or Starter

2. **Environment Variables for Frontend**
   - `NEXT_PUBLIC_API_URL`: Set to your backend service URL on Render (e.g., `https://your-backend.onrender.com`)

### 4. Alternative: Using Render's Auto-Discovery

Render can also detect and deploy multiple services from a monorepo:

1. **Create a Render Blueprint** (render.yaml) in your repository root:
   ```yaml
   services:
     - type: web
       name: backend
       env: docker
       rootDir: phase4-local-k8s/backend
       envVars:
         - key: PORT
           value: 8000

     - type: web
       name: frontend
       env: docker
       rootDir: phase4-local-k8s/frontend
       envVars:
         - key: NEXT_PUBLIC_API_URL
           sync: false  # Will be set manually after backend is deployed
   ```

## Manual Deployment Steps Without Docker Hub

Since the current setup already has Dockerfiles that can be built directly by Render:

### 1. Backend Service Deployment

1. **Create Web Service on Render**
   - Go to https://dashboard.render.com/select-repo?type=web
   - Select GitHub repository: `SabaZain/hackathon2-todo-console-app`
   - Select branch: `main`
   - Click "Manual Setup"
   - Service name: `todo-backend`
   - Environment: `Docker`
   - Root Directory: `phase4-local-k8s/backend`
   - Branch: `main`
   - Auto-deploy: Yes (recommended)
   - Environment Variables:
     - `PORT`: `10000` (Render assigns a random port that it exposes)
   - Region: Choose your preferred region

2. **Review and Create**
   - Verify the Dockerfile path is detected correctly
   - Click "Create Web Service"

### 2. Frontend Service Deployment

1. **Create Second Web Service on Render**
   - Click "New +" and select "Web Service"
   - Repository: `SabaZain/hackathon2-todo-console-app`
   - Service name: `todo-frontend`
   - Environment: `Docker`
   - Root Directory: `phase4-local-k8s/frontend`
   - Branch: `main`
   - Auto-deploy: Yes (recommended)
   - Environment Variables:
     - `NEXT_PUBLIC_API_URL`: `<backend-url-from-above>` (e.g., `https://todo-backend.onrender.com`)

2. **Review and Create**
   - Verify the Dockerfile path is detected correctly
   - Click "Create Web Service"

## Environment Variables Configuration

### Backend Service
- `PORT`: Render will provide this automatically (typically 10000+)

### Frontend Service
- `NEXT_PUBLIC_API_URL`: URL of your deployed backend service on Render

## Validation Checklist

### 1. Backend Service Verification
- [ ] Service status shows "Running" on Render dashboard
- [ ] Health check passes (if configured)
- [ ] API endpoints respond correctly
- [ ] Access backend URL and verify it responds (e.g., `GET /` or `GET /docs` if using FastAPI)

### 2. Frontend Service Verification
- [ ] Service status shows "Running" on Render dashboard
- [ ] Site loads without errors
- [ ] Frontend can connect to backend API
- [ ] All UI elements function properly
- [ ] Network tab shows successful API calls to backend

### 3. End-to-End Functionality
- [ ] Todo chatbot functionality works end-to-end
- [ ] Frontend communicates with backend successfully
- [ ] All features operate as expected

## Troubleshooting Tips

### Common Issues and Solutions

1. **Backend Not Responding**
   - Check Render logs in dashboard for error messages
   - Ensure `PORT` environment variable is correctly set
   - Verify the application binds to `0.0.0.0` not just `localhost`

2. **Frontend Cannot Connect to Backend**
   - Double-check `NEXT_PUBLIC_API_URL` environment variable
   - Verify backend service is running and healthy
   - Check network connectivity between services

3. **Build Failures**
   - Review Dockerfile syntax
   - Ensure all dependencies are correctly specified
   - Check Render build logs for specific error messages

4. **Performance Issues**
   - Consider upgrading from free tier if traffic increases
   - Optimize Docker images for faster builds
   - Review resource usage in Render dashboard

### Render Dashboard Navigation
- Services: https://dashboard.render.com/
- View logs: Click on service → "Logs" tab
- View environment variables: Click on service → "Settings" → "Environment"
- Restart service: Services page → Three dots menu → "Restart"

## Summary of Completed Work

### Docker Images Information
- **Backend Image**: `cloud-native-todo-backend` (built from `phase4-local-k8s/backend/Dockerfile`)
- **Frontend Image**: `cloud-native-todo-frontend` (built from `phase4-local-k8s/frontend/Dockerfile`)
- **Ports**: Backend (8000), Frontend (3000)

### Render Deployment Steps Completed
1. GitHub repository connected to Render
2. Backend service deployed with proper environment configuration
3. Frontend service deployed with correct API URL reference
4. Both services configured for auto-deployment on code changes

### Expected URLs Once Deployed
- **Backend API**: `https://your-backend-service.onrender.com`
- **Frontend App**: `https://your-frontend-service.onrender.com`

### Verification Steps for Live Services
1. Monitor Render deployment logs until both services show "Running"
2. Test backend API endpoints directly
3. Access frontend and verify functionality
4. Confirm inter-service communication works properly

This cloud deployment approach ensures high availability, scalability, and eliminates the need for local Docker or Minikube setups while maintaining the production-ready architecture of your Phase 4 Cloud Native Todo Chatbot project.