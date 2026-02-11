# Phase 5 TaskFlow - Quick Start Summary

## 🎯 Two Ways to Run

### 1️⃣ Manual Mode (No Kafka) - 2 Minutes Setup

**What you get:** Core task management (CRUD, recurring tasks, reminders, auth)

```bash
# Terminal 1 - Backend
cd phase-5/backend
npm install
npm run dev

# Terminal 2 - Frontend
cd phase-5/frontend
npm install
npm run dev
```

✅ Open http://localhost:3000 and start using!

**Note:** You'll see Kafka warnings - that's normal and expected.

---

### 2️⃣ Full Mode (With Kafka) - 5 Minutes Setup

**What you get:** Everything + real-time sync, audit logs, event streaming, 4 background agents

```bash
cd phase-5/infrastructure/docker
docker-compose up -d
```

✅ Open http://localhost:3000 and enjoy all features!
✅ Monitor events at http://localhost:8080 (Kafka UI)

---

## 📊 What's the Difference?

| Feature | Manual Mode | Full Mode |
|---------|-------------|-----------|
| Task Management | ✅ | ✅ |
| Recurring Tasks | ✅ | ✅ |
| Reminders | ✅ | ✅ |
| Real-time Sync | ❌ | ✅ |
| Audit Logs | ❌ | ✅ |
| Event Streaming | ❌ | ✅ |

---

## 🔧 Troubleshooting

**Port in use?**
```bash
# Windows
netstat -ano | findstr :3001
taskkill //F //PID <PID>

# Mac/Linux
lsof -i :3001
kill -9 <PID>
```

**Docker issues?**
```bash
docker-compose down -v
docker-compose up -d --build
```

---

## 📚 Need More Details?

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for comprehensive documentation.

---

**That's it! Choose your mode and start building! 🚀**
