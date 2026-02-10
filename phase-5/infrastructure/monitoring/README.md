# Phase 5 Monitoring Infrastructure

Complete observability stack for Phase 5 event-driven task management system.

## Overview

The monitoring infrastructure provides comprehensive observability across all Phase 5 components:

- **Metrics**: Prometheus for time-series metrics collection
- **Visualization**: Grafana dashboards for metrics and logs
- **Tracing**: Jaeger for distributed tracing
- **Logging**: Loki for centralized log aggregation
- **Alerting**: Alertmanager for alert routing and notifications

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Phase 5 Application                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │ Backend  │  │ Frontend │  │  Agents  │  │ Database │       │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘       │
│       │             │              │             │              │
└───────┼─────────────┼──────────────┼─────────────┼──────────────┘
        │             │              │             │
        │ metrics     │ metrics      │ metrics     │ metrics
        │ traces      │ traces       │ traces      │
        │ logs        │ logs         │ logs        │
        ▼             ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Monitoring Infrastructure                     │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Prometheus  │  │    Jaeger    │  │     Loki     │         │
│  │  (Metrics)   │  │   (Traces)   │  │    (Logs)    │         │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘         │
│         │                  │                  │                  │
│         │                  └──────┬───────────┘                  │
│         │                         │                              │
│         ▼                         ▼                              │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │ Alertmanager │         │   Grafana    │                     │
│  │  (Alerts)    │────────▶│     (UI)     │                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Deploy Complete Monitoring Stack

```bash
cd phase-5/infrastructure/scripts
./deploy-monitoring.sh
```

This script deploys:
- Prometheus with recording rules and alerts
- Grafana with pre-configured dashboards
- Jaeger for distributed tracing
- Loki with Promtail for log aggregation
- Alertmanager for alert routing

### Access Services

After deployment, access services via port forwarding:

```bash
# Grafana (main UI)
kubectl port-forward -n monitoring svc/grafana 3000:3000
# http://localhost:3000 (admin/admin123)

# Prometheus
kubectl port-forward -n monitoring svc/prometheus 9090:9090
# http://localhost:9090

# Jaeger
kubectl port-forward -n tracing svc/jaeger-query 16686:16686
# http://localhost:16686

# Alertmanager
kubectl port-forward -n monitoring svc/alertmanager 9093:9093
# http://localhost:9093
```

## Components

### 1. Prometheus

**Purpose**: Metrics collection and alerting

**Features**:
- Scrapes metrics from all Phase 5 services
- 12 recording rules for metric aggregations
- 13 alert rules for critical conditions
- 15-second scrape interval
- Kubernetes service discovery

**Configuration**: `prometheus/prometheus.yaml`

**Metrics Collected**:
- HTTP request rates and latencies
- Error rates by service
- CPU and memory usage
- Database connection pool metrics
- Kafka consumer lag
- WebSocket connections
- Task operation rates
- Reminder delivery rates

### 2. Grafana

**Purpose**: Visualization and dashboards

**Features**:
- 3 pre-configured dashboards
- Prometheus, Loki, and Jaeger datasources
- 30-second auto-refresh
- Alert visualization

**Dashboards**:
1. **System Overview**: Request rates, errors, response times, resource usage
2. **Database & Infrastructure**: DB connections, query performance, Redis, Kafka
3. **Agents Monitoring**: Task operations, reminders, audit logs, WebSocket activity

**Configuration**: `grafana/grafana.yaml`

### 3. Jaeger

**Purpose**: Distributed tracing

**Features**:
- All-in-one deployment (collector, query, UI)
- In-memory storage (Badger DB)
- OTLP support (gRPC and HTTP)
- Prometheus metrics integration
- 10,000 trace retention

**Configuration**: `jaeger/jaeger.yaml`

**Trace Operations**:
- HTTP API requests
- Kafka event processing
- Database queries
- WebSocket messages
- Inter-service calls

### 4. Loki

**Purpose**: Log aggregation

**Features**:
- Centralized log storage
- Promtail DaemonSet for log collection
- 31-day log retention
- LogQL query language
- Automatic label extraction

**Configuration**: `loki/loki.yaml`

**Log Sources**:
- All Phase 5 pods (backend, frontend, agents)
- Container stdout/stderr
- System logs

### 5. Alertmanager

**Purpose**: Alert routing and notifications

**Features**:
- Slack integration
- Email notifications
- Alert grouping and inhibition
- Customizable routing rules
- Silence management

**Configuration**: `alertmanager/alertmanager.yaml`

**Alert Channels**:
- Critical: Slack + Email (immediate)
- Warning: Slack (30s delay)
- Component-specific: Dedicated channels

## Metrics Reference

### Backend Metrics

```
# Request rate
phase5:http_requests:rate5m

# Error rate
phase5:http_errors:rate5m

# Response time percentiles
phase5:http_request_duration:p50
phase5:http_request_duration:p95
phase5:http_request_duration:p99
```

### Resource Metrics

```
# CPU usage ratio
phase5:cpu_usage:ratio

# Memory usage ratio
phase5:memory_usage:ratio

# Database connection pool
phase5:database_connections:ratio
```

### Agent Metrics

```
# Task operations
phase5:task_operations:rate5m

# Reminder delivery
phase5:reminder_delivery:rate5m

# Audit log writes
phase5:audit_log_writes:rate5m

# WebSocket connections
phase5:websocket_connections:current
```

### Kafka Metrics

```
# Consumer lag
phase5:kafka_consumer_lag:sum
```

## Alert Rules

### Critical Alerts

1. **HighErrorRate**: Error rate > 5% for 5 minutes
2. **PodDown**: Pod unavailable for 2 minutes
3. **DatabaseConnectionPoolExhausted**: Pool usage > 90%
4. **AuditLogFailures**: Audit logging failing

### Warning Alerts

1. **HighResponseTime**: p95 latency > 1s
2. **HighCPUUsage**: CPU > 80% for 10 minutes
3. **HighMemoryUsage**: Memory > 80% for 10 minutes
4. **KafkaConsumerLag**: Lag > 1000 messages
5. **DiskSpaceLow**: < 10% disk space remaining
6. **PodRestartingTooOften**: > 0.1 restarts/15min
7. **DeploymentReplicaMismatch**: Replicas don't match spec
8. **HPAMaxedOut**: HPA at max replicas for 15 minutes
9. **ReminderDeliveryFailures**: > 10% failure rate

## Configuration

### Update Alertmanager Secrets

```bash
# Slack webhook
kubectl create secret generic alertmanager-secrets \
  --from-literal=slack-webhook-url='https://hooks.slack.com/services/YOUR/WEBHOOK' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -

# Email (Gmail)
kubectl create secret generic alertmanager-secrets \
  --from-literal=smtp-host='smtp.gmail.com' \
  --from-literal=smtp-port='587' \
  --from-literal=smtp-from='alerts@phase5.example.com' \
  --from-literal=smtp-username='your-email@gmail.com' \
  --from-literal=smtp-password='your-app-password' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

### Update Grafana Password

```bash
kubectl create secret generic grafana-secrets \
  --from-literal=admin-password='your-secure-password' \
  --from-literal=secret-key='your-secret-key' \
  -n monitoring --dry-run=client -o yaml | kubectl apply -f -
```

## Instrumentation

### Backend Service

Add Prometheus metrics:

```typescript
// backend/src/metrics.ts
import promClient from 'prom-client';

const register = new promClient.Registry();

export const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5],
  registers: [register],
});

export const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register],
});

// Expose metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

### Add Jaeger Tracing

```typescript
// backend/src/tracing.ts
import { initTracer } from 'jaeger-client';

const config = {
  serviceName: 'phase5-backend',
  sampler: { type: 'const', param: 1 },
  reporter: {
    collectorEndpoint: 'http://jaeger-collector.tracing:14268/api/traces',
  },
};

export const tracer = initTracer(config);
```

### Structured Logging

```typescript
// backend/src/logger.ts
import winston from 'winston';

export const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [new winston.transports.Console()],
});

// Usage
logger.info('Task created', {
  taskId: task.id,
  userId: user.id,
  operation: 'create',
});
```

## Querying

### Prometheus Queries

```promql
# Request rate by service
sum(rate(http_requests_total[5m])) by (service)

# Error rate percentage
(sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m]))) * 100

# p95 latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service))
```

### Loki Queries

```logql
# All backend logs
{app="phase5-backend"}

# Error logs only
{app="phase5-backend"} |= "error"

# Logs for specific task
{app="phase5-backend"} | json | taskId="abc-123"

# Error rate
sum(rate({app="phase5-backend"} |= "error" [5m]))
```

## Troubleshooting

### No Metrics Appearing

1. Check pod annotations:
   ```bash
   kubectl get pods -n phase5-production -o yaml | grep prometheus.io
   ```

2. Verify Prometheus targets:
   ```bash
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   # Open http://localhost:9090/targets
   ```

3. Check application metrics endpoint:
   ```bash
   kubectl port-forward -n phase5-production pod/backend-xxx 3001:3001
   curl http://localhost:3001/metrics
   ```

### No Logs in Loki

1. Check Promtail is running:
   ```bash
   kubectl get pods -n monitoring -l app=promtail
   ```

2. Check Promtail logs:
   ```bash
   kubectl logs -n monitoring -l app=promtail
   ```

3. Verify namespace labels:
   ```bash
   kubectl get pods -n phase5-production --show-labels
   ```

### Alerts Not Firing

1. Check alert rules in Prometheus:
   ```bash
   kubectl port-forward -n monitoring svc/prometheus 9090:9090
   # Open http://localhost:9090/alerts
   ```

2. Check Alertmanager:
   ```bash
   kubectl logs -n monitoring -l app=alertmanager
   ```

3. Test alert manually:
   ```bash
   curl -X POST http://localhost:9093/api/v1/alerts -d '[...]'
   ```

## Best Practices

1. **Use Recording Rules**: Pre-compute expensive queries
2. **Set Appropriate Retention**: Balance storage vs. history
3. **Label Wisely**: Use labels for filtering, not high-cardinality data
4. **Sample Traces**: Use probabilistic sampling in production
5. **Structure Logs**: Use JSON format for easy parsing
6. **Test Alerts**: Regularly test notification channels
7. **Monitor the Monitors**: Set up alerts for monitoring components

## Performance Tuning

### Prometheus

```yaml
# Increase retention
--storage.tsdb.retention.time=30d

# Increase memory
resources:
  limits:
    memory: 4Gi
```

### Loki

```yaml
# Reduce retention
retention_period: 168h  # 7 days

# Increase ingestion rate
ingestion_rate_mb: 20
```

### Jaeger

```yaml
# Reduce memory usage
--memory.max-traces=5000

# Use probabilistic sampling
sampler: { type: 'probabilistic', param: 0.1 }
```

## Resources

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Loki Documentation](https://grafana.com/docs/loki/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)

## Directory Structure

```
monitoring/
├── README.md                          # This file
├── prometheus/
│   ├── prometheus.yaml                # Prometheus deployment
│   ├── rules/
│   │   └── recording-rules.yaml       # Metric aggregations
│   └── alerts/
│       └── phase5-alerts.yaml         # Alert rules
├── grafana/
│   ├── grafana.yaml                   # Grafana deployment
│   ├── datasources.yaml               # Datasource config
│   ├── dashboards.yaml                # Dashboard ConfigMap
│   └── dashboards/
│       ├── phase5-overview.json       # System overview
│       ├── phase5-database.json       # Database metrics
│       └── phase5-agents.json         # Agent metrics
├── jaeger/
│   ├── README.md                      # Jaeger documentation
│   └── jaeger.yaml                    # Jaeger deployment
├── loki/
│   ├── README.md                      # Loki documentation
│   └── loki.yaml                      # Loki + Promtail
└── alertmanager/
    ├── README.md                      # Alertmanager docs
    └── alertmanager.yaml              # Alertmanager config
```
