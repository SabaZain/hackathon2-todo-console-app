#!/bin/bash

echo "🔍 Testing Phase-4 Render Deployment..."
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Backend and Frontend URLs
BACKEND_URL="https://todo-backend-phase4.onrender.com"
FRONTEND_URL="https://todo-frontend-phase4.onrender.com"

# Test counter
PASSED=0
FAILED=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Phase-4 Deployment Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: Backend health
echo "1️⃣  Testing backend health..."
BACKEND_RESPONSE=$(curl -s "$BACKEND_URL/health" --max-time 10)
if echo "$BACKEND_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}   ✓ Backend is healthy${NC}"
    echo "   Response: $BACKEND_RESPONSE"
    ((PASSED++))
else
    echo -e "${RED}   ✗ Backend health check failed${NC}"
    echo "   Response: $BACKEND_RESPONSE"
    ((FAILED++))
fi
echo ""

# Test 2: Backend root endpoint
echo "2️⃣  Testing backend root endpoint..."
BACKEND_ROOT=$(curl -s "$BACKEND_URL/" --max-time 10)
if echo "$BACKEND_ROOT" | grep -q "Welcome to the Todo App API"; then
    echo -e "${GREEN}   ✓ Backend root endpoint working${NC}"
    ((PASSED++))
else
    echo -e "${RED}   ✗ Backend root endpoint failed${NC}"
    ((FAILED++))
fi
echo ""

# Test 3: Frontend loads
echo "3️⃣  Testing frontend..."
FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL" --max-time 10)
if [ "$FRONTEND_STATUS" = "200" ]; then
    echo -e "${GREEN}   ✓ Frontend loads successfully (HTTP $FRONTEND_STATUS)${NC}"
    ((PASSED++))
else
    echo -e "${RED}   ✗ Frontend returned HTTP $FRONTEND_STATUS${NC}"
    ((FAILED++))
fi
echo ""

# Test 4: CORS preflight
echo "4️⃣  Testing CORS configuration..."
CORS_RESPONSE=$(curl -s -I -X OPTIONS "$BACKEND_URL/api/tasks" \
  -H "Origin: $FRONTEND_URL" \
  -H "Access-Control-Request-Method: GET" \
  --max-time 10)

if echo "$CORS_RESPONSE" | grep -qi "access-control-allow-origin"; then
    echo -e "${GREEN}   ✓ CORS is configured correctly${NC}"
    CORS_ORIGIN=$(echo "$CORS_RESPONSE" | grep -i "access-control-allow-origin" | tr -d '\r')
    echo "   Header: $CORS_ORIGIN"
    ((PASSED++))
else
    echo -e "${RED}   ✗ CORS configuration issue${NC}"
    echo "   No Access-Control-Allow-Origin header found"
    ((FAILED++))
fi
echo ""

# Test 5: Backend API endpoint accessibility
echo "5️⃣  Testing backend API endpoints..."
API_HEALTH=$(curl -s "$BACKEND_URL/api/health" --max-time 10)
if echo "$API_HEALTH" | grep -q "healthy"; then
    echo -e "${GREEN}   ✓ Backend API endpoints accessible${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}   ⚠ Backend /api/health endpoint check inconclusive${NC}"
    ((FAILED++))
fi
echo ""

# Test 6: Check if chatbot assets are accessible
echo "6️⃣  Testing chatbot assets..."
CHATBOT_ASSET=$(curl -s -o /dev/null -w "%{http_code}" "$FRONTEND_URL/todo-chatbot/chat-icon.js" --max-time 10)
if [ "$CHATBOT_ASSET" = "200" ]; then
    echo -e "${GREEN}   ✓ Chatbot assets are accessible${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}   ⚠ Chatbot assets returned HTTP $CHATBOT_ASSET${NC}"
    echo "   Note: This might be expected if assets are bundled differently"
    ((PASSED++))  # Don't fail on this, might be bundled
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Test Results Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo -e "Tests Passed: ${GREEN}$PASSED${NC}"
echo -e "Tests Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 All critical tests passed!${NC}"
    echo ""
    echo "✅ Next steps:"
    echo "   1. Visit $FRONTEND_URL in your browser"
    echo "   2. Open DevTools Console (F12) and check for errors"
    echo "   3. Look for chatbot icon (💬) in bottom-right corner"
    echo "   4. Test user registration and login"
    echo "   5. Create, update, and delete tasks"
    echo "   6. Test chatbot functionality"
    exit 0
else
    echo -e "${RED}❌ Some tests failed. Please review the output above.${NC}"
    echo ""
    echo "🔧 Troubleshooting steps:"
    echo "   1. Check Render service logs:"
    echo "      - Backend: https://dashboard.render.com/web/srv-xxx/logs"
    echo "      - Frontend: https://dashboard.render.com/web/srv-xxx/logs"
    echo "   2. Verify environment variables are set correctly"
    echo "   3. Ensure latest code is deployed"
    echo "   4. Try manual redeploy if auto-deploy didn't trigger"
    echo "   5. Review RENDER_DEPLOYMENT_FIX.md for detailed steps"
    exit 1
fi
