import { Router, Response } from 'express';
import { taskService } from '../../services/task.service';
import { recurringTaskService } from '../../services/recurring-task.service';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import { validateRequest, validateQuery, validateParams } from '../middleware/validation.middleware';
import Joi from 'joi';
import { TaskStatus, TaskPriority } from '@prisma/client';

const router = Router();

// Validation schemas
const createTaskSchema = Joi.object({
  title: Joi.string().required().min(1).max(500),
  description: Joi.string().optional().max(5000),
  priority: Joi.string().valid(...Object.values(TaskPriority)).optional(),
  tags: Joi.array().items(Joi.string().max(50)).optional(),
  dueDate: Joi.date().iso().optional(),
});

const createRecurringTaskSchema = Joi.object({
  title: Joi.string().required().min(1).max(500),
  description: Joi.string().optional().max(5000),
  priority: Joi.string().valid(...Object.values(TaskPriority)).optional(),
  tags: Joi.array().items(Joi.string().max(50)).optional(),
  dueDate: Joi.date().iso().optional(),
  recurrencePattern: Joi.object({
    frequency: Joi.string().required().valid('DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY', 'CUSTOM'),
    interval: Joi.number().integer().min(1).required(),
    dayOfWeek: Joi.number().integer().min(0).max(6).optional(),
    dayOfMonth: Joi.number().integer().min(1).max(31).optional(),
    endDate: Joi.date().iso().optional(),
    occurrencesCount: Joi.number().integer().min(1).optional(),
  }).required(),
});

const updateTaskSchema = Joi.object({
  title: Joi.string().optional().min(1).max(500),
  description: Joi.string().optional().max(5000),
  priority: Joi.string().valid(...Object.values(TaskPriority)).optional(),
  tags: Joi.array().items(Joi.string().max(50)).optional(),
  dueDate: Joi.date().iso().optional(),
  status: Joi.string().valid(...Object.values(TaskStatus)).optional(),
});

const taskIdSchema = Joi.object({
  id: Joi.string().uuid().required(),
});

const getTasksQuerySchema = Joi.object({
  status: Joi.string().valid(...Object.values(TaskStatus)).optional(),
  priority: Joi.string().valid(...Object.values(TaskPriority)).optional(),
  tags: Joi.string().optional(), // Comma-separated tags
  search: Joi.string().optional().max(200),
  dueDateFrom: Joi.date().iso().optional(),
  dueDateTo: Joi.date().iso().optional(),
});

/**
 * POST /api/tasks
 * Create a new task
 */
router.post(
  '/',
  authMiddleware,
  validateRequest(createTaskSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const task = await taskService.createTask({
        ...req.body,
        userId: req.user!.id,
      });

      res.status(201).json({
        success: true,
        data: task,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to create task',
        message: error.message,
      });
    }
  }
);

/**
 * POST /api/tasks/recurring
 * Create a new recurring task
 */
router.post(
  '/recurring',
  authMiddleware,
  validateRequest(createRecurringTaskSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const task = await recurringTaskService.createRecurringTask({
        ...req.body,
        userId: req.user!.id,
      });

      res.status(201).json({
        success: true,
        data: task,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to create recurring task',
        message: error.message,
      });
    }
  }
);

/**
 * GET /api/tasks
 * Get all tasks for the authenticated user
 */
router.get(
  '/',
  authMiddleware,
  validateQuery(getTasksQuerySchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const filters: any = {
        userId: req.user!.id,
        status: req.query.status as any,
        priority: req.query.priority as any,
        search: req.query.search as string,
        dueDateFrom: req.query.dueDateFrom ? new Date(req.query.dueDateFrom as string) : undefined,
        dueDateTo: req.query.dueDateTo ? new Date(req.query.dueDateTo as string) : undefined,
      };

      // Parse comma-separated tags
      if (req.query.tags) {
        filters.tags = (req.query.tags as string).split(',').map((t) => t.trim());
      }

      const tasks = await taskService.getTasks(filters);

      res.json({
        success: true,
        data: tasks,
        count: tasks.length,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get tasks',
        message: error.message,
      });
    }
  }
);

/**
 * GET /api/tasks/:id
 * Get a specific task by ID
 */
router.get(
  '/:id',
  authMiddleware,
  validateParams(taskIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const task = await taskService.getTaskById(req.params.id, req.user!.id);

      if (!task) {
        res.status(404).json({
          success: false,
          error: 'Task not found',
        });
        return;
      }

      res.json({
        success: true,
        data: task,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get task',
        message: error.message,
      });
    }
  }
);

/**
 * GET /api/tasks/:id/occurrences
 * Get all occurrences of a recurring task
 */
router.get(
  '/:id/occurrences',
  authMiddleware,
  validateParams(taskIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const occurrences = await recurringTaskService.getTaskOccurrences(req.params.id);

      res.json({
        success: true,
        data: occurrences,
        count: occurrences.length,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get task occurrences',
        message: error.message,
      });
    }
  }
);

/**
 * PUT /api/tasks/:id
 * Update a task
 */
router.put(
  '/:id',
  authMiddleware,
  validateParams(taskIdSchema),
  validateRequest(updateTaskSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const task = await taskService.updateTask(req.params.id, req.user!.id, req.body);

      res.json({
        success: true,
        data: task,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to update task',
        message: error.message,
      });
    }
  }
);

/**
 * POST /api/tasks/:id/complete
 * Mark a task as complete (and generate next occurrence if recurring)
 */
router.post(
  '/:id/complete',
  authMiddleware,
  validateParams(taskIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const task = await taskService.completeTask(req.params.id, req.user!.id);

      res.json({
        success: true,
        data: task,
        message: task.isRecurring ? 'Task completed and next occurrence generated' : 'Task completed',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to complete task',
        message: error.message,
      });
    }
  }
);

/**
 * DELETE /api/tasks/:id
 * Delete a task
 */
router.delete(
  '/:id',
  authMiddleware,
  validateParams(taskIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      await taskService.deleteTask(req.params.id, req.user!.id);

      res.json({
        success: true,
        message: 'Task deleted successfully',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to delete task',
        message: error.message,
      });
    }
  }
);

export default router;
