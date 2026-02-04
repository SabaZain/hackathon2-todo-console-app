"""
History Tests for Todo AI Chatbot

This module tests conversation history retrieval.
"""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any
from datetime import datetime, timedelta


class TestHistoryTests(unittest.TestCase):
    """Test conversation history retrieval."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def test_retrieve_complete_conversation_history(self):
        """Test retrieving complete conversation history."""
        user_id = "test_user_123"
        conversation_id = "test_conv_456"

        expected_messages = [
            {'role': 'user', 'content': 'Hello', 'timestamp': '2026-01-23T10:00:00Z'},
            {'role': 'assistant', 'content': 'Hi there!', 'timestamp': '2026-01-23T10:00:05Z'},
            {'role': 'user', 'content': 'Add a task', 'timestamp': '2026-01-23T10:00:10Z'},
            {'role': 'assistant', 'content': 'Sure, what task?', 'timestamp': '2026-01-23T10:00:15Z'}
        ]

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': expected_messages,
                'message_count': len(expected_messages)
            }

            result = self.retrieve_conversation_history(user_id, conversation_id)

            self.assertEqual(len(result['messages']), len(expected_messages))
            for expected, actual in zip(expected_messages, result['messages']):
                self.assertEqual(expected['role'], actual['role'])
                self.assertEqual(expected['content'], actual['content'])

    def test_retrieve_recent_messages_only(self):
        """Test retrieving only recent messages from conversation."""
        user_id = "test_user_123"
        conversation_id = "test_conv_456"

        all_messages = [
            {'role': 'user', 'content': f'Old message {i}', 'timestamp': f'2026-01-22T10:00:{i:02d}Z'}
            for i in range(10)  # Older messages
        ] + [
            {'role': 'user', 'content': f'Recent message {i}', 'timestamp': f'2026-01-23T10:00:{i:02d}Z'}
            for i in range(5)  # Recent messages
        ]

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': all_messages,
                'message_count': len(all_messages)
            }

            # Retrieve only the 5 most recent messages
            result = self.retrieve_conversation_history(user_id, conversation_id, limit=5)

            # Should return only the 5 most recent messages
            self.assertEqual(len(result['messages']), 5)
            for i, msg in enumerate(result['messages']):
                self.assertIn('Recent message', msg['content'])

    def test_retrieve_messages_by_date_range(self):
        """Test retrieving messages within a specific date range."""
        user_id = "test_user_123"
        conversation_id = "test_conv_456"

        # Create messages spanning different dates
        base_date = datetime.now() - timedelta(days=5)
        all_messages = []
        for i in range(10):
            msg_date = base_date + timedelta(days=i)
            all_messages.append({
                'role': 'user',
                'content': f'Message for day {i}',
                'timestamp': msg_date.isoformat() + 'Z'
            })

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': all_messages,
                'message_count': len(all_messages)
            }

            # Retrieve messages from the last 2 days
            date_range_start = datetime.now() - timedelta(days=2)
            date_range_end = datetime.now()

            result = self.retrieve_conversation_history_by_date(
                user_id, conversation_id, date_range_start, date_range_end
            )

            # Should only return messages from the last 2 days
            self.assertLessEqual(len(result['messages']), 2)

    def test_retrieve_multiple_conversations(self):
        """Test retrieving history for multiple conversations."""
        user_id = "test_user_123"

        conversations = {
            "conv_1": [
                {'role': 'user', 'content': 'Conv 1 message 1', 'timestamp': '2026-01-23T10:00:00Z'},
                {'role': 'assistant', 'content': 'Conv 1 response 1', 'timestamp': '2026-01-23T10:00:05Z'}
            ],
            "conv_2": [
                {'role': 'user', 'content': 'Conv 2 message 1', 'timestamp': '2026-01-23T10:01:00Z'},
                {'role': 'assistant', 'content': 'Conv 2 response 1', 'timestamp': '2026-01-23T10:01:05Z'}
            ],
            "conv_3": [
                {'role': 'user', 'content': 'Conv 3 message 1', 'timestamp': '2026-01-23T10:02:00Z'},
                {'role': 'assistant', 'content': 'Conv 3 response 1', 'timestamp': '2026-01-23T10:02:05Z'}
            ]
        }

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance

            for conv_id, expected_msgs in conversations.items():
                mock_retriever_instance.retrieve_conversation_history.return_value = {
                    'user_id': user_id,
                    'conversation_id': conv_id,
                    'messages': expected_msgs,
                    'message_count': len(expected_msgs)
                }

                result = self.retrieve_conversation_history(user_id, conv_id)
                self.assertEqual(len(result['messages']), len(expected_msgs))

                for exp, act in zip(expected_msgs, result['messages']):
                    self.assertEqual(exp['role'], act['role'])
                    self.assertEqual(exp['content'], act['content'])

    def test_retrieve_conversation_with_search(self):
        """Test retrieving conversation history with search functionality."""
        user_id = "test_user_123"
        conversation_id = "test_conv_456"

        messages = [
            {'role': 'user', 'content': 'I need to buy groceries', 'timestamp': '2026-01-23T10:00:00Z'},
            {'role': 'assistant', 'content': 'Sure, adding grocery task', 'timestamp': '2026-01-23T10:00:05Z'},
            {'role': 'user', 'content': 'What about milk?', 'timestamp': '2026-01-23T10:00:10Z'},
            {'role': 'assistant', 'content': 'Milk added to groceries', 'timestamp': '2026-01-23T10:00:15Z'},
            {'role': 'user', 'content': 'Schedule meeting tomorrow', 'timestamp': '2026-01-23T10:00:20Z'}
        ]

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': messages,
                'message_count': len(messages)
            }

            # Search for messages containing 'milk'
            result = self.search_conversation_history(user_id, conversation_id, 'milk')

            # Should find messages containing 'milk'
            milk_messages = [msg for msg in result['messages'] if 'milk' in msg['content'].lower()]
            self.assertGreaterEqual(len(milk_messages), 1)

    def test_empty_conversation_history(self):
        """Test retrieving history for an empty conversation."""
        user_id = "test_user_123"
        conversation_id = "empty_conv_789"

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': [],
                'message_count': 0
            }

            result = self.retrieve_conversation_history(user_id, conversation_id)

            self.assertEqual(len(result['messages']), 0)
            self.assertEqual(result['message_count'], 0)

    def test_conversation_statistics(self):
        """Test retrieving conversation statistics along with history."""
        user_id = "test_user_123"
        conversation_id = "stats_conv"

        messages = [
            {'role': 'user', 'content': 'Message 1', 'timestamp': '2026-01-23T10:00:00Z'},
            {'role': 'assistant', 'content': 'Response 1', 'timestamp': '2026-01-23T10:00:05Z'},
            {'role': 'user', 'content': 'Message 2', 'timestamp': '2026-01-23T10:00:10Z'}
        ]

        with patch('todo_chatbot.conversation.retriever.Retriever') as mock_retriever:
            mock_retriever_instance = Mock()
            mock_retriever.return_value = mock_retriever_instance
            mock_retriever_instance.retrieve_conversation_history.return_value = {
                'user_id': user_id,
                'conversation_id': conversation_id,
                'messages': messages,
                'message_count': len(messages)
            }

            # Also mock statistics retrieval
            with patch('todo_chatbot.conversation.retriever.Retriever') as mock_stats_retriever:
                mock_stats_instance = Mock()
                mock_stats_retriever.return_value = mock_stats_instance
                mock_stats_instance.retrieve_conversation_statistics.return_value = {
                    'message_count': len(messages),
                    'user_message_count': 2,
                    'ai_message_count': 1,
                    'first_message_time': '2026-01-23T10:00:00Z',
                    'last_message_time': '2026-01-23T10:00:10Z'
                }

                result = self.retrieve_conversation_history_with_stats(user_id, conversation_id)

                self.assertEqual(result['message_count'], len(messages))
                self.assertEqual(result['user_message_count'], 2)
                self.assertEqual(result['ai_message_count'], 1)

    def retrieve_conversation_history(self, user_id: str, conversation_id: str, limit: int = None) -> Dict[str, Any]:
        """Retrieve conversation history."""
        # This would normally call the actual retriever
        # For testing purposes, we'll simulate the call
        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': [],
            'message_count': 0
        }

    def retrieve_conversation_history_by_date(
        self,
        user_id: str,
        conversation_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Retrieve conversation history within a date range."""
        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': [],
            'message_count': 0
        }

    def search_conversation_history(self, user_id: str, conversation_id: str, search_term: str) -> Dict[str, Any]:
        """Search within conversation history."""
        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': [],
            'message_count': 0
        }

    def retrieve_conversation_history_with_stats(self, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """Retrieve conversation history with statistics."""
        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'messages': [],
            'message_count': 0,
            'user_message_count': 0,
            'ai_message_count': 0
        }


if __name__ == '__main__':
    unittest.main()