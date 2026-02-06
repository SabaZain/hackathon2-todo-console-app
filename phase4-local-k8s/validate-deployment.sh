#!/bin/bash
# Phase 4 Deployment Validation Script
# This script performs comprehensive validation of the Cloud Native Todo Chatbot deployment

echo "==========================================="
echo "Phase 4 Deployment Validation Script"
echo "==========================================="
echo ""

# Function to print section headers
print_section() {
    echo ""
    echo "==========================================="
    echo "$1"
    echo "==========================================="
}

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo "✅ $2"
    else
        echo "❌ $2"
    fi
}

# Function to print warning
print_warning() {
    echo "⚠️  $1"
}

# Function to print info
print_info() {
    echo "ℹ️  $1"
}

# Check prerequisites
print_section "Checking Prerequisites"

# Check if kubectl is available
if command -v kubectl &> /dev/null; then
    echo "✅ kubectl is installed"
    KUBECTL_AVAILABLE=1
else
    echo "❌ kubectl is not installed"
    KUBECTL_AVAILABLE=0
fi

# Check if Minikube is available
if command -v minikube &> /dev/null; then
    echo "✅ minikube is installed"
    MINIKUBE_AVAILABLE=1
else
    echo "❌ minikube is not installed"
    MINIKUBE_AVAILABLE=0
fi

# Check if Docker is running
if docker info &> /dev/null; then
    echo "✅ Docker is running"
    DOCKER_RUNNING=1
else
    echo "❌ Docker is not running"
    DOCKER_RUNNING=0
fi

# Check if we're in the right directory
if [ -d "phase4-local-k8s" ]; then
    echo "✅ Phase 4 directory found"
    cd phase4-local-k8s
else
    echo "❌ Phase 4 directory not found"
    echo "Please run this script from the hackathontwo directory"
    exit 1
fi

# Check if required files exist
if [ -f "frontend/Dockerfile" ] && [ -f "backend/Dockerfile" ]; then
    echo "✅ Dockerfiles found"
    DOCKERFILES_EXIST=1
else
    echo "❌ Dockerfiles not found"
    DOCKERFILES_EXIST=0
fi

if [ -f "frontend/frontend-deployment.yaml" ] && [ -f "backend/backend-deployment.yaml" ]; then
    echo "✅ Kubernetes deployment files found"
    K8S_FILES_EXIST=1
else
    echo "❌ Kubernetes deployment files not found"
    K8S_FILES_EXIST=0
fi

print_section "Checking Minikube Status"

if [ $MINIKUBE_AVAILABLE -eq 1 ]; then
    MINIKUBE_STATUS=$(minikube status --format='{{.Host}}' 2>/dev/null)
    if [ "$MINIKUBE_STATUS" = "Running" ]; then
        echo "✅ Minikube is running"
        MINIKUBE_RUNNING=1
    else
        echo "❌ Minikube is not running"
        MINIKUBE_RUNNING=0
    fi
else
    MINIKUBE_RUNNING=0
fi

print_section "Checking Docker Images"

# Check if frontend image exists
FRONTEND_IMAGE_EXISTS=0
if [ $DOCKER_RUNNING -eq 1 ]; then
    if docker images | grep -q "cloud-native-todo-frontend"; then
        echo "✅ Frontend Docker image exists"
        FRONTEND_IMAGE_EXISTS=1

        # Check if optimized image exists
        if docker images | grep -q "cloud-native-todo-frontend:optimized-v1.0.0"; then
            echo "✅ Optimized frontend image exists"
            FRONTEND_OPTIMIZED_EXISTS=1
        else
            echo "⚠️  Optimized frontend image does not exist"
            FRONTEND_OPTIMIZED_EXISTS=0
        fi
    else
        echo "❌ Frontend Docker image does not exist"
        FRONTEND_IMAGE_EXISTS=0
        FRONTEND_OPTIMIZED_EXISTS=0
    fi

    # Check if backend image exists
    BACKEND_IMAGE_EXISTS=0
    if docker images | grep -q "cloud-native-todo-backend"; then
        echo "✅ Backend Docker image exists"
        BACKEND_IMAGE_EXISTS=1

        # Check if optimized image exists
        if docker images | grep -q "cloud-native-todo-backend:optimized-v1.0.0"; then
            echo "✅ Optimized backend image exists"
            BACKEND_OPTIMIZED_EXISTS=1
        else
            echo "⚠️  Optimized backend image does not exist"
            BACKEND_OPTIMIZED_EXISTS=0
        fi
    else
        echo "❌ Backend Docker image does not exist"
        BACKEND_IMAGE_EXISTS=0
        BACKEND_OPTIMIZED_EXISTS=0
    fi
else
    FRONTEND_IMAGE_EXISTS=0
    BACKEND_IMAGE_EXISTS=0
    FRONTEND_OPTIMIZED_EXISTS=0
    BACKEND_OPTIMIZED_EXISTS=0
fi

print_section "Checking Kubernetes Resources"

if [ $KUBECTL_AVAILABLE -eq 1 ] && [ $MINIKUBE_RUNNING -eq 1 ]; then
    # Check deployments
    echo "Checking deployments..."

    # Check backend deployment
    if kubectl get deployment backend-deployment &> /dev/null; then
        echo "✅ Backend deployment exists"
        BACKEND_DEPLOYMENT_EXISTS=1

        # Check if backend pods are running
        BACKEND_REPLICAS=$(kubectl get deployment backend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null)
        BACKEND_EXPECTED_REPLICAS=$(kubectl get deployment backend-deployment -o jsonpath='{.spec.replicas}' 2>/dev/null)

        if [ "$BACKEND_REPLICAS" = "$BACKEND_EXPECTED_REPLICAS" ] && [ "$BACKEND_REPLICAS" != "" ]; then
            echo "✅ Backend deployment has $BACKEND_REPLICAS/$BACKEND_EXPECTED_REPLICAS ready replicas"
            BACKEND_DEPLOYMENT_READY=1
        else
            echo "❌ Backend deployment has $BACKEND_REPLICAS/$BACKEND_EXPECTED_REPLICAS ready replicas"
            BACKEND_DEPLOYMENT_READY=0
        fi
    else
        echo "❌ Backend deployment does not exist"
        BACKEND_DEPLOYMENT_EXISTS=0
        BACKEND_DEPLOYMENT_READY=0
    fi

    # Check frontend deployment
    if kubectl get deployment frontend-deployment &> /dev/null; then
        echo "✅ Frontend deployment exists"
        FRONTEND_DEPLOYMENT_EXISTS=1

        # Check if frontend pods are running
        FRONTEND_REPLICAS=$(kubectl get deployment frontend-deployment -o jsonpath='{.status.readyReplicas}' 2>/dev/null)
        FRONTEND_EXPECTED_REPLICAS=$(kubectl get deployment frontend-deployment -o jsonpath='{.spec.replicas}' 2>/dev/null)

        if [ "$FRONTEND_REPLICAS" = "$FRONTEND_EXPECTED_REPLICAS" ] && [ "$FRONTEND_REPLICAS" != "" ]; then
            echo "✅ Frontend deployment has $FRONTEND_REPLICAS/$FRONTEND_EXPECTED_REPLICAS ready replicas"
            FRONTEND_DEPLOYMENT_READY=1
        else
            echo "❌ Frontend deployment has $FRONTEND_REPLICAS/$FRONTEND_EXPECTED_REPLICAS ready replicas"
            FRONTEND_DEPLOYMENT_READY=0
        fi
    else
        echo "❌ Frontend deployment does not exist"
        FRONTEND_DEPLOYMENT_EXISTS=0
        FRONTEND_DEPLOYMENT_READY=0
    fi

    # Check services
    echo "Checking services..."

    if kubectl get service backend-service &> /dev/null; then
        echo "✅ Backend service exists"
        BACKEND_SERVICE_EXISTS=1
    else
        echo "❌ Backend service does not exist"
        BACKEND_SERVICE_EXISTS=0
    fi

    if kubectl get service frontend-service &> /dev/null; then
        echo "✅ Frontend service exists"
        FRONTEND_SERVICE_EXISTS=1

        # Get NodePort for frontend
        FRONTEND_NODEPORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
        if [ "$FRONTEND_NODEPORT" != "" ]; then
            MINIKUBE_IP=$(minikube ip 2>/dev/null)
            if [ "$MINIKUBE_IP" != "" ]; then
                echo "ℹ️  Frontend should be accessible at: http://$MINIKUBE_IP:$FRONTEND_NODEPORT"
            fi
        fi
    else
        echo "❌ Frontend service does not exist"
        FRONTEND_SERVICE_EXISTS=0
    fi

    # Check pods
    echo "Checking pods..."
    POD_COUNT=$(kubectl get pods --no-headers 2>/dev/null | wc -l)
    echo "ℹ️  Total pods running: $POD_COUNT"

    # Check if pods are in Running state
    RUNNING_PODS=$(kubectl get pods --field-selector=status.phase=Running --no-headers 2>/dev/null | wc -l)
    echo "ℹ️  Pods in Running state: $RUNNING_PODS"

    if [ "$POD_COUNT" -gt 0 ] && [ "$RUNNING_PODS" -eq "$POD_COUNT" ]; then
        echo "✅ All pods are running"
        PODS_RUNNING=1
    elif [ "$RUNNING_PODS" -gt 0 ]; then
        echo "⚠️  Some pods are running, some are not"
        PODS_RUNNING=0
    else
        echo "❌ No pods are running"
        PODS_RUNNING=0
    fi
else
    # Set defaults if kubectl/minikube not available
    BACKEND_DEPLOYMENT_EXISTS=0
    BACKEND_DEPLOYMENT_READY=0
    FRONTEND_DEPLOYMENT_EXISTS=0
    FRONTEND_DEPLOYMENT_READY=0
    BACKEND_SERVICE_EXISTS=0
    FRONTEND_SERVICE_EXISTS=0
    PODS_RUNNING=0
fi

print_section "Checking Inter-Service Communication"

if [ $KUBECTL_AVAILABLE -eq 1 ] && [ $MINIKUBE_RUNNING -eq 1 ] && [ $BACKEND_SERVICE_EXISTS -eq 1 ]; then
    # Test connectivity from within the cluster
    echo "Testing inter-service communication..."

    # Create a temporary pod to test connectivity
    cat <<EOF | kubectl apply -f - 2>/dev/null
apiVersion: v1
kind: Pod
metadata:
  name: connectivity-test-validation
spec:
  containers:
  - name: connectivity-test
    image: busybox
    command: ['sh', '-c', 'echo Testing... && wget -qO- http://backend-service:80 || echo Failed to reach backend']
  restartPolicy: Never
EOF

    # Wait a bit for the pod to run
    sleep 10

    # Check the result
    CONNECTIVITY_RESULT=$(kubectl logs connectivity-test-validation 2>/dev/null)
    if echo "$CONNECTIVITY_RESULT" | grep -q "Testing\|Failed"; then
        if echo "$CONNECTIVITY_RESULT" | grep -q "Failed"; then
            echo "❌ Inter-service communication test failed"
            INTER_SERVICE_COMM=0
        else
            echo "✅ Inter-service communication test passed"
            INTER_SERVICE_COMM=1
        fi
    else
        echo "⚠️  Could not complete inter-service communication test"
        INTER_SERVICE_COMM=0
    fi

    # Clean up the test pod
    kubectl delete pod connectivity-test-validation 2>/dev/null
else
    INTER_SERVICE_COMM=0
fi

print_section "Checking External Accessibility"

if [ $KUBECTL_AVAILABLE -eq 1 ] && [ $MINIKUBE_RUNNING -eq 1 ] && [ $FRONTEND_SERVICE_EXISTS -eq 1 ]; then
    # Get frontend service access info
    FRONTEND_NODEPORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
    MINIKUBE_IP=$(minikube ip 2>/dev/null)

    if [ "$FRONTEND_NODEPORT" != "" ] && [ "$MINIKUBE_IP" != "" ]; then
        ACCESS_URL="http://$MINIKUBE_IP:$FRONTEND_NODEPORT"
        echo "ℹ️  Testing external access: $ACCESS_URL"

        # Test accessibility if curl is available
        if command -v curl &> /dev/null; then
            if curl -s --max-time 10 "$ACCESS_URL" &> /dev/null; then
                echo "✅ External access test passed"
                EXTERNAL_ACCESS=1
            else
                echo "⚠️  External access test timed out (may still be starting up)"
                EXTERNAL_ACCESS=0
            fi
        else
            echo "ℹ️  curl not available for external access test"
            EXTERNAL_ACCESS=0
        fi
    else
        echo "❌ Could not determine external access URL"
        EXTERNAL_ACCESS=0
    fi
else
    EXTERNAL_ACCESS=0
fi

print_section "Checking Resource Utilization"

if [ $KUBECTL_AVAILABLE -eq 1 ] && [ $MINIKUBE_RUNNING -eq 1 ]; then
    echo "Checking resource utilization..."

    # Check if metrics server is available
    if kubectl top pods &> /dev/null; then
        echo "ℹ️  Resource utilization:"
        kubectl top pods 2>/dev/null || echo "  Resource metrics not available"
    else
        echo "⚠️  Metrics server not available, skipping resource utilization check"
    fi
else
    echo "ℹ️  Skipping resource utilization check (kubectl/minikube not available)"
fi

print_section "Checking Helm Releases (if installed)"

HELM_AVAILABLE=0
if command -v helm &> /dev/null; then
    HELM_AVAILABLE=1
    echo "✅ Helm is installed"

    # Check for Helm releases
    HELM_RELEASES=$(helm list --short 2>/dev/null | wc -l)
    if [ "$HELM_RELEASES" -gt 0 ]; then
        echo "ℹ️  Helm releases found: $HELM_RELEASES"
        helm list 2>/dev/null || echo "  Could not list releases"
        HELM_DEPLOYED=1
    else
        echo "ℹ️  No Helm releases found"
        HELM_DEPLOYED=0
    fi
else
    echo "ℹ️  Helm not installed, skipping Helm check"
    HELM_DEPLOYED=0
fi

print_section "Deployment Validation Summary"

# Calculate scores
SCORE=0
TOTAL=0

echo "Prerequisites:"
((TOTAL++))
if [ $KUBECTL_AVAILABLE -eq 1 ]; then ((SCORE++)); print_status 0 "kubectl available"; else print_status 1 "kubectl available"; fi

((TOTAL++))
if [ $MINIKUBE_AVAILABLE -eq 1 ]; then ((SCORE++)); print_status 0 "minikube available"; else print_status 1 "minikube available"; fi

((TOTAL++))
if [ $DOCKER_RUNNING -eq 1 ]; then ((SCORE++)); print_status 0 "docker running"; else print_status 1 "docker running"; fi

((TOTAL++))
if [ $DOCKERFILES_EXIST -eq 1 ]; then ((SCORE++)); print_status 0 "dockerfiles exist"; else print_status 1 "dockerfiles exist"; fi

((TOTAL++))
if [ $K8S_FILES_EXIST -eq 1 ]; then ((SCORE++)); print_status 0 "k8s files exist"; else print_status 1 "k8s files exist"; fi

echo ""
echo "Docker Images:"
((TOTAL++))
if [ $FRONTEND_IMAGE_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "frontend image exists"; else print_status 1 "frontend image exists"; fi

((TOTAL++))
if [ $BACKEND_IMAGE_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "backend image exists"; else print_status 1 "backend image exists"; fi

((TOTAL++))
if [ $FRONTEND_OPTIMIZED_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "frontend optimized image exists"; else print_status 1 "frontend optimized image exists"; fi

((TOTAL++))
if [ $BACKEND_OPTIMIZED_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "backend optimized image exists"; else print_status 1 "backend optimized image exists"; fi

echo ""
echo "Kubernetes Resources:"
((TOTAL++))
if [ $MINIKUBE_RUNNING -eq 1 ]; then ((SCORE++)); print_status 0 "minikube running"; else print_status 1 "minikube running"; fi

((TOTAL++))
if [ $BACKEND_DEPLOYMENT_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "backend deployment exists"; else print_status 1 "backend deployment exists"; fi

((TOTAL++))
if [ $BACKEND_DEPLOYMENT_READY -eq 1 ]; then ((SCORE++)); print_status 0 "backend deployment ready"; else print_status 1 "backend deployment ready"; fi

((TOTAL++))
if [ $FRONTEND_DEPLOYMENT_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "frontend deployment exists"; else print_status 1 "frontend deployment exists"; fi

((TOTAL++))
if [ $FRONTEND_DEPLOYMENT_READY -eq 1 ]; then ((SCORE++)); print_status 0 "frontend deployment ready"; else print_status 1 "frontend deployment ready"; fi

((TOTAL++))
if [ $BACKEND_SERVICE_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "backend service exists"; else print_status 1 "backend service exists"; fi

((TOTAL++))
if [ $FRONTEND_SERVICE_EXISTS -eq 1 ]; then ((SCORE++)); print_status 0 "frontend service exists"; else print_status 1 "frontend service exists"; fi

((TOTAL++))
if [ $PODS_RUNNING -eq 1 ]; then ((SCORE++)); print_status 0 "pods running"; else print_status 1 "pods running"; fi

echo ""
echo "Connectivity & Validation:"
((TOTAL++))
if [ $INTER_SERVICE_COMM -eq 1 ]; then ((SCORE++)); print_status 0 "inter-service communication"; else print_status 1 "inter-service communication"; fi

((TOTAL++))
if [ $EXTERNAL_ACCESS -eq 1 ]; then ((SCORE++)); print_status 0 "external access"; else print_status 1 "external access"; fi

((TOTAL++))
if [ $HELM_DEPLOYED -eq 1 ]; then ((SCORE++)); print_status 0 "helm releases deployed"; else print_status 1 "helm releases deployed"; fi

echo ""
echo "==========================================="
echo "VALIDATION SCORE: $SCORE/$TOTAL"
PERCENTAGE=$((SCORE * 100 / TOTAL))
echo "SUCCESS RATE: $PERCENTAGE%"
echo "==========================================="

if [ $PERCENTAGE -ge 90 ]; then
    echo "🎉 EXCELLENT! Deployment validation passed with high score!"
    echo "Your Cloud Native Todo Chatbot is properly deployed and accessible."
elif [ $PERCENTAGE -ge 70 ]; then
    echo "👍 GOOD! Deployment validation passed with acceptable score!"
    echo "Most components are working, but there may be minor issues."
elif [ $PERCENTAGE -ge 50 ]; then
    echo "⚠️  NEEDS ATTENTION! Deployment validation has issues."
    echo "Several components are not working as expected."
else
    echo "❌ FAILED! Deployment validation has major issues."
    echo "Critical components are not working properly."
fi

echo ""
echo "==========================================="
echo "RECOMMENDATIONS:"
echo "==========================================="

if [ $KUBECTL_AVAILABLE -eq 0 ]; then
    echo "• Install kubectl to manage Kubernetes resources"
fi

if [ $MINIKUBE_AVAILABLE -eq 0 ]; then
    echo "• Install Minikube to run Kubernetes locally"
fi

if [ $DOCKER_RUNNING -eq 0 ]; then
    echo "• Start Docker Desktop to build and run container images"
fi

if [ $FRONTEND_IMAGE_EXISTS -eq 0 ]; then
    echo "• Build frontend Docker image: cd frontend && ./build-image.sh"
fi

if [ $BACKEND_IMAGE_EXISTS -eq 0 ]; then
    echo "• Build backend Docker image: cd backend && ./build-image.sh"
fi

if [ $MINIKUBE_RUNNING -eq 0 ]; then
    echo "• Start Minikube: minikube start --cpus=4 --memory=8192 --disk-size=20g"
fi

if [ $BACKEND_DEPLOYMENT_EXISTS -eq 0 ]; then
    echo "• Deploy backend: kubectl apply -f backend/backend-deployment.yaml"
fi

if [ $FRONTEND_DEPLOYMENT_EXISTS -eq 0 ]; then
    echo "• Deploy frontend: kubectl apply -f frontend/frontend-deployment.yaml"
fi

if [ $BACKEND_SERVICE_EXISTS -eq 0 ]; then
    echo "• Verify backend deployment has a service component"
fi

if [ $FRONTEND_SERVICE_EXISTS -eq 0 ]; then
    echo "• Verify frontend deployment has a service component"
fi

if [ $INTER_SERVICE_COMM -eq 0 ]; then
    echo "• Check if backend service name matches what frontend expects"
    echo "• Verify environment variables in frontend deployment"
fi

if [ $EXTERNAL_ACCESS -eq 0 ]; then
    echo "• Wait a bit longer for services to become available"
    echo "• Check NodePort and Minikube IP: minikube ip && kubectl get service frontend-service"
fi

echo ""
echo "For detailed troubleshooting, check:"
echo "• Pod logs: kubectl logs -l app=backend"
echo "• Pod logs: kubectl logs -l app=frontend"
echo "• Pod status: kubectl get pods -o wide"
echo "• Events: kubectl get events --sort-by='.lastTimestamp'"
echo ""