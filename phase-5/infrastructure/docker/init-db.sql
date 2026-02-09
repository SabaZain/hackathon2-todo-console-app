-- Phase 5 Database Initialization Script
-- This script runs automatically when the PostgreSQL container starts

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create audit schema for separation
CREATE SCHEMA IF NOT EXISTS audit;

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE phase5_todo TO phase5_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO phase5_user;
GRANT ALL PRIVILEGES ON SCHEMA audit TO phase5_user;

-- Create indexes for full-text search (will be used by Prisma)
-- Additional indexes will be created by Prisma migrations

COMMENT ON DATABASE phase5_todo IS 'Phase 5 Todo Application Database - Event-Driven Architecture';
