"""
Database module for conversation persistence in Todo AI Chatbot.

This module provides functions for saving and loading conversation messages
using ONLY PostgreSQL database (Neon).
"""

import os
import json
import datetime
import uuid
from typing import Dict, List, Optional
from dataclasses import dataclass
from typing import Union

# Import PostgreSQL adapter - this is now mandatory
import psycopg2
from psycopg2.extras import RealDictCursor

# Log database connection at startup
print("Connecting to PostgreSQL (Neon) database...")
print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')}")

@dataclass
class Conversation:
    """Represents a conversation with metadata."""
    id: str
    user_id: str
    created_at: str
    updated_at: str
    title: Optional[str] = None

@dataclass
class Message:
    """Represents a message in a conversation."""
    id: str
    conversation_id: str
    user_id: str
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str

class DatabaseManager:
    """Manages database connections and operations for conversations."""

    def __init__(self):
        """Initialize the database manager with connection details."""
        self.connection_string = os.getenv(
            "DATABASE_URL",
            "postgresql://neondb_owner:npg_kLl6eaUMti8Y@ep-snowy-mode-a7iblijc-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
        )

        # Force PostgreSQL - no SQLite allowed
        if self.connection_string.startswith("sqlite://"):
            raise Exception("SQLite is not allowed. Please configure PostgreSQL database.")

        print("Connected to PostgreSQL (Neon) successfully")
        self.init_database()

    def get_connection(self):
        """Get a PostgreSQL database connection."""
        return psycopg2.connect(self.connection_string)

    def init_database(self):
        """Initialize the database with required tables."""
        conn = self.get_connection()

        # PostgreSQL specific table creation
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("""
            SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename IN ('conversations', 'messages')
        """)
        existing_tables = [row[0] for row in cursor.fetchall()]

        if 'conversations' in existing_tables or 'messages' in existing_tables:
            print("Tables already exist. Verifying schema...")

            # Verify that the tables have the correct schema by checking column types
            cursor.execute("""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = 'conversations' AND column_name = 'id'
            """)
            id_cols = cursor.fetchall()

            if id_cols and id_cols[0][1] != 'character varying':
                print("Schema mismatch detected: conversations.id is not VARCHAR. Recreating tables...")

                # Drop foreign key constraints first
                try:
                    cursor.execute("ALTER TABLE messages DROP CONSTRAINT IF EXISTS fk_messages_conversation")
                except:
                    pass

                # Drop existing tables to recreate with proper schema
                cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
                cursor.execute("DROP TABLE IF EXISTS conversations CASCADE")

        # Create conversations table with correct schema (only if it doesn't exist)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                title VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create messages table with correct schema and foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id VARCHAR(255) PRIMARY KEY,
                conversation_id VARCHAR(255) NOT NULL,
                user_id VARCHAR(255) NOT NULL,
                role VARCHAR(50) NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_messages_conversation
                    FOREIGN KEY (conversation_id)
                    REFERENCES conversations(id)
                    ON DELETE CASCADE
            )
        """)

        # Create indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conv_user ON messages (conversation_id, user_id)")
        except:
            pass

        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations (user_id)")
        except:
            pass

        conn.commit()
        cursor.close()
        conn.close()

    def save_message(self, user_id: str, conversation_id: str, content: str, role: str) -> str:
        """Save a message to the database."""
        conn = self.get_connection()
        message_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        cursor = conn.cursor()

        # Check if all expected columns exist
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'messages' AND column_name = 'role'
        """)
        role_column_exists = cursor.fetchone() is not None

        if role_column_exists:
            cursor.execute(
                "INSERT INTO messages (id, conversation_id, user_id, role, content, timestamp) VALUES (%s, %s, %s, %s, %s, %s)",
                (message_id, conversation_id, user_id, role, content, timestamp)
            )
        else:
            # Insert without role column if it doesn't exist
            cursor.execute(
                "INSERT INTO messages (id, conversation_id, user_id, content, timestamp) VALUES (%s, %s, %s, %s, %s)",
                (message_id, conversation_id, user_id, content, timestamp)
            )

        conn.commit()
        cursor.close()

        conn.close()
        return message_id

    def load_conversation(self, user_id: str, conversation_id: str) -> List[Dict]:
        """Load all messages for a specific conversation."""
        conn = self.get_connection()

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT id, user_id, conversation_id, role, content, timestamp FROM messages WHERE conversation_id = %s AND user_id = %s ORDER BY timestamp ASC",
            (conversation_id, user_id)
        )
        rows = cursor.fetchall()
        cursor.close()

        conn.close()

        messages = []
        for row in rows:
            # For PostgreSQL, row is a dict-like object
            message = dict(row)
            messages.append(message)

        return messages

    def get_user_conversations(self, user_id: str) -> List[Dict]:
        """Get all conversations for a user."""
        conn = self.get_connection()

        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(
            "SELECT id, user_id, title, created_at, updated_at FROM conversations WHERE user_id = %s ORDER BY updated_at DESC",
            (user_id,)
        )
        rows = cursor.fetchall()
        cursor.close()

        conn.close()

        conversations = []
        for row in rows:
            # For PostgreSQL, row is a dict-like object
            conv = dict(row)
            conversations.append(conv)

        return conversations

    def create_conversation(self, user_id: str, title: Optional[str] = None) -> str:
        """Create a new conversation and return its ID."""
        conn = self.get_connection()
        conversation_id = str(uuid.uuid4())
        timestamp = datetime.datetime.now().isoformat()

        cursor = conn.cursor()

        # Check if title column exists
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'conversations' AND column_name = 'title'
        """)
        title_column_exists = cursor.fetchone() is not None

        if title_column_exists:
            cursor.execute(
                "INSERT INTO conversations (id, user_id, title, created_at, updated_at) VALUES (%s, %s, %s, %s, %s)",
                (conversation_id, user_id, title, timestamp, timestamp)
            )
        else:
            # Insert without title column
            cursor.execute(
                "INSERT INTO conversations (id, user_id, created_at, updated_at) VALUES (%s, %s, %s, %s)",
                (conversation_id, user_id, timestamp, timestamp)
            )

        conn.commit()
        cursor.close()

        conn.close()
        return conversation_id

    def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        """Delete a conversation and all its messages."""
        conn = self.get_connection()

        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM conversations WHERE id = %s AND user_id = %s",
            (conversation_id, user_id)
        )
        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()

        conn.close()
        return affected_rows > 0

# Create a global instance of the database manager
db_manager = DatabaseManager()


def save_message(user_id: str, conversation_id: str, content: str, role: str) -> str:
    """Public function to save a message."""
    return db_manager.save_message(user_id, conversation_id, content, role)


def load_conversation(user_id: str, conversation_id: str) -> List[Dict]:
    """Public function to load a conversation."""
    return db_manager.load_conversation(user_id, conversation_id)


def get_user_conversations(user_id: str) -> List[Dict]:
    """Public function to get all conversations for a user."""
    return db_manager.get_user_conversations(user_id)


def create_conversation(user_id: str, title: Optional[str] = None) -> str:
    """Public function to create a new conversation."""
    return db_manager.create_conversation(user_id, title)


def create_new_conversation(user_id: str, title: Optional[str] = None) -> str:
    """Public function to create a new conversation (alias for create_conversation)."""
    return db_manager.create_conversation(user_id, title)


def delete_conversation(user_id: str, conversation_id: str) -> bool:
    """Public function to delete a conversation."""
    return db_manager.delete_conversation(user_id, conversation_id)


def get_conversation_summary(user_id: str, conversation_id: str) -> Dict:
    """Public function to get a summary of a conversation."""
    conn = db_manager.get_connection()

    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute(
        "SELECT COUNT(*) as message_count, MIN(timestamp) as first_message, MAX(timestamp) as last_message FROM messages WHERE conversation_id = %s AND user_id = %s",
        (conversation_id, user_id)
    )
    row = cursor.fetchone()
    cursor.close()

    conn.close()

    # For PostgreSQL, row is a dict-like object
    summary = dict(row)

    return summary