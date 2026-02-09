# Phase 5 Architecture

## Overview

Phase 5 implements an event-driven, microservices architecture using Kafka for event streaming, Dapr for distributed application runtime, and Kubernetes for orchestration.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Next.js 14 + React 18 + TailwindCSS                     │  │
│  │  - Task Management UI                                     │  │
│  │  - Real-time Updates (WebSocket)                         │  │
│  │  - Authentication & Authorization                         │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ HTTP/WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Backend Layer                           │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Express.js + TypeScript + Prisma ORM                    │  │
│  │  - REST API Endpoints                                     │  │
│  │  - Business Logic                                         │  │
│  │  - Event Publishing (Kafka Producer)                     │  │
│  │  - WebSocket Server (Socket.io)                          │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ Kafka Events
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Event Streaming Layer                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Apache Kafka                                             │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐         │  │
│  │  │task-events │  │task-updates│  │ reminders  │         │  │
│  │  └────────────┘  └────────────┘  └────────────┘         │  │
│  │  ┌────────────┐                                          │  │
│  │  │audit-logs  │                                          │  │
│  │  └────────────┘                                          │  │
│  └────────────────────┬─────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────────┘
                         │ Event Consumption
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Agent Layer                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ AuditAgent   │  │RecurringTask │  │ReminderAgent │         │
│  │              │  │    Agent     │  │              │         │
│  │ - Consumes   │  │ - Consumes   │  │ - Consumes   │         │
│  │   task-events│  │   task-events│  │   reminders  │         │
│  │ - Stores     │  │ - Generates  │  │ - Sends      │         │
│  │   audit logs │  │   next tasks │  │   notifications       │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│  ┌──────────────┐                                              │
│  │RealTimeSync  │                                              │
│  │    Agent     │                                              │
│  │ - Consumes   │                                              │
│  │   task-updates                                             │
│  │ - Broadcasts │                                              │
│  │   via WebSocket                                            │
│  └──────────────┘                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │ Database Operations
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Persistence Layer                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL / Neon DB                                     │  │
│  │  - Users, Tasks, Reminders                                │  │
│  │  - Recurrence Patterns                                    │  │
│  │  - Audit Logs (Immutable)                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Redis (Dapr State Store)                                 │  │
│  │  - Distributed Cache                                      │  │
│  │  - Session Storage                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Next.js)

**Technology**: Next.js 14, React 18, TypeScript, TailwindCSS

**Responsibilities**:
- User interface for task management
- Real-time updates via WebSocket
- Client-side state management
- Authentication and authorization

**Key Features**:
- Server-side rendering (SSR)
- Static site generation (SSG)
- API routes for backend communication
- Responsive design with TailwindCSS

### Backend (Express.js)

**Technology**: Express.js, TypeScript, Prisma ORM

**Responsibilities**:
- REST API endpoints
- Business logic execution
- Event publishing to Kafka
- WebSocket server for real-time updates
- Authentication and authorization

**Key Components**:
- **Models**: Prisma models for database entities
- **Services**: Business logic layer
- **Routes**: API endpoint definitions
- **Middleware**: Auth, validation, error handling
- **Events**: Kafka producer for event publishing

### Event Streaming (Kafka)

**Technology**: Apache Kafka 7.5.0

**Topics**:
1. **task-events**: All task lifecycle events (create, update, delete, complete)
   - Partitions: 3
   - Retention: 7 days
   - Consumers: AuditAgent, RecurringTaskAgent

2. **task-updates**: Real-time task state changes
   - Partitions: 3
   - Retention: 1 day
   - Consumers: RealTimeSyncAgent

3. **reminders**: Scheduled reminder events
   - Partitions: 3
   - Retention: 1 day
   - Consumers: ReminderAgent

4. **audit-logs**: Immutable audit trail
   - Partitions: 3
   - Retention: 90 days
   - Consumers: Analytics services

### Agents

#### AuditAgent

**Responsibility**: Capture and store all task operations

**Implementation**:
- Consumes events from `task-events` topic
- Stores immutable audit logs in PostgreSQL
- Supports querying by user, task, timestamp
- Ensures 100% capture (NON-NEGOTIABLE)

**Event Flow**:
```
task-events → AuditAgent → audit_logs table
```

#### RecurringTaskAgent

**Responsibility**: Generate next occurrences for recurring tasks

**Implementation**:
- Consumes `task.completed` events from `task-events` topic
- Calculates next occurrence based on recurrence pattern
- Creates new task via backend API
- Handles edge cases (month-end, leap years, DST)

**Event Flow**:
```
task-events (task.completed) → RecurringTaskAgent → Backend API (create task)
```

#### ReminderAgent

**Responsibility**: Send multi-channel notifications

**Implementation**:
- Consumes events from `reminders` topic
- Sends notifications via push, email, in-app
- Handles retry logic for failed deliveries
- Integrates with Dapr bindings for scheduled reminders

**Event Flow**:
```
reminders → ReminderAgent → Notification Services (push/email/in-app)
```

#### RealTimeSyncAgent

**Responsibility**: Broadcast task updates to all connected clients

**Implementation**:
- Consumes events from `task-updates` topic
- Broadcasts updates via WebSocket (Socket.io)
- Manages WebSocket connections
- Handles conflict resolution

**Event Flow**:
```
task-updates → RealTimeSyncAgent → WebSocket → Frontend Clients
```

### Dapr Integration

**Technology**: Dapr 1.12+

**Components**:

1. **Pub/Sub (Kafka)**
   - Type: `pubsub.kafka`
   - Broker: `localhost:9092`
   - Consumer Group: `phase5-group`

2. **State Store (Redis)**
   - Type: `state.redis`
   - Host: `localhost:6379`
   - Use: Distributed cache, session storage

3. **Bindings (Cron)**
   - Type: `bindings.cron`
   - Schedule: Every minute (reminders), Every 5 minutes (recurring tasks)

4. **Secrets (Kubernetes)**
   - Type: `secretstores.kubernetes`
   - Use: Database credentials, API keys

### Database (PostgreSQL)

**Technology**: PostgreSQL 16

**Schema**:
- **users**: User accounts and preferences
- **tasks**: Task entities with recurring support
- **recurrence_patterns**: Recurrence rules
- **reminders**: Scheduled reminders
- **audit_logs**: Immutable audit trail

**Indexes**:
- user_id, task_id, timestamp (for efficient querying)
- tags (GIN index for array search)
- Full-text search on title and description

## Event Flow Examples

### Creating a Task

```
1. Frontend → POST /api/tasks → Backend
2. Backend → Save to PostgreSQL
3. Backend → Publish task.created event → Kafka (task-events)
4. Backend → Publish task update → Kafka (task-updates)
5. AuditAgent → Consume task.created → Store audit log
6. RealTimeSyncAgent → Consume task update → Broadcast via WebSocket
7. Frontend → Receive WebSocket update → Update UI
```

### Completing a Recurring Task

```
1. Frontend → PUT /api/tasks/:id (status=completed) → Backend
2. Backend → Update task in PostgreSQL
3. Backend → Publish task.completed event → Kafka (task-events)
4. RecurringTaskAgent → Consume task.completed
5. RecurringTaskAgent → Calculate next occurrence
6. RecurringTaskAgent → POST /api/tasks (create next occurrence) → Backend
7. Backend → Publish task.created event → Kafka
8. AuditAgent → Store audit logs for both operations
9. RealTimeSyncAgent → Broadcast updates → Frontend
```

### Sending a Reminder

```
1. Backend → Publish reminder.scheduled event → Kafka (reminders)
2. ReminderAgent → Consume reminder.scheduled
3. ReminderAgent → Wait until reminder time
4. ReminderAgent → Send notification (push/email/in-app)
5. ReminderAgent → Publish reminder.sent event → Kafka
6. Backend → Update reminder status in PostgreSQL
```

## Scalability

### Horizontal Scaling

- **Backend**: Multiple instances behind load balancer
- **Agents**: Multiple instances per agent type (Kafka consumer groups)
- **Kafka**: Multiple brokers with replication
- **PostgreSQL**: Read replicas for queries

### Performance Targets

- API latency: p95 < 500ms, p99 < 1s
- Event processing: 1,000 events/second
- Real-time sync: < 1 second propagation
- Concurrent users: 10,000 without degradation

## Security

- **Authentication**: JWT tokens
- **Authorization**: Role-based access control (RBAC)
- **Encryption**: TLS for all external communication
- **Secrets**: Managed via Dapr secrets component
- **Input Validation**: Joi schemas for all API requests
- **Rate Limiting**: Express rate limiter middleware

## Monitoring

- **Metrics**: Prometheus (request rate, latency, error rate)
- **Dashboards**: Grafana (system health, performance)
- **Tracing**: Jaeger (distributed tracing with correlation IDs)
- **Logging**: Winston (structured logging to files and console)
- **Alerting**: Prometheus Alertmanager (critical metrics)

## Deployment

### Local (Minikube)

- Docker Compose for infrastructure
- Dapr CLI for local development
- kubectl for Kubernetes management

### Cloud (DOKS/GKE/AKS)

- Terraform for infrastructure provisioning
- Helm charts for application deployment
- Kubernetes manifests for services
- CI/CD via GitHub Actions

---

**Last Updated**: 2026-02-10
**Version**: 1.0.0
**Status**: Foundation Complete
