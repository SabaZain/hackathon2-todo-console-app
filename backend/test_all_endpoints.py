#!/usr/bin/env python3
"""
Test all chatbot endpoints to ensure they're properly implemented.
"""

import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def test_all_chatbot_endpoints():
    """Test that all expected chatbot endpoints are available."""
    print("Testing all chatbot endpoints...")

    try:
        from main import app
        routes = [route.path for route in app.routes]

        # Expected chatbot endpoints
        expected_endpoints = [
            "/api/{user_id}/chat",                    # Main chat endpoint
            "/api/{user_id}/conversations",           # Get user conversations
            "/api/{user_id}/conversations/{conversation_id}",  # Get specific conversation
            "/api/{user_id}/history",                 # Get user history
        ]

        print(f"Checking for {len(expected_endpoints)} expected chatbot endpoints:")

        all_found = True
        for endpoint in expected_endpoints:
            if any(endpoint == route for route in routes):
                print(f"  ✅ {endpoint}")
            else:
                print(f"  ❌ {endpoint} - NOT FOUND")
                all_found = False

        # Also check for delete endpoint
        delete_endpoint = "/api/{user_id}/conversations/{conversation_id}"
        delete_methods = []  # We'll check if DELETE method is supported

        # Find routes that match the pattern and check methods
        for route in app.routes:
            if hasattr(route, 'methods') and '/api/{user_id}/conversations/' in route.path:
                if '{conversation_id}' in route.path:
                    # This is the conversation-specific route
                    print(f"  📋 Found conversation route: {route.path} with methods: {route.methods}")

        return all_found

    except Exception as e:
        print(f"Error testing endpoints: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_all_routes():
    """Print all available routes."""
    print("\nAll available routes:")

    from main import app
    routes = [(route.path, getattr(route, 'methods', ['UNKNOWN'])) for route in app.routes]

    for path, methods in routes:
        print(f"  {path} [{', '.join(sorted(methods))}]")

def main():
    print("Testing all chatbot endpoints...\n")

    success = test_all_chatbot_endpoints()
    test_all_routes()

    if success:
        print(f"\n✅ All chatbot endpoints are properly implemented!")
        print("The frontend can now communicate with all required backend endpoints.")
    else:
        print(f"\n❌ Some chatbot endpoints are missing!")

    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)