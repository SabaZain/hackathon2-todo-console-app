---
id: PHR-0002
title: Update Frontend to Use Render Backend in Production While Keeping Localhost for Development
date: 2026-01-19
author: Claude
status: completed
tags: ["frontend", "backend", "render", "api", "configuration", "environment"]
---

# Update Frontend to Use Render Backend in Production While Keeping Localhost for Development

## Original Request
Update the frontend to use the new backend deployed at "https://hackathon2-todo-backend.onrender.com", without breaking local development. The local development environment should continue using http://localhost:8000.

## Changes Made

### 1. Environment Variables Update
- Updated `.env.local` file with:
  - `NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000`
  - `NEXT_PUBLIC_API_BASE_URL_PROD=https://hackathon2-todo-backend.onrender.com`

### 2. API Client Update
- Modified `lib/api.ts` to use conditional API_BASE_URL based on NODE_ENV:
  ```typescript
  const API_BASE_URL = process.env.NODE_ENV === 'production'
    ? process.env.NEXT_PUBLIC_API_BASE_URL_PROD
    : process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL;
  ```

## Technical Details

- In development (`NODE_ENV !== 'production'`): Uses `NEXT_PUBLIC_API_BASE_URL_LOCAL` (http://localhost:8000)
- In production (`NODE_ENV === 'production'`): Uses `NEXT_PUBLIC_API_BASE_URL_PROD` (https://hackathon2-todo-backend.onrender.com)
- All API calls in the frontend now use the dynamic API_BASE_URL variable
- Maintains backward compatibility for local development

## Files Modified
- `.env.local`: Updated environment variables
- `lib/api.ts`: Updated API client to use conditional environment-based URL

## Testing
- Local development continues to work with localhost:8000 backend
- Production deployment will use Render backend URL
- All existing API functionality preserved

## Deployment Impact
- Frontend deployed at https://hackathon2-todo-console-app-qu73.vercel.app/ will now connect to Render backend
- Local development environment remains unchanged
- No breaking changes to existing functionality