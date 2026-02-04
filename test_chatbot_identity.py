#!/usr/bin/env python3
"""
Test script to verify that the chatbot responds with the correct identity
and doesn't mention Cohere or generic language model responses.
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_agent_identity():
    """Test that the agent identifies itself correctly."""
    print("Testing agent identity response...")

    try:
        # Import the chat agent
        from backend.agent.chat_agent import ChatAgent

        # Set a fake API key for testing (we won't actually call Cohere in this test)
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        # Create the agent
        agent = ChatAgent()

        # Test identity question in English
        print("\nTesting 'who are you?' query...")
        result = await agent._generate_general_response("who are you?")
        print(f"Response: {result}")

        # Check if it contains the correct identity
        if "Main aapka Todo AI Assistant hoon" in result:
            print("[PASS] English identity response is correct!")
        else:
            print("[FAIL] English identity response is incorrect")

        # Test identity question in English with question mark
        print("\nTesting 'who are you?' query with question mark...")
        result2 = await agent._generate_general_response("who are you?")
        print(f"Response: {result2}")

        # Check if it contains the correct identity
        if "Main aapka Todo AI Assistant hoon" in result2:
            print("[PASS] English identity response (with ?) is correct!")
        else:
            print("[FAIL] English identity response (with ?) is incorrect")

        # Test with "what are you"
        print("\nTesting 'what are you?' query...")
        result3 = await agent._generate_general_response("what are you?")
        print(f"Response: {result3}")

        # Check if it contains the correct identity
        if "Main aapka Todo AI Assistant hoon" in result3:
            print("[PASS] 'What are you' response is correct!")
        else:
            print("[FAIL] 'What are you' response is incorrect")

        # Test a non-identity question to make sure normal functionality still works
        print("\nTesting non-identity query...")
        result4 = await agent._generate_general_response("What can you help me with?")
        print(f"Response: {result4}")

        # Should not contain identity response for non-identity questions
        if "Main aapka Todo AI Assistant hoon" not in result4:
            print("[PASS] Non-identity query response is correct (doesn't show identity unnecessarily)")
        else:
            print("[FAIL] Non-identity query incorrectly shows identity")

        return True

    except Exception as e:
        print(f"[FAIL] Error during identity test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_system_prompt_enforcement():
    """Test that the system prompt is properly enforced."""
    print("\n\nTesting system prompt enforcement...")

    try:
        from backend.agent.system_prompt import get_system_prompt

        prompt = get_system_prompt()

        # Check for required elements
        required_elements = [
            "Main aapka Todo AI Assistant hoon",
            "Never introduce yourself as a generic AI model",
            "Never say you don't have access to the user's todo app or tasks",
            "Under no circumstances should you mention Cohere, Command, or any other language model names"
        ]

        all_present = True
        for element in required_elements:
            if element not in prompt:
                print(f"[FAIL] Missing required element: {element}")
                all_present = False
            else:
                print(f"[PASS] Found required element: {element[:50]}...")

        if all_present:
            print("[PASS] All required system prompt elements are present!")
            return True
        else:
            print("[FAIL] Some required elements are missing")
            return False

    except Exception as e:
        print(f"[FAIL] Error during system prompt test: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("=== Testing Chatbot Identity and System Prompt Enforcement ===\n")

    identity_ok = await test_agent_identity()
    prompt_ok = await test_system_prompt_enforcement()

    print(f"\n=== Results ===")
    print(f"Identity test: {'[PASS]' if identity_ok else '[FAIL]'}")
    print(f"System prompt test: {'[PASS]' if prompt_ok else '[FAIL]'}")

    overall_success = identity_ok and prompt_ok
    print(f"Overall: {'[PASS]' if overall_success else '[FAIL]'}")

    return overall_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)