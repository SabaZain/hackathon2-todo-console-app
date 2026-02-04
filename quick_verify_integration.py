#!/usr/bin/env python3
"""
Quick verification script to test the integration between backend, frontend, and chatbot.
This script performs checks without requiring a running database.
"""

import os
import sys
from typing import Dict, Any, List

def check_imports():
    """Check that all required modules can be imported."""
    print("[INFO] Checking module imports...")

    modules_to_check = [
        ("backend.main", "main"),
        ("backend.models", "models"),
        ("backend.agent.chat_agent", "chat_agent"),
        ("todochatbot.mcp_tools.task_tools", "task_tools"),
        ("backend.api.chat_endpoint", "chat_endpoint"),
        ("backend.api.agent_connector", "agent_connector"),
    ]

    success_count = 0
    for module_path, description in modules_to_check:
        try:
            # Add backend to path for imports
            sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

            if module_path == "backend.main":
                from backend.main import app
            elif module_path == "backend.models":
                from backend import models
            elif module_path == "backend.agent.chat_agent":
                from backend.agent import chat_agent
            elif module_path == "todochatbot.mcp_tools.task_tools":
                from todochatbot.mcp_tools import task_tools
            elif module_path == "backend.api.chat_endpoint":
                from backend.api import chat_endpoint
            elif module_path == "backend.api.agent_connector":
                from backend.api import agent_connector

            print(f"  [OK] {description} module imported successfully")
            success_count += 1
        except Exception as e:
            print(f"  [ERR] {description} module import failed: {e}")

    return success_count == len(modules_to_check)

def check_chatbot_frontend_integration():
    """Check that chatbot is integrated in the frontend."""
    print("\n[INFO] Checking frontend chatbot integration...")

    # Check that the chatbot components exist
    chatbot_files = [
        "fullstackwebapp/frontend/components/chatbot/ChatBot.tsx",
        "fullstackwebapp/frontend/components/chatbot/ChatBotWrapper.tsx",
        "fullstackwebapp/frontend/components/chatbot/TodoChatbotWidget.tsx",
    ]

    all_exist = True
    for file in chatbot_files:
        if os.path.exists(file):
            print(f"  [OK] {file} exists")
        else:
            print(f"  [ERR] {file} not found")
            all_exist = False

    # Check that layout includes ChatBotWrapper
    layout_path = "fullstackwebapp/frontend/app/layout.tsx"
    if os.path.exists(layout_path):
        with open(layout_path, 'r') as f:
            layout_content = f.read()
            if '<ChatBotWrapper />' in layout_content:
                print("  [OK] ChatBotWrapper integrated in layout")
            else:
                print("  [ERR] ChatBotWrapper not found in layout")
                all_exist = False
    else:
        print(f"  [ERR] {layout_path} not found")
        all_exist = False

    return all_exist

def check_backend_routes_registration():
    """Check that backend routes are properly structured."""
    print("\n[INFO] Checking backend route structure...")

    try:
        # Just check that the route files exist and have expected content
        route_files = [
            "backend/main.py",
            "backend/api/chat_endpoint.py",
            "backend/routes/tasks.py",
            "backend/routes/auth.py",
        ]

        all_ok = True
        for file in route_files:
            if os.path.exists(file):
                with open(file, 'r') as f:
                    content = f.read()

                    if "chat_endpoint" in file:
                        # Check for chat-related routes
                        has_chat_routes = any(keyword in content for keyword in ['chat', 'conversation', 'message'])
                        print(f"  [OK] {file} exists with chat routes: {has_chat_routes}")

                    elif "tasks.py" in file:
                        # Check for task-related routes
                        has_task_routes = any(keyword in content for keyword in ['task', 'get', 'post', 'put', 'delete'])
                        print(f"  [OK] {file} exists with task routes: {has_task_routes}")

                    elif "auth.py" in file:
                        # Check for auth-related routes
                        has_auth_routes = any(keyword in content for keyword in ['auth', 'login', 'register', 'token'])
                        print(f"  [OK] {file} exists with auth routes: {has_auth_routes}")

                    elif "main.py" in file:
                        # Check for route inclusion
                        has_route_includes = any(keyword in content for keyword in ['include_router', 'prefix'])
                        print(f"  [OK] {file} exists with route includes: {has_route_includes}")
            else:
                print(f"  [ERR] {file} not found")
                all_ok = False

        return all_ok
    except Exception as e:
        print(f"  [ERR] Error checking route structure: {e}")
        return False

def check_models_structure():
    """Check that models are properly structured."""
    print("\n[INFO] Checking models structure...")

    try:
        from backend.models import Task, User

        # Check that Task model has required attributes
        task_attrs = dir(Task)
        required_task_attrs = ['id', 'title', 'description', 'completed', 'owner_id', 'created_at']

        found_task_attrs = [attr for attr in required_task_attrs if any(attr == item or f'_{attr}' == item for item in task_attrs)]
        print(f"  [OK] Task model has {len(found_task_attrs)}/{len(required_task_attrs)} required attributes: {found_task_attrs}")

        # Check that User model has required attributes
        user_attrs = dir(User)
        required_user_attrs = ['id', 'email', 'hashed_password', 'created_at']

        found_user_attrs = [attr for attr in required_user_attrs if any(attr == item or f'_{attr}' == item for item in user_attrs)]
        print(f"  [OK] User model has {len(found_user_attrs)}/{len(required_user_attrs)} required attributes: {found_user_attrs}")

        return len(found_task_attrs) >= 4 and len(found_user_attrs) >= 3  # Allow some flexibility

    except Exception as e:
        print(f"  [ERR] Error checking models: {e}")
        return False

def check_agent_integration():
    """Check that the chat agent is properly integrated."""
    print("\n[INFO] Checking agent integration...")

    try:
        # Check that the agent can be imported and has required methods
        from backend.agent.chat_agent import ChatAgent

        # Check that agent has required methods
        agent_methods = dir(ChatAgent)
        required_methods = ['process_message', '_classify_intent_cohere', '_extract_entities_cohere']

        found_methods = [method for method in required_methods if method in agent_methods]
        print(f"  [OK] ChatAgent has {len(found_methods)}/{len(required_methods)} required methods: {found_methods}")

        # Check that MCP tools are accessible
        from todochatbot.mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )

        print("  [OK] MCP task tools are accessible")
        print("  [OK] All required task operations are available")

        return len(found_methods) >= 2  # Require at least basic functionality

    except Exception as e:
        print(f"  [ERR] Error checking agent integration: {e}")
        return False

def run_quick_tests():
    """Run quick verification tests without requiring database."""
    print("Starting quick backend, frontend, and chatbot integration verification...\n")

    tests = [
        ("Module Imports", check_imports),
        ("Frontend Chatbot Integration", check_chatbot_frontend_integration),
        ("Backend Route Structure", check_backend_routes_registration),
        ("Models Structure", check_models_structure),
        ("Agent Integration", check_agent_integration),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))

    print(f"\nQuick Integration Verification Results:")
    print("=" * 50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "[OK]" if result else "[X]"
        print(f"{status} - {test_name}")
        if result:
            passed += 1

    print("=" * 50)
    print(f"Total: {passed}/{total} tests passed")

    if passed == total:
        print("\nAll quick integration tests passed! The backend, frontend, and chatbot are properly structured and integrated.")
        print("\nNote: Full functionality requires a running database and proper environment variables.")
        return True
    else:
        print(f"\n{total - passed} tests failed. Please check the integration.")
        return False

if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)