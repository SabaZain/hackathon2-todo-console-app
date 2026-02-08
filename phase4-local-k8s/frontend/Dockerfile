# Multi-stage build for Next.js frontend
# Node.js 20 for Next.js 16.x compatibility
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
# Install all dependencies (including devDependencies needed for build)
RUN npm ci

# Build the application
FROM node:20-alpine AS builder
WORKDIR /app
COPY . ./
COPY --from=deps /app/node_modules ./node_modules

# Set build-time environment variables for Next.js
ENV NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
ENV NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000
ENV NODE_ENV=production

RUN npm run build

# Production image - minimal runtime
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=10000

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy standalone build output properly
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone /app/standalone

# Set working directory to standalone folder
WORKDIR /app/standalone

USER nextjs

EXPOSE 10000

# Run the standalone server
CMD ["node", "server.js"]
