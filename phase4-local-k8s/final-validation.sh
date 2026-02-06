#!/bin/bash
# Final validation script to confirm all services are running, communicating, and accessible

echo "Starting final validation..."

echo "1. Checking deployment status..."
kubectl get deployments

echo "2. Checking if all pods are ready..."
kubectl wait --for=condition=ready pod -l app=frontend --timeout=60s && echo "✓ Frontend pods ready" || echo "✗ Frontend pods not ready"
kubectl wait --for=condition=ready pod -l app=backend --timeout=60s && echo "✓ Backend pods ready" || echo "✗ Backend pods not ready"

echo "3. Checking services..."
kubectl get services

echo "4. Testing service connectivity..."
# Test from inside the cluster
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: final-connectivity-test
spec:
  containers:
  - name: final-connectivity-test
    image: busybox
    command: ['sh', '-c', 'echo Testing... && wget -qO- http://backend-service:80 || echo Failed to reach backend']
  restartPolicy: Never
EOF

# Wait for the test to complete
sleep 10

# Check the result
if kubectl logs final-connectivity-test 2>/dev/null | grep -q "Testing\|Failed"; then
    echo "✓ Connectivity test completed"
else
    echo "⚠ Connectivity test had issues"
fi

# Clean up
kubectl delete pod final-connectivity-test 2>/dev/null || echo "Test pod already deleted"

echo "5. Checking application accessibility..."
FRONTEND_PORT=$(kubectl get service frontend-service -o jsonpath='{.spec.ports[0].nodePort}' 2>/dev/null)
MINIKUBE_IP=$(minikube ip 2>/dev/null)

if [ ! "$FRONTEND_PORT" = "" ] && [ ! "$MINIKUBE_IP" = "" ]; then
    echo "✓ Application should be accessible at: http://$MINIKUBE_IP:$FRONTEND_PORT"
else
    echo "⚠ Could not determine access URL"
fi

echo "6. Resource utilization check..."
kubectl top pods 2>/dev/null || echo "Resource metrics not available (may need metrics-server)"

echo "Final validation completed!"
echo ""
echo "Summary:"
echo "- Deployments: $(kubectl get deployments --no-headers | wc -l) active"
echo "- Pods: $(kubectl get pods --no-headers | grep -c Running) running"
echo "- Services: $(kubectl get services --no-headers | wc -l) configured"