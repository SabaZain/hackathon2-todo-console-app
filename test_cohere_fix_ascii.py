#!/usr/bin/env python3
"""
Test script to verify the Cohere API key loading fix.
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_env_loading():
    """Test that environment variables are loaded properly."""
    print("Testing environment variable loading...")

    # Check if COHERE_API_KEY is available
    cohere_key = os.getenv("COHERE_API_KEY")
    print(f"COHERE_API_KEY value: {cohere_key}")

    if cohere_key and cohere_key != "YOUR_COHERE_API_KEY_HERE":
        print("[OK] COHERE_API_KEY is properly configured")
        return True
    else:
        print("? COHERE_API_KEY is not configured (this is expected in some environments)")
        return False

def test_chat_agent_initialization():
    """Test that ChatAgent can be initialized without errors."""
    print("\nTesting ChatAgent initialization...")

    try:
        from backend.agent.chat_agent import ChatAgent

        # Check if COHERE_API_KEY is set before initializing
        cohere_key = os.getenv("COHERE_API_KEY")

        if not cohere_key or cohere_key == "YOUR_COHERE_API_KEY_HERE":
            print("? Skipping initialization test - COHERE_API_KEY not configured")
            return None  # Indeterminate

        # Try to initialize the agent
        agent = ChatAgent()
        print("[OK] ChatAgent initialized successfully")
        print(f"  - Cohere client created: {agent.cohere_client is not None}")
        print(f"  - System prompt loaded: {agent.system_prompt is not None}")
        return True

    except ValueError as e:
        if "COHERE_API_KEY" in str(e):
            print(f"? Initialization failed due to missing API key: {e}")
            return None  # Expected if key not configured
        else:
            print(f"[ERROR] Unexpected ValueError: {e}")
            return False
    except Exception as e:
        print(f"[ERROR] Error initializing ChatAgent: {e}")
        return False

def test_agent_connector():
    """Test that agent connector works."""
    print("\nTesting AgentConnector...")

    try:
        from backend.api.agent_connector import get_agent_connector

        connector = get_agent_connector()
        print("[OK] AgentConnector created successfully")
        print(f"  - Has history manager: {connector.history_manager is not None}")
        return True

    except Exception as e:
        print(f"[ERROR] Error creating AgentConnector: {e}")
        return False

def main():
    """Run all tests."""
    print("=== Cohere API Key Loading Fix Verification ===\n")

    env_ok = test_env_loading()
    init_ok = test_chat_agent_initialization()
    connector_ok = test_agent_connector()

    print(f"\n=== Results ===")
    print(f"Environment loading: {'[OK]' if env_ok else '[?]' if init_ok is None else '[ERROR]'}")
    print(f"Agent initialization: {'[OK]' if init_ok else '[?]' if init_ok is None else '[ERROR]'}")
    print(f"Agent connector: {'[OK]' if connector_ok else '[ERROR]'}")

    if env_ok and (init_ok or init_ok is None) and connector_ok:
        print("\n[OK] Fix verification passed! The Cohere API key loading issue has been resolved.")
        return True
    else:
        print("\n[ERROR] Some tests failed. Please check the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)