import { initTracer, JaegerTracer } from 'jaeger-client';
import { FORMAT_HTTP_HEADERS, Span, SpanContext } from 'opentracing';

// Initialize Jaeger tracer
const config = {
  serviceName: 'phase5-backend',
  sampler: {
    type: 'const',
    param: 1, // Sample all traces in development, use probabilistic in production
  },
  reporter: {
    logSpans: true,
    collectorEndpoint: process.env.JAEGER_COLLECTOR_ENDPOINT || 'http://jaeger-collector.tracing:14268/api/traces',
    agentHost: process.env.JAEGER_AGENT_HOST || 'jaeger-agent.tracing',
    agentPort: parseInt(process.env.JAEGER_AGENT_PORT || '6831'),
  },
};

const options = {
  tags: {
    'phase5.version': process.env.APP_VERSION || '1.0.0',
    'phase5.environment': process.env.NODE_ENV || 'development',
  },
  logger: {
    info: (msg: string) => console.log('Jaeger INFO:', msg),
    error: (msg: string) => console.error('Jaeger ERROR:', msg),
  },
};

export const tracer: JaegerTracer = initTracer(config, options);

// Middleware to create spans for HTTP requests
export const tracingMiddleware = (req: any, res: any, next: any) => {
  // Extract parent span context from headers
  const parentSpanContext = tracer.extract(FORMAT_HTTP_HEADERS, req.headers) as SpanContext | null;

  // Create span for this request
  const span = tracer.startSpan('http_request', {
    childOf: parentSpanContext || undefined,
    tags: {
      'span.kind': 'server',
      'http.method': req.method,
      'http.url': req.url,
      'http.path': req.path,
      'http.route': req.route?.path || req.path,
    },
  });

  // Add span to request for use in handlers
  req.span = span;

  // Track response
  res.on('finish', () => {
    span.setTag('http.status_code', res.statusCode);

    if (res.statusCode >= 400) {
      span.setTag('error', true);
      span.setTag('error.kind', res.statusCode >= 500 ? 'server_error' : 'client_error');
    }

    span.finish();
  });

  next();
};

// Helper to create child spans
export const createChildSpan = (
  parentSpan: Span,
  operationName: string,
  tags?: { [key: string]: any }
): Span => {
  return tracer.startSpan(operationName, {
    childOf: parentSpan,
    tags: tags || {},
  });
};

// Helper to trace database operations
export const traceDatabaseOperation = async <T>(
  parentSpan: Span,
  operation: string,
  queryType: string,
  queryFn: () => Promise<T>
): Promise<T> => {
  const span = createChildSpan(parentSpan, 'database_query', {
    'db.type': 'postgresql',
    'db.operation': operation,
    'db.query_type': queryType,
  });

  try {
    const result = await queryFn();
    span.setTag('db.success', true);
    span.finish();
    return result;
  } catch (error: any) {
    span.setTag('error', true);
    span.setTag('error.message', error.message);
    span.log({
      event: 'error',
      'error.object': error,
      message: error.message,
      stack: error.stack,
    });
    span.finish();
    throw error;
  }
};

// Helper to trace Kafka operations
export const traceKafkaOperation = async <T>(
  parentSpan: Span,
  operation: 'produce' | 'consume',
  topic: string,
  operationFn: () => Promise<T>
): Promise<T> => {
  const span = createChildSpan(parentSpan, `kafka_${operation}`, {
    'messaging.system': 'kafka',
    'messaging.destination': topic,
    'messaging.operation': operation,
  });

  try {
    const result = await operationFn();
    span.setTag('messaging.success', true);
    span.finish();
    return result;
  } catch (error: any) {
    span.setTag('error', true);
    span.setTag('error.message', error.message);
    span.log({
      event: 'error',
      'error.object': error,
      message: error.message,
      stack: error.stack,
    });
    span.finish();
    throw error;
  }
};

// Helper to inject trace context into Kafka message headers
export const injectTraceContext = (span: Span): { [key: string]: string } => {
  const headers: { [key: string]: string } = {};
  tracer.inject(span, FORMAT_HTTP_HEADERS, headers);
  return headers;
};

// Helper to extract trace context from Kafka message headers
export const extractTraceContext = (headers: { [key: string]: any }): SpanContext | null => {
  try {
    return tracer.extract(FORMAT_HTTP_HEADERS, headers) as SpanContext | null;
  } catch (error) {
    console.error('Failed to extract trace context:', error);
    return null;
  }
};

// Helper to add custom tags to span
export const addSpanTags = (span: Span, tags: { [key: string]: any }) => {
  Object.entries(tags).forEach(([key, value]) => {
    span.setTag(key, value);
  });
};

// Helper to log events to span
export const logSpanEvent = (span: Span, event: string, data?: { [key: string]: any }) => {
  span.log({
    event,
    ...data,
  });
};

// Graceful shutdown
export const closeTracer = (): Promise<void> => {
  return new Promise((resolve) => {
    tracer.close(() => {
      console.log('Jaeger tracer closed');
      resolve();
    });
  });
};
