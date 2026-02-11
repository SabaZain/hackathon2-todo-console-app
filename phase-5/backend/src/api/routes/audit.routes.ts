import { Router, Response } from 'express';
import { PrismaClient, AuditOperationType } from '@prisma/client';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import { validateQuery } from '../middleware/validation.middleware';
import Joi from 'joi';
import logger from '../../config/logger';

const router = Router();
const prisma = new PrismaClient();

// Validation schemas
const getAuditLogsQuerySchema = Joi.object({
  taskId: Joi.string().uuid().optional(),
  operationType: Joi.string()
    .valid(...Object.values(AuditOperationType))
    .optional(),
  startDate: Joi.date().iso().optional(),
  endDate: Joi.date().iso().optional(),
  limit: Joi.number().integer().min(1).max(100).optional().default(50),
  offset: Joi.number().integer().min(0).optional().default(0),
});

/**
 * @swagger
 * /api/audit:
 *   get:
 *     summary: Get audit logs for the authenticated user
 *     tags: [Audit]
 *     parameters:
 *       - in: query
 *         name: taskId
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Filter by task ID
 *       - in: query
 *         name: operationType
 *         schema:
 *           type: string
 *           enum: [CREATE, UPDATE, DELETE, COMPLETE]
 *         description: Filter by operation type
 *       - in: query
 *         name: startDate
 *         schema:
 *           type: string
 *           format: date-time
 *         description: Filter logs after this date
 *       - in: query
 *         name: endDate
 *         schema:
 *           type: string
 *           format: date-time
 *         description: Filter logs before this date
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           minimum: 1
 *           maximum: 100
 *           default: 50
 *         description: Number of records to return
 *       - in: query
 *         name: offset
 *         schema:
 *           type: integer
 *           minimum: 0
 *           default: 0
 *         description: Number of records to skip
 *     responses:
 *       200:
 *         description: List of audit logs
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/AuditLog'
 *                 pagination:
 *                   type: object
 *                   properties:
 *                     total:
 *                       type: integer
 *                     limit:
 *                       type: integer
 *                     offset:
 *                       type: integer
 *                     hasMore:
 *                       type: boolean
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.get(
  '/',
  authMiddleware,
  validateQuery(getAuditLogsQuerySchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const {
        taskId,
        operationType,
        startDate,
        endDate,
        limit = 50,
        offset = 0,
      } = req.query;

      const where: any = {
        userId: req.user!.id,
      };

      if (taskId) {
        where.taskId = taskId as string;
      }

      if (operationType) {
        where.operationType = operationType as AuditOperationType;
      }

      if (startDate || endDate) {
        where.timestamp = {};
        if (startDate) {
          where.timestamp.gte = new Date(startDate as string);
        }
        if (endDate) {
          where.timestamp.lte = new Date(endDate as string);
        }
      }

      // Get total count
      const total = await prisma.auditLog.count({ where });

      // Get audit logs
      const auditLogs = await prisma.auditLog.findMany({
        where,
        include: {
          task: {
            select: {
              id: true,
              title: true,
              status: true,
            },
          },
        },
        orderBy: {
          timestamp: 'desc',
        },
        take: Number(limit),
        skip: Number(offset),
      });

      res.json({
        success: true,
        data: auditLogs,
        pagination: {
          total,
          limit: Number(limit),
          offset: Number(offset),
          hasMore: Number(offset) + auditLogs.length < total,
        },
      });
    } catch (error: any) {
      logger.error('Failed to get audit logs:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get audit logs',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/audit/task/{taskId}:
 *   get:
 *     summary: Get audit logs for a specific task
 *     tags: [Audit]
 *     parameters:
 *       - in: path
 *         name: taskId
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     responses:
 *       200:
 *         description: List of audit logs for the task
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/AuditLog'
 *                 count:
 *                   type: integer
 *       404:
 *         description: Task not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.get(
  '/task/:taskId',
  authMiddleware,
  async (req: AuthRequest, res: Response) => {
    try {
      const { taskId } = req.params;

      // Verify task belongs to user
      const task = await prisma.task.findFirst({
        where: {
          id: taskId,
          userId: req.user!.id,
        },
      });

      if (!task) {
        res.status(404).json({
          success: false,
          error: 'Task not found',
        });
        return;
      }

      // Get audit logs for the task
      const auditLogs = await prisma.auditLog.findMany({
        where: {
          taskId,
          userId: req.user!.id,
        },
        orderBy: {
          timestamp: 'desc',
        },
      });

      res.json({
        success: true,
        data: auditLogs,
        count: auditLogs.length,
      });
    } catch (error: any) {
      logger.error('Failed to get task audit logs:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get task audit logs',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/audit/stats:
 *   get:
 *     summary: Get audit statistics for the authenticated user
 *     tags: [Audit]
 *     responses:
 *       200:
 *         description: Audit statistics
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   type: object
 *                   properties:
 *                     totalOperations:
 *                       type: integer
 *                       description: Total number of operations
 *                     recentActivity:
 *                       type: integer
 *                       description: Number of operations in the last 7 days
 *                     operationCounts:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           operationType:
 *                             type: string
 *                             enum: [CREATE, UPDATE, DELETE, COMPLETE]
 *                           count:
 *                             type: integer
 *                     mostActiveTasks:
 *                       type: array
 *                       items:
 *                         type: object
 *                         properties:
 *                           taskId:
 *                             type: string
 *                           count:
 *                             type: integer
 *                           task:
 *                             type: object
 *                             properties:
 *                               id:
 *                                 type: string
 *                               title:
 *                                 type: string
 *                               status:
 *                                 type: string
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.get(
  '/stats',
  authMiddleware,
  async (req: AuthRequest, res: Response) => {
    try {
      const userId = req.user!.id;

      // Get operation type counts
      const operationCounts = await prisma.auditLog.groupBy({
        by: ['operationType'],
        where: { userId },
        _count: {
          operationType: true,
        },
      });

      // Get total count
      const totalOperations = await prisma.auditLog.count({
        where: { userId },
      });

      // Get recent activity (last 7 days)
      const sevenDaysAgo = new Date();
      sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);

      const recentActivity = await prisma.auditLog.count({
        where: {
          userId,
          timestamp: {
            gte: sevenDaysAgo,
          },
        },
      });

      // Get most active tasks
      const mostActiveTasks = await prisma.auditLog.groupBy({
        by: ['taskId'],
        where: {
          userId,
          taskId: { not: null },
        },
        _count: {
          taskId: true,
        },
        orderBy: {
          _count: {
            taskId: 'desc',
          },
        },
        take: 5,
      });

      // Get task details for most active tasks
      const taskIds = mostActiveTasks
        .map((t) => t.taskId)
        .filter((id): id is string => id !== null);

      const tasks = await prisma.task.findMany({
        where: {
          id: { in: taskIds },
        },
        select: {
          id: true,
          title: true,
          status: true,
        },
      });

      const mostActiveTasksWithDetails = mostActiveTasks.map((item) => ({
        taskId: item.taskId,
        count: item._count.taskId,
        task: tasks.find((t) => t.id === item.taskId),
      }));

      res.json({
        success: true,
        data: {
          totalOperations,
          recentActivity,
          operationCounts: operationCounts.map((item) => ({
            operationType: item.operationType,
            count: item._count.operationType,
          })),
          mostActiveTasks: mostActiveTasksWithDetails,
        },
      });
    } catch (error: any) {
      logger.error('Failed to get audit stats:', error);
      res.status(500).json({
        success: false,
        error: 'Failed to get audit stats',
        message: error.message,
      });
    }
  }
);

export default router;
