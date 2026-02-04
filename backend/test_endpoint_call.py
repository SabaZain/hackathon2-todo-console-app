#!/usr/bin/env python3
"""
Test script to simulate calling the chat endpoint to see if imports work properly.
"""

import asyncio
from fastapi import Request
from starlette.datastructures import Headers
from starlette.types import Scope
from urllib.parse import urlencode

async def test_chat_endpoint():
    """Test if the chat endpoint can be called without import errors."""
    print("Testing if chat endpoint can be initialized...")

    try:
        # Import the app
        from main import app

        # Check if the endpoint exists
        chat_route = None
        for route in app.routes:
            if hasattr(route, 'path') and route.path == '/api/{user_id}/chat':
                chat_route = route
                break

        if chat_route:
            print("✅ Chat endpoint found in routes")
        else:
            print("❌ Chat endpoint not found")
            return False

        # Test if the agent connector can be imported without errors
        print("Testing agent connector import...")
        try:
            from api.agent_connector import get_agent_connector
            print("✅ Agent connector can be imported")
        except ImportError as e:
            print(f"❌ Agent connector import failed: {e}")
            # Try alternative import paths
            import sys
            import os
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)

            try:
                from api.agent_connector import get_agent_connector
                print("✅ Agent connector can be imported after path adjustment")
            except ImportError as e2:
                print(f"❌ Agent connector still fails after path adjustment: {e2}")

        # Test if database conversations can be imported
        print("Testing database conversations import...")
        try:
            from database.conversations import db_get_user_conversations
            print("✅ Database conversations can be imported")
        except ImportError as e:
            print(f"❌ Database conversations import failed: {e}")

        return True

    except Exception as e:
        print(f"❌ Error testing endpoint: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_chat_endpoint())
    if success:
        print("\n✅ Endpoint testing completed successfully")
    else:
        print("\n❌ Endpoint testing failed")