#!/bin/bash

# Phase 5 - Stop Local Services Script
# This script stops all Phase 5 services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$SCRIPT_DIR/../docker"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 5 - Stopping Services${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Navigate to docker directory
cd "$DOCKER_DIR"

echo -e "${YELLOW}Stopping all services...${NC}"
docker-compose down

echo ""
echo -e "${GREEN}✓ All services stopped${NC}"
echo ""
echo -e "${YELLOW}To remove volumes (data will be lost):${NC}"
echo -e "  ${BLUE}docker-compose down -v${NC}"
echo ""
echo -e "${YELLOW}To remove volumes and images:${NC}"
echo -e "  ${BLUE}./scripts/clean.sh${NC}"
echo ""
