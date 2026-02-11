import { Request, Response, NextFunction } from 'express';
import Joi from 'joi';
import logger from '../../logger';

export const validateRequest = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error, value } = schema.validate(req.body, {
      abortEarly: false,
      stripUnknown: true,
    });

    if (error) {
      const errors = error.details.map((detail) => ({
        field: detail.path.join('.'),
        message: detail.message,
      }));

      logger.warn('Validation failed:', { errors, body: req.body });

      res.status(400).json({
        error: 'Validation Error',
        message: 'Request validation failed',
        details: errors,
      });
      return;
    }

    req.body = value;
    next();
  };
};

export const validateQuery = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error, value } = schema.validate(req.query, {
      abortEarly: false,
      stripUnknown: true,
    });

    if (error) {
      const errors = error.details.map((detail) => ({
        field: detail.path.join('.'),
        message: detail.message,
      }));

      logger.warn('Query validation failed:', { errors, query: req.query });

      res.status(400).json({
        error: 'Validation Error',
        message: 'Query validation failed',
        details: errors,
      });
      return;
    }

    req.query = value;
    next();
  };
};

export const validateParams = (schema: Joi.ObjectSchema) => {
  return (req: Request, res: Response, next: NextFunction): void => {
    const { error, value } = schema.validate(req.params, {
      abortEarly: false,
      stripUnknown: true,
    });

    if (error) {
      const errors = error.details.map((detail) => ({
        field: detail.path.join('.'),
        message: detail.message,
      }));

      logger.warn('Params validation failed:', { errors, params: req.params });

      res.status(400).json({
        error: 'Validation Error',
        message: 'Path parameter validation failed',
        details: errors,
      });
      return;
    }

    req.params = value;
    next();
  };
};
