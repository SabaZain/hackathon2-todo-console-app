import winston from 'winston';

// Define log levels
const levels = {
  error: 0,
  warn: 1,
  info: 2,
  http: 3,
  debug: 4,
};

// Define colors for each level
const colors = {
  error: 'red',
  warn: 'yellow',
  info: 'green',
  http: 'magenta',
  debug: 'blue',
};

// Tell winston about our colors
winston.addColors(colors);

// Define format for logs
const format = winston.format.combine(
  winston.format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss:ms' }),
  winston.format.errors({ stack: true }),
  winston.format.splat(),
  winston.format.json()
);

// Define which transports to use
const transports = [
  // Console transport with JSON format for Loki
  new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize({ all: false }), // No colors in JSON
      format
    ),
  }),
];

// Create the logger
export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  levels,
  format,
  transports,
  exitOnError: false,
});

// Create a stream for Morgan HTTP logging
export const httpLogStream = {
  write: (message: string) => {
    logger.http(message.trim());
  },
};

// Helper to create child logger with context
export const createContextLogger = (context: {
  requestId?: string;
  userId?: string;
  taskId?: string;
  [key: string]: any;
}) => {
  return {
    error: (message: string, meta?: any) => {
      logger.error(message, { ...context, ...meta });
    },
    warn: (message: string, meta?: any) => {
      logger.warn(message, { ...context, ...meta });
    },
    info: (message: string, meta?: any) => {
      logger.info(message, { ...context, ...meta });
    },
    http: (message: string, meta?: any) => {
      logger.http(message, { ...context, ...meta });
    },
    debug: (message: string, meta?: any) => {
      logger.debug(message, { ...context, ...meta });
    },
  };
};

// Middleware to add request ID and logging context
export const loggingMiddleware = (req: any, res: any, next: any) => {
  // Generate request ID if not present
  req.requestId = req.headers['x-request-id'] || `req-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

  // Add request ID to response headers
  res.setHeader('X-Request-ID', req.requestId);

  // Create context logger for this request
  req.logger = createContextLogger({
    requestId: req.requestId,
    userId: req.user?.id,
  });

  // Log incoming request
  req.logger.http('Incoming request', {
    method: req.method,
    url: req.url,
    path: req.path,
    ip: req.ip,
    userAgent: req.headers['user-agent'],
  });

  // Track response time
  const start = Date.now();

  res.on('finish', () => {
    const duration = Date.now() - start;

    req.logger.http('Request completed', {
      method: req.method,
      url: req.url,
      path: req.path,
      status: res.statusCode,
      duration,
    });

    // Log errors
    if (res.statusCode >= 400) {
      const level = res.statusCode >= 500 ? 'error' : 'warn';
      req.logger[level]('Request failed', {
        method: req.method,
        url: req.url,
        path: req.path,
        status: res.statusCode,
        duration,
      });
    }
  });

  next();
};

// Helper to log task operations
export const logTaskOperation = (
  logger: ReturnType<typeof createContextLogger>,
  operation: string,
  taskId: string,
  data?: any
) => {
  logger.info(`Task ${operation}`, {
    operation,
    taskId,
    ...data,
  });
};

// Helper to log database operations
export const logDatabaseOperation = (
  logger: ReturnType<typeof createContextLogger>,
  operation: string,
  queryType: string,
  duration: number,
  error?: any
) => {
  if (error) {
    logger.error('Database operation failed', {
      operation,
      queryType,
      duration,
      error: error.message,
      stack: error.stack,
    });
  } else {
    logger.debug('Database operation completed', {
      operation,
      queryType,
      duration,
    });
  }
};

// Helper to log Kafka operations
export const logKafkaOperation = (
  logger: ReturnType<typeof createContextLogger>,
  operation: 'produce' | 'consume',
  topic: string,
  eventType: string,
  success: boolean,
  error?: any
) => {
  if (success) {
    logger.info(`Kafka event ${operation}d`, {
      operation,
      topic,
      eventType,
    });
  } else {
    logger.error(`Kafka event ${operation} failed`, {
      operation,
      topic,
      eventType,
      error: error?.message,
      stack: error?.stack,
    });
  }
};

// Helper to log WebSocket events
export const logWebSocketEvent = (
  logger: ReturnType<typeof createContextLogger>,
  event: string,
  data?: any
) => {
  logger.info(`WebSocket ${event}`, {
    event,
    ...data,
  });
};

export default logger;
