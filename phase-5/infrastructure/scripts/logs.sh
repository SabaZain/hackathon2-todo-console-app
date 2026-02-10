#!/bin/bash

# Phase 5 - View Logs Script
# This script displays logs from Phase 5 services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$SCRIPT_DIR/../docker"

# Navigate to docker directory
cd "$DOCKER_DIR"

# Check if a service name was provided
if [ -z "$1" ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Phase 5 - View All Logs${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Showing logs from all services (Ctrl+C to exit)...${NC}"
    echo ""
    docker-compose logs -f
else
    SERVICE=$1
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}Phase 5 - View Logs: $SERVICE${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}Showing logs from $SERVICE (Ctrl+C to exit)...${NC}"
    echo ""
    docker-compose logs -f "$SERVICE"
fi

echo ""
echo -e "${BLUE}Available services:${NC}"
echo -e "  - backend"
echo -e "  - frontend"
echo -e "  - audit-agent"
echo -e "  - reminder-agent"
echo -e "  - recurring-task-agent"
echo -e "  - realtime-sync-agent"
echo -e "  - postgres"
echo -e "  - redis"
echo -e "  - kafka"
echo -e "  - zookeeper"
echo -e "  - kafka-ui"
echo ""
echo -e "${YELLOW}Usage:${NC}"
echo -e "  All logs:     ${BLUE}./scripts/logs.sh${NC}"
echo -e "  Single service: ${BLUE}./scripts/logs.sh <service-name>${NC}"
echo ""
