#!/bin/bash

# Phase 5 - Local Deployment Script
# This script starts all Phase 5 services using Docker Compose

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
BACKEND_DIR="$SCRIPT_DIR/../../backend"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Phase 5 - Local Deployment${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Docker is running${NC}"

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose is not installed. Please install it and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ docker-compose is available${NC}"
echo ""

# Navigate to docker directory
cd "$DOCKER_DIR"

# Check if .env file exists in backend
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo -e "${YELLOW}⚠ Backend .env file not found. Creating from .env.example...${NC}"
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        echo -e "${GREEN}✓ Created backend .env file${NC}"
    else
        echo -e "${RED}Error: .env.example not found in backend directory${NC}"
        exit 1
    fi
fi

echo -e "${BLUE}Starting infrastructure services...${NC}"
docker-compose up -d postgres redis zookeeper kafka

echo ""
echo -e "${YELLOW}Waiting for infrastructure to be ready (30 seconds)...${NC}"
sleep 30

echo ""
echo -e "${BLUE}Initializing Kafka topics...${NC}"
docker-compose up kafka-init

echo ""
echo -e "${BLUE}Starting Kafka UI...${NC}"
docker-compose up -d kafka-ui

echo ""
echo -e "${BLUE}Running database migrations...${NC}"
cd "$BACKEND_DIR"
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}Installing backend dependencies...${NC}"
    npm install
fi

echo -e "${YELLOW}Generating Prisma client...${NC}"
npx prisma generate

echo -e "${YELLOW}Running Prisma migrations...${NC}"
npx prisma migrate deploy || npx prisma migrate dev --name init

cd "$DOCKER_DIR"

echo ""
echo -e "${BLUE}Building and starting application services...${NC}"
docker-compose up -d --build backend frontend audit-agent reminder-agent recurring-task-agent realtime-sync-agent

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo -e "${BLUE}Services:${NC}"
echo -e "  Frontend:    ${GREEN}http://localhost:3000${NC}"
echo -e "  Backend API: ${GREEN}http://localhost:3001${NC}"
echo -e "  Kafka UI:    ${GREEN}http://localhost:8080${NC}"
echo -e "  PostgreSQL:  ${GREEN}localhost:5432${NC}"
echo -e "  Redis:       ${GREEN}localhost:6379${NC}"
echo ""
echo -e "${BLUE}Health Checks:${NC}"
echo -e "  Backend:     ${GREEN}http://localhost:3001/health${NC}"
echo ""
echo -e "${YELLOW}View logs:${NC}"
echo -e "  All services:     ${BLUE}./scripts/logs.sh${NC}"
echo -e "  Specific service: ${BLUE}docker-compose -f infrastructure/docker/docker-compose.yml logs -f <service-name>${NC}"
echo ""
echo -e "${YELLOW}Stop services:${NC}"
echo -e "  ${BLUE}./scripts/stop-local.sh${NC}"
echo ""
