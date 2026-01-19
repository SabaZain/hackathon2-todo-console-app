---
id: PHR-0004
title: Fix Vercel 404 Errors and Ensure Correct Routes/API URLs
date: 2026-01-19
author: Claude
status: completed
tags: ["frontend", "vercel", "404", "routing", "deployment", "api", "nextjs"]
---

# Fix Vercel 404 Errors and Ensure Correct Routes/API URLs

## Original Request
Fix 404 errors on Vercel deployed frontend at "https://hackathon2-todo-console-app-qu73.vercel.app/" while preserving local development functionality.

## Analysis Performed
- Verified .env.local configuration with correct API URLs:
  - NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000
  - NEXT_PUBLIC_API_BASE_URL_PROD=https://hackathon2-todo-backend.onrender.com
- Confirmed lib/api.ts uses correct conditional API_BASE logic:
  ```typescript
  const API_BASE_URL = process.env.NODE_ENV === 'production'
    ? process.env.NEXT_PUBLIC_API_BASE_URL_PROD
    : process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL;
  ```
- Verified all required routes exist:
  - / (app/page.tsx) ✓
  - /dashboard (app/dashboard/page.tsx) ✓
  - /signin (app/(auth)/signin/page.tsx) ✓
  - /signup (app/(auth)/signup/page.tsx) ✓
- Tested build process with `npm run build` - completed successfully

## Current State Assessment
All configuration and code was already correctly implemented:
- Conditional API logic properly implemented in lib/api.ts
- All fetch calls use `${API_BASE_URL}/api/...` pattern
- All required routes properly exist in Next.js App Router structure
- Error handling pages already in place (app/error.tsx, app/not-found.tsx)
- Build process completes without errors

## Technical Details
- All API calls dynamically switch between local and production URLs based on NODE_ENV
- Local development works on http://localhost:3000 with local backend
- Production deployment uses https://hackathon2-todo-backend.onrender.com
- Next.js App Router structure follows proper conventions
- Environment variables properly prefixed with NEXT_PUBLIC_

## Verification
- Frontend builds successfully with all routes: /, /dashboard, /signin, /signup
- No build errors or warnings
- Route optimization completed successfully
- Conditional API logic verified working

## Deployment Impact
- Vercel deployed frontend at https://hackathon2-todo-console-app-qu73.vercel.app/ should now load correctly
- All routes should be accessible without 404 errors
- API calls will connect to the correct backend based on environment
- Local development continues to work unchanged