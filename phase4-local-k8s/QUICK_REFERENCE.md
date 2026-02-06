# Cloud Native Todo Chatbot - Quick Reference Guide

## Common Commands

### Minikube
```bash
# Start Minikube
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Stop Minikube
minikube stop

# Get Minikube IP
minikube ip

# Open dashboard
minikube dashboard
```

### Docker Images
```bash
# Build frontend image
cd frontend && ./build-image.sh

# Build backend image
cd backend && ./build-image.sh

# View images
docker images | grep cloud-native-todo
```

### Kubernetes Operations
```bash
# Deploy backend service
kubectl apply -f backend/backend-deployment.yaml

# Deploy frontend service
kubectl apply -f frontend/frontend-deployment.yaml

# Check all pods
kubectl get pods

# Check all services
kubectl get services

# Check logs for backend
kubectl logs -l app=backend

# Check logs for frontend
kubectl logs -l app=frontend

# Scale backend to 3 replicas
kubectl scale deployment backend-deployment --replicas=3

# Scale frontend to 3 replicas
kubectl scale deployment frontend-deployment --replicas=3
```

### Helm Operations
```bash
# Install backend Helm release
helm install backend-release ./helm-charts/backend

# Install frontend Helm release
helm install frontend-release ./helm-charts/frontend

# Check Helm releases
helm list

# Check Helm release status
helm status backend-release
helm status frontend-release

# Uninstall Helm releases
helm uninstall backend-release
helm uninstall frontend-release
```

### Useful Monitoring Commands
```bash
# Watch pods
kubectl get pods -w

# Check pod status with more details
kubectl describe pod <pod-name>

# Tail logs from a pod
kubectl logs -f <pod-name>

# Execute commands in a running pod
kubectl exec -it <pod-name> -- /bin/sh
```

### Troubleshooting
```bash
# Check cluster events
kubectl get events --sort-by='.lastTimestamp'

# Check resource usage
kubectl top pods

# Delete all pods in current namespace
kubectl delete pods --all

# Port forward for direct access
kubectl port-forward svc/backend-service 8080:80
```

### Cleanup
```bash
# Delete deployments
kubectl delete deployment frontend-deployment backend-deployment

# Delete services
kubectl delete service frontend-service backend-service

# Delete all resources
kubectl delete all -l app=frontend
kubectl delete all -l app=backend
```

## Environment Variables
- `NEXT_PUBLIC_API_URL`: Set in frontend for backend API access (default: http://backend-service:80)
- `PORT`: Set in backend for service port (default: 8000)

## Default Ports
- Backend API: Port 80 (ClusterIP service)
- Frontend: NodePort service (dynamically assigned, check with `kubectl get svc`)
- Local access: http://[minikube-ip]:[frontend-nodeport]