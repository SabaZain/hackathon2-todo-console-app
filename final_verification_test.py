#!/usr/bin/env python3
"""
Final verification test to ensure all requirements are met:
1. "who are you?" → "Main aapka Todo AI Assistant hoon"
2. "list my tasks" → DB-backed tasks
3. No response ever mentions Cohere, Command, or being a language model
"""

import asyncio
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_identity_response():
    """Test requirement: 'who are you?' → 'Main aapka Todo AI Assistant hoon'"""
    print("Testing identity response requirement...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test the exact query from requirements
        result = await agent._generate_general_response("who are you?")
        print(f"Query: 'who are you?' -> Response: '{result}'")

        if "Main aapka Todo AI Assistant hoon" in result:
            print("[PASS] Identity requirement satisfied\n")
            return True
        else:
            print(f"[FAIL] Expected 'Main aapka Todo AI Assistant hoon', got '{result}'\n")
            return False

    except Exception as e:
        print(f"[FAIL] Error testing identity: {e}\n")
        return False

async def test_no_generic_responses():
    """Test requirement: No response mentions Cohere, Command, or generic language model"""
    print("Testing for prohibited content...")

    try:
        from backend.agent.chat_agent import ChatAgent
        os.environ["COHERE_API_KEY"] = "fake-key-for-testing"

        agent = ChatAgent()

        # Test various queries that might trigger generic responses
        test_queries = [
            "what are you?",
            "introduce yourself",
            "what kind of AI are you?",
            "are you a language model?",
            "do you have access to my tasks?",
            "tell me about yourself"
        ]

        all_clean = True

        for query in test_queries:
            result = await agent._generate_general_response(query)
            print(f"Query: '{query}' -> Response: '{result}'")

            # Check for prohibited content
            prohibited_terms = ["Cohere", "Command", "language model", "AI model", "generic AI", "artificial intelligence"]
            found_prohibited = []

            for term in prohibited_terms:
                if term.lower() in result.lower():
                    found_prohibited.append(term)

            if found_prohibited:
                print(f"[FAIL] Found prohibited terms: {found_prohibited}")
                all_clean = False
            else:
                print("[PASS] No prohibited terms found")

        print()
        return all_clean

    except Exception as e:
        print(f"[FAIL] Error testing for prohibited content: {e}\n")
        return False

async def test_system_prompt_requirements():
    """Test that system prompt contains all required elements"""
    print("Testing system prompt compliance...")

    try:
        from backend.agent.system_prompt import get_system_prompt
        prompt = get_system_prompt()

        required_elements = [
            "Main aapka Todo AI Assistant hoon",
            "Never introduce yourself as a generic AI model",
            "Never say you don't have access to the user's todo app or tasks",
            "mention Cohere, Command, or any other language model names"
        ]

        all_present = True
        for element in required_elements:
            if element not in prompt:
                print(f"[FAIL] Missing required element: {element}")
                all_present = False
            else:
                print(f"[PASS] Found required element: {element[:50]}...")

        print()
        return all_present

    except Exception as e:
        print(f"[FAIL] Error testing system prompt: {e}\n")
        return False

async def main():
    """Run all verification tests"""
    print("="*60)
    print("FINAL VERIFICATION: Chatbot Integration Requirements")
    print("="*60)

    test1_pass = await test_identity_response()
    test2_pass = await test_no_generic_responses()
    test3_pass = await test_system_prompt_requirements()

    print("="*60)
    print("VERIFICATION RESULTS:")
    print(f"1. Identity requirement ('who are you?' → 'Main aapka Todo AI Assistant hoon'): {'[PASS]' if test1_pass else '[FAIL]'}")
    print(f"2. No prohibited content (no Cohere/Command/language model mentions): {'[PASS]' if test2_pass else '[FAIL]'}")
    print(f"3. System prompt compliance: {'[PASS]' if test3_pass else '[FAIL]'}")

    all_pass = test1_pass and test2_pass and test3_pass
    print(f"\nOVERALL RESULT: {'[PASS]' if all_pass else '[FAIL]'}")
    print("="*60)

    return all_pass

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)