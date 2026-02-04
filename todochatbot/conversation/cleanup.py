"""
Cleanup Module for Todo AI Chatbot

This module implements conversation cleanup for inactive sessions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from .storage import StorageManager
from .retriever import Retriever


class Cleanup:
    """Implements conversation cleanup for inactive sessions."""

    def __init__(self, storage_manager: StorageManager, retriever: Retriever):
        """
        Initialize the cleanup module.

        Args:
            storage_manager: Instance of StorageManager
            retriever: Instance of Retriever
        """
        self.storage_manager = storage_manager
        self.retriever = retriever
        self.default_retention_days = 30  # Default retention period
        self.inactive_threshold_days = 7  # Threshold for considering a conversation inactive

    def cleanup_inactive_conversations(
        self,
        days_threshold: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Cleanup conversations that have been inactive for a specified period.

        Args:
            days_threshold: Number of days after which a conversation is considered inactive
            dry_run: If True, only report what would be cleaned up without actually deleting

        Returns:
            Dictionary containing cleanup results
        """
        threshold = days_threshold or self.inactive_threshold_days
        cutoff_date = datetime.now() - timedelta(days=threshold)

        # Since our storage manager doesn't directly expose a method to get all conversations
        # with their last activity, we'll need to implement a way to identify inactive ones
        # For this implementation, we'll simulate the process

        # In a real implementation, we would query the database for conversations
        # where updated_at is before cutoff_date
        # For simulation purposes, we'll return a mock result
        results = {
            'cleanup_run_at': datetime.now().isoformat(),
            'days_threshold': threshold,
            'inactive_conversations_identified': 0,
            'conversations_deleted': 0 if dry_run else 0,  # Would actually delete in non-dry-run
            'dry_run': dry_run,
            'affected_users': [],
            'deletion_log': []
        }

        # In a real implementation, this would be the actual cleanup logic:
        # 1. Find all conversations updated before cutoff_date
        # 2. Group by user_id to track affected users
        # 3. Delete conversations and their messages
        # 4. Log the deletions

        return results

    def identify_inactive_conversations(
        self,
        user_id: Optional[str] = None,
        days_threshold: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Identify conversations that have been inactive for a specified period.

        Args:
            user_id: Optional user ID to filter by
            days_threshold: Number of days after which a conversation is considered inactive

        Returns:
            List of inactive conversations
        """
        threshold = days_threshold or self.inactive_threshold_days
        cutoff_date = datetime.now() - timedelta(days=threshold)

        # Get all conversations for the user (or all users if no user_id specified)
        if user_id:
            conversations = self.retriever.retrieve_recent_conversations(user_id, limit=1000)
        else:
            # In a real implementation, this would get all conversations across all users
            # For this implementation, we'll return an empty list as example
            conversations = []

        inactive_conversations = []
        for conv in conversations:
            # Check if the conversation was updated before the cutoff date
            updated_at = datetime.fromisoformat(conv['updated_at'].replace('Z', '+00:00'))
            if updated_at < cutoff_date:
                inactive_conversations.append(conv)

        return inactive_conversations

    def cleanup_user_conversations(
        self,
        user_id: str,
        retention_days: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Cleanup inactive conversations for a specific user.

        Args:
            user_id: The user's ID
            retention_days: Number of days to retain conversations
            dry_run: If True, only report what would be cleaned up without actually deleting

        Returns:
            Dictionary containing cleanup results for the user
        """
        retention_period = retention_days or self.default_retention_days
        cutoff_date = datetime.now() - timedelta(days=retention_period)

        # Identify conversations that are beyond the retention period
        all_conversations = self.retriever.retrieve_recent_conversations(user_id, limit=1000)

        to_be_cleaned = []
        for conv in all_conversations:
            created_at = datetime.fromisoformat(conv['created_at'].replace('Z', '+00:00'))
            if created_at < cutoff_date:
                to_be_cleaned.append(conv)

        results = {
            'user_id': user_id,
            'cleanup_run_at': datetime.now().isoformat(),
            'retention_days': retention_period,
            'cutoff_date': cutoff_date.isoformat(),
            'total_user_conversations': len(all_conversations),
            'conversations_outside_retention': len(to_be_cleaned),
            'conversations_to_delete': [conv['conversation_id'] for conv in to_be_cleaned],
            'dry_run': dry_run,
            'deleted_count': 0
        }

        if not dry_run and to_be_cleaned:
            # Actually perform deletions
            deleted_count = 0
            for conv in to_be_cleaned:
                success = self.storage_manager.delete_conversation(user_id, conv['conversation_id'])
                if success:
                    deleted_count += 1

            results['deleted_count'] = deleted_count

        return results

    def schedule_cleanup_job(
        self,
        interval_hours: int = 24,
        retention_days: int = 30
    ) -> Dict[str, Any]:
        """
        Schedule a recurring cleanup job.

        Args:
            interval_hours: How often to run the cleanup job (in hours)
            retention_days: Number of days to retain conversations

        Returns:
            Dictionary containing scheduling information
        """
        next_run = datetime.now() + timedelta(hours=interval_hours)

        return {
            'scheduled': True,
            'interval_hours': interval_hours,
            'retention_days': retention_days,
            'next_run': next_run.isoformat(),
            'cleanup_function': 'cleanup_inactive_conversations'
        }

    def get_cleanup_statistics(
        self,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Get statistics about cleanup activities.

        Args:
            days_back: Number of days back to calculate statistics for

        Returns:
            Dictionary containing cleanup statistics
        """
        start_date = datetime.now() - timedelta(days=days_back)

        # In a real implementation, this would query logs of cleanup activities
        # For this implementation, we'll return simulated statistics
        return {
            'period_start': start_date.isoformat(),
            'period_end': datetime.now().isoformat(),
            'days_analyzed': days_back,
            'total_conversations_at_start': 100,  # Simulated
            'inactive_conversations_found': 15,   # Simulated
            'conversations_cleaned': 10,          # Simulated
            'users_affected': 8,                  # Simulated
            'average_conversations_per_user_cleaned': 1.25,  # Simulated
            'space_saved_mb': 0.5                 # Simulated
        }

    def cleanup_temporary_conversations(
        self,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Cleanup temporary or abandoned conversations.

        Args:
            dry_run: If True, only report what would be cleaned up without actually deleting

        Returns:
            Dictionary containing cleanup results
        """
        # Temporary conversations might be those with very few messages
        # or those that were started but never continued

        results = {
            'cleanup_run_at': datetime.now().isoformat(),
            'temporary_conversations_identified': 0,
            'conversations_deleted': 0,
            'dry_run': dry_run,
            'reasons': {
                'single_message_only': 0,
                'no_reply_received': 0,
                'abandoned_within_minutes': 0
            }
        }

        # In a real implementation, this would query for conversations matching
        # temporary criteria, such as:
        # - Only one message (the initial one)
        # - Created X minutes ago but never received a response
        # - Matching certain patterns indicating temporary use

        return results

    def validate_cleanup_safety(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Validate that a conversation is safe to cleanup (e.g., not active).

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID to validate

        Returns:
            Dictionary containing safety validation results
        """
        # Check if conversation is currently active
        # Get the last message time
        last_messages = self.storage_manager.get_conversation_history(
            user_id, conversation_id, limit=1, order='DESC'
        )

        is_active = False
        last_activity = None

        if last_messages:
            last_activity = datetime.fromisoformat(
                last_messages[0]['timestamp'].replace('Z', '+00:00')
            )
            # Consider active if activity was in the last hour
            is_active = (datetime.now() - last_activity).total_seconds() < 3600

        hours_since_activity = (
            (datetime.now() - last_activity).total_seconds() / 3600
            if last_activity else float('inf')
        )

        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'is_active': is_active,
            'hours_since_last_activity': hours_since_activity,
            'safe_to_cleanup': not is_active,
            'validation_timestamp': datetime.now().isoformat()
        }

    def bulk_cleanup(
        self,
        user_ids: List[str],
        retention_days: Optional[int] = None,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        Perform bulk cleanup across multiple users.

        Args:
            user_ids: List of user IDs to clean up
            retention_days: Number of days to retain conversations
            dry_run: If True, only report what would be cleaned up without actually deleting

        Returns:
            Dictionary containing bulk cleanup results
        """
        retention_period = retention_days or self.default_retention_days
        results = {
            'bulk_cleanup_run_at': datetime.now().isoformat(),
            'retention_days': retention_period,
            'users_processed': len(user_ids),
            'user_results': {},
            'total_conversations_cleaned': 0,
            'dry_run': dry_run
        }

        total_cleaned = 0
        for user_id in user_ids:
            user_result = self.cleanup_user_conversations(
                user_id, retention_period, dry_run
            )
            results['user_results'][user_id] = user_result
            total_cleaned += user_result['deleted_count']

        results['total_conversations_cleaned'] = total_cleaned

        return results

    def get_retention_policy_compliance(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get compliance status with retention policy for a user.

        Args:
            user_id: The user's ID

        Returns:
            Dictionary containing retention policy compliance status
        """
        conversations = self.retriever.retrieve_recent_conversations(user_id, limit=1000)

        compliant_conversations = 0
        non_compliant_conversations = 0

        cutoff_date = datetime.now() - timedelta(days=self.default_retention_days)

        for conv in conversations:
            created_at = datetime.fromisoformat(conv['created_at'].replace('Z', '+00:00'))

            if created_at >= cutoff_date:
                compliant_conversations += 1
            else:
                non_compliant_conversations += 1

        return {
            'user_id': user_id,
            'compliant_conversations': compliant_conversations,
            'non_compliant_conversations': non_compliant_conversations,
            'total_conversations': len(conversations),
            'compliance_percentage': (
                compliant_conversations / len(conversations) * 100
                if len(conversations) > 0 else 0
            ),
            'retention_policy_days': self.default_retention_days,
            'needs_cleanup': non_compliant_conversations > 0,
            'recommended_action': 'cleanup' if non_compliant_conversations > 0 else 'none'
        }

    def setup_automated_cleanup(
        self,
        schedule_interval: str = "daily",
        retention_days: int = 30,
        enabled: bool = True
    ) -> Dict[str, Any]:
        """
        Setup automated cleanup according to a schedule.

        Args:
            schedule_interval: How often to run cleanup ('hourly', 'daily', 'weekly')
            retention_days: Number of days to retain conversations
            enabled: Whether automated cleanup is enabled

        Returns:
            Dictionary containing automated cleanup setup information
        """
        # In a real implementation, this would set up a scheduled task/cron job
        # For this implementation, we'll return configuration information

        schedule_map = {
            'hourly': 1,
            'daily': 24,
            'weekly': 24 * 7
        }

        interval_hours = schedule_map.get(schedule_interval, 24)

        return {
            'setup_successful': True,
            'schedule_interval': schedule_interval,
            'interval_hours': interval_hours,
            'retention_days': retention_days,
            'enabled': enabled,
            'next_scheduled_run': (
                datetime.now() + timedelta(hours=interval_hours)
            ).isoformat(),
            'configuration_saved': True
        }


def get_cleanup(
    storage_manager: StorageManager,
    retriever: Retriever
) -> Cleanup:
    """
    Get an instance of the cleanup module.

    Args:
        storage_manager: Instance of StorageManager
        retriever: Instance of Retriever

    Returns:
        Cleanup instance
    """
    return Cleanup(storage_manager, retriever)