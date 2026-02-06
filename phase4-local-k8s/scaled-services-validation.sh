#!/bin/bash
# Script to validate that the application maintains functionality with scaled services

echo "Validating application functionality with scaled services..."

# Check that all deployments have the expected number of replicas
echo "=== Deployment Status ==="
kubectl get deployment backend-deployment
kubectl get deployment frontend-deployment

# Check that all pods are ready
echo "=== Ready Pods Count ==="
BACKEND_READY=$(kubectl get deployment backend-deployment -o jsonpath='{.status.readyReplicas}')
FRONTEND_READY=$(kubectl get deployment frontend-deployment -o jsonpath='{.status.readyReplicas}')

echo "Backend ready replicas: $BACKEND_READY"
echo "Frontend ready replicas: $FRONTEND_READY"

if [ "$BACKEND_READY" -eq 3 ] && [ "$FRONTEND_READY" -eq 3 ]; then
    echo "✓ All expected replicas are ready"
else
    echo "⚠ Some replicas are not ready as expected"
fi

# Check service accessibility
echo "=== Service Accessibility ==="
kubectl get svc frontend-service
kubectl get svc backend-service

# Test inter-service communication
echo "=== Testing Inter-Service Communication ==="
# Create a temporary pod to test connectivity
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: connectivity-test-scaled
spec:
  containers:
  - name: connectivity-test
    image: busybox
    command: ['sh', '-c', 'wget -qO- http://backend-service:80 || echo "Failed to reach backend"']
  restartPolicy: Never
EOF

# Wait for the test to complete
sleep 5

# Check the logs/results of the connectivity test
kubectl logs connectivity-test-scaled

# Clean up the test pod
kubectl delete pod connectivity-test-scaled

echo "Scaled services validation completed!"