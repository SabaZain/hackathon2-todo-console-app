#!/bin/bash

# Phase 5 Local Development Startup Script
# This script starts all Phase 5 services for local development

set -e

echo "🚀 Starting Phase 5 Local Development Environment"
echo "=================================================="

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Start infrastructure
echo ""
echo "🐳 Starting infrastructure services (Kafka, PostgreSQL, Redis)..."
cd infrastructure/docker
docker-compose up -d

echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo "🏥 Checking service health..."
docker-compose ps

cd ../..

# Install dependencies
echo ""
echo "📦 Installing dependencies..."

if [ ! -d "backend/node_modules" ]; then
    echo "Installing backend dependencies..."
    cd backend && npm install && cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Run database migrations
echo ""
echo "🗄️  Running database migrations..."
cd backend
npx prisma generate
npx prisma migrate dev --name init
cd ..

echo ""
echo "✅ Phase 5 Local Development Environment is ready!"
echo ""
echo "📝 Next steps:"
echo "   1. Start backend:  cd backend && npm run dev"
echo "   2. Start frontend: cd frontend && npm run dev"
echo "   3. Start agents:   cd agents/audit-agent && npm run dev"
echo ""
echo "🌐 Services:"
echo "   - Frontend:    http://localhost:3000"
echo "   - Backend API: http://localhost:3001"
echo "   - Kafka UI:    http://localhost:8080"
echo "   - PostgreSQL:  localhost:5432"
echo "   - Redis:       localhost:6379"
echo ""
echo "🛑 To stop all services: cd infrastructure/docker && docker-compose down"
