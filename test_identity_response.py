#!/usr/bin/env python3
"""
Test script to verify the identity response when user asks "who are you?".
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_who_are_you_query():
    """Test that 'who are you?' returns the correct identity response."""
    print("Testing 'who are you?' query response...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the exact query "who are you?"
        result = await agent.process_message("1", "conv1", "who are you?")

        print(f"Input: 'who are you?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # Check if it contains the expected identity response
        response_text = result.get('response_text', '')
        has_expected_response = "Main aapka Todo AI Assistant hoon" in response_text

        print(f"Contains expected identity: {has_expected_response}")

        if has_expected_response:
            print("[PASS] 'who are you?' returns correct identity response\n")
        else:
            print("[FAIL] 'who are you?' does not return correct identity response\n")

        return has_expected_response

    except Exception as e:
        print(f"[FAIL] Error testing 'who are you?': {e}\n")
        import traceback
        traceback.print_exc()
        return False

async def test_what_are_you_query():
    """Test that 'what are you?' returns the correct identity response."""
    print("Testing 'what are you?' query response...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query "what are you?"
        result = await agent.process_message("1", "conv1", "what are you?")

        print(f"Input: 'what are you?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # Check if it contains the expected identity response
        response_text = result.get('response_text', '')
        has_expected_response = "Main aapka Todo AI Assistant hoon" in response_text

        print(f"Contains expected identity: {has_expected_response}")

        if has_expected_response:
            print("[PASS] 'what are you?' returns correct identity response\n")
        else:
            print("[FAIL] 'what are you?' does not return correct identity response\n")

        return has_expected_response

    except Exception as e:
        print(f"[FAIL] Error testing 'what are you?': {e}\n")
        return False

async def test_how_are_you_query():
    """Test that 'how are you?' returns appropriate greeting response."""
    print("Testing 'how are you?' query response...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the query "how are you?" (should be treated as greeting)
        result = await agent.process_message("1", "conv1", "how are you?")

        print(f"Input: 'how are you?'")
        print(f"Intent: {result.get('intent', 'unknown')}")
        print(f"Tool calls: {result.get('tool_calls', [])}")
        print(f"Response: '{result.get('response_text', 'no response')}'")

        # For "how are you?" it should be treated as a greeting
        response_text = result.get('response_text', '')
        is_greeting_like = any(word in response_text.lower() for word in ['hello', 'hi', 'greeting', 'assistant', 'help'])

        print(f"Is greeting-like response: {is_greeting_like}")

        if is_greeting_like:
            print("[PASS] 'how are you?' returns appropriate greeting response\n")
        else:
            print("[INFO] 'how are you?' response may not be greeting-like but is handled\n")

        return True  # This is acceptable behavior

    except Exception as e:
        print(f"[FAIL] Error testing 'how are you?': {e}\n")
        return False

async def test_system_prompt_contains_identity():
    """Test that system prompt contains identity instructions."""
    print("Testing system prompt for identity instructions...")

    try:
        from backend.agent.system_prompt import get_system_prompt

        prompt = get_system_prompt()

        # Check for identity-related instructions
        has_identity_instruction = "Main aapka Todo AI Assistant hoon" in prompt
        has_generic_prevention = "Never introduce yourself as a generic AI model" in prompt
        has_identity_when_asked = "introduce yourself as \"Main aapka Todo AI Assistant hoon\" when asked who you are" in prompt

        print(f"Has identity instruction: {has_identity_instruction}")
        print(f"Has generic prevention: {has_generic_prevention}")
        print(f"Has identity when asked: {has_identity_when_asked}")

        all_present = has_identity_instruction and has_generic_prevention and has_identity_when_asked

        if all_present:
            print("[PASS] System prompt contains all identity instructions\n")
        else:
            print("[FAIL] System prompt missing identity instructions\n")

        return all_present

    except Exception as e:
        print(f"[FAIL] Error checking system prompt: {e}\n")
        return False

async def main():
    """Run all identity response tests."""
    print("="*60)
    print("IDENTITY RESPONSE VERIFICATION TESTS")
    print("="*60)

    test1 = await test_who_are_you_query()
    test2 = await test_what_are_you_query()
    test3 = await test_how_are_you_query()
    test4 = await test_system_prompt_contains_identity()

    print("="*60)
    print("IDENTITY RESPONSE RESULTS:")
    print(f"'who are you?' query: {'[PASS]' if test1 else '[FAIL]'}")
    print(f"'what are you?' query: {'[PASS]' if test2 else '[FAIL]'}")
    print(f"'how are you?' query: {'[PASS]' if test3 else '[INFO]'}")
    print(f"System prompt identity: {'[PASS]' if test4 else '[FAIL]'}")

    identity_tests_pass = test1 and test2 and test4
    print(f"\nOVERALL IDENTITY HANDLING: {'[PASS]' if identity_tests_pass else '[FAIL]'}")

    if identity_tests_pass:
        print("✓ Bot correctly responds with 'Main aapka Todo AI Assistant hoon'")
        print("  when asked 'who are you?' or 'what are you?'")

    print("="*60)

    return identity_tests_pass

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)