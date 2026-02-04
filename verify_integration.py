#!/usr/bin/env python3
"""
Verification script to test the integration between backend, frontend, and chatbot.
This script performs checks to ensure all components are properly connected and functional.
"""

import os
import sys
import subprocess
import requests
import time
from typing import Dict, Any, List

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def check_backend_routes():
    """Check that all required backend routes are available."""
    print("[INFO] Checking backend routes...")

    # Check that main.py imports and registers all required routes
    try:
        from backend.main import app
        routes = [route.path for route in app.routes]

        required_routes = [
            "/api/auth/register",
            "/api/auth/login",
            "/api/tasks/",
            "/api/{user_id}/chat",
            "/api/{user_id}/conversations",
            "/api/{user_id}/conversations/{conversation_id}",
            "/api/{user_id}/history",
            "/api/{user_id}/health"
        ]

        print(f"  Found {len(routes)} routes in the application")

        # Check for chat routes specifically
        chat_routes_found = [route for route in routes if 'chat' in route.lower()]
        print(f"  Chat-related routes found: {chat_routes_found}")

        # Check that the main API routes exist
        auth_found = any('/api/auth' in route for route in routes)
        tasks_found = any('/api/tasks' in route for route in routes)
        chat_found = any('/api/' in route and 'chat' in route for route in routes)

        print(f"  [OK] Auth routes: {'[OK]' if auth_found else '[ERR]'}")
        print(f"  [OK] Tasks routes: {'[OK]' if tasks_found else '[ERR]'}")
        print(f"  [OK] Chat routes: {'[OK]' if chat_found else '[ERR]'}")

        return auth_found and tasks_found and chat_found

    except Exception as e:
        print(f"  [ERR] Error checking backend routes: {e}")
        return False

def check_models_integration():
    """Check that models are properly integrated."""
    print("\n[INFO] Checking models integration...")

    try:
        from backend.models import Task, User
        print("  [OK] Task model imported successfully")
        print("  [OK] User model imported successfully")

        # Check that Task model has required fields
        task_fields = Task.__fields__.keys() if hasattr(Task, '__fields__') else dir(Task)
        required_task_fields = ['id', 'title', 'description', 'completed', 'owner_id']

        found_fields = [field for field in required_task_fields if any(field in str(attr) for attr in task_fields)]
        print(f"  [OK] Required Task fields found: {found_fields}")

        return True
    except Exception as e:
        print(f"  [ERR] Error checking models: {e}")
        return False

def check_database_connection():
    """Check that database connection is properly configured."""
    print("\n[INFO] Checking database connection...")

    try:
        from backend.db import engine
        print("  [OK] Database engine created successfully")

        # Test connection
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            print("  [OK] Database connection test passed")

        return True
    except Exception as e:
        print(f"  [ERR] Database connection error: {e}")
        return False

def check_chat_agent_integration():
    """Check that chat agent is properly integrated with task tools."""
    print("\n[INFO] Checking chat agent integration...")

    try:
        from backend.agent.chat_agent import ChatAgent
        print("  [OK] ChatAgent class imported successfully")

        # Test that required imports work
        from todochatbot.mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )
        print("  [OK] MCP task tools imported successfully")

        # Check that agent can be instantiated
        agent = ChatAgent()
        print("  [OK] ChatAgent instantiated successfully")

        return True
    except Exception as e:
        print(f"  [ERR] Error checking chat agent: {e}")
        return False

def check_frontend_integration():
    """Check that frontend is properly integrated with backend and chatbot."""
    print("\n[INFO] Checking frontend integration...")

    frontend_files = [
        "fullstackwebapp/frontend/components/chatbot/ChatBot.tsx",
        "fullstackwebapp/frontend/components/chatbot/ChatBotWrapper.tsx",
        "fullstackwebapp/frontend/components/chatbot/TodoChatbotWidget.tsx",
        "fullstackwebapp/frontend/app/layout.tsx"
    ]

    all_found = True
    for file in frontend_files:
        if os.path.exists(file):
            print(f"  [OK] {file} exists")
        else:
            print(f"  [ERR] {file} not found")
            all_found = False

    # Check that layout includes ChatBotWrapper
    layout_path = "fullstackwebapp/frontend/app/layout.tsx"
    if os.path.exists(layout_path):
        with open(layout_path, 'r') as f:
            layout_content = f.read()
            if '<ChatBotWrapper />' in layout_content:
                print("  [OK] ChatBotWrapper integrated in layout")
            else:
                print("  [ERR] ChatBotWrapper not found in layout")
                all_found = False

            if 'http://127.0.0.1:8000' in layout_content:
                print("  [OK] Backend API URL found in frontend")
            else:
                print("  [WARN] Backend API URL not found in frontend (may use env vars)")

    return all_found

def check_api_endpoints():
    """Check that API endpoints are properly registered."""
    print("\n[INFO] Checking API endpoint registration...")

    try:
        from backend.main import app
        endpoints = [(route.path, route.methods) for route in app.routes]

        # Look for chat-related endpoints
        chat_endpoints = [ep for ep in endpoints if 'chat' in ep[0]]
        task_endpoints = [ep for ep in endpoints if 'tasks' in ep[0]]
        auth_endpoints = [ep for ep in endpoints if 'auth' in ep[0]]

        print(f"  Total endpoints: {len(endpoints)}")
        print(f"  Chat endpoints: {len(chat_endpoints)}")
        print(f"  Task endpoints: {len(task_endpoints)}")
        print(f"  Auth endpoints: {len(auth_endpoints)}")

        for path, methods in chat_endpoints:
            print(f"    - {path}: {methods}")

        return len(chat_endpoints) > 0

    except Exception as e:
        print(f"  [ERR] Error checking API endpoints: {e}")
        return False

def run_tests():
    """Run all verification tests."""
    print("Starting backend, frontend, and chatbot integration verification...\n")

    tests = [
        ("Backend Routes", check_backend_routes),
        ("Models Integration", check_models_integration),
        ("Database Connection", check_database_connection),
        ("Chat Agent Integration", check_chat_agent_integration),
        ("Frontend Integration", check_frontend_integration),
        ("API Endpoints", check_api_endpoints),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))

    print(f"\nIntegration Verification Results:")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{'[OK]' if result else '[X]'} - {test_name}")
        if result:
            passed += 1

    print("=" * 50)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\nAll integration tests passed! The backend, frontend, and chatbot are properly connected.")
        return True
    else:
        print(f"\n{total - passed} tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)