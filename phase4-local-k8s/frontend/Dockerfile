# ===========================
# Phase 4 Frontend Dockerfile
# Next.js 16 + Node 20
# Render deployment ready
# ===========================

# ---------- STEP 1: Build Stage ----------
FROM node:20-alpine AS builder
WORKDIR /app

# Copy package.json and package-lock.json for dependency install
COPY package.json package-lock.json ./

# Install all dependencies (devDependencies required for build)
RUN npm ci

# Copy full source code
COPY . ./

# Build Next.js production assets
RUN npm run build

# ---------- STEP 2: Production Stage ----------
FROM node:20-alpine AS runner
WORKDIR /app

# Copy package.json and node_modules from builder
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules

# Copy Next.js build output and public folder
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public

# Set environment variables for Render
ENV NODE_ENV=production
ENV PORT=10000

# Expose the port Render expects
EXPOSE 10000

# Start the production server
CMD ["npx", "next", "start", "-p", "10000"]
