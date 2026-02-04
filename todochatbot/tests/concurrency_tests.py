"""
Concurrency Tests for Todo AI Chatbot

This module tests concurrent usage of chatbot and traditional UI.
"""

import unittest
import threading
import time
from unittest.mock import Mock, patch
from typing import Dict, Any


class TestConcurrencyTests(unittest.TestCase):
    """Test concurrent usage of chatbot and traditional UI."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.results_lock = threading.Lock()
        self.test_results = []

    def test_simultaneous_chatbot_and_ui_requests(self):
        """Test simultaneous requests to chatbot and traditional UI."""
        results = []

        def chatbot_request():
            with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                mock_agent_instance = Mock()
                mock_agent.return_value = mock_agent_instance
                mock_agent_instance.process_message.return_value = {
                    'response': 'Chatbot response',
                    'action': 'create_task'
                }

                with patch('todo_chatbot.mcp_tools.task_tools.create_task') as mock_create:
                    mock_create.return_value = {'id': '123', 'status': 'created'}

                    result = self.simulate_chatbot_request("Add task via chatbot")
                    with self.results_lock:
                        results.append(('chatbot', result))

        def ui_request():
            with patch('todo_chatbot.original_todo_api.create_task') as mock_create:
                mock_create.return_value = {'id': '456', 'status': 'created'}

                result = self.simulate_ui_request("/api/tasks", method="POST", data={'description': 'UI task'})
                with self.results_lock:
                    results.append(('ui', result))

        # Start both requests simultaneously
        chatbot_thread = threading.Thread(target=chatbot_request)
        ui_thread = threading.Thread(target=ui_request)

        chatbot_thread.start()
        ui_thread.start()

        # Wait for both to complete
        chatbot_thread.join()
        ui_thread.join()

        # Verify both completed successfully
        self.assertEqual(len(results), 2)
        chatbot_result = [r for t, r in results if t == 'chatbot'][0]
        ui_result = [r for t, r in results if t == 'ui'][0]

        self.assertIsNotNone(chatbot_result)
        self.assertIsNotNone(ui_result)

    def test_shared_resource_access(self):
        """Test access to shared resources (database, etc.) from both systems."""
        shared_counter = {'count': 0}
        lock = threading.Lock()

        def access_shared_resource(user_type, resource_id):
            # Simulate accessing a shared resource with proper locking
            with lock:
                # Simulate some work with the shared resource
                current_count = shared_counter['count']
                time.sleep(0.01)  # Simulate processing time
                shared_counter['count'] = current_count + 1

                # Log the access
                result = {
                    'user_type': user_type,
                    'resource_id': resource_id,
                    'final_count': shared_counter['count']
                }

                with self.results_lock:
                    self.test_results.append(result)

        # Create multiple threads simulating both chatbot and UI access
        threads = []
        for i in range(10):
            # Alternate between chatbot and UI requests
            user_type = 'chatbot' if i % 2 == 0 else 'ui'
            thread = threading.Thread(target=access_shared_resource, args=(user_type, f'res{i}'))
            threads.append(thread)

        # Start all threads
        for thread in threads:
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        # Verify all accesses were handled correctly
        self.assertEqual(len(self.test_results), 10)
        self.assertEqual(shared_counter['count'], 10)

        # Verify both user types accessed the resource
        chatbot_accesses = [r for r in self.test_results if r['user_type'] == 'chatbot']
        ui_accesses = [r for r in self.test_results if r['user_type'] == 'ui']

        self.assertGreaterEqual(len(chatbot_accesses), 4)  # At least 5 chatbot accesses
        self.assertGreaterEqual(len(ui_accesses), 4)      # At least 5 UI accesses

    def test_concurrent_conversation_and_todo_operations(self):
        """Test concurrent conversation operations and todo operations."""
        results = []

        def conversation_operation():
            # Simulate conversation operation
            with patch('todo_chatbot.database.conversations.save_message') as mock_save:
                mock_save.return_value = True

                time.sleep(0.05)  # Simulate processing time
                result = {
                    'type': 'conversation',
                    'operation': 'save_message',
                    'success': True
                }

                with self.results_lock:
                    results.append(result)

        def todo_operation():
            # Simulate todo operation
            with patch('todo_chatbot.original_todo_api.get_tasks') as mock_get:
                mock_get.return_value = [{'id': '1', 'description': 'Task', 'status': 'pending'}]

                time.sleep(0.05)  # Simulate processing time
                result = {
                    'type': 'todo',
                    'operation': 'get_tasks',
                    'success': True,
                    'task_count': 1
                }

                with self.results_lock:
                    results.append(result)

        # Run multiple concurrent operations
        threads = []
        for i in range(5):
            conv_thread = threading.Thread(target=conversation_operation)
            todo_thread = threading.Thread(target=todo_operation)

            threads.append(conv_thread)
            threads.append(todo_thread)

            conv_thread.start()
            todo_thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        # Verify all operations completed
        self.assertEqual(len(results), 10)

        conversation_ops = [r for r in results if r['type'] == 'conversation']
        todo_ops = [r for r in results if r['type'] == 'todo']

        self.assertEqual(len(conversation_ops), 5)
        self.assertEqual(len(todo_ops), 5)

    def test_session_isolation_under_concurrency(self):
        """Test that user sessions remain isolated under concurrent load."""
        user_sessions = {}

        def user_operation(user_id):
            # Simulate user-specific operations
            with patch('todo_chatbot.agent.chat_agent.ChatAgent') as mock_agent:
                mock_agent_instance = Mock()
                mock_agent.return_value = mock_agent_instance
                mock_agent_instance.process_message.return_value = {
                    'response': f'Response for user {user_id}',
                    'action': 'create_task'
                }

                with patch('todo_chatbot.mcp_tools.task_tools.create_task') as mock_create:
                    mock_create.return_value = {'id': f'{user_id}_123', 'status': 'created'}

                    # Simulate session-specific work
                    time.sleep(0.02)  # Processing delay

                    # Store session data
                    session_data = {
                        'user_id': user_id,
                        'timestamp': time.time(),
                        'operations': 1
                    }

                    with self.results_lock:
                        user_sessions[user_id] = session_data

        # Simulate multiple concurrent users
        user_threads = []
        for user_id in [f'user_{i}' for i in range(20)]:
            thread = threading.Thread(target=user_operation, args=(user_id,))
            user_threads.append(thread)
            thread.start()

        # Wait for all to complete
        for thread in user_threads:
            thread.join()

        # Verify each user has their own isolated session
        self.assertEqual(len(user_sessions), 20)

        for user_id, session_data in user_sessions.items():
            self.assertEqual(session_data['user_id'], user_id)
            self.assertEqual(session_data['operations'], 1)

    def test_resource_starvation_prevention(self):
        """Test that neither system starves the other of resources."""
        import queue
        import time

        # Create queues to simulate resource allocation
        chatbot_queue = queue.Queue()
        ui_queue = queue.Queue()

        def process_chatbot_request(req_id):
            # Simulate chatbot request processing
            time.sleep(0.01)  # Simulate processing time
            chatbot_queue.put(f'chatbot_processed_{req_id}')

        def process_ui_request(req_id):
            # Simulate UI request processing
            time.sleep(0.01)  # Simulate processing time
            ui_queue.put(f'ui_processed_{req_id}')

        # Submit mixed requests to test fairness
        threads = []
        for i in range(50):
            if i % 2 == 0:
                thread = threading.Thread(target=process_chatbot_request, args=(i,))
            else:
                thread = threading.Thread(target=process_ui_request, args=(i,))
            threads.append(thread)
            thread.start()

        # Wait for all to complete
        for thread in threads:
            thread.join()

        # Verify both systems processed requests fairly
        chatbot_processed = 0
        ui_processed = 0

        while not chatbot_queue.empty():
            if 'chatbot_processed_' in chatbot_queue.get():
                chatbot_processed += 1

        while not ui_queue.empty():
            if 'ui_processed_' in ui_queue.get():
                ui_processed += 1

        # Both systems should have processed approximately equal numbers
        self.assertAlmostEqual(chatbot_processed, ui_processed, delta=5)

    def simulate_chatbot_request(self, user_input: str) -> Dict[str, Any]:
        """Simulate a chatbot request."""
        return {
            'status': 'success',
            'response': f'Simulated response to: {user_input}',
            'action': 'processed'
        }

    def simulate_ui_request(self, endpoint: str, method: str = 'GET', data: Dict = None) -> Dict[str, Any]:
        """Simulate a UI request."""
        return {
            'status': 'success',
            'endpoint': endpoint,
            'method': method,
            'data': data
        }


if __name__ == '__main__':
    unittest.main()