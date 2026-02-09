import { Server as HTTPServer } from 'http';
import { Server as SocketIOServer, Socket } from 'socket.io';
import { Kafka, Consumer, EachMessagePayload } from 'kafkajs';
import logger from '../config/logger';

interface AuthenticatedSocket extends Socket {
  userId?: string;
}

export class WebSocketService {
  private io: SocketIOServer;
  private kafka: Kafka;
  private consumer: Consumer;
  private connectedUsers: Map<string, Set<string>> = new Map(); // userId -> Set of socketIds

  constructor(httpServer: HTTPServer) {
    this.io = new SocketIOServer(httpServer, {
      cors: {
        origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
        credentials: true,
      },
    });

    this.kafka = new Kafka({
      clientId: 'websocket-service',
      brokers: [process.env.KAFKA_BROKERS || 'localhost:9092'],
    });

    this.consumer = this.kafka.consumer({ groupId: 'websocket-service-group' });

    this.setupSocketHandlers();
  }

  private setupSocketHandlers(): void {
    this.io.on('connection', (socket: AuthenticatedSocket) => {
      logger.info('Client connected:', { socketId: socket.id });

      // Authentication
      socket.on('authenticate', (data: { userId: string; token: string }) => {
        // TODO: Verify JWT token
        // For now, just accept the userId
        socket.userId = data.userId;

        // Track connected user
        if (!this.connectedUsers.has(data.userId)) {
          this.connectedUsers.set(data.userId, new Set());
        }
        this.connectedUsers.get(data.userId)!.add(socket.id);

        // Join user-specific room
        socket.join(`user:${data.userId}`);

        logger.info('Client authenticated:', {
          socketId: socket.id,
          userId: data.userId,
        });

        socket.emit('authenticated', { success: true });
      });

      // Handle disconnection
      socket.on('disconnect', () => {
        if (socket.userId) {
          const userSockets = this.connectedUsers.get(socket.userId);
          if (userSockets) {
            userSockets.delete(socket.id);
            if (userSockets.size === 0) {
              this.connectedUsers.delete(socket.userId);
            }
          }
        }

        logger.info('Client disconnected:', {
          socketId: socket.id,
          userId: socket.userId,
        });
      });

      // Handle task subscription
      socket.on('subscribe:task', (taskId: string) => {
        socket.join(`task:${taskId}`);
        logger.info('Client subscribed to task:', {
          socketId: socket.id,
          taskId,
        });
      });

      // Handle task unsubscription
      socket.on('unsubscribe:task', (taskId: string) => {
        socket.leave(`task:${taskId}`);
        logger.info('Client unsubscribed from task:', {
          socketId: socket.id,
          taskId,
        });
      });
    });
  }

  public async start(): Promise<void> {
    try {
      // Connect to Kafka
      await this.consumer.connect();
      logger.info('WebSocket service connected to Kafka');

      // Subscribe to task-updates topic
      await this.consumer.subscribe({ topic: 'task-updates', fromBeginning: false });
      logger.info('WebSocket service subscribed to task-updates topic');

      // Start consuming messages
      await this.consumer.run({
        eachMessage: async (payload: EachMessagePayload) => {
          await this.handleTaskUpdate(payload);
        },
      });

      logger.info('WebSocket service started successfully');
    } catch (error) {
      logger.error('Failed to start WebSocket service:', error);
      throw error;
    }
  }

  private async handleTaskUpdate(payload: EachMessagePayload): Promise<void> {
    const { message } = payload;

    try {
      const event = JSON.parse(message.value?.toString() || '{}');

      logger.info('Processing task update:', {
        eventType: event.eventType,
        eventId: event.eventId,
        taskId: event.taskId,
        userId: event.userId,
      });

      // Broadcast to user's room
      if (event.userId) {
        this.io.to(`user:${event.userId}`).emit('task:update', {
          eventType: event.eventType,
          taskId: event.taskId,
          payload: event.payload,
          timestamp: event.timestamp,
        });
      }

      // Broadcast to task-specific room (for users viewing the task)
      if (event.taskId) {
        this.io.to(`task:${event.taskId}`).emit('task:update', {
          eventType: event.eventType,
          taskId: event.taskId,
          payload: event.payload,
          timestamp: event.timestamp,
        });
      }

      logger.info('Task update broadcasted:', {
        eventId: event.eventId,
        taskId: event.taskId,
      });
    } catch (error) {
      logger.error('Failed to process task update:', error);
    }
  }

  public async stop(): Promise<void> {
    await this.consumer.disconnect();
    this.io.close();
    logger.info('WebSocket service stopped');
  }

  // Utility methods
  public getConnectedUsers(): string[] {
    return Array.from(this.connectedUsers.keys());
  }

  public getUserConnectionCount(userId: string): number {
    return this.connectedUsers.get(userId)?.size || 0;
  }

  public isUserConnected(userId: string): boolean {
    return this.connectedUsers.has(userId) && this.connectedUsers.get(userId)!.size > 0;
  }
}
