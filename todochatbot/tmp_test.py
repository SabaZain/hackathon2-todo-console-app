import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test individual imports to identify the issue
try:
    print("Testing basic imports...")
    from sqlmodel import SQLModel
    print("✓ SQLModel import successful")

    from database.conversations import save_message
    print("✓ Database import successful")

    # Try importing the agent
    from agent.chat_agent import ChatAgent
    print("✓ ChatAgent import successful")

    # Try importing the API
    from api.chat_endpoint import get_router
    print("✓ API import successful")

    # Finally try importing main
    from main import app
    print("✓ Main app import successful")

    print("All imports successful!")

except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()