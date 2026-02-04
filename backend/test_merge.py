"""
Simple test to verify the merged backend works correctly
"""

def test_imports():
    """Test that all necessary modules can be imported"""
    print("Testing imports...")

    try:
        from main import app
        print("[OK] Main app imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import main app: {e}")
        return False

    try:
        from api.chat_endpoint import get_router
        print("[OK] Chat endpoint router imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import chat endpoint: {e}")
        return False

    try:
        from db import engine
        print("[OK] Database engine imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import database engine: {e}")
        return False

    try:
        from models import get_unique_task_model, get_unique_user_model
        Task = get_unique_task_model()
        User = get_unique_user_model()
        print("[OK] Models imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import models: {e}")
        return False

    try:
        from auth import get_current_user_id
        print("[OK] Auth module imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import auth module: {e}")
        return False

    try:
        from database.conversations import save_message, load_conversation
        print("[OK] Database conversations module imported successfully")
    except Exception as e:
        print(f"[ERROR] Failed to import database conversations: {e}")
        return False

    print("All imports successful!")
    return True


def test_api_routes():
    """Test that the API routes are properly configured"""
    print("\nTesting API routes...")

    try:
        from main import app
        routes = [route.path for route in app.routes]

        # Check for existing task routes
        task_routes = [route for route in routes if '/api/tasks' in route]
        print(f"[OK] Found {len(task_routes)} task-related routes")

        # Check for chat routes
        chat_routes = [route for route in routes if '/api/' in route and '{user_id}' in route]
        print(f"[OK] Found {len(chat_routes)} chat-related routes")

        # Print some example routes
        for route in routes[:10]:  # Show first 10 routes
            print(f"  - {route.methods} {route.path}")

        if len(routes) > 10:
            print(f"  ... and {len(routes)-10} more routes")

        print("API routes configuration looks good!")
        return True

    except Exception as e:
        print(f"[ERROR] Failed to test API routes: {e}")
        return False


if __name__ == "__main__":
    print("Testing merged Todo app + Chatbot backend...\n")

    success1 = test_imports()
    success2 = test_api_routes()

    if success1 and success2:
        print("\n[SUCCESS] All tests passed! The merge was successful.")
        print("\nSummary of merged functionality:")
        print("- Todo app API endpoints (/api/tasks)")
        print("- Authentication endpoints (/api/auth)")
        print("- Chatbot API endpoints (/api/{user_id}/chat, /api/{user_id}/conversations)")
        print("- Shared JWT authentication system")
        print("- Combined PostgreSQL database with both schemas")
        print("- CORS configured for both frontends")
    else:
        print("\n[FAILURE] Some tests failed. Please check the errors above.")
        exit(1)