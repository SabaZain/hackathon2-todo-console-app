# API Documentation Setup

## Swagger UI Documentation

Your API documentation is now available at: **http://localhost:3001/docs**

## What's Included

### Endpoints Documented:

**Tasks** (`/api/tasks`)
- POST `/api/tasks` - Create a new task
- POST `/api/tasks/recurring` - Create a recurring task
- GET `/api/tasks` - Get all tasks (with filters)
- GET `/api/tasks/:id` - Get task by ID
- GET `/api/tasks/:id/occurrences` - Get recurring task occurrences
- PUT `/api/tasks/:id` - Update a task
- POST `/api/tasks/:id/complete` - Mark task as complete
- DELETE `/api/tasks/:id` - Delete a task

**Reminders** (`/api/reminders`)
- POST `/api/reminders` - Create a reminder
- GET `/api/reminders` - Get all reminders
- GET `/api/reminders/:id` - Get reminder by ID
- GET `/api/reminders/tasks/:taskId/reminders` - Get task reminders
- PUT `/api/reminders/:id` - Update a reminder
- DELETE `/api/reminders/:id` - Delete a reminder

**Audit** (`/api/audit`)
- GET `/api/audit` - Get audit logs (with pagination)
- GET `/api/audit/task/:taskId` - Get task audit logs
- GET `/api/audit/stats` - Get audit statistics

**Health**
- GET `/health` - Health check endpoint

## Features

✓ Interactive API testing interface
✓ Request/response schemas
✓ Authentication support (Bearer token)
✓ Query parameter documentation
✓ Request body examples
✓ Response status codes

## How to Use

1. Start the server: `npm run dev`
2. Open browser: http://localhost:3001/docs
3. Click "Authorize" to add your JWT token
4. Try out any endpoint directly from the UI

## Authentication

Most endpoints require authentication. To test authenticated endpoints:
1. Click the "Authorize" button in Swagger UI
2. Enter your JWT token in the format: `Bearer <your-token>`
3. Click "Authorize" and "Close"
4. Now you can test protected endpoints

