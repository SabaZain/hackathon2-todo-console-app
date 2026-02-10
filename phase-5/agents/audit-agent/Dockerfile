# Multi-stage build for AuditAgent
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && \
    npm cache clean --force

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install all dependencies
RUN npm ci

# Copy source code
COPY src ./src

# Build TypeScript
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 agent

# Copy dependencies from deps stage
COPY --from=deps --chown=agent:nodejs /app/node_modules ./node_modules

# Copy built application from builder stage
COPY --from=builder --chown=agent:nodejs /app/dist ./dist
COPY --from=builder --chown=agent:nodejs /app/package*.json ./

# Set environment variables
ENV NODE_ENV=production

# Switch to non-root user
USER agent

# Health check (check if process is running)
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
  CMD ps aux | grep -v grep | grep node || exit 1

# Start agent
CMD ["node", "dist/index.js"]
