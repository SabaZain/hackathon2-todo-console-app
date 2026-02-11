# Phase 5 TaskFlow - Deployment Guide

## 📋 Overview

Phase 5 TaskFlow is a full-stack task management application with event-driven architecture. It can run in two modes:

### 🔹 Manual Mode (Without Kafka)
**Best for:** Quick development, testing core features, minimal setup

**What Works:**
- ✅ Task CRUD operations (Create, Read, Update, Delete)
- ✅ Recurring tasks (manual generation on completion)
- ✅ Reminders (stored in database)
- ✅ User authentication & authorization
- ✅ Task filtering, search, and sorting
- ✅ Priority and status management
- ✅ Tags and due dates

**What Doesn't Work:**
- ❌ Real-time sync across multiple clients
- ❌ Automatic audit logging
- ❌ Event-driven recurring task generation
- ❌ Background reminder processing
- ❌ WebSocket live updates

### 🔹 Full Mode (With Kafka)
**Best for:** Production deployment, full feature testing, event-driven workflows

**Everything Works:**
- ✅ All Manual Mode features
- ✅ Real-time task synchronization across devices
- ✅ Complete audit trail of all operations
- ✅ Event-driven recurring task generation
- ✅ Background reminder notifications
- ✅ WebSocket live updates
- ✅ Kafka event streaming
- ✅ 4 specialized agents running in background

---

## 🚀 Option 1: Manual Start (No Kafka Required)

### Prerequisites
```bash
# Required
- Node.js 18+
- npm or yarn
- PostgreSQL database (using Neon cloud)

# Check versions
node --version  # Should be 18+
npm --version
```

### Step 1: Backend Setup

```bash
# Navigate to backend
cd phase-5/backend

# Install dependencies (first time only)
npm install

# Setup environment variables
# Edit .env file with your database URL
# DATABASE_URL is already configured for Neon

# Run database migrations (first time only)
npx prisma migrate dev

# Generate Prisma client (first time only)
npx prisma generate

# Start backend server
npm run dev
```

**Expected Output:**
```
✅ Database connected successfully
⚠️  Kafka connection failed - running without event streaming
⚠️  WebSocket service failed to start - running without real-time sync
✅ Server running on port 3001 in development mode
```

Backend is now running at: **http://localhost:3001**

### Step 2: Frontend Setup

Open a **new terminal** and run:

```bash
# Navigate to frontend
cd phase-5/frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Expected Output:**
```
✓ Ready in 2.5s
○ Local: http://localhost:3000
```

Frontend is now running at: **http://localhost:3000**

### Step 3: Access Application

1. Open browser: **http://localhost:3000**
2. Click "Create a new account"
3. Register with your details
4. Login and start creating tasks!

### Stopping Manual Mode

Press `Ctrl+C` in each terminal (backend and frontend)

---

## 🔥 Option 2: Full Start (With Kafka & All Features)

### Prerequisites
```bash
# Required
- Docker Desktop installed and running
- Docker Compose v2+
- 8GB+ RAM available
- Ports available: 3000, 3001, 5432, 6379, 9092, 2181, 8080

# Check Docker
docker --version
docker-compose --version
```

### Step 1: Start Full Stack with Docker

```bash
# Navigate to infrastructure directory
cd phase-5/infrastructure/docker

# Start all services (first time will take 5-10 minutes)
docker-compose up -d

# View logs (optional)
docker-compose logs -f

# Check service health
docker-compose ps
```

### Step 2: Verify Services

All services should show as "healthy" or "running":

```bash
docker-compose ps
```

**Expected Services:**
- ✅ phase5-postgres (healthy)
- ✅ phase5-redis (healthy)
- ✅ phase5-zookeeper (running)
- ✅ phase5-kafka (healthy)
- ✅ phase5-kafka-ui (running)
- ✅ phase5-backend (healthy)
- ✅ phase5-frontend (running)
- ✅ phase5-audit-agent (running)
- ✅ phase5-reminder-agent (running)
- ✅ phase5-recurring-task-agent (running)
- ✅ phase5-realtime-sync-agent (running)

### Step 3: Access Application & Tools

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3000 | Main application UI |
| **Backend API** | http://localhost:3001 | REST API |
| **API Docs** | http://localhost:3001/docs | Swagger documentation |
| **Kafka UI** | http://localhost:8080 | Monitor Kafka topics & messages |
| **Health Check** | http://localhost:3001/health | Backend health status |

### Step 4: Verify Kafka Integration

1. **Check Backend Logs:**
```bash
docker-compose logs backend | grep -i kafka
```

Should see:
```
✅ Kafka producer connected successfully
✅ WebSocket service started successfully
```

2. **Check Kafka Topics:**
```bash
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

Should see:
```
task-events
task-updates
reminders
audit-logs
```

3. **Monitor Events in Kafka UI:**
   - Open http://localhost:8080
   - Click on "phase5-cluster"
   - View topics and messages in real-time

### Step 5: Test Event-Driven Features

**Test Real-time Sync:**
1. Open http://localhost:3000 in two browser windows
2. Create a task in one window
3. See it appear instantly in the other window ✨

**Test Audit Logging:**
1. Create/update/delete tasks
2. Check Kafka UI → `audit-logs` topic
3. See all operations logged with timestamps

**Test Recurring Tasks:**
1. Create a recurring task (e.g., daily)
2. Mark it as complete
3. New occurrence is automatically generated via Kafka event

### Stopping Full Mode

```bash
cd phase-5/infrastructure/docker

# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

---

## 🔍 Verification Checklist

### Manual Mode Verification

- [ ] Backend starts without errors (Kafka warnings are OK)
- [ ] Frontend loads at http://localhost:3000
- [ ] Can register a new account
- [ ] Can login successfully
- [ ] Can create a task
- [ ] Can update a task
- [ ] Can complete a task
- [ ] Can delete a task
- [ ] Can create recurring task
- [ ] Can add reminder to task
- [ ] Task filters work (status, priority)
- [ ] Search functionality works

### Full Mode Verification

All Manual Mode checks PLUS:

- [ ] All Docker containers are healthy
- [ ] Kafka UI accessible at http://localhost:8080
- [ ] Backend logs show Kafka connected
- [ ] 4 Kafka topics exist
- [ ] Real-time sync works across browser tabs
- [ ] Audit logs appear in Kafka UI
- [ ] Recurring task generates next occurrence automatically
- [ ] All 4 agents are running without errors

---

## 🛠️ Troubleshooting

### Manual Mode Issues

**Problem: Backend won't start**
```bash
# Check if port 3001 is in use
netstat -ano | findstr :3001  # Windows
lsof -i :3001                  # Mac/Linux

# Kill process if needed
taskkill //F //PID <PID>       # Windows
kill -9 <PID>                  # Mac/Linux
```

**Problem: Database connection failed**
```bash
# Verify DATABASE_URL in backend/.env
# Ensure Neon database is accessible
# Check internet connection

# Test connection
cd phase-5/backend
npx prisma db push
```

**Problem: Frontend can't connect to backend**
```bash
# Check backend is running on port 3001
curl http://localhost:3001/health

# Verify NEXT_PUBLIC_API_URL in frontend/.env
# Should be: http://localhost:3001/api
```

### Full Mode Issues

**Problem: Docker containers won't start**
```bash
# Check Docker Desktop is running
docker ps

# Check available disk space (need 5GB+)
docker system df

# Clean up old containers/images
docker system prune -a
```

**Problem: Kafka not connecting**
```bash
# Check Kafka health
docker-compose ps kafka

# View Kafka logs
docker-compose logs kafka

# Restart Kafka
docker-compose restart kafka
```

**Problem: Agents not working**
```bash
# Check agent logs
docker-compose logs audit-agent
docker-compose logs reminder-agent
docker-compose logs recurring-task-agent
docker-compose logs realtime-sync-agent

# Restart specific agent
docker-compose restart audit-agent
```

**Problem: Port conflicts**
```bash
# Change ports in docker-compose.yml
# Example: Change 3000:3000 to 3002:3000

# Or stop conflicting services
docker ps  # Find conflicting containers
docker stop <container-id>
```

**Problem: Database migration issues**
```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
docker-compose exec backend npx prisma migrate deploy
docker-compose up -d
```

---

## 📊 Feature Comparison Matrix

| Feature | Manual Mode | Full Mode (Kafka) |
|---------|-------------|-------------------|
| **Core Features** |
| Task CRUD | ✅ | ✅ |
| User Authentication | ✅ | ✅ |
| Recurring Tasks | ✅ Manual | ✅ Event-driven |
| Reminders | ✅ Database only | ✅ + Background processing |
| Task Filters/Search | ✅ | ✅ |
| Priority & Status | ✅ | ✅ |
| Tags & Due Dates | ✅ | ✅ |
| **Advanced Features** |
| Real-time Sync | ❌ | ✅ |
| Audit Logging | ❌ | ✅ |
| Event Streaming | ❌ | ✅ |
| WebSocket Updates | ❌ | ✅ |
| Background Agents | ❌ | ✅ |
| Kafka Integration | ❌ | ✅ |
| **Monitoring** |
| API Documentation | ✅ | ✅ |
| Health Checks | ✅ | ✅ |
| Kafka UI | ❌ | ✅ |
| Event Monitoring | ❌ | ✅ |

---

## 🎯 Quick Command Reference

### Manual Mode
```bash
# Start backend
cd phase-5/backend && npm run dev

# Start frontend (new terminal)
cd phase-5/frontend && npm run dev

# Database migrations
cd phase-5/backend && npx prisma migrate dev

# Generate Prisma client
cd phase-5/backend && npx prisma generate
```

### Full Mode (Docker)
```bash
# Start everything
cd phase-5/infrastructure/docker && docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f kafka

# Check status
docker-compose ps

# Stop everything
docker-compose down

# Stop and remove data
docker-compose down -v

# Rebuild after code changes
docker-compose up -d --build

# Restart specific service
docker-compose restart backend
```

### Useful Commands
```bash
# Check Kafka topics
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092

# View Kafka messages
docker-compose exec kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic task-events --from-beginning

# Database shell
docker-compose exec postgres psql -U phase5_user -d phase5_todo

# Backend shell
docker-compose exec backend sh

# View all containers
docker ps -a
```

---

## 🌐 Environment Variables

### Backend (.env)
```env
# Database
DATABASE_URL="postgresql://user:pass@host:5432/dbname"

# Authentication
JWT_SECRET="your-secret-key-change-in-production"
JWT_EXPIRES_IN="7d"

# Server
NODE_ENV="development"
PORT=3001

# Kafka (optional - app works without it)
KAFKA_BROKERS="localhost:9092"

# Redis (optional)
REDIS_HOST="localhost"
REDIS_PORT=6379

# CORS
CORS_ORIGIN="http://localhost:3000"
```

### Frontend (.env)
```env
NEXT_PUBLIC_API_URL="http://localhost:3001/api"
NEXT_PUBLIC_WS_URL="ws://localhost:3001"
```

---

## 📝 Important Notes

### Graceful Degradation
The application is designed to work gracefully with or without Kafka:
- **With Kafka:** Full event-driven architecture with all features
- **Without Kafka:** Core task management works perfectly, advanced features disabled

### Kafka Warnings Are Normal
When running in Manual Mode, you'll see:
```
⚠️  Kafka connection failed - running without event streaming
⚠️  WebSocket service failed to start - running without real-time sync
```
**This is expected and normal!** The application continues to work with core features.

### Database
- Manual Mode uses Neon PostgreSQL (cloud)
- Full Mode uses local PostgreSQL in Docker
- Both use the same Prisma schema

### Agents
The 4 background agents only run in Full Mode:
1. **Audit Agent** - Logs all operations to database
2. **Reminder Agent** - Processes scheduled reminders
3. **Recurring Task Agent** - Generates next task occurrences
4. **Real-time Sync Agent** - Broadcasts updates via WebSocket

---

## 🆘 Getting Help

### Check Logs
```bash
# Manual Mode
# Backend logs are in the terminal
# Frontend logs are in the terminal

# Full Mode
docker-compose logs backend
docker-compose logs frontend
docker-compose logs kafka
docker-compose logs <agent-name>
```

### Health Checks
```bash
# Backend health
curl http://localhost:3001/health

# Check if backend is responding
curl http://localhost:3001/api/tasks
```

### Common Issues
1. **Port conflicts** - Change ports or stop conflicting services
2. **Database connection** - Verify DATABASE_URL is correct
3. **Kafka warnings** - Normal in Manual Mode, ignore them
4. **Docker issues** - Restart Docker Desktop, clean up old containers

---

## ✅ Success Indicators

### Manual Mode Success
```
✅ Database connected successfully
⚠️  Kafka connection failed - running without event streaming (EXPECTED)
⚠️  WebSocket service failed to start - running without real-time sync (EXPECTED)
✅ Server running on port 3001 in development mode
✅ Frontend ready at http://localhost:3000
```

### Full Mode Success
```
✅ All 11 containers running
✅ Backend: Kafka producer connected successfully
✅ Backend: WebSocket service started successfully
✅ All 4 agents connected to Kafka
✅ 4 Kafka topics created
✅ Frontend accessible at http://localhost:3000
✅ Kafka UI accessible at http://localhost:8080
```

---

## 🎉 You're Ready!

Choose your deployment mode:
- **Quick testing?** → Use Manual Mode
- **Full features?** → Use Full Mode with Docker

Both modes provide a fully functional task management application!
