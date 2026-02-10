#!/bin/bash

# Phase 5 - Cloud Deployment Script
# Supports DigitalOcean (DOKS), Google Cloud (GKE), and Azure (AKS)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TERRAFORM_DIR="$SCRIPT_DIR/../terraform"
HELM_DIR="$SCRIPT_DIR/../helm"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 5 - Cloud Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check for required tools
check_requirements() {
    local missing_tools=()

    if ! command -v terraform &> /dev/null; then
        missing_tools+=("terraform")
    fi

    if ! command -v kubectl &> /dev/null; then
        missing_tools+=("kubectl")
    fi

    if ! command -v helm &> /dev/null; then
        missing_tools+=("helm")
    fi

    if [ ${#missing_tools[@]} -ne 0 ]; then
        echo -e "${RED}Error: Missing required tools: ${missing_tools[*]}${NC}"
        echo "Please install them and try again."
        exit 1
    fi

    echo -e "${GREEN}✓ All required tools are installed${NC}"
}

# Detect cloud provider
detect_cloud_provider() {
    echo ""
    echo -e "${BLUE}Select cloud provider:${NC}"
    echo "1) DigitalOcean (DOKS)"
    echo "2) Google Cloud (GKE)"
    echo "3) Azure (AKS)"
    read -p "Enter choice [1-3]: " choice

    case $choice in
        1)
            CLOUD_PROVIDER="digitalocean"
            echo -e "${GREEN}Selected: DigitalOcean${NC}"
            ;;
        2)
            CLOUD_PROVIDER="gcp"
            echo -e "${GREEN}Selected: Google Cloud${NC}"
            ;;
        3)
            CLOUD_PROVIDER="azure"
            echo -e "${GREEN}Selected: Azure${NC}"
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac
}

# Check cloud provider CLI
check_cloud_cli() {
    case $CLOUD_PROVIDER in
        digitalocean)
            if ! command -v doctl &> /dev/null; then
                echo -e "${RED}Error: doctl is not installed${NC}"
                echo "Install: https://docs.digitalocean.com/reference/doctl/how-to/install/"
                exit 1
            fi
            echo -e "${GREEN}✓ doctl is installed${NC}"
            ;;
        gcp)
            if ! command -v gcloud &> /dev/null; then
                echo -e "${RED}Error: gcloud is not installed${NC}"
                echo "Install: https://cloud.google.com/sdk/docs/install"
                exit 1
            fi
            echo -e "${GREEN}✓ gcloud is installed${NC}"
            ;;
        azure)
            if ! command -v az &> /dev/null; then
                echo -e "${RED}Error: az CLI is not installed${NC}"
                echo "Install: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
                exit 1
            fi
            echo -e "${GREEN}✓ az CLI is installed${NC}"
            ;;
    esac
}

# Get environment
get_environment() {
    echo ""
    read -p "Enter environment (dev/staging/production) [production]: " ENVIRONMENT
    ENVIRONMENT=${ENVIRONMENT:-production}
    echo -e "${GREEN}Environment: $ENVIRONMENT${NC}"
}

# Get region
get_region() {
    echo ""
    case $CLOUD_PROVIDER in
        digitalocean)
            echo "Common regions: nyc1, nyc3, sfo3, sgp1, lon1, fra1"
            read -p "Enter region [nyc3]: " REGION
            REGION=${REGION:-nyc3}
            ;;
        gcp)
            echo "Common regions: us-central1, us-east1, europe-west1, asia-east1"
            read -p "Enter region [us-central1]: " REGION
            REGION=${REGION:-us-central1}
            ;;
        azure)
            echo "Common regions: eastus, westus2, westeurope, southeastasia"
            read -p "Enter region [eastus]: " REGION
            REGION=${REGION:-eastus}
            ;;
    esac
    echo -e "${GREEN}Region: $REGION${NC}"
}

# Initialize Terraform
init_terraform() {
    echo ""
    echo -e "${BLUE}Initializing Terraform...${NC}"
    cd "$TERRAFORM_DIR"

    terraform init

    echo -e "${GREEN}✓ Terraform initialized${NC}"
}

# Plan Terraform
plan_terraform() {
    echo ""
    echo -e "${BLUE}Planning infrastructure...${NC}"

    terraform plan \
        -var="cloud_provider=$CLOUD_PROVIDER" \
        -var="environment=$ENVIRONMENT" \
        -var="region=$REGION" \
        -out=tfplan

    echo ""
    read -p "Do you want to apply this plan? (yes/no): " APPLY
    if [ "$APPLY" != "yes" ]; then
        echo -e "${YELLOW}Deployment cancelled${NC}"
        exit 0
    fi
}

# Apply Terraform
apply_terraform() {
    echo ""
    echo -e "${BLUE}Creating infrastructure...${NC}"

    terraform apply tfplan

    echo -e "${GREEN}✓ Infrastructure created${NC}"
}

# Configure kubectl
configure_kubectl() {
    echo ""
    echo -e "${BLUE}Configuring kubectl...${NC}"

    KUBECTL_CMD=$(terraform output -raw kubectl_config_command)
    eval "$KUBECTL_CMD"

    echo -e "${GREEN}✓ kubectl configured${NC}"
}

# Install Helm charts
install_helm_charts() {
    echo ""
    echo -e "${BLUE}Installing Helm charts...${NC}"

    cd "$HELM_DIR"

    # Get database connection string
    DB_URL=$(cd "$TERRAFORM_DIR" && terraform output -raw database_connection_string)
    REDIS_HOST=$(cd "$TERRAFORM_DIR" && terraform output -raw redis_host)
    REDIS_PORT=$(cd "$TERRAFORM_DIR" && terraform output -raw redis_port)

    # Install backend
    echo -e "${YELLOW}Installing backend...${NC}"
    helm install phase5-backend ./backend \
        --set database.url="$DB_URL" \
        --set redis.host="$REDIS_HOST" \
        --set redis.port="$REDIS_PORT" \
        --set config.nodeEnv="$ENVIRONMENT"

    # Install frontend
    echo -e "${YELLOW}Installing frontend...${NC}"
    helm install phase5-frontend ./frontend \
        --set config.nodeEnv="$ENVIRONMENT"

    # Install agents
    echo -e "${YELLOW}Installing agents...${NC}"
    helm install phase5-agents ./agents \
        --set database.url="$DB_URL" \
        --set config.nodeEnv="$ENVIRONMENT"

    echo -e "${GREEN}✓ Helm charts installed${NC}"
}

# Wait for deployments
wait_for_deployments() {
    echo ""
    echo -e "${BLUE}Waiting for deployments to be ready...${NC}"

    kubectl wait --for=condition=available --timeout=300s deployment --all

    echo -e "${GREEN}✓ All deployments are ready${NC}"
}

# Display access information
display_info() {
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Deployment Complete!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""

    cd "$TERRAFORM_DIR"

    FRONTEND_URL=$(terraform output -raw frontend_url)
    BACKEND_URL=$(terraform output -raw backend_url)

    echo -e "${BLUE}Access URLs:${NC}"
    echo -e "  Frontend: ${GREEN}$FRONTEND_URL${NC}"
    echo -e "  Backend:  ${GREEN}$BACKEND_URL${NC}"
    echo ""

    echo -e "${BLUE}Kubernetes Cluster:${NC}"
    CLUSTER_NAME=$(terraform output -raw kubernetes_cluster_name)
    echo -e "  Name: ${GREEN}$CLUSTER_NAME${NC}"
    echo ""

    echo -e "${BLUE}Next Steps:${NC}"
    echo "1. Configure DNS records to point to your cluster"
    echo "2. Set up SSL certificates (cert-manager)"
    echo "3. Configure monitoring (Prometheus, Grafana)"
    echo "4. Set up CI/CD pipeline"
    echo ""

    echo -e "${BLUE}Useful Commands:${NC}"
    echo "  View pods:        kubectl get pods"
    echo "  View services:    kubectl get svc"
    echo "  View logs:        kubectl logs -f <pod-name>"
    echo "  Helm releases:    helm list"
    echo ""
}

# Main execution
main() {
    check_requirements
    detect_cloud_provider
    check_cloud_cli
    get_environment
    get_region
    init_terraform
    plan_terraform
    apply_terraform
    configure_kubectl
    install_helm_charts
    wait_for_deployments
    display_info
}

# Run main function
main
