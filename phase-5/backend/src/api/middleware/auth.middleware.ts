import { Request, Response, NextFunction } from 'express';
import jwt from 'jsonwebtoken';
import logger from '../../logger';

export interface AuthRequest extends Request {
  user?: {
    id: string;
    email: string;
    name: string;
  };
}

export const authMiddleware = async (
  req: AuthRequest,
  res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({
        error: 'Unauthorized',
        message: 'No token provided',
      });
      return;
    }

    const token = authHeader.substring(7);
    const jwtSecret = process.env.JWT_SECRET || 'phase5-secret-key-change-in-production';

    // Development mode: Allow demo token
    if (process.env.NODE_ENV === 'development' && token === 'demo-token') {
      req.user = {
        id: 'demo-user',
        email: 'demo@example.com',
        name: 'Demo User',
      };
      next();
      return;
    }

    try {
      const decoded = jwt.verify(token, jwtSecret) as {
        id: string;
        email: string;
        name: string;
      };

      req.user = decoded;
      next();
    } catch (error) {
      logger.error('JWT verification failed:', error);
      res.status(401).json({
        error: 'Unauthorized',
        message: 'Invalid or expired token',
      });
    }
  } catch (error) {
    logger.error('Auth middleware error:', error);
    res.status(500).json({
      error: 'Internal Server Error',
      message: 'Authentication failed',
    });
  }
};

export const optionalAuthMiddleware = async (
  req: AuthRequest,
  _res: Response,
  next: NextFunction
): Promise<void> => {
  try {
    const authHeader = req.headers.authorization;

    if (authHeader && authHeader.startsWith('Bearer ')) {
      const token = authHeader.substring(7);
      const jwtSecret = process.env.JWT_SECRET || 'phase5-secret-key-change-in-production';

      try {
        const decoded = jwt.verify(token, jwtSecret) as {
          id: string;
          email: string;
          name: string;
        };
        req.user = decoded;
      } catch (error) {
        logger.warn('Optional auth: Invalid token provided');
      }
    }

    next();
  } catch (error) {
    logger.error('Optional auth middleware error:', error);
    next();
  }
};
