# Phase 5 Quick Start Guide

## Prerequisites

- Node.js 18+
- Docker & Docker Compose
- Git

## Local Development Setup

### 1. Start Infrastructure Services

```bash
cd phase-5/infrastructure/docker
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Kafka + Zookeeper (port 9092)
- Kafka UI (port 8080)

### 2. Set Up Backend

```bash
cd phase-5/backend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Generate Prisma client
npx prisma generate

# Run database migrations
npx prisma migrate dev --name init

# Start development server
npm run dev
```

Backend will run on `http://localhost:3001`

### 3. Set Up Frontend

```bash
cd phase-5/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run on `http://localhost:3000`

### 4. Start Agents (Optional)

```bash
# Terminal 1 - Audit Agent
cd phase-5/agents/audit-agent
npm install
npm run dev

# Terminal 2 - Recurring Task Agent (when implemented)
cd phase-5/agents/recurring-task-agent
npm install
npm run dev

# Terminal 3 - Reminder Agent (when implemented)
cd phase-5/agents/reminder-agent
npm install
npm run dev

# Terminal 4 - RealTime Sync Agent (when implemented)
cd phase-5/agents/realtime-sync-agent
npm install
npm run dev
```

## Verify Installation

### Check Infrastructure

```bash
# Check Docker containers
docker ps

# Check Kafka topics
docker exec -it phase5-kafka kafka-topics --list --bootstrap-server localhost:9092

# Check PostgreSQL
docker exec -it phase5-postgres psql -U phase5_user -d phase5_todo -c "\dt"
```

### Check Backend

```bash
curl http://localhost:3001/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2026-02-10T...",
  "service": "phase5-backend",
  "version": "1.0.0"
}
```

### Check Frontend

Open browser: `http://localhost:3000`

You should see the Phase 5 Todo Application homepage.

## Development Workflow

### Making Changes

1. **Backend changes**: Edit files in `backend/src/`, server auto-reloads
2. **Frontend changes**: Edit files in `frontend/src/`, page auto-reloads
3. **Database changes**: Update `backend/prisma/schema.prisma`, run `npx prisma migrate dev`

### Testing

```bash
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm test
```

### Viewing Logs

```bash
# Backend logs
cd backend
tail -f logs/combined.log

# Docker logs
docker-compose logs -f kafka
docker-compose logs -f postgres
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :3001  # Backend
lsof -i :3000  # Frontend
lsof -i :5432  # PostgreSQL
lsof -i :9092  # Kafka

# Kill process
kill -9 <PID>
```

### Database Connection Issues

```bash
# Reset database
cd backend
npx prisma migrate reset

# Regenerate client
npx prisma generate
```

### Kafka Issues

```bash
# Restart Kafka
cd infrastructure/docker
docker-compose restart kafka

# View Kafka UI
open http://localhost:8080
```

### Clean Start

```bash
# Stop all services
cd infrastructure/docker
docker-compose down -v

# Remove node_modules
rm -rf backend/node_modules frontend/node_modules

# Start fresh
./start-local.sh
```

## Next Steps

1. **Implement User Story 1**: Recurring Tasks (T031-T042)
2. **Implement User Story 2**: Reminders (T043-T052)
3. **Test MVP**: End-to-end testing of core features
4. **Deploy to Minikube**: Local Kubernetes deployment

## Useful Commands

```bash
# Prisma Studio (Database GUI)
cd backend && npx prisma studio

# View Kafka messages
docker exec -it phase5-kafka kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic task-events \
  --from-beginning

# PostgreSQL CLI
docker exec -it phase5-postgres psql -U phase5_user -d phase5_todo

# Redis CLI
docker exec -it phase5-redis redis-cli -a phase5_redis_password
```

## Architecture Overview

```
┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend   │
│  (Next.js)  │     │  (Express)  │
└─────────────┘     └──────┬──────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    Kafka     │
                    │  (4 topics)  │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
┌───────────────┐  ┌───────────────┐  ┌──────────────┐
│  AuditAgent   │  │RecurringAgent │  │ReminderAgent │
└───────┬───────┘  └───────┬───────┘  └──────┬───────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    ┌──────────────┐
                    │  PostgreSQL  │
                    └──────────────┘
```

## Support

For issues or questions:
1. Check `IMPLEMENTATION_STATUS.md` for current progress
2. Review `sp.tasks` for task breakdown
3. Check logs in `backend/logs/` and agent logs
4. Verify Docker containers are running: `docker ps`

---

**Phase 5 Team** | Hackathon II Project
