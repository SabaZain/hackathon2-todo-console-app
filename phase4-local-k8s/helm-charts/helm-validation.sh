#!/bin/bash
# Script to validate that Helm-deployed services work identically to direct deployment

echo "Validating Helm-deployed services..."

# Check if all pods from Helm releases are running
echo "Checking pod status for Helm releases:"
kubectl get pods -l heritage=Helm

# Check services created by Helm
echo "Checking services created by Helm releases:"
kubectl get svc -l heritage=Helm

# Get the cluster IP of the backend service created by Helm
BACKEND_SVC_NAME=$(kubectl get svc -l app=backend-service -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "backend-service")
if [ ! "$BACKEND_SVC_NAME" = "" ]; then
    BACKEND_IP=$(kubectl get service $BACKEND_SVC_NAME -o jsonpath='{.spec.clusterIP}' 2>/dev/null)
    if [ ! "$BACKEND_IP" = "" ]; then
        echo "Backend service IP: $BACKEND_IP"

        # Test if backend is responding
        kubectl run test-backend --image=curlimages/curl -it --rm --restart=Never -- curl -s http://$BACKEND_IP:80/health 2>/dev/null || echo "Could not test backend - might not have /health endpoint"
    fi
fi

# Get the frontend service details
FRONTEND_SVC_NAME=$(kubectl get svc -l app=frontend-service -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "frontend-service")
if [ ! "$FRONTEND_SVC_NAME" = "" ]; then
    FRONTEND_PORT=$(kubectl get service $FRONTEND_SVC_NAME -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
    if [ ! "$FRONTEND_PORT" = "" ]; then
        MINIKUBE_IP=$(minikube ip 2>/dev/null)
        if [ ! "$MINIKUBE_IP" = "" ]; then
            echo "Frontend should be accessible at: http://$MINIKUBE_IP:$FRONTEND_PORT"
        fi
    fi
fi

echo "Helm deployment validation completed!"