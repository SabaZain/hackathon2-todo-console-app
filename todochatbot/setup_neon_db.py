#!/usr/bin/env python3
"""
Script to set up the Neon database with correct schema
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

def setup_database():
    """Set up the database with correct schema"""
    print("Setting up PostgreSQL (Neon) database with correct schema...")

    # Get database connection string
    db_url = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_kLl6eaUMti8Y@ep-snowy-mode-a7iblijc-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
    )

    print(f"Connecting to: {db_url}")

    try:
        # Connect to the database
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        print("Connected to database successfully!")

        # Drop tables if they exist (cascade to handle dependencies)
        print("Dropping existing tables if they exist...")
        cursor.execute("DROP TABLE IF EXISTS messages CASCADE")
        cursor.execute("DROP TABLE IF EXISTS conversations CASCADE")

        # Create conversations table with correct schema
        print("Creating conversations table...")
        cursor.execute("""
            CREATE TABLE conversations (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255) NOT NULL,
                title VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create messages table with correct schema and foreign key
        print("Creating messages table...")
        cursor.execute("""
            CREATE TABLE messages (
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
        print("Creating indexes...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_messages_conv_user ON messages (conversation_id, user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations (user_id)")

        # Commit the changes
        conn.commit()
        print("Database schema created successfully!")

        # Test the schema by inserting and retrieving data
        print("Testing schema with sample data...")

        import uuid
        test_user_id = f"test_user_{uuid.uuid4().hex[:8]}"
        conversation_id = str(uuid.uuid4())

        # Insert a conversation
        cursor.execute("""
            INSERT INTO conversations (id, user_id, title, created_at, updated_at)
            VALUES (%s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
        """, (conversation_id, test_user_id, "Test Conversation"))

        # Insert a message
        message_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO messages (id, conversation_id, user_id, role, content, timestamp)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """, (message_id, conversation_id, test_user_id, "user", "Test message for verification"))

        # Retrieve the data
        cursor.execute("""
            SELECT id, user_id, conversation_id, role, content
            FROM messages
            WHERE conversation_id = %s AND user_id = %s
        """, (conversation_id, test_user_id))

        rows = cursor.fetchall()
        print(f"Retrieved {len(rows)} messages from test conversation")

        # Clean up test data
        cursor.execute("DELETE FROM conversations WHERE id = %s", (conversation_id,))

        conn.commit()
        print("Schema test completed successfully!")

        cursor.close()
        conn.close()

        print("\n[OK] PostgreSQL (Neon) database is ready with correct schema!")
        print("[OK] Tables created with proper VARCHAR(255) types for IDs")
        print("[OK] Foreign key relationships established")
        print("[OK] Indexes created for performance")

        return True

    except Exception as e:
        print(f"[ERROR] Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = setup_database()
    if not success:
        sys.exit(1)