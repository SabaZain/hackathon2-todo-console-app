"""
Persistence Handler for Todo AI Chatbot API.

This module ensures conversations survive server restarts by managing persistent storage.
"""

import asyncio
import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from pathlib import Path


class PersistenceHandler:
    """Handles persistence of conversations to ensure they survive server restarts."""

    def __init__(self, storage_directory: Optional[str] = None):
        """
        Initialize the persistence handler.

        Args:
            storage_directory: Directory to store persistent data (defaults to ./storage)
        """
        self.storage_directory = Path(storage_directory or "./storage")
        self.storage_directory.mkdir(exist_ok=True)

        # Subdirectory for conversations
        self.conversation_storage = self.storage_directory / "conversations"
        self.conversation_storage.mkdir(exist_ok=True)

    async def save_conversation_state(self, conversation_id: str, state_data: Dict[str, Any]) -> bool:
        """
        Save the state of a conversation to persistent storage.

        Args:
            conversation_id: The ID of the conversation
            state_data: The state data to save

        Returns:
            True if successfully saved
        """
        try:
            # Add timestamp to the state data
            state_with_timestamp = {
                **state_data,
                "saved_at": datetime.utcnow().isoformat(),
                "conversation_id": conversation_id
            }

            # Create file path
            file_path = self.conversation_storage / f"{conversation_id}.json"

            # Write state data to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(state_with_timestamp, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving conversation state: {str(e)}")
            return False

    async def load_conversation_state(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Load the state of a conversation from persistent storage.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            The state data if found, None otherwise
        """
        try:
            # Create file path
            file_path = self.conversation_storage / f"{conversation_id}.json"

            # Check if file exists
            if not file_path.exists():
                return None

            # Read state data from file
            with open(file_path, 'r', encoding='utf-8') as f:
                state_data = json.load(f)

            return state_data
        except Exception as e:
            print(f"Error loading conversation state: {str(e)}")
            return None

    async def delete_conversation_state(self, conversation_id: str) -> bool:
        """
        Delete the persistent state of a conversation.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            True if successfully deleted
        """
        try:
            # Create file path
            file_path = self.conversation_storage / f"{conversation_id}.json"

            # Check if file exists and remove it
            if file_path.exists():
                file_path.unlink()

            return True
        except Exception as e:
            print(f"Error deleting conversation state: {str(e)}")
            return False

    async def list_saved_conversations(self) -> List[str]:
        """
        List all conversation IDs that have been saved.

        Returns:
            List of conversation IDs
        """
        try:
            conversation_files = list(self.conversation_storage.glob("*.json"))
            conversation_ids = []

            for file_path in conversation_files:
                # Extract conversation ID from filename (without .json extension)
                conversation_id = file_path.stem
                conversation_ids.append(conversation_id)

            return conversation_ids
        except Exception as e:
            print(f"Error listing saved conversations: {str(e)}")
            return []

    async def cleanup_old_conversations(self, days_to_keep: int = 30) -> int:
        """
        Clean up conversation files older than the specified number of days.

        Args:
            days_to_keep: Number of days to keep conversation files

        Returns:
            Number of files cleaned up
        """
        import time

        try:
            current_time = time.time()
            seconds_per_day = 24 * 60 * 60
            cutoff_time = current_time - (days_to_keep * seconds_per_day)

            conversation_files = list(self.conversation_storage.glob("*.json"))
            cleaned_count = 0

            for file_path in conversation_files:
                # Get file modification time
                mod_time = file_path.stat().st_mtime

                if mod_time < cutoff_time:
                    file_path.unlink()
                    cleaned_count += 1

            return cleaned_count
        except Exception as e:
            print(f"Error cleaning up old conversations: {str(e)}")
            return 0

    async def save_user_session_data(self, user_id: str, session_data: Dict[str, Any]) -> bool:
        """
        Save user-specific session data to persistent storage.

        Args:
            user_id: The ID of the user
            session_data: The session data to save

        Returns:
            True if successfully saved
        """
        try:
            # Create user data subdirectory
            user_storage = self.storage_directory / "users"
            user_storage.mkdir(exist_ok=True)

            # Add timestamp to the session data
            session_with_timestamp = {
                **session_data,
                "saved_at": datetime.utcnow().isoformat(),
                "user_id": user_id
            }

            # Create file path
            file_path = user_storage / f"{user_id}_session.json"

            # Write session data to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_with_timestamp, f, indent=2, ensure_ascii=False)

            return True
        except Exception as e:
            print(f"Error saving user session data: {str(e)}")
            return False

    async def load_user_session_data(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Load user-specific session data from persistent storage.

        Args:
            user_id: The ID of the user

        Returns:
            The session data if found, None otherwise
        """
        try:
            # Create user data subdirectory
            user_storage = self.storage_directory / "users"

            # Create file path
            file_path = user_storage / f"{user_id}_session.json"

            # Check if file exists
            if not file_path.exists():
                return None

            # Read session data from file
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            return session_data
        except Exception as e:
            print(f"Error loading user session data: {str(e)}")
            return None

    async def backup_all_data(self, backup_directory: str) -> bool:
        """
        Create a backup of all persistent data.

        Args:
            backup_directory: Directory to store the backup

        Returns:
            True if backup was successful
        """
        import shutil

        try:
            backup_path = Path(backup_directory)
            backup_path.mkdir(parents=True, exist_ok=True)

            # Copy the entire storage directory
            backup_storage_path = backup_path / "storage_backup"
            if backup_storage_path.exists():
                shutil.rmtree(backup_storage_path)

            shutil.copytree(self.storage_directory, backup_storage_path)

            return True
        except Exception as e:
            print(f"Error creating backup: {str(e)}")
            return False

    async def restore_from_backup(self, backup_directory: str) -> bool:
        """
        Restore persistent data from a backup.

        Args:
            backup_directory: Directory containing the backup

        Returns:
            True if restoration was successful
        """
        import shutil

        try:
            backup_path = Path(backup_directory)
            backup_storage_path = backup_path / "storage_backup"

            if not backup_storage_path.exists():
                return False

            # Remove current storage and copy from backup
            if self.storage_directory.exists():
                shutil.rmtree(self.storage_directory)

            shutil.copytree(backup_storage_path, self.storage_directory)

            return True
        except Exception as e:
            print(f"Error restoring from backup: {str(e)}")
            return False

    async def get_storage_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the persistent storage.

        Returns:
            Dictionary with storage statistics
        """
        try:
            total_size = 0
            file_count = 0

            for file_path in self.storage_directory.rglob("*"):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1

            stats = {
                "total_files": file_count,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "storage_path": str(self.storage_directory.absolute()),
                "timestamp": datetime.utcnow().isoformat()
            }

            return stats
        except Exception as e:
            print(f"Error getting storage stats: {str(e)}")
            return {"error": str(e)}

    def is_persistence_available(self) -> bool:
        """
        Check if persistent storage is available.

        Returns:
            True if storage directory is accessible
        """
        try:
            # Test if we can write to the directory
            test_file = self.storage_directory / ".test_write"
            test_file.touch()
            test_file.unlink()
            return True
        except Exception:
            return False


class APIPersistenceHandler:
    """Persistence handler specifically for API-level operations."""

    def __init__(self, persistence_handler: Optional[PersistenceHandler] = None):
        """
        Initialize the API persistence handler.

        Args:
            persistence_handler: Optional existing PersistenceHandler instance
        """
        self.persistence_handler = persistence_handler or PersistenceHandler()

    async def ensure_conversation_survives_restart(self, conversation_id: str,
                                                 conversation_data: Dict[str, Any]) -> bool:
        """
        Ensure a conversation survives server restarts by persisting it.

        Args:
            conversation_id: The ID of the conversation
            conversation_data: The conversation data to persist

        Returns:
            True if successfully persisted
        """
        return await self.persistence_handler.save_conversation_state(conversation_id, conversation_data)

    async def load_conversation_if_exists(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Load a conversation if it exists in persistent storage.

        Args:
            conversation_id: The ID of the conversation

        Returns:
            The conversation data if it exists, None otherwise
        """
        return await self.persistence_handler.load_conversation_state(conversation_id)

    async def cleanup_on_shutdown(self) -> bool:
        """
        Perform cleanup operations before shutdown.

        Returns:
            True if cleanup was successful
        """
        # In a real implementation, this would handle any necessary cleanup
        # For now, just return True
        return True


def get_persistence_handler(storage_directory: Optional[str] = None) -> PersistenceHandler:
    """
    Get an instance of the persistence handler.

    Args:
        storage_directory: Optional directory for storage

    Returns:
        PersistenceHandler instance
    """
    return PersistenceHandler(storage_directory)


def get_api_persistence_handler(persistence_handler: Optional[PersistenceHandler] = None) -> APIPersistenceHandler:
    """
    Get an instance of the API persistence handler.

    Args:
        persistence_handler: Optional existing PersistenceHandler instance

    Returns:
        APIPersistenceHandler instance
    """
    return APIPersistenceHandler(persistence_handler)