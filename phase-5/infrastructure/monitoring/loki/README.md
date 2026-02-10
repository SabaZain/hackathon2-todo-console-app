# Loki Log Aggregation

This directory contains Grafana Loki deployment configuration for centralized log aggregation across Phase 5 microservices.

## Overview

Loki is a horizontally-scalable, highly-available log aggregation system inspired by Prometheus. It includes:
- **Loki**: Log storage and query engine
- **Promtail**: Log collection agent (DaemonSet on each node)
- **Grafana Integration**: Query logs directly from Grafana

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Backend   │────▶│  Promtail   │────▶│    Loki     │
│    Pods     │     │  (DaemonSet)│     │  (Storage)  │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
┌─────────────┐     ┌─────────────┐            │
│   Agents    │────▶│  Promtail   │────────────┤
│    Pods     │     │  (DaemonSet)│            │
└─────────────┘     └─────────────┘            ▼
                                        ┌─────────────┐
┌─────────────┐                         │   Grafana   │
│  Frontend   │                         │  (Query UI) │
│    Pods     │                         └─────────────┘
└─────────────┘
```

## Deployment

### Deploy to Kubernetes

```bash
kubectl apply -f loki.yaml
```

### Verify Deployment

```bash
# Check Loki pod
kubectl get pods -n monitoring -l app=loki

# Check Promtail DaemonSet
kubectl get daemonset -n monitoring promtail

# View Loki logs
kubectl logs -n monitoring -l app=loki

# View Promtail logs
kubectl logs -n monitoring -l app=promtail
```

### Access Loki

Loki is accessed through Grafana (already configured as a datasource).

**Port Forward (for direct API access):**
```bash
kubectl port-forward -n monitoring svc/loki 3100:3100
```

Then query: http://localhost:3100/loki/api/v1/query

## Log Collection

### Automatic Collection

Promtail automatically collects logs from:
- All pods in `phase5-*` namespaces
- Container stdout/stderr
- System logs from `/var/log`

### Log Labels

Logs are automatically labeled with:
- `namespace`: Kubernetes namespace
- `pod`: Pod name
- `container`: Container name
- `app`: Application name (from labels)
- `component`: Component name (from labels)
- `level`: Log level (parsed from JSON logs)

### Structured Logging

For best results, use structured JSON logging in your applications:

```typescript
// Backend/Agents
import winston from 'winston';

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

logger.info('Task created', {
  taskId: '123',
  userId: 'user-456',
  operation: 'create'
});
```

## Querying Logs in Grafana

### Basic Queries

**All logs from backend:**
```logql
{app="phase5-backend"}
```

**Error logs only:**
```logql
{app="phase5-backend"} |= "error" or "ERROR"
```

**Logs from specific pod:**
```logql
{pod="phase5-backend-abc123"}
```

**Logs with JSON parsing:**
```logql
{app="phase5-backend"} | json | level="error"
```

### Advanced Queries

**Count errors per minute:**
```logql
sum(rate({app="phase5-backend"} |= "error" [1m]))
```

**Filter by task ID:**
```logql
{app="phase5-backend"} | json | taskId="123"
```

**Aggregate by component:**
```logql
sum by (component) (rate({namespace=~"phase5-.*"}[5m]))
```

**Pattern matching:**
```logql
{app="phase5-backend"} |~ "Task .* created"
```

## Log Retention

**Default Retention**: 31 days (744 hours)

To change retention, edit `loki-config` ConfigMap:
```yaml
limits_config:
  retention_period: 744h  # Change this value
```

Then restart Loki:
```bash
kubectl rollout restart statefulset/loki -n monitoring
```

## Storage

**Default**: 10Gi persistent volume per Loki instance

To increase storage:
```yaml
volumeClaimTemplates:
  - metadata:
      name: storage
    spec:
      resources:
        requests:
          storage: 50Gi  # Increase this
```

## Performance Tuning

### Ingestion Rate Limits

Default: 10MB/s per tenant

To increase:
```yaml
limits_config:
  ingestion_rate_mb: 20
  ingestion_burst_size_mb: 40
```

### Query Performance

**Use time ranges:**
```logql
{app="phase5-backend"} [5m]  # Last 5 minutes only
```

**Limit results:**
```logql
{app="phase5-backend"} | limit 100
```

**Use label filters first:**
```logql
{app="phase5-backend", level="error"}  # Good
{app="phase5-backend"} | json | level="error"  # Slower
```

## Troubleshooting

### No Logs Appearing

1. **Check Promtail is running:**
   ```bash
   kubectl get pods -n monitoring -l app=promtail
   ```

2. **Check Promtail logs:**
   ```bash
   kubectl logs -n monitoring -l app=promtail
   ```

3. **Verify pod labels:**
   ```bash
   kubectl get pods -n phase5-production --show-labels
   ```

4. **Test Loki API:**
   ```bash
   kubectl port-forward -n monitoring svc/loki 3100:3100
   curl http://localhost:3100/ready
   ```

### High Memory Usage

1. **Reduce retention period:**
   ```yaml
   retention_period: 168h  # 7 days
   ```

2. **Limit query results:**
   ```yaml
   max_query_series: 100
   ```

3. **Increase compaction frequency:**
   ```yaml
   compaction_interval: 5m
   ```

### Slow Queries

1. **Add more specific labels** to your queries
2. **Reduce time range** being queried
3. **Use metric queries** instead of log queries when possible
4. **Enable query caching** (already enabled by default)

## Integration with Alerts

Create alerts based on log patterns:

```yaml
# In Prometheus alert rules
- alert: HighErrorLogRate
  expr: |
    sum(rate({app="phase5-backend"} |= "error" [5m])) > 10
  for: 5m
  annotations:
    summary: "High error log rate detected"
```

## Best Practices

1. **Use Structured Logging**: JSON format for easy parsing
2. **Add Context**: Include relevant IDs (taskId, userId, etc.)
3. **Consistent Log Levels**: Use standard levels (debug, info, warn, error)
4. **Avoid Logging Secrets**: Never log passwords, tokens, or sensitive data
5. **Use Labels Wisely**: Add labels for filtering, not for high-cardinality data
6. **Query Efficiently**: Always use label filters first

## Example Log Queries

### Debugging Task Operations

```logql
# Find all operations for a specific task
{app="phase5-backend"} | json | taskId="abc-123"

# Find failed task operations
{app="phase5-backend"} | json | operation="task" | status="failed"

# Count task operations by type
sum by (operation) (rate({app="phase5-backend"} | json | operation=~"task.*" [5m]))
```

### Monitoring Agents

```logql
# Audit agent activity
{component="audit-agent"} | json

# Reminder delivery failures
{component="reminder-agent"} | json | status="failed"

# Recurring task generation
{component="recurring-task-agent"} | json | operation="generate"
```

### Performance Analysis

```logql
# Slow database queries
{app="phase5-backend"} | json | duration > 1000

# High memory usage warnings
{namespace=~"phase5-.*"} |= "memory" |= "high"

# Connection pool exhaustion
{app="phase5-backend"} |= "connection pool" |= "exhausted"
```

## Resources

- [Loki Documentation](https://grafana.com/docs/loki/latest/)
- [LogQL Query Language](https://grafana.com/docs/loki/latest/logql/)
- [Promtail Configuration](https://grafana.com/docs/loki/latest/clients/promtail/)
