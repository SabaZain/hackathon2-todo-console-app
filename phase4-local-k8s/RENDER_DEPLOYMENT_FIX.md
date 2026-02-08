# Phase-4 Render Deployment Fix Guide

## Issues Addressed

1. ✅ **Frontend environment variables** - Added `.env.production` with backend URL
2. ✅ **Backend CORS configuration** - Added Phase-4 frontend URL to CORS origins
3. ✅ **Dockerfile optimization** - Environment variables embedded at build time
4. ✅ **Chatbot icon** - Uses emoji (💬), should display correctly after fix
5. ✅ **API connectivity** - Proper URL configuration for production

## Files Modified

### Frontend Files
- `frontend/.env.production` - **CREATED** with production backend URL
- `frontend/.env.local` - **CREATED** for local development
- `frontend/Dockerfile` - **UPDATED** with build-time environment variables

### Backend Files
- `backend/main.py` - **UPDATED** CORS origins to include Phase-4 URLs

## Deployment Steps

### Option 1: Automatic Redeployment (Recommended)

If you have Render configured with auto-deploy from Git:

1. **Commit the changes:**
   ```bash
   cd phase4-local-k8s
   git add .
   git commit -m "fix: Phase-4 Render deployment - CORS, env vars, and Dockerfile updates"
   git push origin main
   ```

2. **Render will automatically:**
   - Detect the changes
   - Rebuild both frontend and backend
   - Redeploy the services

3. **Monitor deployment:**
   - Frontend: https://dashboard.render.com (check todo-frontend-phase4 logs)
   - Backend: https://dashboard.render.com (check todo-backend-phase4 logs)

### Option 2: Manual Deployment via Render Dashboard

1. **Go to Render Dashboard:** https://dashboard.render.com

2. **Deploy Backend:**
   - Navigate to `todo-backend-phase4` service
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for build to complete (~2-5 minutes)
   - Verify logs show: "Chatbot API routes included successfully"

3. **Deploy Frontend:**
   - Navigate to `todo-frontend-phase4` service
   - Click "Manual Deploy" → "Deploy latest commit"
   - Wait for build to complete (~3-7 minutes)
   - Check logs for successful build output

### Option 3: Local Docker Build & Test (Before Deploying)

Test the changes locally first:

```bash
# Navigate to Phase-4 directory
cd phase4-local-k8s

# Build frontend Docker image
cd frontend
docker build -t todo-frontend-phase4:test .

# Build backend Docker image
cd ../backend
docker build -t todo-backend-phase4:test .

# Run backend
docker run -d -p 8000:8000 --name backend-test todo-backend-phase4:test

# Run frontend
docker run -d -p 10000:10000 --name frontend-test \
  -e NEXT_PUBLIC_API_BASE_URL_PROD=http://localhost:8000 \
  todo-frontend-phase4:test

# Test the services
curl http://localhost:8000/health
curl http://localhost:10000

# Cleanup
docker stop frontend-test backend-test
docker rm frontend-test backend-test
```

## Render Environment Variables Configuration

### Backend Service (`todo-backend-phase4`)

Ensure these environment variables are set in Render Dashboard:

```
PORT=8000
PYTHON_VERSION=3.11
```

### Frontend Service (`todo-frontend-phase4`)

Ensure these environment variables are set in Render Dashboard:

```
NODE_VERSION=20
PORT=10000
NEXT_PUBLIC_API_BASE_URL_PROD=https://todo-backend-phase4.onrender.com
NEXT_PUBLIC_API_BASE_URL_LOCAL=http://localhost:8000
NODE_ENV=production
```

**Note:** Even though these are in `.env.production`, it's best practice to set them in Render Dashboard as well for redundancy.

## Validation Checklist

After deployment, verify the following:

### 1. Backend Health Check
```bash
curl https://todo-backend-phase4.onrender.com/health
# Expected: {"status":"healthy","api":"Todo App API"}
```

### 2. Frontend Loads
- Visit: https://todo-frontend-phase4.onrender.com
- Expected: Page loads without 502 errors
- Check browser console for errors

### 3. CORS Configuration
```bash
curl -I -X OPTIONS https://todo-backend-phase4.onrender.com/api/tasks \
  -H "Origin: https://todo-frontend-phase4.onrender.com" \
  -H "Access-Control-Request-Method: GET"
# Expected: Access-Control-Allow-Origin header present
```

### 4. API Connectivity from Frontend
- Open browser console on https://todo-frontend-phase4.onrender.com
- Run:
  ```javascript
  fetch('https://todo-backend-phase4.onrender.com/health')
    .then(r => r.json())
    .then(console.log)
  // Expected: {status: "healthy", api: "Todo App API"}
  ```

### 5. Chatbot Icon Visible
- Look for 💬 emoji icon in the bottom-right corner of the page
- Click it to test chatbot interface
- Check browser console for JavaScript errors

### 6. API Requests Work
- Register a new user
- Login
- Create a task
- Check Network tab in browser DevTools
- All requests should show 200/201 status codes

## Troubleshooting

### Issue: Frontend shows 502 errors
**Solution:**
- Check Render logs: Is the Node server starting correctly?
- Verify PORT=10000 is set in Render environment variables
- Check if `server.js` exists in `.next/standalone` after build

### Issue: Chatbot icon not visible
**Solution:**
- Open browser console and check for JavaScript errors
- Verify `/todo-chatbot/` files are accessible (check Network tab)
- Confirm `public` folder was copied in Docker build

### Issue: API calls fail with CORS errors
**Solution:**
- Verify backend CORS origins include frontend URL
- Check backend logs for CORS middleware initialization
- Test CORS with curl command above

### Issue: API calls return 401/403 errors
**Solution:**
- Check if JWT token is being stored in localStorage
- Verify Authorization header is sent with requests
- Check backend auth middleware configuration

### Issue: Environment variables not working
**Solution:**
- NEXT_PUBLIC_* variables must be set at **build time**
- Redeploy frontend after setting env vars
- Verify env vars are in Render Dashboard

## Quick Test Script

Save this as `test-phase4-deployment.sh` and run after deployment:

```bash
#!/bin/bash

echo "🔍 Testing Phase-4 Deployment..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test backend health
echo "1. Testing backend health..."
BACKEND_RESPONSE=$(curl -s https://todo-backend-phase4.onrender.com/health)
if echo "$BACKEND_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Backend is healthy${NC}"
else
    echo -e "${RED}✗ Backend health check failed${NC}"
fi
echo ""

# Test frontend loads
echo "2. Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://todo-frontend-phase4.onrender.com)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}✓ Frontend loads successfully (HTTP $FRONTEND_STATUS)${NC}"
else
    echo -e "${RED}✗ Frontend returned HTTP $FRONTEND_STATUS${NC}"
fi
echo ""

# Test CORS
echo "3. Testing CORS..."
CORS_HEADER=$(curl -s -I -X OPTIONS https://todo-backend-phase4.onrender.com/api/tasks \
  -H "Origin: https://todo-frontend-phase4.onrender.com" \
  -H "Access-Control-Request-Method: GET" | grep -i "access-control-allow-origin")
if [ -n "$CORS_HEADER" ]; then
    echo -e "${GREEN}✓ CORS is configured correctly${NC}"
else
    echo -e "${RED}✗ CORS configuration issue${NC}"
fi
echo ""

echo "✅ Testing complete!"
echo ""
echo "Next steps:"
echo "1. Visit https://todo-frontend-phase4.onrender.com in your browser"
echo "2. Open DevTools Console (F12) and check for errors"
echo "3. Look for chatbot icon (💬) in bottom-right corner"
echo "4. Test registration, login, and task creation"
```

## Support

If issues persist after following this guide:

1. Check Render service logs for detailed error messages
2. Compare deployed files with local files
3. Verify Dockerfile builds successfully locally
4. Review Render service configuration (especially environment variables)

## Summary

This fix ensures:
- ✅ Frontend knows where to find the backend API
- ✅ Backend allows requests from the frontend
- ✅ Static assets (including chatbot) are properly included
- ✅ Environment variables are embedded at build time
- ✅ CORS is properly configured for cross-origin requests

**Estimated deployment time:** 5-10 minutes for both services.
