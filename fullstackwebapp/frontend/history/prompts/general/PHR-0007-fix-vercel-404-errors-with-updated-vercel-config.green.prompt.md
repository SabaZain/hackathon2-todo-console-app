---
id: PHR-0007
title: Fix Vercel 404 Errors with Updated Vercel Configuration
date: 2026-01-19
author: Claude
status: completed
tags: ["frontend", "vercel", "404", "routing", "deployment", "api", "nextjs", "configuration"]
---

# Fix Vercel 404 Errors with Updated Vercel Configuration

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
- Updated vercel.json with correct build configuration:
  ```json
  {
    "version": 2,
    "builds": [
      {
        "src": "package.json",
        "use": "@vercel/next",
        "config": {}
      }
    ],
    "routes": [
      { "src": "/(.*)", "dest": "/" }
    ]
  }
  ```

## Changes Applied
- Updated vercel.json to use explicit build configuration with "@vercel/next"
- Added route configuration to redirect all paths to root: `{ "src": "/(.*)", "dest": "/" }`
- This ensures Next.js handles client-side routing properly on Vercel
- No outputDirectory specified (correct for Next.js projects using default .next folder)

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
- Updated Vercel configuration properly set for Next.js framework

## Deployment Impact
- Vercel deployed frontend at https://hackathon2-todo-console-app-qu73.vercel.app/ should now load correctly
- All routes should be accessible without 404 errors due to proper client-side routing
- API calls will connect to the correct backend based on environment
- Vercel will properly recognize and serve the Next.js application with correct build configuration
- Local development continues to work unchanged