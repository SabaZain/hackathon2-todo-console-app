# Phase-4 Todo Chatbot - Render Deployment

Complete guide for deploying Phase-4 Todo Chatbot application to Render.

---

## 🎯 Quick Start

**Already deployed and having issues?** → Jump to [Fix Deployment Issues](#-fix-deployment-issues)

**First time deploying?** → Follow [Initial Deployment](#-initial-deployment)

**Want to test your deployment?** → Use [Validation Scripts](#-validation)

---

## 📦 Project Structure

```
phase4-local-k8s/
├── backend/
│   ├── main.py                 # FastAPI app with CORS ✅ UPDATED
│   ├── Dockerfile              # Backend Docker config
│   └── requirements.txt        # Python dependencies
│
├── frontend/
│   ├── Dockerfile              # Frontend Docker config ✅ UPDATED
│   ├── .env.production         # Production env vars ✅ NEW
│   ├── .env.local              # Local dev env vars ✅ NEW
│   ├── next.config.js          # Next.js configuration
│   ├── package.json            # Node dependencies
│   ├── lib/api.ts              # API client
│   └── public/todo-chatbot/    # Chatbot assets
│
└── Documentation/
    ├── RENDER_DEPLOYMENT_FIX.md        # Detailed fix guide ✅ NEW
    ├── DEPLOYMENT_FIXES_SUMMARY.md     # Quick summary ✅ NEW
    ├── RENDER_ENVIRONMENT_SETUP.md     # Env vars guide ✅ NEW
    ├── test-phase4-deployment.sh       # Test script (Unix) ✅ NEW
    └── test-phase4-deployment.bat      # Test script (Windows) ✅ NEW
```

---

## 🚀 Initial Deployment

### Prerequisites

- ✅ GitHub repository with your code
- ✅ Render account (https://render.com)
- ✅ Git installed locally

### Step 1: Prepare Code

```bash
# Navigate to Phase-4 directory
cd phase4-local-k8s

# Verify all fixes are in place
git status

# Should show:
# - frontend/.env.production (new)
# - frontend/.env.local (new)
# - frontend/Dockerfile (modified)
# - backend/main.py (modified)
```

### Step 2: Commit Changes

```bash
git add .
git commit -m "feat: Phase-4 Render deployment configuration"
git push origin main
```

### Step 3: Create Backend Service on Render

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name:** `todo-backend-phase4`
   - **Region:** Choose closest to you
   - **Root Directory:** `phase4-local-k8s/backend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `Dockerfile`
   - **Plan:** Free (or as needed)

5. Add Environment Variables:
   ```
   PORT=8000
   PYTHON_VERSION=3.11
   ```

6. Click "Create Web Service"
7. Wait for deployment (2-5 minutes)

### Step 4: Create Frontend Service on Render

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name:** `todo-frontend-phase4`
   - **Region:** Same as backend
   - **Root Directory:** `phase4-local-k8s/frontend`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `Dockerfile`
   - **Plan:** Free (or as needed)

4. Add Environment Variables:
   ```
   NODE_VERSION=20
   PORT=10000
   NODE_ENV=production
   NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
   NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000
   ```

5. Click "Create Web Service"
6. Wait for deployment (3-7 minutes)

### Step 5: Verify Deployment

```bash
# Run validation script
./test-phase4-deployment.sh
# OR on Windows:
# test-phase4-deployment.bat
```

**Expected result:** All tests pass ✅

---

## 🔧 Fix Deployment Issues

### Problem: Frontend shows HTTP 502 errors

**Symptoms:**
- Frontend URL returns 502 Bad Gateway
- Application not loading
- Render logs show errors

**Solution:**

1. **Verify environment variables are set:**
   - Go to Render Dashboard → `todo-frontend-phase4` → Environment
   - Check that all variables from Step 4 above are present
   - If missing, add them and save

2. **Check Dockerfile:**
   - Verify `frontend/Dockerfile` has updated content with ENV variables
   - Should see lines like:
     ```dockerfile
     ENV NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
     ```

3. **Redeploy:**
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for build to complete
   - Check logs for errors

4. **Verify PORT:**
   - Ensure `PORT=10000` in environment variables
   - Check start command uses correct port

### Problem: API calls failing / CORS errors

**Symptoms:**
- Frontend loads but API calls fail
- Browser console shows CORS errors
- Network tab shows failed requests

**Solution:**

1. **Verify backend CORS configuration:**
   ```bash
   # Check if backend/main.py includes frontend URL
   cat backend/main.py | grep "todo-frontend-phase4"
   # Should see: "https://todo-frontend-phase4.onrender.com"
   ```

2. **Test CORS directly:**
   ```bash
   curl -I -X OPTIONS https://todo-backend-phase4.onrender.com/api/tasks \
     -H "Origin: https://todo-frontend-phase4.onrender.com"
   # Look for: Access-Control-Allow-Origin header
   ```

3. **If CORS not working:**
   - Verify `backend/main.py` has updated CORS origins
   - Redeploy backend service
   - Wait for deployment to complete
   - Test again

### Problem: Chatbot icon not visible

**Symptoms:**
- No 💬 emoji icon in bottom-right corner
- Chatbot not functioning
- JavaScript errors in console

**Solution:**

1. **Check if chatbot assets loaded:**
   - Open browser DevTools → Network tab
   - Look for `/todo-chatbot/` requests
   - Should see 200 status codes

2. **Verify Dockerfile copies public folder:**
   ```dockerfile
   COPY --from=builder --chown=nextjs:nodejs /app/public ./public
   ```

3. **Check browser console for errors:**
   - Press F12 → Console tab
   - Look for JavaScript errors related to chatbot
   - Fix any loading issues

4. **Verify integration:**
   - Check that chatbot files are in `public/todo-chatbot/`
   - Ensure files are referenced correctly in HTML

### Problem: Environment variables not working

**Symptoms:**
- API calls going to wrong URL
- Console shows `undefined` for env variables
- Application behavior incorrect

**Solution:**

1. **Verify variables in Render Dashboard:**
   - Go to service → Environment
   - Check variable names (case-sensitive!)
   - Verify values have no extra spaces

2. **For NEXT_PUBLIC_* variables:**
   - These MUST be set at build time
   - After changing them, click "Manual Deploy"
   - Wait for new build to complete
   - Old build has old values embedded!

3. **Test in browser console:**
   ```javascript
   // This should show the backend URL
   console.log(process.env.NEXT_PUBLIC_API_BASE_URL_PROD)
   ```

4. **If still not working:**
   - Check `.env.production` file exists
   - Verify Dockerfile sets ENV variables
   - Rebuild and redeploy

---

## ✅ Validation

### Automated Testing

Run the validation script:

```bash
# Unix/Linux/Mac
./test-phase4-deployment.sh

# Windows
test-phase4-deployment.bat
```

**What it tests:**
- ✅ Backend health endpoint
- ✅ Frontend loads successfully
- ✅ CORS configuration
- ✅ API endpoints accessibility
- ✅ Chatbot assets

### Manual Testing

1. **Backend API:**
   ```bash
   curl https://todo-backend-phase4.onrender.com/health
   # Expected: {"status":"healthy","api":"Todo App API"}
   ```

2. **Frontend:**
   - Visit: https://todo-frontend-phase4.onrender.com
   - Should load without errors
   - Check browser console (F12)

3. **Full User Flow:**
   - [ ] Register new user
   - [ ] Login successfully
   - [ ] Create a task
   - [ ] Update a task
   - [ ] Complete a task
   - [ ] Delete a task
   - [ ] Open chatbot (click 💬)
   - [ ] Send chatbot message
   - [ ] Receive chatbot response

4. **API Connectivity:**
   ```javascript
   // In browser console on frontend
   fetch('https://todo-backend-phase4.onrender.com/health')
     .then(r => r.json())
     .then(console.log)
   // Expected: {status: "healthy", api: "Todo App API"}
   ```

---

## 📊 Monitoring & Logs

### View Logs

**Backend:**
```
Dashboard → todo-backend-phase4 → Logs
```

**Frontend:**
```
Dashboard → todo-frontend-phase4 → Logs
```

### What to Look For

**Backend Logs (Good):**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
Chatbot API routes included successfully
```

**Frontend Logs (Good):**
```
ready - started server on 0.0.0.0:10000
```

**Backend Logs (Bad):**
```
ERROR: Could not import...
ModuleNotFoundError...
Connection refused...
```

**Frontend Logs (Bad):**
```
Error: Cannot find module...
Build failed...
TypeError...
```

---

## 🛠️ Configuration Reference

### Backend Configuration

**Environment Variables:**
```yaml
PORT: 8000
PYTHON_VERSION: 3.11
```

**CORS Origins (in main.py):**
```python
origins = [
    "http://localhost:3000",
    "http://localhost:10000",
    "https://todo-frontend-phase4.onrender.com",  # Phase-4
    "https://todo-backend-phase4.onrender.com",   # Phase-4
    # ... other origins
]
```

**Endpoints:**
- Health: `GET /health`
- API Health: `GET /api/health`
- Auth: `POST /api/auth/login`, `POST /api/auth/register`
- Tasks: `/api/tasks/*`
- Chat: `/api/{user_id}/chat`

### Frontend Configuration

**Environment Variables:**
```yaml
NODE_VERSION: 20
PORT: 10000
NODE_ENV: production
NEXT_PUBLIC_API_BASE_URL_PROD: https://todo-backend-phase4.onrender.com
NEXT_PUBLIC_API_BASE_URL_LOCAL: http://localhost:8000
```

**API Client (lib/api.ts):**
```typescript
const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? process.env.NEXT_PUBLIC_API_BASE_URL_PROD
  : process.env.NEXT_PUBLIC_API_BASE_URL_LOCAL;
```

**Chatbot:**
- Assets: `/public/todo-chatbot/`
- Icon: 💬 emoji (no image file needed)
- Integration: Loaded via public scripts

---

## 📚 Documentation Index

| Document | Purpose | Audience |
|----------|---------|----------|
| **PHASE4_RENDER_DEPLOYMENT_README.md** (this file) | Complete deployment guide | Everyone |
| **RENDER_DEPLOYMENT_FIX.md** | Detailed fix instructions | Debugging issues |
| **DEPLOYMENT_FIXES_SUMMARY.md** | Quick reference | Quick overview |
| **RENDER_ENVIRONMENT_SETUP.md** | Env vars step-by-step | Setting up env vars |
| **test-phase4-deployment.sh** | Automated validation | Testing deployment |
| **test-phase4-deployment.bat** | Automated validation (Windows) | Testing deployment |

---

## 🎯 Deployment Checklist

### Before Deploying

- [ ] All code changes committed and pushed
- [ ] `.env.production` file exists in frontend
- [ ] Backend `main.py` has updated CORS origins
- [ ] Frontend `Dockerfile` has updated ENV variables
- [ ] Git repository connected to Render

### During Deployment

- [ ] Backend service created on Render
- [ ] Backend environment variables set
- [ ] Backend deployment successful (check logs)
- [ ] Frontend service created on Render
- [ ] Frontend environment variables set
- [ ] Frontend deployment successful (check logs)

### After Deployment

- [ ] Backend health check passes
- [ ] Frontend loads without 502 errors
- [ ] CORS working (no console errors)
- [ ] API calls successful (check Network tab)
- [ ] Chatbot icon visible (💬)
- [ ] Full user flow works end-to-end
- [ ] Validation script passes all tests

---

## ⚡ Quick Commands

```bash
# Commit and push changes
git add . && git commit -m "fix: Phase-4 deployment" && git push

# Test deployment (Unix)
./test-phase4-deployment.sh

# Test deployment (Windows)
test-phase4-deployment.bat

# Check backend health
curl https://todo-backend-phase4.onrender.com/health

# Check frontend
curl -I https://todo-frontend-phase4.onrender.com

# Test CORS
curl -I -X OPTIONS https://todo-backend-phase4.onrender.com/api/tasks \
  -H "Origin: https://todo-frontend-phase4.onrender.com"
```

---

## 🆘 Getting Help

1. **Check logs first:**
   - Backend logs for API errors
   - Frontend logs for build/runtime errors
   - Browser console for client-side errors

2. **Review documentation:**
   - Start with this README
   - Check `RENDER_DEPLOYMENT_FIX.md` for detailed steps
   - Review `RENDER_ENVIRONMENT_SETUP.md` for env vars

3. **Common issues:**
   - See "Fix Deployment Issues" section above
   - Check troubleshooting in `RENDER_DEPLOYMENT_FIX.md`

4. **Still stuck?**
   - Verify all files match the changes listed in `DEPLOYMENT_FIXES_SUMMARY.md`
   - Compare with local Docker build
   - Check Render service configuration

---

## 📞 Support Resources

- **Render Documentation:** https://render.com/docs
- **Next.js Deployment:** https://nextjs.org/docs/deployment
- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **Render Dashboard:** https://dashboard.render.com

---

## ✨ Features

✅ **Backend (FastAPI):**
- RESTful API
- JWT authentication
- Task management (CRUD)
- AI chatbot integration
- Secure user isolation
- CORS configured for frontend

✅ **Frontend (Next.js 16):**
- Modern React app
- TypeScript
- Tailwind CSS styling
- Task management UI
- Embedded chatbot (💬)
- Responsive design

✅ **Deployment:**
- Dockerized applications
- Render hosting
- Production-ready configuration
- Environment-based settings
- Health check endpoints

---

**Ready to deploy?** Start with [Quick Start](#-quick-start) or [Initial Deployment](#-initial-deployment)! 🚀
