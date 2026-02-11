import { Router, Response } from 'express';
import { reminderService } from '../../services/reminder.service';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import { validateRequest, validateQuery, validateParams } from '../middleware/validation.middleware';
import Joi from 'joi';
import { ReminderChannel, ReminderStatus } from '@prisma/client';

const router = Router();

// Validation schemas
const createReminderSchema = Joi.object({
  taskId: Joi.string().uuid().required(),
  reminderTime: Joi.date().iso().required().greater('now'),
  channels: Joi.array()
    .items(Joi.string().valid(...Object.values(ReminderChannel)))
    .min(1)
    .required(),
});

const updateReminderSchema = Joi.object({
  reminderTime: Joi.date().iso().optional().greater('now'),
  channels: Joi.array()
    .items(Joi.string().valid(...Object.values(ReminderChannel)))
    .min(1)
    .optional(),
  status: Joi.string()
    .valid(...Object.values(ReminderStatus))
    .optional(),
});

const reminderIdSchema = Joi.object({
  id: Joi.string().uuid().required(),
});

const taskIdSchema = Joi.object({
  taskId: Joi.string().uuid().required(),
});

const getRemindersQuerySchema = Joi.object({
  status: Joi.string()
    .valid(...Object.values(ReminderStatus))
    .optional(),
});

/**
 * @swagger
 * /api/reminders:
 *   post:
 *     summary: Create a new reminder for a task
 *     tags: [Reminders]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - taskId
 *               - reminderTime
 *               - channels
 *             properties:
 *               taskId:
 *                 type: string
 *                 format: uuid
 *               reminderTime:
 *                 type: string
 *                 format: date-time
 *               channels:
 *                 type: array
 *                 items:
 *                   type: string
 *                   enum: [EMAIL, PUSH, SMS, IN_APP]
 *     responses:
 *       201:
 *         description: Reminder created successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Reminder'
 *                 message:
 *                   type: string
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.post(
  '/',
  authMiddleware,
  validateRequest(createReminderSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const reminder = await reminderService.createReminder({
        ...req.body,
        userId: req.user!.id,
      });

      res.status(201).json({
        success: true,
        data: reminder,
        message: 'Reminder created successfully',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to create reminder',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/reminders:
 *   get:
 *     summary: Get all reminders for the authenticated user
 *     tags: [Reminders]
 *     parameters:
 *       - in: query
 *         name: status
 *         schema:
 *           type: string
 *           enum: [PENDING, SENT, FAILED, CANCELLED]
 *         description: Filter by reminder status
 *     responses:
 *       200:
 *         description: List of reminders
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
 *                     $ref: '#/components/schemas/Reminder'
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
  validateQuery(getRemindersQuerySchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const status = req.query.status as ReminderStatus | undefined;
      const reminders = await reminderService.getUserReminders(req.user!.id, status);

      res.json({
        success: true,
        data: reminders,
        count: reminders.length,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get reminders',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/reminders/{id}:
 *   get:
 *     summary: Get a specific reminder by ID
 *     tags: [Reminders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Reminder ID
 *     responses:
 *       200:
 *         description: Reminder details
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Reminder'
 *       404:
 *         description: Reminder not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.get(
  '/:id',
  authMiddleware,
  validateParams(reminderIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const reminder = await reminderService.getReminderById(req.params.id, req.user!.id);

      if (!reminder) {
        res.status(404).json({
          success: false,
          error: 'Reminder not found',
        });
        return;
      }

      res.json({
        success: true,
        data: reminder,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get reminder',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/reminders/tasks/{taskId}/reminders:
 *   get:
 *     summary: Get all reminders for a specific task
 *     tags: [Reminders]
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
 *         description: List of reminders for the task
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
 *                     $ref: '#/components/schemas/Reminder'
 *                 count:
 *                   type: integer
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.get(
  '/tasks/:taskId/reminders',
  authMiddleware,
  validateParams(taskIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const reminders = await reminderService.getTaskReminders(
        req.params.taskId,
        req.user!.id
      );

      res.json({
        success: true,
        data: reminders,
        count: reminders.length,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get task reminders',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/reminders/{id}:
 *   put:
 *     summary: Update a reminder
 *     tags: [Reminders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Reminder ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               reminderTime:
 *                 type: string
 *                 format: date-time
 *               channels:
 *                 type: array
 *                 items:
 *                   type: string
 *                   enum: [EMAIL, PUSH, SMS, IN_APP]
 *               status:
 *                 type: string
 *                 enum: [PENDING, SENT, FAILED, CANCELLED]
 *     responses:
 *       200:
 *         description: Reminder updated successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                 data:
 *                   $ref: '#/components/schemas/Reminder'
 *                 message:
 *                   type: string
 *       404:
 *         description: Reminder not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.put(
  '/:id',
  authMiddleware,
  validateParams(reminderIdSchema),
  validateRequest(updateReminderSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const reminder = await reminderService.updateReminder(
        req.params.id,
        req.user!.id,
        req.body
      );

      res.json({
        success: true,
        data: reminder,
        message: 'Reminder updated successfully',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to update reminder',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/reminders/{id}:
 *   delete:
 *     summary: Delete a reminder
 *     tags: [Reminders]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *           format: uuid
 *         description: Reminder ID
 *     responses:
 *       200:
 *         description: Reminder deleted successfully
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
 *         description: Reminder not found
 *       401:
 *         description: Unauthorized
 *       500:
 *         description: Server error
 */
router.delete(
  '/:id',
  authMiddleware,
  validateParams(reminderIdSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      await reminderService.deleteReminder(req.params.id, req.user!.id);

      res.json({
        success: true,
        message: 'Reminder deleted successfully',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to delete reminder',
        message: error.message,
      });
    }
  }
);

export default router;
