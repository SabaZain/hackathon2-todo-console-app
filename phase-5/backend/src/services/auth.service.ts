import { PrismaClient } from '@prisma/client';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { v4 as uuidv4 } from 'uuid';
import logger from '../logger';

const prisma = new PrismaClient();

export interface RegisterInput {
  email: string;
  password: string;
  name: string;
  timezone?: string;
}

export interface LoginInput {
  email: string;
  password: string;
}

export interface AuthResponse {
  user: {
    id: string;
    email: string;
    name: string;
    timezone: string;
  };
  token: string;
}

export class AuthService {
  private readonly JWT_SECRET = process.env.JWT_SECRET || 'phase5-secret-key-change-in-production';
  private readonly JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '7d';
  private readonly SALT_ROUNDS = 10;

  /**
   * Register a new user
   */
  async register(input: RegisterInput): Promise<AuthResponse> {
    const correlationId = uuidv4();

    try {
      // Check if user already exists
      const existingUser = await prisma.user.findUnique({
        where: { email: input.email },
      });

      if (existingUser) {
        throw new Error('User with this email already exists');
      }

      // Hash password
      const hashedPassword = await bcrypt.hash(input.password, this.SALT_ROUNDS);

      // Create user
      const user = await prisma.user.create({
        data: {
          email: input.email,
          password: hashedPassword,
          name: input.name,
          timezone: input.timezone || 'UTC',
        },
      });

      // Generate JWT token
      const token = this.generateToken({
        id: user.id,
        email: user.email,
        name: user.name,
      });

      logger.info('User registered successfully', {
        userId: user.id,
        email: user.email,
        correlationId,
      });

      return {
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          timezone: user.timezone,
        },
        token,
      };
    } catch (error) {
      logger.error('Registration failed:', error);
      throw error;
    }
  }

  /**
   * Login user
   */
  async login(input: LoginInput): Promise<AuthResponse> {
    const correlationId = uuidv4();

    try {
      // Find user by email
      const user = await prisma.user.findUnique({
        where: { email: input.email },
      });

      if (!user) {
        throw new Error('Invalid email or password');
      }

      // Verify password
      const isPasswordValid = await bcrypt.compare(input.password, user.password);

      if (!isPasswordValid) {
        throw new Error('Invalid email or password');
      }

      // Generate JWT token
      const token = this.generateToken({
        id: user.id,
        email: user.email,
        name: user.name,
      });

      logger.info('User logged in successfully', {
        userId: user.id,
        email: user.email,
        correlationId,
      });

      return {
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          timezone: user.timezone,
        },
        token,
      };
    } catch (error) {
      logger.error('Login failed:', error);
      throw error;
    }
  }

  /**
   * Get user profile
   */
  async getProfile(userId: string) {
    try {
      const user = await prisma.user.findUnique({
        where: { id: userId },
        select: {
          id: true,
          email: true,
          name: true,
          timezone: true,
          notificationPreferences: true,
          createdAt: true,
          updatedAt: true,
        },
      });

      if (!user) {
        throw new Error('User not found');
      }

      return user;
    } catch (error) {
      logger.error('Failed to get user profile:', error);
      throw error;
    }
  }

  /**
   * Update user profile
   */
  async updateProfile(userId: string, data: { name?: string; timezone?: string }) {
    try {
      const user = await prisma.user.update({
        where: { id: userId },
        data,
        select: {
          id: true,
          email: true,
          name: true,
          timezone: true,
          notificationPreferences: true,
          updatedAt: true,
        },
      });

      logger.info('User profile updated', { userId });

      return user;
    } catch (error) {
      logger.error('Failed to update user profile:', error);
      throw error;
    }
  }

  /**
   * Generate JWT token
   */
  private generateToken(payload: { id: string; email: string; name: string }): string {
    return jwt.sign(payload, this.JWT_SECRET, {
      expiresIn: this.JWT_EXPIRES_IN,
    } as jwt.SignOptions);
  }

  /**
   * Verify JWT token
   */
  verifyToken(token: string): { id: string; email: string; name: string } {
    try {
      return jwt.verify(token, this.JWT_SECRET) as {
        id: string;
        email: string;
        name: string;
      };
    } catch (error) {
      throw new Error('Invalid or expired token');
    }
  }
}

export const authService = new AuthService();
