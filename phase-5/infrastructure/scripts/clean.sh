#!/bin/bash

# Phase 5 - Clean Up Script
# This script removes all containers, volumes, and images

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

echo -e "${RED}========================================${NC}"
echo -e "${RED}Phase 5 - Clean Up${NC}"
echo -e "${RED}========================================${NC}"
echo ""
echo -e "${YELLOW}⚠ WARNING: This will remove:${NC}"
echo -e "  - All Phase 5 containers"
echo -e "  - All Phase 5 volumes (DATABASE DATA WILL BE LOST)"
echo -e "  - All Phase 5 images"
echo ""
read -p "Are you sure you want to continue? (yes/no): " -r
echo ""

if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
    echo -e "${GREEN}Cancelled.${NC}"
    exit 0
fi

# Navigate to docker directory
cd "$DOCKER_DIR"

echo -e "${YELLOW}Stopping all services...${NC}"
docker-compose down -v

echo ""
echo -e "${YELLOW}Removing Phase 5 images...${NC}"
docker-compose down --rmi all

echo ""
echo -e "${YELLOW}Removing dangling volumes...${NC}"
docker volume prune -f

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Clean Up Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}All Phase 5 containers, volumes, and images have been removed.${NC}"
echo ""
