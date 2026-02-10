#!/bin/bash

# Phase 5 - Minikube Deployment Script
# This script deploys Phase 5 to a local Minikube cluster

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
K8S_DIR="$SCRIPT_DIR/../kubernetes/minikube"
BACKEND_DIR="$SCRIPT_DIR/../../backend"
FRONTEND_DIR="$SCRIPT_DIR/../../frontend"
AGENTS_DIR="$SCRIPT_DIR/../../agents"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 5 - Minikube Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Minikube is installed
if ! command -v minikube &> /dev/null; then
    echo -e "${RED}Error: Minikube is not installed. Please install it and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Minikube is installed${NC}"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed. Please install it and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ kubectl is installed${NC}"
echo ""

# Check if Minikube is running
if ! minikube status &> /dev/null; then
    echo -e "${YELLOW}Minikube is not running. Starting Minikube...${NC}"
    minikube start --cpus=4 --memory=8192 --driver=docker
    echo -e "${GREEN}✓ Minikube started${NC}"
else
    echo -e "${GREEN}✓ Minikube is running${NC}"
fi

# Enable Ingress addon
echo ""
echo -e "${BLUE}Enabling Ingress addon...${NC}"
minikube addons enable ingress
echo -e "${GREEN}✓ Ingress addon enabled${NC}"

# Set Docker environment to use Minikube's Docker daemon
echo ""
echo -e "${BLUE}Setting Docker environment to Minikube...${NC}"
eval $(minikube docker-env)
echo -e "${GREEN}✓ Docker environment set${NC}"

# Build Docker images
echo ""
echo -e "${BLUE}Building Docker images...${NC}"

echo -e "${YELLOW}Building backend image...${NC}"
docker build -t phase5-backend:latest "$BACKEND_DIR"

echo -e "${YELLOW}Building frontend image...${NC}"
docker build -t phase5-frontend:latest "$FRONTEND_DIR"

echo -e "${YELLOW}Building audit-agent image...${NC}"
docker build -t phase5-audit-agent:latest "$AGENTS_DIR/audit-agent"

echo -e "${YELLOW}Building reminder-agent image...${NC}"
docker build -t phase5-reminder-agent:latest "$AGENTS_DIR/reminder-agent"

echo -e "${YELLOW}Building recurring-task-agent image...${NC}"
docker build -t phase5-recurring-task-agent:latest "$AGENTS_DIR/recurring-task-agent"

echo -e "${YELLOW}Building realtime-sync-agent image...${NC}"
docker build -t phase5-realtime-sync-agent:latest "$AGENTS_DIR/realtime-sync-agent"

echo -e "${GREEN}✓ All images built${NC}"

# Apply Kubernetes manifests
echo ""
echo -e "${BLUE}Applying Kubernetes manifests...${NC}"

echo -e "${YELLOW}Creating namespace...${NC}"
kubectl apply -f "$K8S_DIR/namespace.yaml"

echo -e "${YELLOW}Creating ConfigMap...${NC}"
kubectl apply -f "$K8S_DIR/configmap.yaml"

echo -e "${YELLOW}Creating Secrets...${NC}"
kubectl apply -f "$K8S_DIR/secrets.yaml"

echo -e "${YELLOW}Deploying PostgreSQL and Redis...${NC}"
kubectl apply -f "$K8S_DIR/postgres.yaml"

echo -e "${YELLOW}Deploying Kafka and Zookeeper...${NC}"
kubectl apply -f "$K8S_DIR/kafka.yaml"

echo ""
echo -e "${BLUE}Waiting for infrastructure to be ready...${NC}"
kubectl wait --for=condition=ready --timeout=300s pod -l app=postgres -n phase5
kubectl wait --for=condition=ready --timeout=300s pod -l app=kafka -n phase5
echo -e "${GREEN}✓ Infrastructure is ready${NC}"

echo ""
echo -e "${YELLOW}Initializing Kafka topics...${NC}"
kubectl wait --for=condition=complete --timeout=120s job/kafka-init -n phase5
echo -e "${GREEN}✓ Kafka topics initialized${NC}"

echo ""
echo -e "${YELLOW}Deploying backend...${NC}"
kubectl apply -f "$K8S_DIR/backend.yaml"

echo -e "${YELLOW}Deploying frontend...${NC}"
kubectl apply -f "$K8S_DIR/frontend.yaml"

echo -e "${YELLOW}Deploying agents...${NC}"
kubectl apply -f "$K8S_DIR/agents.yaml"

echo -e "${YELLOW}Creating Ingress...${NC}"
kubectl apply -f "$K8S_DIR/ingress.yaml"

echo -e "${GREEN}✓ All manifests applied${NC}"

# Wait for deployments to be ready
echo ""
echo -e "${BLUE}Waiting for application deployments to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/backend -n phase5
kubectl wait --for=condition=available --timeout=300s deployment/frontend -n phase5
echo -e "${GREEN}✓ Application deployments are ready${NC}"

# Get Minikube IP
MINIKUBE_IP=$(minikube ip)

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Access the application:${NC}"
echo -e "  Frontend:    ${GREEN}http://$MINIKUBE_IP:30000${NC}"
echo -e "  Backend API: ${GREEN}http://$MINIKUBE_IP:30001${NC}"
echo ""
echo -e "${BLUE}Or use port forwarding:${NC}"
echo -e "  Frontend:    ${YELLOW}kubectl port-forward -n phase5 svc/frontend 3000:3000${NC}"
echo -e "  Backend:     ${YELLOW}kubectl port-forward -n phase5 svc/backend 3001:3001${NC}"
echo ""
echo -e "${BLUE}View resources:${NC}"
echo -e "  Pods:        ${YELLOW}kubectl get pods -n phase5${NC}"
echo -e "  Services:    ${YELLOW}kubectl get svc -n phase5${NC}"
echo -e "  Deployments: ${YELLOW}kubectl get deployments -n phase5${NC}"
echo ""
echo -e "${BLUE}View logs:${NC}"
echo -e "  Backend:     ${YELLOW}kubectl logs -n phase5 -l app=backend -f${NC}"
echo -e "  Frontend:    ${YELLOW}kubectl logs -n phase5 -l app=frontend -f${NC}"
echo ""
echo -e "${BLUE}Delete deployment:${NC}"
echo -e "  ${YELLOW}kubectl delete namespace phase5${NC}"
echo ""
