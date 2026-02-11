# TaskFlow - Simple Task Management

A professional task management application with authentication, recurring tasks, reminders, and real-time sync.

## Features

- **User Authentication** - Secure email/password registration and login with JWT tokens
- **Task Management** - Create, update, complete, and delete tasks
- **Recurring Tasks** - Automatic next occurrence generation
- **Smart Reminders** - Multi-channel notifications
- **Real-Time Sync** - Live updates across all devices
- **Search & Filter** - Advanced task discovery
- **Audit Trail** - Complete operation history

## Tech Stack

- **Frontend**: Next.js 15, React 18, TypeScript, Tailwind CSS
- **Backend**: Node.js, Express, TypeScript, Prisma ORM
- **Database**: PostgreSQL (Neon - cloud hosted)
- **Authentication**: JWT with bcrypt password hashing
- **Real-time**: WebSocket for live updates
- **Event Streaming**: Kafka (optional)

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Docker Desktop (for Docker deployment option)
- Neon PostgreSQL database (already configured)

### Option 1: Docker Deployment (Recommended)

Start all services with Docker:

```bash
cd phase-5
docker-compose up
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **API Docs**: http://localhost:3001/docs

To stop:
```bash
docker-compose down
```

### Option 2: Manual Development Setup

**1. Install Dependencies**

```bash
# Backend
cd phase-5/backend
npm install

# Frontend (in a new terminal)
cd phase-5/frontend
npm install
```

**2. Configure Environment**

The `.env` files are already configured to use the Neon database. No changes needed.

**3. Run Database Migrations**

```bash
cd phase-5/backend
npx prisma migrate deploy
```

**4. Start Services**

```bash
# Terminal 1 - Backend
cd phase-5/backend
npm run dev

# Terminal 2 - Frontend
cd phase-5/frontend
npm run dev
```

Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:3001
- **API Docs**: http://localhost:3001/docs

---

## 📝 Usage

### First Time Setup

1. Open http://localhost:3000
2. Click "Get Started" to register a new account
3. Enter your email, name, and password
4. Login with your credentials
5. Start creating tasks!

### API Documentation

Full API documentation with interactive testing is available at:
http://localhost:3001/docs

### Authentication

All API endpoints (except `/api/auth/register` and `/api/auth/login`) require authentication:

```bash
# Register
curl -X POST http://localhost:3001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123","name":"John Doe"}'

# Login
curl -X POST http://localhost:3001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Use the returned token in subsequent requests
curl http://localhost:3001/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔧 Configuration

### Environment Variables

**Backend** (`phase-5/backend/.env`):
```env
DATABASE_URL=postgresql://neondb_owner:npg_k05UWxOueCjr@ep-curly-mud-aifl6lej-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
JWT_SECRET=f6a4cdf97324adfc392ba802253b5881208660fdcaa7be4e5e0dc79c5145f192
NODE_ENV=development
PORT=3001
```

**Frontend** (`phase-5/frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_WS_URL=ws://localhost:3001
```

### Database

The application uses Neon PostgreSQL (cloud-hosted). The database is already configured and migrations are applied automatically.

To view the database schema:
```bash
cd phase-5/backend
npx prisma studio
```

---

## 🏗️ Project Structure

```
phase-5/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   │   ├── routes/          # API endpoints
│   │   │   └── middleware/      # Auth, validation, error handling
│   │   ├── services/            # Business logic
│   │   ├── events/              # Kafka event producers
│   │   ├── prisma/              # Database schema
│   │   └── index.ts             # Server entry point
│   ├── Dockerfile
│   └── package.json
├── frontend/
│   ├── src/
│   │   ├── app/                 # Next.js pages
│   │   ├── components/          # React components
│   │   └── lib/                 # Utilities
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

---

## 🧪 Testing

### Backend Tests
```bash
cd phase-5/backend
npm test
```

### Frontend Tests
```bash
cd phase-5/frontend
npm test
```

---

## 🐛 Troubleshooting

### Backend won't start
- Check if port 3001 is already in use: `netstat -ano | findstr :3001`
- Verify database connection in `.env` file
- Check logs for specific error messages

### Frontend won't start
- Check if port 3000 is already in use: `netstat -ano | findstr :3000`
- Verify `NEXT_PUBLIC_API_URL` in `.env.local`
- Clear Next.js cache: `rm -rf .next`

### Docker issues
- Ensure Docker Desktop is running
- Check container logs: `docker-compose logs backend` or `docker-compose logs frontend`
- Rebuild containers: `docker-compose up --build`

### Database connection errors
- The Neon database is cloud-hosted and should always be accessible
- Check your internet connection
- Verify the DATABASE_URL in `.env` files

### Kafka warnings (optional)
- Kafka is optional and warnings can be ignored for basic usage
- The application works without Kafka (no event streaming)
- To disable Kafka warnings, set `KAFKAJS_NO_PARTITIONER_WARNING=1`

---

## 📚 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/profile` - Get user profile (requires auth)
- `PUT /api/auth/profile` - Update user profile (requires auth)

### Tasks
- `GET /api/tasks` - List all tasks (requires auth)
- `POST /api/tasks` - Create task (requires auth)
- `GET /api/tasks/:id` - Get task details (requires auth)
- `PUT /api/tasks/:id` - Update task (requires auth)
- `DELETE /api/tasks/:id` - Delete task (requires auth)
- `POST /api/tasks/:id/complete` - Mark task complete (requires auth)

### Reminders
- `GET /api/reminders` - List reminders (requires auth)
- `POST /api/reminders` - Create reminder (requires auth)
- `PUT /api/reminders/:id` - Update reminder (requires auth)
- `DELETE /api/reminders/:id` - Delete reminder (requires auth)

### Audit
- `GET /api/audit` - Get audit logs (requires auth)

---

## 🔒 Security

- Passwords are hashed using bcrypt with 10 salt rounds
- JWT tokens expire after 7 days
- All API endpoints (except auth) require valid JWT token
- CORS is configured to allow requests from frontend only
- Helmet.js provides security headers
- Input validation on all endpoints

---

## 📄 License

MIT License - feel free to use this project for learning or production.

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review API documentation at http://localhost:3001/docs
3. Check application logs for error messages
