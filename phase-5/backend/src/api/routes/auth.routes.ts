import { Router, Response } from 'express';
import { authService } from '../../services/auth.service';
import { authMiddleware, AuthRequest } from '../middleware/auth.middleware';
import { validateRequest } from '../middleware/validation.middleware';
import Joi from 'joi';

const router = Router();

// Validation schemas
const registerSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).required(),
  name: Joi.string().min(2).max(100).required(),
  timezone: Joi.string().optional(),
});

const loginSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().required(),
});

const updateProfileSchema = Joi.object({
  name: Joi.string().min(2).max(100).optional(),
  timezone: Joi.string().optional(),
});

/**
 * @swagger
 * /api/auth/register:
 *   post:
 *     summary: Register a new user
 *     tags: [Authentication]
 *     security: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *               - name
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *               password:
 *                 type: string
 *                 minLength: 8
 *               name:
 *                 type: string
 *               timezone:
 *                 type: string
 *                 default: UTC
 *     responses:
 *       201:
 *         description: User registered successfully
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
 *                     user:
 *                       type: object
 *                       properties:
 *                         id:
 *                           type: string
 *                         email:
 *                           type: string
 *                         name:
 *                           type: string
 *                         timezone:
 *                           type: string
 *                     token:
 *                       type: string
 *       400:
 *         description: Invalid input or user already exists
 */
router.post(
  '/register',
  validateRequest(registerSchema),
  async (req, res: Response) => {
    try {
      const result = await authService.register(req.body);

      res.status(201).json({
        success: true,
        data: result,
        message: 'User registered successfully',
      });
    } catch (error: any) {
      res.status(400).json({
        success: false,
        error: 'Registration failed',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/auth/login:
 *   post:
 *     summary: Login user
 *     tags: [Authentication]
 *     security: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             required:
 *               - email
 *               - password
 *             properties:
 *               email:
 *                 type: string
 *                 format: email
 *               password:
 *                 type: string
 *     responses:
 *       200:
 *         description: Login successful
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
 *                     user:
 *                       type: object
 *                     token:
 *                       type: string
 *       401:
 *         description: Invalid credentials
 */
router.post(
  '/login',
  validateRequest(loginSchema),
  async (req, res: Response) => {
    try {
      const result = await authService.login(req.body);

      res.json({
        success: true,
        data: result,
        message: 'Login successful',
      });
    } catch (error: any) {
      res.status(401).json({
        success: false,
        error: 'Login failed',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/auth/profile:
 *   get:
 *     summary: Get user profile
 *     tags: [Authentication]
 *     responses:
 *       200:
 *         description: User profile
 *       401:
 *         description: Unauthorized
 */
router.get(
  '/profile',
  authMiddleware,
  async (req: AuthRequest, res: Response) => {
    try {
      const profile = await authService.getProfile(req.user!.id);

      res.json({
        success: true,
        data: profile,
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to get profile',
        message: error.message,
      });
    }
  }
);

/**
 * @swagger
 * /api/auth/profile:
 *   put:
 *     summary: Update user profile
 *     tags: [Authentication]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               timezone:
 *                 type: string
 *     responses:
 *       200:
 *         description: Profile updated
 *       401:
 *         description: Unauthorized
 */
router.put(
  '/profile',
  authMiddleware,
  validateRequest(updateProfileSchema),
  async (req: AuthRequest, res: Response) => {
    try {
      const profile = await authService.updateProfile(req.user!.id, req.body);

      res.json({
        success: true,
        data: profile,
        message: 'Profile updated successfully',
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        error: 'Failed to update profile',
        message: error.message,
      });
    }
  }
);

export default router;
