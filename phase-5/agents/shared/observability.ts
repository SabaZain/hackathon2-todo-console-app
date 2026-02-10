import { initTracer, JaegerTracer } from 'jaeger-client';
import { Span } from 'opentracing';
import winston from 'winston';
import promClient from 'prom-client';

// ============================================================================
// Jaeger Tracing Configuration
// ============================================================================

const tracerConfig = {
  serviceName: process.env.SERVICE_NAME || 'phase5-agent',
  sampler: {
    type: 'const',
    param: 1,
  },
  reporter: {
    logSpans: true,
    collectorEndpoint: process.env.JAEGER_COLLECTOR_ENDPOINT || 'http://jaeger-collector.tracing:14268/api/traces',
  },
};

export const tracer: JaegerTracer = initTracer(tracerConfig, {
  tags: {
    'phase5.version': process.env.APP_VERSION || '1.0.0',
    'phase5.environment': process.env.NODE_ENV || 'development',
  },
});

export const createSpan = (operationName: string, parentSpan?: Span): Span => {
  return tracer.startSpan(operationName, {
    childOf: parentSpan,
  });
};

export const finishSpan = (span: Span, error?: Error) => {
  if (error) {
    span.setTag('error', true);
    span.log({
      event: 'error',
      message: error.message,
      stack: error.stack,
    });
  }
  span.finish();
};

// ============================================================================
// Winston Logging Configuration
// ============================================================================

const logFormat = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
  winston.format.errors({ stack: true }),
  winston.format.json()
);

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: logFormat,
  transports: [
    new winston.transports.Console({
      format: logFormat,
    }),
  ],
});

export const createContextLogger = (context: { [key: string]: any }) => {
  return {
    error: (message: string, meta?: any) => logger.error(message, { ...context, ...meta }),
    warn: (message: string, meta?: any) => logger.warn(message, { ...context, ...meta }),
    info: (message: string, meta?: any) => logger.info(message, { ...context, ...meta }),
    debug: (message: string, meta?: any) => logger.debug(message, { ...context, ...meta }),
  };
};

// ============================================================================
// Prometheus Metrics Configuration
// ============================================================================

export const register = new promClient.Registry();

// Add default metrics
promClient.collectDefaultMetrics({ register });

// Kafka event processing metrics
export const kafkaEventsProcessed = new promClient.Counter({
  name: 'kafka_events_processed_total',
  help: 'Total number of Kafka events processed',
  labelNames: ['topic', 'event_type', 'status'],
  registers: [register],
});

export const kafkaEventProcessingDuration = new promClient.Histogram({
  name: 'kafka_event_processing_duration_seconds',
  help: 'Duration of Kafka event processing in seconds',
  labelNames: ['topic', 'event_type'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5],
  registers: [register],
});

export const kafkaConsumerLag = new promClient.Gauge({
  name: 'kafka_consumer_lag',
  help: 'Kafka consumer lag in messages',
  labelNames: ['consumer_group', 'topic', 'partition'],
  registers: [register],
});

// Agent-specific operation metrics
export const agentOperationsTotal = new promClient.Counter({
  name: 'agent_operations_total',
  help: 'Total number of agent operations',
  labelNames: ['operation', 'status'],
  registers: [register],
});

export const agentOperationDuration = new promClient.Histogram({
  name: 'agent_operation_duration_seconds',
  help: 'Duration of agent operations in seconds',
  labelNames: ['operation'],
  buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10],
  registers: [register],
});

// Helper functions
export const trackKafkaEvent = (
  topic: string,
  eventType: string,
  status: 'success' | 'error',
  duration: number
) => {
  kafkaEventsProcessed.inc({ topic, event_type: eventType, status });
  kafkaEventProcessingDuration.observe({ topic, event_type: eventType }, duration);
};

export const trackAgentOperation = (
  operation: string,
  status: 'success' | 'error',
  duration: number
) => {
  agentOperationsTotal.inc({ operation, status });
  agentOperationDuration.observe({ operation }, duration);
};

export const updateConsumerLag = (
  consumerGroup: string,
  topic: string,
  partition: number,
  lag: number
) => {
  kafkaConsumerLag.set(
    { consumer_group: consumerGroup, topic, partition: partition.toString() },
    lag
  );
};

// ============================================================================
// Graceful Shutdown
// ============================================================================

export const closeTracer = (): Promise<void> => {
  return new Promise((resolve) => {
    tracer.close(() => {
      logger.info('Jaeger tracer closed');
      resolve();
    });
  });
};
