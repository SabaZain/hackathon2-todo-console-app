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
 * @swagger
 * /api/tasks:
 *   post:
 *     summary: Create a new task
 *     tags: [Tasks]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/CreateTaskInput'
 *     responses:
 *       201:
 *         description: Task created successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Task'
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/recurring:
 *   post:
 *     summary: Create a new recurring task
 *     tags: [Tasks]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - title
 *               - recurrencePattern
 *             properties:
 *               title:
 *                 type: string
 *               description:
 *                 type: string
 *               priority:
 *                 type: string
 *                 enum: [LOW, MEDIUM, HIGH, URGENT]
 *               tags:
 *                 type: array
 *                 items:
 *                   type: string
 *               dueDate:
 *                 type: string
 *                 format: date-time
 *               recurrencePattern:
 *                 type: object
 *                 required:
 *                   - frequency
 *                   - interval
 *                 properties:
 *                   frequency:
 *                     type: string
 *                     enum: [DAILY, WEEKLY, MONTHLY, YEARLY, CUSTOM]
 *                   interval:
 *                     type: integer
 *                     minimum: 1
 *                   dayOfWeek:
 *                     type: integer
 *                     minimum: 0
 *                     maximum: 6
 *                   dayOfMonth:
 *                     type: integer
 *                     minimum: 1
 *                     maximum: 31
 *                   endDate:
 *                     type: string
 *                     format: date-time
 *                   occurrencesCount:
 *                     type: integer
 *                     minimum: 1
 *     responses:
 *       201:
 *         description: Recurring task created successfully
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks:
 *   get:
 *     summary: Get all tasks for the authenticated user
 *     tags: [Tasks]
 *     parameters:
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [PENDING, IN_PROGRESS, COMPLETED, CANCELLED]
 *         description: Filter by task status
 *       - in: query
 *         name: priority
 *         schema:
 *           type: string
 *           enum: [LOW, MEDIUM, HIGH, URGENT]
 *         description: Filter by task priority
 *       - in: query
 *         name: tags
 *         schema:
 *           type: string
 *         description: Comma-separated list of tags
 *       - in: query
 *         name: search
 *         schema:
 *           type: string
 *         description: Search in title and description
 *       - in: query
 *         name: dueDateFrom
 *         schema:
 *           type: string
 *           format: date-time
 *         description: Filter tasks due after this date
 *       - in: query
 *         name: dueDateTo
 *         schema:
 *           type: string
 *           format: date-time
 *         description: Filter tasks due before this date
 *     responses:
 *       200:
 *         description: List of tasks
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
 *                     $ref: '#/components/schemas/Task'
 *                 count:
 *                   type: integer
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/{id}:
 *   get:
 *     summary: Get a specific task by ID
 *     tags: [Tasks]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     responses:
 *       200:
 *         description: Task details
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Task'
 *       404:
 *         description: Task not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/{id}/occurrences:
 *   get:
 *     summary: Get all occurrences of a recurring task
 *     tags: [Tasks]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     responses:
 *       200:
 *         description: List of task occurrences
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
 *                     $ref: '#/components/schemas/Task'
 *                 count:
 *                   type: integer
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/{id}:
 *   put:
 *     summary: Update a task
 *     tags: [Tasks]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/UpdateTaskInput'
 *     responses:
 *       200:
 *         description: Task updated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Task'
 *       404:
 *         description: Task not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/{id}/complete:
 *   post:
 *     summary: Mark a task as complete
 *     description: Marks a task as complete. If the task is recurring, automatically generates the next occurrence.
 *     tags: [Tasks]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     responses:
 *       200:
 *         description: Task completed successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Task'
 *                 message:
 *                   type: string
 *       404:
 *         description: Task not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
 * @swagger
 * /api/tasks/{id}:
 *   delete:
 *     summary: Delete a task
 *     tags: [Tasks]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Task ID
 *     responses:
 *       200:
 *         description: Task deleted successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 message:
 *                   type: string
 *       404:
 *         description: Task not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
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
