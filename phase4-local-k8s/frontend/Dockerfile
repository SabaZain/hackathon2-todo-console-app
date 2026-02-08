# Multi-stage build for Next.js frontend
# Updated to Node.js 20 for Next.js 16.x compatibility (requires Node >= 20.9.0)
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json ./
# Install ALL dependencies (including devDependencies needed for build)
RUN npm ci

# Build the application
FROM node:20-alpine AS builder
WORKDIR /app
COPY . ./
COPY --from=deps /app/node_modules ./node_modules
RUN npm run build

# Production image - minimal runtime dependencies only
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy necessary files from builder
COPY --from=builder --chown=nextjs:nodejs /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./package.json

# Copy standalone build output
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

ENV PORT=10000
EXPOSE 10000

CMD ["node", "server.js"]
