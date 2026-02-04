#!/usr/bin/env python3
"""
Test script to verify PostgreSQL (Neon) database connection
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_db_connection():
    """Test the database connection"""
    print("Testing PostgreSQL (Neon) database connection...")

    try:
        # Import the database manager
        from database.conversations import db_manager

        print("[OK] Database manager imported successfully")
        print(f"[OK] Connection string: {db_manager.connection_string[:50]}...")

        # Test creating a connection
        conn = db_manager.get_connection()
        print("[OK] Successfully connected to PostgreSQL database")

        # Test creating a conversation
        import uuid
        test_user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        conversation_id = db_manager.create_conversation(test_user_id, "Test Conversation")
        print(f"[OK] Created test conversation: {conversation_id}")

        # Test saving a message
        message_id = db_manager.save_message(
            test_user_id,
            conversation_id,
            "Test message for verification",
            "user"
        )
        print(f"[OK] Saved test message: {message_id}")

        # Test loading the conversation
        messages = db_manager.load_conversation(test_user_id, conversation_id)
        print(f"[OK] Loaded {len(messages)} messages from conversation")

        # Test getting user conversations
        conversations = db_manager.get_user_conversations(test_user_id)
        print(f"[OK] Found {len(conversations)} conversations for user")

        # Clean up test data
        success = db_manager.delete_conversation(test_user_id, conversation_id)
        print(f"[OK] Cleaned up test conversation: {'Success' if success else 'Failed'}")

        conn.close()
        print("[OK] Database connection test completed successfully")
        print("[OK] PostgreSQL (Neon) database is working properly")

        return True

    except Exception as e:
        print(f"[ERROR] Database connection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_db_connection()
    if success:
        print("\n[SUCCESS] PostgreSQL (Neon) database integration verified!")
    else:
        print("\n[FAILURE] Database connection failed!")
        sys.exit(1)