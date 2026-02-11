import swaggerJsdoc from 'swagger-jsdoc';

const options: swaggerJsdoc.Options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Phase 5 Backend API',
      version: '1.0.0',
      description: 'Event-Driven Todo Application with Kafka, Dapr, and Kubernetes',
      contact: {
        name: 'Phase 5 Team',
      },
    },
    servers: [
      {
        url: 'http://localhost:3001',
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
      schemas: {
        Task: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            title: { type: 'string' },
            description: { type: 'string', nullable: true },
            userId: { type: 'string' },
            status: {
              type: 'string',
              enum: ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'],
            },
            priority: {
              type: 'string',
              enum: ['LOW', 'MEDIUM', 'HIGH', 'URGENT'],
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
            },
            dueDate: { type: 'string', format: 'date-time', nullable: true },
            completedAt: { type: 'string', format: 'date-time', nullable: true },
            isRecurring: { type: 'boolean' },
            recurrencePatternId: { type: 'string', nullable: true },
            parentTaskId: { type: 'string', nullable: true },
            createdAt: { type: 'string', format: 'date-time' },
            updatedAt: { type: 'string', format: 'date-time' },
          },
        },
        CreateTaskInput: {
          type: 'object',
          required: ['title', 'userId'],
          properties: {
            title: { type: 'string' },
            description: { type: 'string' },
            userId: { type: 'string' },
            priority: {
              type: 'string',
              enum: ['LOW', 'MEDIUM', 'HIGH', 'URGENT'],
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
            },
            dueDate: { type: 'string', format: 'date-time' },
          },
        },
        UpdateTaskInput: {
          type: 'object',
          properties: {
            title: { type: 'string' },
            description: { type: 'string' },
            priority: {
              type: 'string',
              enum: ['LOW', 'MEDIUM', 'HIGH', 'URGENT'],
            },
            tags: {
              type: 'array',
              items: { type: 'string' },
            },
            dueDate: { type: 'string', format: 'date-time' },
            status: {
              type: 'string',
              enum: ['PENDING', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED'],
            },
          },
        },
        Reminder: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            taskId: { type: 'string' },
            reminderTime: { type: 'string', format: 'date-time' },
            channels: {
              type: 'array',
              items: {
                type: 'string',
                enum: ['EMAIL', 'PUSH', 'SMS', 'IN_APP'],
              },
            },
            status: {
              type: 'string',
              enum: ['PENDING', 'SENT', 'FAILED', 'CANCELLED'],
            },
            sentAt: { type: 'string', format: 'date-time', nullable: true },
            createdAt: { type: 'string', format: 'date-time' },
            updatedAt: { type: 'string', format: 'date-time' },
          },
        },
        AuditLog: {
          type: 'object',
          properties: {
            id: { type: 'string', format: 'uuid' },
            userId: { type: 'string' },
            taskId: { type: 'string', nullable: true },
            operationType: {
              type: 'string',
              enum: ['CREATE', 'UPDATE', 'DELETE', 'COMPLETE'],
            },
            beforeState: { type: 'object', nullable: true },
            afterState: { type: 'object', nullable: true },
            timestamp: { type: 'string', format: 'date-time' },
            correlationId: { type: 'string' },
            metadata: { type: 'object' },
          },
        },
        Error: {
          type: 'object',
          properties: {
            error: { type: 'string' },
            message: { type: 'string' },
            details: { type: 'object' },
            stack: { type: 'string' },
          },
        },
      },
    },
    security: [
      {
        bearerAuth: [],
      },
    ],
  },
  apis: ['./src/api/routes/*.ts', './src/index.ts'],
};

export const swaggerSpec = swaggerJsdoc(options);
