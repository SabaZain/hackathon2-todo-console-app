import express, { Application } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { Server, createServer } from 'http';
import { PrismaClient } from '@prisma/client';
import swaggerUi from 'swagger-ui-express';
import config from './config';
import logger from './logger';
import { kafkaProducer } from './events/kafka-producer';
import { errorHandler, notFoundHandler } from './api/middleware/error.middleware';
import { WebSocketService } from './services/websocket.service';
import { swaggerSpec } from './swagger';

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
    // Security - Allow Swagger UI inline scripts
    this.app.use(
      helmet({
        contentSecurityPolicy: {
          directives: {
            defaultSrc: ["'self'"],
            styleSrc: ["'self'", "'unsafe-inline'"],
            scriptSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", 'data:', 'https:'],
          },
        },
      })
    );

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
    this.app.use((req, _res, next) => {
      logger.info(`${req.method} ${req.path}`, {
        query: req.query,
        ip: req.ip,
      });
      next();
    });
  }

  private initializeRoutes(): void {
    /**
     * @swagger
     * /health:
     *   get:
     *     summary: Health check endpoint
     *     tags: [Health]
     *     security: []
     *     responses:
     *       200:
     *         description: Service is healthy
     *         content:
     *           application/json:
     *             schema:
     *               type: object
     *               properties:
     *                 status:
     *                   type: string
     *                   example: healthy
     *                 timestamp:
     *                   type: string
     *                   format: date-time
     *                 service:
     *                   type: string
     *                   example: phase5-backend
     *                 version:
     *                   type: string
     *                   example: 1.0.0
     */
    this.app.get('/health', (_req, res) => {
      res.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        service: 'phase5-backend',
        version: '1.0.0',
      });
    });

    // Swagger documentation
    this.app.use('/docs', swaggerUi.serve, swaggerUi.setup(swaggerSpec, {
      customCss: '.swagger-ui .topbar { display: none }',
      customSiteTitle: 'Phase 5 Backend API Documentation',
    }));

    // API routes
    const authRoutes = require('./api/routes/auth.routes').default;
    const taskRoutes = require('./api/routes/tasks.routes').default;
    const reminderRoutes = require('./api/routes/reminders.routes').default;
    const auditRoutes = require('./api/routes/audit.routes').default;
    this.app.use('/api/auth', authRoutes);
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

      // Try to connect to Kafka (optional)
      try {
        await kafkaProducer.connect();
        logger.info('Kafka producer connected successfully');
      } catch (error) {
        logger.warn('Kafka connection failed - running without event streaming', { error });
      }

      // Start HTTP server
      const httpServer = createServer(this.app);
      this.server = httpServer.listen(config.port, () => {
        logger.info(`Server running on port ${config.port} in ${config.nodeEnv} mode`);
        logger.info(`Health check: http://localhost:${config.port}/health`);
      });

      // Try to initialize WebSocket service (optional)
      try {
        this.wsService = new WebSocketService(httpServer);
        await this.wsService.start();
        logger.info('WebSocket service started successfully');
      } catch (error) {
        logger.warn('WebSocket service failed to start - running without real-time sync', { error });
      }
    } catch (error) {
      logger.error('Failed to start server:', error);
      process.exit(1);
    }
  }

  public async stop(): Promise<void> {
    try {
      // Stop WebSocket service
      if (this.wsService) {
        try {
          await this.wsService.stop();
          logger.info('WebSocket service stopped');
        } catch (error) {
          logger.warn('Error stopping WebSocket service', { error });
        }
      }

      // Disconnect Kafka
      try {
        await kafkaProducer.disconnect();
        logger.info('Kafka producer disconnected');
      } catch (error) {
        logger.warn('Error disconnecting Kafka', { error });
      }

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
const appInstance = new App();

// Handle graceful shutdown
process.on('SIGTERM', async () => {
  logger.info('SIGTERM received, shutting down gracefully');
  await appInstance.stop();
  process.exit(0);
});

process.on('SIGINT', async () => {
  logger.info('SIGINT received, shutting down gracefully');
  await appInstance.stop();
  process.exit(0);
});

// Start the server
appInstance.start().catch((error) => {
  logger.error('Failed to start application:', error);
  process.exit(1);
});

export const app = appInstance.app;
export default appInstance;
