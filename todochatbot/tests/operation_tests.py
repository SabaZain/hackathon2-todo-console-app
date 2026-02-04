"""
Operation Tests for Todo AI Chatbot

This module verifies all todo operations work through chat interface using natural language.
"""

import unittest
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestOperationTests(unittest.TestCase):
    """Test all todo operations through chat interface using natural language."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        pass

    def test_add_task_operation(self):
        """Test adding tasks via natural language commands."""
        test_inputs = [
            "Add a task to buy milk",
            "Create a new task to walk the dog",
            "Make a task to call mom tomorrow",
            "I need to add a task to finish report"
        ]

        for user_input in test_inputs:
            with self.subTest(input=user_input):
                # Simulate AI processing
                with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                    mock_agent_instance = Mock()
                    mock_agent.return_value = mock_agent_instance
                    mock_agent_instance.process_message.return_value = {
                        'response': f'Task "{user_input}" processed.',
                        'action': 'create_task',
                        'task_data': {'description': 'extracted description', 'priority': 'medium'}
                    }

                    # Simulate MCP tool call
                    with patch('todo_chatbot.mcp_tools.task_tools.create_task') as mock_create:
                        mock_create.return_value = {'id': '123', 'status': 'created'}

                        result = self.process_natural_language_command(user_input)

                        self.assertEqual(result['action'], 'create_task')
                        self.assertIsNotNone(result['task_id'])

    def test_list_tasks_operation(self):
        """Test listing tasks via natural language commands."""
        test_inputs = [
            "Show my tasks",
            "List all my tasks",
            "What tasks do I have?",
            "Display my pending tasks"
        ]

        for user_input in test_inputs:
            with self.subTest(input=user_input):
                # Simulate AI processing
                with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                    mock_agent_instance = Mock()
                    mock_agent.return_value = mock_agent_instance
                    mock_agent_instance.process_message.return_value = {
                        'response': 'Here are your tasks.',
                        'action': 'list_tasks',
                        'filters': {}
                    }

                    # Simulate MCP tool call
                    with patch('todo_chatbot.mcp_tools.task_tools.list_tasks') as mock_list:
                        mock_list.return_value = [
                            {'id': '1', 'description': 'Task 1', 'status': 'pending'},
                            {'id': '2', 'description': 'Task 2', 'status': 'pending'}
                        ]

                        result = self.process_natural_language_command(user_input)

                        self.assertEqual(result['action'], 'list_tasks')
                        self.assertIsInstance(result['tasks'], list)

    def test_update_task_operation(self):
        """Test updating tasks via natural language commands."""
        test_inputs = [
            "Change task 1 to have high priority",
            "Update task 2 to be completed",
            "Modify task 1 description to 'new description'"
        ]

        for user_input in test_inputs:
            with self.subTest(input=user_input):
                # Simulate AI processing
                with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                    mock_agent_instance = Mock()
                    mock_agent.return_value = mock_agent_instance
                    mock_agent_instance.process_message.return_value = {
                        'response': 'Task updated successfully.',
                        'action': 'update_task',
                        'task_id': '1',
                        'updates': {'priority': 'high'}
                    }

                    # Simulate MCP tool call
                    with patch('todo_chatbot.mcp_tools.task_tools.update_task') as mock_update:
                        mock_update.return_value = {'id': '1', 'status': 'updated'}

                        result = self.process_natural_language_command(user_input)

                        self.assertEqual(result['action'], 'update_task')
                        self.assertEqual(result['task_id'], '1')

    def test_complete_task_operation(self):
        """Test completing tasks via natural language commands."""
        test_inputs = [
            "Complete task 1",
            "Mark task 2 as done",
            "Finish task 3"
        ]

        for user_input in test_inputs:
            with self.subTest(input=user_input):
                # Simulate AI processing
                with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                    mock_agent_instance = Mock()
                    mock_agent.return_value = mock_agent_instance
                    mock_agent_instance.process_message.return_value = {
                        'response': 'Task completed successfully.',
                        'action': 'complete_task',
                        'task_id': '1'
                    }

                    # Simulate MCP tool call
                    with patch('todo_chatbot.mcp_tools.task_tools.complete_task') as mock_complete:
                        mock_complete.return_value = {'id': '1', 'status': 'completed'}

                        result = self.process_natural_language_command(user_input)

                        self.assertEqual(result['action'], 'complete_task')
                        self.assertEqual(result['task_id'], '1')

    def test_delete_task_operation(self):
        """Test deleting tasks via natural language commands."""
        test_inputs = [
            "Delete task 1",
            "Remove task 2",
            "Cancel task 3"
        ]

        for user_input in test_inputs:
            with self.subTest(input=user_input):
                # Simulate AI processing
                with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                    mock_agent_instance = Mock()
                    mock_agent.return_value = mock_agent_instance
                    mock_agent_instance.process_message.return_value = {
                        'response': 'Task deleted successfully.',
                        'action': 'delete_task',
                        'task_id': '1'
                    }

                    # Simulate MCP tool call
                    with patch('todo_chatbot.mcp_tools.task_tools.delete_task') as mock_delete:
                        mock_delete.return_value = {'id': '1', 'status': 'deleted'}

                        result = self.process_natural_language_command(user_input)

                        self.assertEqual(result['action'], 'delete_task')
                        self.assertEqual(result['task_id'], '1')

    def process_natural_language_command(self, user_input: str) -> Dict[str, Any]:
        """Process a natural language command and return result."""
        # Simulate the complete processing pipeline
        return {
            'action': 'unknown',
            'task_id': None,
            'tasks': [],
            'response': f'Processed: {user_input}'
        }


if __name__ == '__main__':
    unittest.main()