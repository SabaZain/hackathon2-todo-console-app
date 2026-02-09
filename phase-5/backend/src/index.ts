import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { Server, createServer } from 'http';
import { PrismaClient } from '@prisma/client';
import config from './config';
import logger from './config/logger';
import { kafkaProducer } from './events/kafka-producer';
import { errorHandler, notFoundHandler } from './api/middleware/error.middleware';
import { WebSocketService } from './services/websocket.service';

export const prisma = new PrismaClient({
  log: config.nodeEnv === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

class App {
  public app: Application;
  private server?: Server;
  private wsService?: WebSocketService;

  constructor() {
    this.app = express();
    this.initializeMiddlewares();
    this.initializeRoutes();
    this.initializeErrorHandling();
  }

  private initializeMiddlewares(): void {
    // Security
    this.app.use(helmet());

    // CORS
    this.app.use(
      cors({
        origin: config.corsOrigin,
        credentials: true,
      })
    );

    // Body parsing
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // Request logging
    this.app.use((req, res, next) => {
      logger.info(`${req.method} ${req.path}`, {
        query: req.query,
        ip: req.ip,
      });
      next();
    });
  }

  private initializeRoutes(): void {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'phase5-backend',
        version: '1.0.0',
      });
    });

    // API routes
    const taskRoutes = require('./api/routes/tasks.routes').default;
    const reminderRoutes = require('./api/routes/reminders.routes').default;
    const auditRoutes = require('./api/routes/audit.routes').default;
    this.app.use('/api/tasks', taskRoutes);
    this.app.use('/api/reminders', reminderRoutes);
    this.app.use('/api/audit', auditRoutes);
  }

  private initializeErrorHandling(): void {
    this.app.use(notFoundHandler);
    this.app.use(errorHandler);
  }

  public async start(): Promise<void> {
    try {
      // Connect to database
      await prisma.$connect();
      logger.info('Database connected successfully');

      // Connect to Kafka
      await kafkaProducer.connect();
      logger.info('Kafka producer connected successfully');

      // Start HTTP server
      const httpServer = createServer(this.app);
      this.server = httpServer.listen(config.port, () => {
        logger.info(`Server running on port ${config.port} in ${config.nodeEnv} mode`);
        logger.info(`Health check: http://localhost:${config.port}/health`);
      });

      // Initialize and start WebSocket service
      this.wsService = new WebSocketService(httpServer);
      await this.wsService.start();
      logger.info('WebSocket service started successfully');
    } catch (error) {
      logger.error('Failed to start server:', error);
      process.exit(1);
    }
  }

  public async stop(): Promise<void> {
    try {
      // Stop WebSocket service
      if (this.wsService) {
        await this.wsService.stop();
        logger.info('WebSocket service stopped');
      }

      // Disconnect Kafka
      await kafkaProducer.disconnect();
      logger.info('Kafka producer disconnected');

      // Disconnect database
      await prisma.$disconnect();
      logger.info('Database disconnected');

      // Close server
      if (this.server) {
        this.server.close(() => {
          logger.info('Server stopped');
        });
      }
    } catch (error) {
      logger.error('Error during shutdown:', error);
      process.exit(1);
    }
  }
}

// Create app instance
const app = new App();

// Handle graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down gracefully');
  await app.stop();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('SIGINT received, shutting down gracefully');
  await app.stop();
  process.exit(0);
});

// Start the server
app.start().catch((error) => {
  logger.error('Failed to start application:', error);
  process.exit(1);
});

export default app;
