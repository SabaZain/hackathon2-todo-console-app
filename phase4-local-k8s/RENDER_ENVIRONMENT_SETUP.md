# Render Environment Variables Setup Guide

This guide walks you through setting environment variables in Render Dashboard for Phase-4 deployment.

---

## 🎯 Why Environment Variables Matter

Environment variables tell your application:
- Where to find the backend API
- What port to run on
- What version of Node.js/Python to use
- Whether to run in production or development mode

**Critical:** `NEXT_PUBLIC_*` variables in Next.js **must** be set at build time. This means:
1. They need to be in `.env.production` file (✅ already done)
2. They should also be in Render Dashboard for redundancy
3. You need to **redeploy** after changing them

---

## 🔧 Backend Service Configuration

### Service: `todo-backend-phase4`

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Click on `todo-backend-phase4` service

2. **Navigate to Environment:**
   - Click "Environment" in the left sidebar
   - Click "Add Environment Variable"

3. **Add these variables:**

   | Key | Value | Description |
   |-----|-------|-------------|
   | `PORT` | `8000` | Port for FastAPI server |
   | `PYTHON_VERSION` | `3.11` | Python version to use |

4. **Optional variables** (if needed):

   | Key | Value | Description |
   |-----|-------|-------------|
   | `DATABASE_URL` | `sqlite:///./todos.db` | Database connection string |
   | `SECRET_KEY` | `your-secret-key` | JWT secret (change this!) |

5. **Save and Deploy:**
   - Click "Save Changes"
   - Render will automatically redeploy the service

### Backend Build Configuration

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## 🎨 Frontend Service Configuration

### Service: `todo-frontend-phase4`

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Click on `todo-frontend-phase4` service

2. **Navigate to Environment:**
   - Click "Environment" in the left sidebar
   - Click "Add Environment Variable"

3. **Add these variables:**

   | Key | Value | Description |
   |-----|-------|-------------|
   | `NODE_VERSION` | `20` | Node.js version (required for Next.js 16+) |
   | `PORT` | `10000` | Port for Next.js server |
   | `NODE_ENV` | `production` | Run in production mode |
   | `NEXT_PUBLIC_API_BASE_URL_PROD` | `https://todo-backend-phase4.onrender.com` | Backend API URL (production) |
   | `NEXT_PUBLIC_API_BASE_URL_LOCAL` | `http://localhost:8000` | Backend API URL (local dev) |

4. **Save and Deploy:**
   - Click "Save Changes"
   - Render will automatically redeploy the service
   - **Wait for build to complete** (3-7 minutes)

### Frontend Build Configuration

**Build Command:**
```bash
npm install && npm run build
```

**Start Command:**
```bash
node server.js
```

**Docker Configuration:**
- ✅ Dockerfile path: `frontend/Dockerfile`
- ✅ Docker Context: `frontend`

---

## 📸 Step-by-Step Screenshots Guide

### Adding Environment Variables

1. **Find your service**
   ```
   Dashboard → Select Service → Environment Tab
   ```

2. **Click "Add Environment Variable"**
   - You'll see a form with:
     - Key (variable name)
     - Value (variable value)

3. **Enter the variable**
   - Example for frontend:
     - Key: `NEXT_PUBLIC_API_BASE_URL_PROD`
     - Value: `https://todo-backend-phase4.onrender.com`

4. **Save**
   - Click "Add" button
   - Repeat for each variable

5. **Deploy**
   - After adding all variables, click "Save Changes"
   - Service will automatically redeploy

---

## ✅ Verification

After setting environment variables:

### Backend Verification

1. **Check deployment logs:**
   ```
   Dashboard → todo-backend-phase4 → Logs
   ```

2. **Look for:**
   ```
   INFO:     Application startup complete.
   INFO:     Uvicorn running on http://0.0.0.0:8000
   ```

3. **Test the endpoint:**
   ```bash
   curl https://todo-backend-phase4.onrender.com/health
   # Expected: {"status":"healthy","api":"Todo App API"}
   ```

### Frontend Verification

1. **Check deployment logs:**
   ```
   Dashboard → todo-frontend-phase4 → Logs
   ```

2. **Look for:**
   ```
   ready - started server on 0.0.0.0:10000, url: http://localhost:10000
   ```

3. **Test the site:**
   - Visit: https://todo-frontend-phase4.onrender.com
   - Should load without errors

4. **Verify API URL in browser:**
   - Open browser console (F12)
   - Run:
     ```javascript
     console.log(process.env.NEXT_PUBLIC_API_BASE_URL_PROD)
     ```
   - Should show: `https://todo-backend-phase4.onrender.com`

---

## 🔄 Updating Environment Variables

**Important:** When you update `NEXT_PUBLIC_*` variables:

1. Update the variable in Render Dashboard
2. **Click "Manual Deploy"** to rebuild
3. Wait for build to complete
4. Old values were embedded in the build, new build needed!

**Why?** Next.js embeds `NEXT_PUBLIC_*` variables into the JavaScript bundle at build time. Changing them without rebuilding won't work.

---

## 🚨 Common Mistakes to Avoid

### ❌ Wrong Variable Names
```
# WRONG - typo in variable name
NEXT_PUBLC_API_BASE_URL=...  # Missing 'I' in PUBLIC

# CORRECT
NEXT_PUBLIC_API_BASE_URL_PROD=...
```

### ❌ Wrong Backend URL
```
# WRONG - using local URL in production
NEXT_PUBLIC_API_BASE_URL_PROD=http://localhost:8000

# CORRECT - using Render backend URL
NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
```

### ❌ Forgetting to Redeploy
```
Change env var → Click "Save Changes" → ✅ Wait for redeploy!
```

### ❌ Wrong Node Version
```
# WRONG - old Node version (Next.js 16+ needs Node 20+)
NODE_VERSION=18

# CORRECT
NODE_VERSION=20
```

---

## 🔍 Troubleshooting

### Issue: "Environment variable not working"

**Check:**
1. ✅ Variable name is spelled correctly (case-sensitive!)
2. ✅ Variable value has no extra spaces
3. ✅ Service was redeployed after adding variable
4. ✅ For `NEXT_PUBLIC_*`: Build completed after setting variable

**Solution:**
```bash
# Verify in browser console
console.log(process.env.NEXT_PUBLIC_API_BASE_URL_PROD)
# If undefined → variable not embedded in build → redeploy needed
```

### Issue: "API calls still failing"

**Check:**
1. ✅ Backend URL in frontend matches actual backend URL
2. ✅ Backend CORS includes frontend URL
3. ✅ Backend is running and healthy
4. ✅ No typos in URLs

**Test:**
```bash
# Test backend directly
curl https://todo-backend-phase4.onrender.com/health

# Test from frontend (browser console)
fetch('https://todo-backend-phase4.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
```

### Issue: "Build failing after adding variables"

**Check:**
1. ✅ No syntax errors in variable values
2. ✅ URLs are valid (no trailing slashes, correct protocol)
3. ✅ Check build logs for specific errors
4. ✅ Verify Dockerfile and build commands are correct

---

## 📋 Quick Reference Card

### Backend (`todo-backend-phase4`)

```yaml
Environment Variables:
  PORT: 8000
  PYTHON_VERSION: 3.11

Build Command:
  pip install -r requirements.txt

Start Command:
  uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend (`todo-frontend-phase4`)

```yaml
Environment Variables:
  NODE_VERSION: 20
  PORT: 10000
  NODE_ENV: production
  NEXT_PUBLIC_API_BASE_URL_PROD: https://todo-backend-phase4.onrender.com
  NEXT_PUBLIC_API_BASE_URL_LOCAL: http://localhost:8000

Build Command:
  npm install && npm run build

Start Command:
  node server.js
```

---

## 🎯 Next Steps

After setting up environment variables:

1. ✅ Wait for both services to finish deploying
2. ✅ Run validation tests:
   ```bash
   ./test-phase4-deployment.sh
   # OR
   test-phase4-deployment.bat
   ```
3. ✅ Test in browser:
   - Visit: https://todo-frontend-phase4.onrender.com
   - Check console for errors
   - Test full user flow (register, login, create tasks)

---

## 📚 Additional Resources

- **Render Docs:** https://render.com/docs/environment-variables
- **Next.js Env Docs:** https://nextjs.org/docs/basic-features/environment-variables
- **Our Deployment Guide:** `RENDER_DEPLOYMENT_FIX.md`
- **Quick Summary:** `DEPLOYMENT_FIXES_SUMMARY.md`

---

**Need help?** Check the troubleshooting sections above or review the detailed deployment guide! 🚀
