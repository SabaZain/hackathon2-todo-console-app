import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config({ path: path.join(__dirname, '../../.env') });

interface Config {
  port: number;
  nodeEnv: string;
  databaseUrl: string;
  jwtSecret: string;
  jwtExpiresIn: string;
  kafkaBrokers: string;
  daprHttpPort: number;
  daprGrpcPort: number;
  corsOrigin: string;
  logLevel: string;
}

const config: Config = {
  port: parseInt(process.env.PORT || '3001', 10),
  nodeEnv: process.env.NODE_ENV || 'development',
  databaseUrl: process.env.DATABASE_URL || 'postgresql://phase5_user:phase5_password@localhost:5432/phase5_todo',
  jwtSecret: process.env.JWT_SECRET || 'phase5-secret-key-change-in-production',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '7d',
  kafkaBrokers: process.env.KAFKA_BROKERS || 'localhost:9092',
  daprHttpPort: parseInt(process.env.DAPR_HTTP_PORT || '3500', 10),
  daprGrpcPort: parseInt(process.env.DAPR_GRPC_PORT || '50001', 10),
  corsOrigin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  logLevel: process.env.LOG_LEVEL || 'info',
};

export default config;
