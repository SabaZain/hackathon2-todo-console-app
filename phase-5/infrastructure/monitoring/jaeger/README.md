# Jaeger Distributed Tracing

This directory contains Jaeger deployment configuration for distributed tracing across Phase 5 microservices.

## Overview

Jaeger is deployed as an all-in-one instance that includes:
- **Collector**: Receives traces from applications
- **Query**: Provides UI and API for trace queries
- **Agent**: Receives traces via UDP (for legacy clients)
- **Storage**: In-memory storage (Badger DB)

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Backend   │────▶│   Jaeger    │────▶│ Prometheus  │
│   Service   │     │  Collector  │     │  (Metrics)  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
┌─────────────┐            │
│   Agents    │────────────┤
│ (4 services)│            │
└─────────────┘            ▼
                    ┌─────────────┐
┌─────────────┐     │   Jaeger    │
│  Frontend   │────▶│    Query    │
└─────────────┘     │     UI      │
                    └─────────────┘
```

## Deployment

### Deploy to Kubernetes

```bash
kubectl apply -f jaeger.yaml
```

### Verify Deployment

```bash
# Check pod status
kubectl get pods -n tracing

# Check services
kubectl get svc -n tracing

# View logs
kubectl logs -n tracing -l app=jaeger
```

### Access Jaeger UI

**Port Forward:**
```bash
kubectl port-forward -n tracing svc/jaeger-query 16686:16686
```

Then open: http://localhost:16686

**Ingress (if configured):**
```bash
# Add to /etc/hosts
echo "$(minikube ip) jaeger.phase5.local" | sudo tee -a /etc/hosts
```

Then open: http://jaeger.phase5.local

## Instrumentation

### Backend Service (Node.js/Express)

Install dependencies:
```bash
npm install jaeger-client opentracing
```

Configure tracing in `backend/src/tracing.ts`:
```typescript
import { initTracer } from 'jaeger-client';

const config = {
  serviceName: 'phase5-backend',
  sampler: {
    type: 'const',
    param: 1,
  },
  reporter: {
    collectorEndpoint: 'http://jaeger-collector.tracing:14268/api/traces',
    logSpans: true,
  },
};

export const tracer = initTracer(config);
```

### Agents (Node.js)

Each agent should initialize its own tracer:
```typescript
const config = {
  serviceName: 'audit-agent', // or reminder-agent, etc.
  sampler: { type: 'const', param: 1 },
  reporter: {
    collectorEndpoint: 'http://jaeger-collector.tracing:14268/api/traces',
  },
};
```

### Frontend (React)

For browser-based tracing, use OpenTelemetry:
```bash
npm install @opentelemetry/api @opentelemetry/sdk-trace-web @opentelemetry/exporter-jaeger
```

## Trace Context Propagation

Ensure trace context is propagated through:
1. **HTTP Headers**: Use `uber-trace-id` header
2. **Kafka Messages**: Include trace context in message headers
3. **WebSocket**: Propagate context in connection metadata

Example Kafka message with trace context:
```typescript
await producer.send({
  topic: 'task-events',
  messages: [{
    key: taskId,
    value: JSON.stringify(event),
    headers: {
      'uber-trace-id': traceContext,
    },
  }],
});
```

## Querying Traces

### Find Traces by Service
1. Open Jaeger UI
2. Select service: `phase5-backend`, `audit-agent`, etc.
3. Click "Find Traces"

### Find Traces by Operation
- `POST /api/tasks` - Task creation
- `PUT /api/tasks/:id` - Task updates
- `GET /api/tasks` - Task queries
- `kafka.consume.task-events` - Event consumption

### Find Traces by Tags
- `http.status_code=500` - Find errors
- `user.id=123` - Find user-specific traces
- `task.id=abc` - Find task-specific operations

## Metrics Integration

Jaeger exports metrics to Prometheus:
- `jaeger_collector_traces_received_total` - Traces received
- `jaeger_collector_spans_received_total` - Spans received
- `jaeger_query_requests_total` - Query requests

## Performance Tuning

### Memory Limits
Default: 10,000 traces in memory. Adjust with:
```yaml
args:
  - "--memory.max-traces=50000"
```

### Sampling
For production, use probabilistic sampling:
```typescript
sampler: {
  type: 'probabilistic',
  param: 0.1, // Sample 10% of traces
}
```

### Storage
For production, use persistent storage:
- **Elasticsearch**: Best for large-scale deployments
- **Cassandra**: Good for high write throughput
- **Badger**: Good for single-node deployments

## Troubleshooting

### No Traces Appearing

1. **Check collector logs:**
   ```bash
   kubectl logs -n tracing -l app=jaeger | grep collector
   ```

2. **Verify network connectivity:**
   ```bash
   kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
     curl http://jaeger-collector.tracing:14268/api/traces
   ```

3. **Check application logs** for tracing errors

### High Memory Usage

1. Reduce max traces:
   ```yaml
   args:
     - "--memory.max-traces=5000"
   ```

2. Increase sampling rate (sample less):
   ```typescript
   sampler: { type: 'probabilistic', param: 0.01 }
   ```

## Best Practices

1. **Use Consistent Service Names**: Match Kubernetes service names
2. **Tag Appropriately**: Add business-relevant tags (user_id, task_id)
3. **Propagate Context**: Always propagate trace context across boundaries
4. **Sample Wisely**: Use probabilistic sampling in production
5. **Monitor Jaeger**: Set up alerts for collector errors

## Resources

- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [OpenTracing Specification](https://opentracing.io/specification/)
- [Jaeger Client Libraries](https://www.jaegertracing.io/docs/latest/client-libraries/)
