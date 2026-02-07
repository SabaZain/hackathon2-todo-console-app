"""
Storage Manager for Todo AI Chatbot

This module manages conversation storage in the database with proper indexing.
"""

from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import sqlite3
import json
from pathlib import Path


class StorageManager:
    """Manages conversation storage in the database with proper indexing."""

    def __init__(self, db_path: str = "conversations.db"):
        """
        Initialize the storage manager.

        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database with required tables and indexes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                conversation_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                UNIQUE(user_id, conversation_id)
            )
        """)

        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(conversation_id)
            )
        """)

        # Create indexes for better performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_conversation ON conversations(user_id, conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversation_created ON conversations(conversation_id, created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)")

        conn.commit()
        conn.close()

    def store_conversation(
        self,
        user_id: str,
        conversation_id: str,
        messages: List[Dict[str, Any]],
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a conversation with its messages in the database.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            messages: List of message dictionaries
            metadata: Additional metadata about the conversation

        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Upsert conversation record
            cursor.execute("""
                INSERT OR REPLACE INTO conversations
                (user_id, conversation_id, metadata, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (user_id, conversation_id, json.dumps(metadata or {})))

            # Insert messages
            for msg in messages:
                cursor.execute("""
                    INSERT INTO messages
                    (conversation_id, role, content, metadata, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    conversation_id,
                    msg.get('role'),
                    msg.get('content'),
                    json.dumps(msg.get('metadata', {})),
                    msg.get('timestamp', datetime.now().isoformat())
                ))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing conversation: {e}")
            return False

    def store_message(
        self,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Store a single message in a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            role: The role of the message (user, assistant, system)
            content: The content of the message
            metadata: Additional metadata about the message

        Returns:
            Boolean indicating success
        """
        try:
            # First ensure the conversation exists
            self._ensure_conversation_exists(user_id, conversation_id)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO messages
                (conversation_id, role, content, metadata, timestamp)
                VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            """, (conversation_id, role, content, json.dumps(metadata or {})))

            # Update conversation timestamp
            cursor.execute("""
                UPDATE conversations
                SET updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ? AND conversation_id = ?
            """, (user_id, conversation_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing message: {e}")
            return False

    def _ensure_conversation_exists(self, user_id: str, conversation_id: str):
        """Ensure a conversation record exists in the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR IGNORE INTO conversations
            (user_id, conversation_id, metadata, updated_at)
            VALUES (?, ?, '{}', CURRENT_TIMESTAMP)
        """, (user_id, conversation_id))

        conn.commit()
        conn.close()

    def get_conversation_history(
        self,
        user_id: str,
        conversation_id: str,
        limit: Optional[int] = None,
        order: str = 'ASC'
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a specific conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            limit: Maximum number of messages to return
            order: Order of messages ('ASC' or 'DESC')

        Returns:
            List of message dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            query = """
                SELECT m.role, m.content, m.timestamp, m.metadata
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.conversation_id
                WHERE c.user_id = ? AND c.conversation_id = ?
                ORDER BY m.timestamp {}
            """.format(order)

            params = [user_id, conversation_id]

            if limit:
                query += " LIMIT ?"
                params.append(str(limit))

            cursor.execute(query, params)
            rows = cursor.fetchall()

            messages = []
            for row in rows:
                message = {
                    'role': row[0],
                    'content': row[1],
                    'timestamp': row[2],
                    'metadata': json.loads(row[3]) if row[3] else {}
                }
                messages.append(message)

            conn.close()
            return messages
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []

    def get_recent_conversations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get a list of recent conversations for a user.

        Args:
            user_id: The user's ID
            limit: Maximum number of conversations to return

        Returns:
            List of conversation dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT conversation_id, created_at, updated_at, metadata
                FROM conversations
                WHERE user_id = ?
                ORDER BY updated_at DESC
                LIMIT ?
            """, (user_id, limit))

            rows = cursor.fetchall()

            conversations = []
            for row in rows:
                conv = {
                    'conversation_id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'metadata': json.loads(row[3]) if row[3] else {}
                }
                conversations.append(conv)

            conn.close()
            return conversations
        except Exception as e:
            print(f"Error retrieving recent conversations: {e}")
            return []

    def get_conversation_count(self, user_id: str) -> int:
        """
        Get the total number of conversations for a user.

        Args:
            user_id: The user's ID

        Returns:
            Number of conversations
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM conversations
                WHERE user_id = ?
            """, (user_id,))

            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting conversation count: {e}")
            return 0

    def get_message_count(self, user_id: str, conversation_id: str) -> int:
        """
        Get the total number of messages in a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Number of messages
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT COUNT(*)
                FROM messages m
                JOIN conversations c ON m.conversation_id = c.conversation_id
                WHERE c.user_id = ? AND c.conversation_id = ?
            """, (user_id, conversation_id))

            count = cursor.fetchone()[0]
            conn.close()
            return count
        except Exception as e:
            print(f"Error getting message count: {e}")
            return 0

    def update_conversation_metadata(
        self,
        user_id: str,
        conversation_id: str,
        metadata: Dict[str, Any]
    ) -> bool:
        """
        Update metadata for a conversation.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            metadata: New metadata to update with

        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Get existing metadata
            cursor.execute("""
                SELECT metadata
                FROM conversations
                WHERE user_id = ? AND conversation_id = ?
            """, (user_id, conversation_id))

            row = cursor.fetchone()
            if row:
                existing_metadata = json.loads(row[0]) if row[0] else {}
                # Merge with new metadata
                existing_metadata.update(metadata)

                cursor.execute("""
                    UPDATE conversations
                    SET metadata = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ? AND conversation_id = ?
                """, (json.dumps(existing_metadata), user_id, conversation_id))

                conn.commit()
            else:
                conn.close()
                return False

            conn.close()
            return True
        except Exception as e:
            print(f"Error updating conversation metadata: {e}")
            return False

    def delete_conversation(self, user_id: str, conversation_id: str) -> bool:
        """
        Delete a conversation and all its messages.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Boolean indicating success
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Delete messages first (due to foreign key constraint)
            cursor.execute("""
                DELETE FROM messages
                WHERE conversation_id IN (
                    SELECT conversation_id
                    FROM conversations
                    WHERE user_id = ? AND conversation_id = ?
                )
            """, (user_id, conversation_id))

            # Then delete conversation
            cursor.execute("""
                DELETE FROM conversations
                WHERE user_id = ? AND conversation_id = ?
            """, (user_id, conversation_id))

            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting conversation: {e}")
            return False

    def delete_old_conversations(
        self,
        user_id: str,
        days_old: int
    ) -> int:
        """
        Delete conversations older than specified days.

        Args:
            user_id: The user's ID
            days_old: Delete conversations older than this many days

        Returns:
            Number of conversations deleted
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                DELETE FROM conversations
                WHERE user_id = ? AND created_at < datetime('now', '-{} days')
            """.format(days_old), (user_id,))

            deleted_count = cursor.rowcount

            # Also delete orphaned messages
            cursor.execute("""
                DELETE FROM messages
                WHERE conversation_id NOT IN (
                    SELECT conversation_id FROM conversations
                )
            """)

            conn.commit()
            conn.close()
            return deleted_count
        except Exception as e:
            print(f"Error deleting old conversations: {e}")
            return 0

    def search_conversations(
        self,
        user_id: str,
        search_term: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for conversations containing a specific term.

        Args:
            user_id: The user's ID
            search_term: Term to search for in conversation messages
            limit: Maximum number of results to return

        Returns:
            List of conversation dictionaries with search matches
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT DISTINCT c.conversation_id, c.created_at, c.updated_at, c.metadata,
                       COUNT(m.id) as message_count
                FROM conversations c
                JOIN messages m ON m.conversation_id = c.conversation_id
                WHERE c.user_id = ? AND m.content LIKE ?
                GROUP BY c.conversation_id
                ORDER BY c.updated_at DESC
                LIMIT ?
            """, (user_id, f"%{search_term}%", limit))

            rows = cursor.fetchall()

            conversations = []
            for row in rows:
                conv = {
                    'conversation_id': row[0],
                    'created_at': row[1],
                    'updated_at': row[2],
                    'metadata': json.loads(row[3]) if row[3] else {},
                    'message_count': row[4]
                }
                conversations.append(conv)

            conn.close()
            return conversations
        except Exception as e:
            print(f"Error searching conversations: {e}")
            return []


def get_storage_manager(db_path: str = "conversations.db") -> StorageManager:
    """
    Get an instance of the storage manager.

    Args:
        db_path: Path to the SQLite database file

    Returns:
        StorageManager instance
    """
    return StorageManager(db_path)