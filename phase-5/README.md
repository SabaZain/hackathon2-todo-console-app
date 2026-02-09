# Phase 5: Advanced Cloud Deployment & Event-Driven Architecture

**Status**: 🚧 In Development
**Phase**: Phase 5
**Architecture**: Event-Driven Microservices with Kafka, Dapr, and Kubernetes

## Overview

Phase 5 transforms the Todo application into a production-ready, cloud-native, event-driven system with advanced features including recurring tasks, reminders, real-time synchronization, and complete audit trails.

## Architecture

### Microservices
- **Backend API**: Express.js + TypeScript + Prisma ORM
- **Frontend**: Next.js 14 + React 18 + TailwindCSS
- **AuditAgent**: Consumes task events and maintains immutable audit logs
- **RecurringTaskAgent**: Automatically generates next occurrences for recurring tasks
- **ReminderAgent**: Sends multi-channel notifications (push/email/in-app)
- **RealTimeSyncAgent**: Broadcasts task updates via WebSocket

### Infrastructure
- **Message Broker**: Apache Kafka (4 topics: task-events, task-updates, reminders, audit-logs)
- **Database**: PostgreSQL/Neon DB with Prisma ORM
- **Runtime**: Dapr (Pub/Sub, State Management, Bindings, Secrets)
- **Orchestration**: Kubernetes (Minikube local, DOKS/GKE/AKS cloud)
- **Monitoring**: Prometheus, Grafana, Jaeger, ELK/Loki

## Features

### Advanced Task Management
- ✅ Recurring tasks (daily, weekly, monthly, custom intervals)
- ✅ Due dates with multi-channel reminders
- ✅ Priority levels (High, Medium, Low)
- ✅ Custom tags for organization
- ✅ Full-text search, filtering, and sorting

### Event-Driven Architecture
- ✅ All task operations publish events to Kafka
- ✅ Asynchronous event processing with retry logic
- ✅ Dead letter queues for failed events
- ✅ Event correlation for distributed tracing

### Audit & Compliance
- ✅ 100% capture of all task operations (NON-NEGOTIABLE)
- ✅ Immutable audit logs (append-only)
- ✅ Queryable history by user, task, timestamp
- ✅ 90-day retention policy (configurable)

### Real-Time Synchronization
- ✅ WebSocket-based updates across all connected clients
- ✅ < 1 second propagation time
- ✅ Conflict resolution for simultaneous updates
- ✅ Offline support with sync on reconnect

## Project Structure

```
phase-5/
├── backend/                 # Express.js API server
│   ├── src/
│   │   ├── models/         # Prisma models
│   │   ├── services/       # Business logic
│   │   ├── api/            # Routes and middleware
│   │   ├── events/         # Kafka producer
│   │   ├── websocket/      # Socket.io server
│   │   └── config/         # Configuration
│   ├── prisma/             # Database schema
│   └── tests/              # Unit, integration, E2E tests
│
├── frontend/               # Next.js application
│   ├── src/
│   │   ├── app/           # Next.js 14 app router
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom hooks
│   │   ├── services/      # API and WebSocket clients
│   │   └── contexts/      # React contexts
│   └── tests/             # Component and E2E tests
│
├── agents/                # Event-driven agents
│   ├── audit-agent/       # Audit trail tracking
│   ├── recurring-task-agent/  # Recurring task generation
│   ├── reminder-agent/    # Notification delivery
│   └── realtime-sync-agent/   # WebSocket broadcasting
│
├── infrastructure/        # Deployment and infrastructure
│   ├── docker/           # Docker Compose files
│   ├── dapr/             # Dapr components
│   ├── kubernetes/       # K8s manifests
│   └── monitoring/       # Observability stack
│
├── .github/workflows/    # CI/CD pipelines
└── docs/                 # Documentation
```

## Getting Started

### Prerequisites

- Node.js 18+
- Docker & Docker Compose
- Minikube (for local Kubernetes)
- Dapr CLI
- kubectl

### Local Development

1. **Start Infrastructure**
   ```bash
   cd infrastructure/docker
   docker-compose up -d
   ```

2. **Initialize Dapr**
   ```bash
   dapr init -k
   ```

3. **Backend Setup**
   ```bash
   cd backend
   npm install
   npm run prisma:migrate
   npm run dev
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Start Agents**
   ```bash
   # Terminal 1
   cd agents/audit-agent && npm run dev

   # Terminal 2
   cd agents/recurring-task-agent && npm run dev

   # Terminal 3
   cd agents/reminder-agent && npm run dev

   # Terminal 4
   cd agents/realtime-sync-agent && npm run dev
   ```

### Deployment

#### Minikube (Local)
```bash
cd infrastructure/kubernetes/minikube
./deploy.sh
```

#### Cloud (DOKS/GKE/AKS)
```bash
cd infrastructure/kubernetes/cloud
terraform init
terraform apply
kubectl apply -f manifests/
```

## Testing

```bash
# Backend tests
cd backend
npm test                    # Unit tests
npm run test:integration    # Integration tests
npm run test:coverage       # Coverage report

# Frontend tests
cd frontend
npm test                    # Component tests
npm run test:e2e           # E2E tests with Playwright

# Load testing
cd infrastructure
k6 run load-tests/scenario.js
```

## Monitoring

- **Grafana**: http://localhost:3000 (admin/admin)
- **Prometheus**: http://localhost:9090
- **Jaeger**: http://localhost:16686
- **Kibana**: http://localhost:5601

## Documentation

- [Architecture](docs/architecture.md)
- [Deployment Guide](docs/deployment.md)
- [Monitoring & Observability](docs/monitoring.md)
- [Runbooks](docs/runbooks/)

## Phase Isolation

⚠️ **CRITICAL**: All Phase 5 work is strictly isolated in the `phase-5/` folder. Phases 1-4 remain completely untouched.

## Contributing

This is Phase 5 of the Hackathon II project. All contributions must:
- Follow the established architecture
- Include tests
- Update documentation
- Maintain phase isolation

## License

MIT

---

**Phase 5 Team** | Hackathon II Project | 2026
