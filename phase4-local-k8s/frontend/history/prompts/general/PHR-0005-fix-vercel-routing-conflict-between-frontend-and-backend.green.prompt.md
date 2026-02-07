---
id: PHR-0005
title: Fix Vercel Routing Conflict Between Frontend and Backend
date: 2026-01-19
author: Claude
status: completed
tags: ["frontend", "vercel", "404", "routing", "deployment", "api", "nextjs", "configuration"]
---

# Fix Vercel Routing Conflict Between Frontend and Backend

## Original Request
Fix 404 errors on Vercel deployed frontend at "https://hackathon2-todo-console-app-qu73.vercel.app/"

## Critical Issue Discovered
Found that the root vercel.json file was routing ALL requests to the backend:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/api.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/backend/api.py" },
    { "src": "/(.*)", "dest": "/backend/api.py" }  // <-- This routes EVERYTHING to backend
  ]
}
```

This meant that frontend routes like `/`, `/dashboard`, `/signin`, `/signup` were being sent to the backend API instead of being served by Next.js, causing 404 errors.

## Solution Applied
Created a proper vercel.json for the frontend project:
```json
{
  "version": 2,
  "framework": "nextjs"
}
```

## Technical Details
- The root vercel.json was configured to handle the backend deployment
- The route `{ "src": "/(.*)", "dest": "/backend/api.py" }` was catching all traffic and sending it to the backend API
- This prevented Next.js from serving the frontend pages, causing 404 errors
- The frontend deployment needs its own Vercel configuration to be treated as a Next.js application

## Expected Result
With the proper vercel.json configuration for the frontend, Vercel will now:
- Recognize the project as a Next.js application
- Serve frontend routes properly through Next.js routing
- Allow API calls to reach the backend when needed through the conditional API logic
- Eliminate the 404 errors for frontend routes

## Deployment Impact
- Frontend deployed at https://hackathon2-todo-console-app-qu73.vercel.app/ should now serve all routes correctly
- No more 404 errors for main routes
- API calls will still work correctly with the backend using conditional logic
- Local development continues to work unchanged