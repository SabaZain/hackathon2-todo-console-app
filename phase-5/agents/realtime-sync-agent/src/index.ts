import express from 'express';
import { Server } from 'socket.io';
import { createServer } from 'http';
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import {
  tracer,
  createSpan,
  finishSpan,
  logger,
  createContextLogger,
  register,
  trackKafkaEvent,
  trackAgentOperation,
  closeTracer,
} from '../shared/observability';
import promClient from 'prom-client';

const app = express();
const httpServer = createServer(app);

const SERVICE_NAME = 'realtime-sync-agent';
const PORT = process.env.PORT || 3104;

// WebSocket server
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  },
});

// Additional metrics specific to realtime sync agent
const websocketConnectionsActive = new promClient.Gauge({
  name: 'websocket_connections_active',
  help: 'Number of active WebSocket connections',
  registers: [register],
});

const websocketMessagesSent = new promClient.Counter({
  name: 'websocket_messages_sent_total',
  help: 'Total number of WebSocket messages sent',
  labelNames: ['message_type'],
  registers: [register],
});

const websocketMessagesReceived = new promClient.Counter({
  name: 'websocket_messages_received_total',
  help: 'Total number of WebSocket messages received',
  labelNames: ['message_type'],
  registers: [register],
});

const websocketBroadcastDuration = new promClient.Histogram({
  name: 'websocket_broadcast_duration_seconds',
  help: 'Duration of WebSocket broadcast in seconds',
  labelNames: ['event_type'],
  buckets: [0.001, 0.005, 0.01, 0.05, 0.1],
  registers: [register],
});

// Kafka configuration
const kafka = new Kafka({
  clientId: SERVICE_NAME,
  brokers: [process.env.KAFKA_BROKER || 'kafka:9092'],
});

const consumer: Consumer = kafka.consumer({
  groupId: `${SERVICE_NAME}-group`,
});

// Track connected clients by user ID
const connectedClients = new Map<string, Set<string>>();

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: SERVICE_NAME,
    timestamp: new Date().toISOString(),
    connections: io.engine.clientsCount,
  });
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (error: any) {
    logger.error('Failed to generate metrics', { error: error.message });
    res.status(500).end(error.message);
  }
});

// WebSocket connection handling
io.on('connection', (socket) => {
  const userId = socket.handshake.auth.userId;

  logger.info('WebSocket client connected', {
    socketId: socket.id,
    userId,
  });

  // Track connection
  if (userId) {
    if (!connectedClients.has(userId)) {
      connectedClients.set(userId, new Set());
    }
    connectedClients.get(userId)!.add(socket.id);
  }

  websocketConnectionsActive.set(io.engine.clientsCount);
  websocketMessagesReceived.inc({ message_type: 'connection' });

  // Handle client messages
  socket.on('message', (data) => {
    websocketMessagesReceived.inc({ message_type: data.type || 'unknown' });

    logger.debug('WebSocket message received', {
      socketId: socket.id,
      userId,
      messageType: data.type,
    });
  });

  // Handle disconnection
  socket.on('disconnect', () => {
    logger.info('WebSocket client disconnected', {
      socketId: socket.id,
      userId,
    });

    // Remove from tracking
    if (userId && connectedClients.has(userId)) {
      connectedClients.get(userId)!.delete(socket.id);
      if (connectedClients.get(userId)!.size === 0) {
        connectedClients.delete(userId);
      }
    }

    websocketConnectionsActive.set(io.engine.clientsCount);
    websocketMessagesReceived.inc({ message_type: 'disconnection' });
  });
});

// Broadcast event to user's connected clients
const broadcastToUser = (userId: string, event: any, span: any): void => {
  const start = Date.now();
  const childSpan = tracer.startSpan('broadcast_to_user', { childOf: span });

  try {
    const userSockets = connectedClients.get(userId);

    if (!userSockets || userSockets.size === 0) {
      logger.debug('No connected clients for user', { userId });
      childSpan.setTag('broadcast.skipped', true);
      childSpan.finish();
      return;
    }

    // Send to all user's connected clients
    userSockets.forEach((socketId) => {
      io.to(socketId).emit('task-update', event);
    });

    const duration = (Date.now() - start) / 1000;
    websocketMessagesSent.inc({
      message_type: event.type,
    });
    websocketBroadcastDuration.observe({ event_type: event.type }, duration);

    childSpan.setTag('broadcast.success', true);
    childSpan.setTag('broadcast.recipients', userSockets.size);
    childSpan.finish();

    logger.debug('Event broadcasted to user', {
      userId,
      eventType: event.type,
      recipients: userSockets.size,
    });
  } catch (error: any) {
    childSpan.setTag('error', true);
    childSpan.log({ event: 'error', message: error.message });
    childSpan.finish();

    throw error;
  }
};

// Process task update event
const processTaskUpdateEvent = async (payload: EachMessagePayload) => {
  const start = Date.now();
  const span = createSpan('process_task_update');
  const contextLogger = createContextLogger({
    service: SERVICE_NAME,
    topic: payload.topic,
    partition: payload.partition,
    offset: payload.message.offset,
  });

  try {
    const event = JSON.parse(payload.message.value?.toString() || '{}');

    contextLogger.info('Processing task update event', {
      eventType: event.type,
      taskId: event.taskId,
      userId: event.userId,
    });

    span.setTag('event.type', event.type);
    span.setTag('task.id', event.taskId);
    span.setTag('user.id', event.userId);

    // Broadcast to user's connected clients
    broadcastToUser(event.userId, event, span);

    const duration = (Date.now() - start) / 1000;
    trackKafkaEvent(payload.topic, event.type, 'success', duration);
    trackAgentOperation('realtime_sync', 'success', duration);

    contextLogger.info('Task update broadcasted successfully', {
      eventType: event.type,
      taskId: event.taskId,
      duration,
    });

    finishSpan(span);
  } catch (error: any) {
    const duration = (Date.now() - start) / 1000;
    trackKafkaEvent(payload.topic, 'unknown', 'error', duration);
    trackAgentOperation('realtime_sync', 'error', duration);

    contextLogger.error('Failed to broadcast task update', {
      error: error.message,
      stack: error.stack,
    });

    finishSpan(span, error);
    throw error;
  }
};

// Start Kafka consumer
const startConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'task-updates', fromBeginning: false });

  await consumer.run({
    eachMessage: processTaskUpdateEvent,
  });

  logger.info('RealTime sync agent started', {
    service: SERVICE_NAME,
    topics: ['task-updates'],
  });
};

// Start HTTP server
httpServer.listen(PORT, () => {
  logger.info('RealTime sync agent HTTP server started', {
    port: PORT,
    service: SERVICE_NAME,
  });
});

// Graceful shutdown
const gracefulShutdown = async (signal: string) => {
  logger.info(`Received ${signal}, starting graceful shutdown`);

  // Close WebSocket connections
  io.close(() => {
    logger.info('WebSocket server closed');
  });

  await consumer.disconnect();
  await closeTracer();

  logger.info('Graceful shutdown complete');
  process.exit(0);
};

process.on('SIGTERM', () => gracefulShutdown('SIGTERM'));
process.on('SIGINT', () => gracefulShutdown('SIGINT'));

// Start the agent
startConsumer().catch((error) => {
  logger.error('Failed to start realtime sync agent', {
    error: error.message,
    stack: error.stack,
  });
  process.exit(1);
});
