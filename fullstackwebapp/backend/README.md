# Todo App Backend

This is the backend service for the Todo application with JWT-based authentication and user isolation.

## Features
- JWT-based authentication
- User isolation (users can only access their own tasks)
- Secure password hashing
- CORS configured for frontend integration

## Prerequisites
- Python 3.8+
- PostgreSQL database

## Environment Variables
Create a `.env` file with the following variables:
```bash
DATABASE_URL=your_postgresql_database_url
BETTER_AUTH_SECRET=your_secure_jwt_secret
```

## Installation
1. Install dependencies: `pip install -r requirements.txt`
2. Set environment variables
3. Start the server: `uvicorn main:app --reload`

## Vercel Deployment
1. Install Vercel CLI: `npm install -g vercel`
2. Login to Vercel: `vercel login`
3. Deploy: `vercel --prod`
4. Set environment variables in Vercel dashboard:
   - `DATABASE_URL`: Your PostgreSQL database URL
   - `BETTER_AUTH_SECRET`: Your JWT secret

## Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `GET /api/tasks/` - Get user's tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion

## CORS Configuration
CORS is configured to allow:
- `http://localhost:3000` (local development)
- `https://hackathon2-todo-console-app-lazz.vercel.app` (backend deployment)
- `https://hackathon2-todo-console-app-qu73.vercel.app` (frontend deployment)

## Security
- All endpoints require authentication (except register/login)
- Users can only access their own tasks
- Passwords are securely hashed using bcrypt
- JWT tokens are used for session management