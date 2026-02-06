#!/bin/bash
# Script to verify inter-service communication between frontend and backend

echo "Checking inter-service communication..."

# Create a test pod to check communication from within the cluster
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: connectivity-test
spec:
  containers:
  - name: connectivity-test
    image: busybox
    command: ['sh', '-c', 'wget -qO- http://backend-service:80']
  restartPolicy: Never
EOF

# Wait for the test to complete
sleep 5

# Check the logs/results of the connectivity test
kubectl logs connectivity-test

# Clean up the test pod
kubectl delete pod connectivity-test

echo "Inter-service communication verification completed!"