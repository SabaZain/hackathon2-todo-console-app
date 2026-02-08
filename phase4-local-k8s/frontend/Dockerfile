# -------------------------
# Phase 4 Frontend Dockerfile
# Multi-stage build for Next.js 16 (Node 20 compatible)
# -------------------------

# Stage 1: Install dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

# Stage 2: Build application
FROM node:20-alpine AS builder
WORKDIR /app
COPY . ./
COPY --from=deps /app/node_modules ./node_modules

# Set build-time environment variables
ENV NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
ENV NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000
ENV NODE_ENV=production

RUN npm run build

# Stage 3: Production runtime image
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production
ENV PORT=10000

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy public + package.json from builder
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Copy standalone build + node_modules into /app/standalone
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./standalone
COPY --from=builder /app/node_modules ./standalone/node_modules

# Switch to non-root user
USER nextjs

# Expose the port Render will use
EXPOSE 10000

# Start server from standalone folder
WORKDIR /app/standalone
CMD ["node", "server.js"]
