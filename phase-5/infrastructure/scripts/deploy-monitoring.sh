#!/bin/bash

# Phase 5 Monitoring Stack Deployment Script
# Deploys Prometheus, Grafana, Jaeger, Loki, and Alertmanager

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITORING_DIR="$(dirname "$SCRIPT_DIR")/monitoring"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    if ! command -v kubectl &> /dev/null; then
        print_error "kubectl not found. Please install kubectl."
        exit 1
    fi
    print_success "kubectl found"

    if ! kubectl cluster-info &> /dev/null; then
        print_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    print_success "Connected to Kubernetes cluster"

    echo ""
}

# Create monitoring namespace
create_namespace() {
    print_header "Creating Monitoring Namespace"

    if kubectl get namespace monitoring &> /dev/null; then
        print_warning "Namespace 'monitoring' already exists"
    else
        kubectl create namespace monitoring
        print_success "Created namespace 'monitoring'"
    fi

    if kubectl get namespace tracing &> /dev/null; then
        print_warning "Namespace 'tracing' already exists"
    else
        kubectl create namespace tracing
        print_success "Created namespace 'tracing'"
    fi

    echo ""
}

# Deploy Prometheus
deploy_prometheus() {
    print_header "Deploying Prometheus"

    print_info "Applying Prometheus configuration..."
    kubectl apply -f "$MONITORING_DIR/prometheus/prometheus.yaml"

    print_info "Applying recording rules..."
    kubectl apply -f "$MONITORING_DIR/prometheus/rules/recording-rules.yaml"

    print_info "Applying alert rules..."
    kubectl apply -f "$MONITORING_DIR/prometheus/alerts/phase5-alerts.yaml"

    print_info "Waiting for Prometheus to be ready..."
    kubectl wait --for=condition=ready pod -l app=prometheus -n monitoring --timeout=300s

    print_success "Prometheus deployed successfully"
    echo ""
}

# Deploy Alertmanager
deploy_alertmanager() {
    print_header "Deploying Alertmanager"

    # Check if secrets exist
    if ! kubectl get secret alertmanager-secrets -n monitoring &> /dev/null; then
        print_warning "Alertmanager secrets not found. Creating default secrets..."
        print_warning "Please update these secrets with your actual configuration!"
        kubectl apply -f "$MONITORING_DIR/alertmanager/alertmanager.yaml"
    else
        print_info "Using existing Alertmanager secrets"
        kubectl apply -f "$MONITORING_DIR/alertmanager/alertmanager.yaml"
    fi

    print_info "Waiting for Alertmanager to be ready..."
    kubectl wait --for=condition=ready pod -l app=alertmanager -n monitoring --timeout=180s

    print_success "Alertmanager deployed successfully"
    echo ""
}

# Deploy Grafana
deploy_grafana() {
    print_header "Deploying Grafana"

    print_info "Applying Grafana datasources..."
    kubectl apply -f "$MONITORING_DIR/grafana/datasources.yaml"

    print_info "Applying Grafana dashboards..."
    kubectl apply -f "$MONITORING_DIR/grafana/dashboards.yaml"

    print_info "Applying Grafana deployment..."
    kubectl apply -f "$MONITORING_DIR/grafana/grafana.yaml"

    print_info "Waiting for Grafana to be ready..."
    kubectl wait --for=condition=ready pod -l app=grafana -n monitoring --timeout=180s

    print_success "Grafana deployed successfully"
    echo ""
}

# Deploy Jaeger
deploy_jaeger() {
    print_header "Deploying Jaeger"

    print_info "Applying Jaeger configuration..."
    kubectl apply -f "$MONITORING_DIR/jaeger/jaeger.yaml"

    print_info "Waiting for Jaeger to be ready..."
    kubectl wait --for=condition=ready pod -l app=jaeger -n tracing --timeout=180s

    print_success "Jaeger deployed successfully"
    echo ""
}

# Deploy Loki
deploy_loki() {
    print_header "Deploying Loki"

    print_info "Applying Loki configuration..."
    kubectl apply -f "$MONITORING_DIR/loki/loki.yaml"

    print_info "Waiting for Loki to be ready..."
    kubectl wait --for=condition=ready pod -l app=loki -n monitoring --timeout=300s

    print_info "Waiting for Promtail DaemonSet..."
    kubectl rollout status daemonset/promtail -n monitoring --timeout=180s

    print_success "Loki and Promtail deployed successfully"
    echo ""
}

# Display access information
display_access_info() {
    print_header "Access Information"

    echo -e "${GREEN}Monitoring Stack Deployed Successfully!${NC}"
    echo ""
    echo "To access the services, use port forwarding:"
    echo ""
    echo -e "${BLUE}Prometheus:${NC}"
    echo "  kubectl port-forward -n monitoring svc/prometheus 9090:9090"
    echo "  URL: http://localhost:9090"
    echo ""
    echo -e "${BLUE}Grafana:${NC}"
    echo "  kubectl port-forward -n monitoring svc/grafana 3000:3000"
    echo "  URL: http://localhost:3000"
    echo "  Username: admin"
    echo "  Password: (check secret: kubectl get secret grafana-secrets -n monitoring -o jsonpath='{.data.admin-password}' | base64 -d)"
    echo ""
    echo -e "${BLUE}Alertmanager:${NC}"
    echo "  kubectl port-forward -n monitoring svc/alertmanager 9093:9093"
    echo "  URL: http://localhost:9093"
    echo ""
    echo -e "${BLUE}Jaeger:${NC}"
    echo "  kubectl port-forward -n tracing svc/jaeger-query 16686:16686"
    echo "  URL: http://localhost:16686"
    echo ""
    echo -e "${BLUE}Loki:${NC}"
    echo "  Access through Grafana (already configured as datasource)"
    echo "  Direct API: kubectl port-forward -n monitoring svc/loki 3100:3100"
    echo ""
    echo -e "${YELLOW}Next Steps:${NC}"
    echo "1. Update Alertmanager secrets with your Slack/Email configuration"
    echo "2. Configure alert notification channels"
    echo "3. Instrument your applications with Prometheus metrics"
    echo "4. Add Jaeger tracing to your services"
    echo "5. Use structured JSON logging for better Loki integration"
    echo ""
}

# Verify deployment
verify_deployment() {
    print_header "Verifying Deployment"

    local all_ready=true

    # Check Prometheus
    if kubectl get pods -n monitoring -l app=prometheus | grep -q "Running"; then
        print_success "Prometheus is running"
    else
        print_error "Prometheus is not running"
        all_ready=false
    fi

    # Check Alertmanager
    if kubectl get pods -n monitoring -l app=alertmanager | grep -q "Running"; then
        print_success "Alertmanager is running"
    else
        print_error "Alertmanager is not running"
        all_ready=false
    fi

    # Check Grafana
    if kubectl get pods -n monitoring -l app=grafana | grep -q "Running"; then
        print_success "Grafana is running"
    else
        print_error "Grafana is not running"
        all_ready=false
    fi

    # Check Jaeger
    if kubectl get pods -n tracing -l app=jaeger | grep -q "Running"; then
        print_success "Jaeger is running"
    else
        print_error "Jaeger is not running"
        all_ready=false
    fi

    # Check Loki
    if kubectl get pods -n monitoring -l app=loki | grep -q "Running"; then
        print_success "Loki is running"
    else
        print_error "Loki is not running"
        all_ready=false
    fi

    # Check Promtail
    if kubectl get daemonset promtail -n monitoring &> /dev/null; then
        print_success "Promtail DaemonSet is deployed"
    else
        print_error "Promtail DaemonSet is not deployed"
        all_ready=false
    fi

    echo ""

    if [ "$all_ready" = true ]; then
        print_success "All monitoring components are healthy!"
    else
        print_warning "Some components are not ready. Check logs for details."
    fi

    echo ""
}

# Main deployment flow
main() {
    print_header "Phase 5 Monitoring Stack Deployment"
    echo ""

    check_prerequisites
    create_namespace
    deploy_prometheus
    deploy_alertmanager
    deploy_grafana
    deploy_jaeger
    deploy_loki
    verify_deployment
    display_access_info

    print_success "Monitoring stack deployment complete!"
}

# Run main function
main
