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
 * POST /api/reminders
 * Create a new reminder for a task
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
 * GET /api/reminders
 * Get all reminders for the authenticated user
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
 * GET /api/reminders/:id
 * Get a specific reminder by ID
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
 * GET /api/tasks/:taskId/reminders
 * Get all reminders for a specific task
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
 * PUT /api/reminders/:id
 * Update a reminder
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
 * DELETE /api/reminders/:id
 * Delete a reminder
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
