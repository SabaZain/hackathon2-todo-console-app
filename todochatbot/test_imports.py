#!/usr/bin/env python3
"""
Test script to verify that all imports work correctly
"""
import sys
import os

# Add the current directory to the Python path to resolve relative imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # Add the parent directory as well to handle package imports
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    from api.chat_endpoint import get_router
    print("SUCCESS: API module imported successfully")

    from agent.chat_agent import ChatAgent
    print("SUCCESS: Agent module imported successfully")

    # Test other important imports
    from api.agent_connector import AgentConnector
    print("SUCCESS: Agent connector imported successfully")

    from database.conversations import save_message
    print("SUCCESS: Database module imported successfully")

    print("\nAll imports successful!")

except ImportError as e:
    print(f"ERROR: Import error: {e}")
    import traceback
    traceback.print_exc()