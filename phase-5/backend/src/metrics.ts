import promClient from 'prom-client';

// Create a Registry to register metrics
export const register = new promClient.Registry();

// Add default metrics (CPU, memory, etc.)
promClient.collectDefaultMetrics({ register });

// HTTP Request Duration Histogram
export const httpRequestDuration = new promClient.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10],
  registers: [register],
});

// HTTP Request Counter
export const httpRequestsTotal = new promClient.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status'],
  registers: [register],
});

// Task Operations Counter
export const taskOperationsTotal = new promClient.Counter({
  name: 'task_operations_total',
  help: 'Total number of task operations',
  labelNames: ['operation', 'status'],
  registers: [register],
});

// Database Query Duration Histogram
export const databaseQueryDuration = new promClient.Histogram({
  name: 'database_query_duration_seconds',
  help: 'Duration of database queries in seconds',
  labelNames: ['query_type'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1],
  registers: [register],
});

// Database Connection Pool Gauge
export const databaseConnectionsActive = new promClient.Gauge({
  name: 'database_connections_active',
  help: 'Number of active database connections',
  registers: [register],
});

export const databaseConnectionsIdle = new promClient.Gauge({
  name: 'database_connections_idle',
  help: 'Number of idle database connections',
  registers: [register],
});

export const databaseConnectionsMax = new promClient.Gauge({
  name: 'database_connections_max',
  help: 'Maximum number of database connections',
  registers: [register],
});

// Kafka Event Counter
export const kafkaEventsProduced = new promClient.Counter({
  name: 'kafka_events_produced_total',
  help: 'Total number of Kafka events produced',
  labelNames: ['topic', 'event_type'],
  registers: [register],
});

export const kafkaEventsProducedErrors = new promClient.Counter({
  name: 'kafka_events_produced_errors_total',
  help: 'Total number of Kafka event production errors',
  labelNames: ['topic', 'event_type', 'error'],
  registers: [register],
});

// WebSocket Connections Gauge
export const websocketConnectionsActive = new promClient.Gauge({
  name: 'websocket_connections_active',
  help: 'Number of active WebSocket connections',
  registers: [register],
});

// WebSocket Messages Counter
export const websocketMessagesSent = new promClient.Counter({
  name: 'websocket_messages_sent_total',
  help: 'Total number of WebSocket messages sent',
  labelNames: ['message_type'],
  registers: [register],
});

export const websocketMessagesReceived = new promClient.Counter({
  name: 'websocket_messages_received_total',
  help: 'Total number of WebSocket messages received',
  labelNames: ['message_type'],
  registers: [register],
});

// Middleware to track HTTP metrics
export const metricsMiddleware = (req: any, res: any, next: any) => {
  const start = Date.now();

  // Track response
  res.on('finish', () => {
    const duration = (Date.now() - start) / 1000;
    const route = req.route?.path || req.path || 'unknown';
    const method = req.method;
    const status = res.statusCode;

    // Record duration
    httpRequestDuration.observe({ method, route, status }, duration);

    // Increment counter
    httpRequestsTotal.inc({ method, route, status });
  });

  next();
};

// Helper function to track task operations
export const trackTaskOperation = (operation: string, status: 'success' | 'error') => {
  taskOperationsTotal.inc({ operation, status });
};

// Helper function to track database queries
export const trackDatabaseQuery = async <T>(
  queryType: string,
  queryFn: () => Promise<T>
): Promise<T> => {
  const start = Date.now();
  try {
    const result = await queryFn();
    const duration = (Date.now() - start) / 1000;
    databaseQueryDuration.observe({ query_type: queryType }, duration);
    return result;
  } catch (error) {
    const duration = (Date.now() - start) / 1000;
    databaseQueryDuration.observe({ query_type: queryType }, duration);
    throw error;
  }
};

// Helper function to track Kafka events
export const trackKafkaEvent = (
  topic: string,
  eventType: string,
  success: boolean,
  error?: string
) => {
  if (success) {
    kafkaEventsProduced.inc({ topic, event_type: eventType });
  } else {
    kafkaEventsProducedErrors.inc({ topic, event_type: eventType, error: error || 'unknown' });
  }
};

// Helper function to update WebSocket connection count
export const updateWebSocketConnections = (count: number) => {
  websocketConnectionsActive.set(count);
};

// Helper function to track WebSocket messages
export const trackWebSocketMessage = (
  direction: 'sent' | 'received',
  messageType: string
) => {
  if (direction === 'sent') {
    websocketMessagesSent.inc({ message_type: messageType });
  } else {
    websocketMessagesReceived.inc({ message_type: messageType });
  }
};
