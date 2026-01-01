import pytest
from unittest.mock import Mock
from datetime import datetime
from domain.entities.task import Task
from application.services.todo_service import TodoService


class TestTodoServiceUseCases:
    """Test cases for TodoService use cases."""

    def test_add_task_use_case(self):
        """Test the AddTask use case."""
        mock_repo = Mock()
        mock_repo.create.return_value = 1  # Mock the return value of create
        mock_id_gen = Mock()
        mock_id_gen.generate_id.return_value = 1

        service = TodoService(mock_repo, mock_id_gen)

        # Add a task
        task_id = service.add_task("Test task", "Test description", "high", ["tag1", "tag2"], None)

        # Verify the task was created with correct parameters
        assert task_id == 1
        mock_repo.create.assert_called_once()
        created_task = mock_repo.create.call_args[0][0]
        assert created_task.title == "Test task"
        assert created_task.description == "Test description"
        assert created_task.priority == "high"
        assert "tag1" in created_task.tags
        assert "tag2" in created_task.tags
        assert created_task.status is False  # Default to pending

    def test_update_task_use_case(self):
        """Test the UpdateTask use case."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.update.return_value = True
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Update a task
        result = service.update_task(1, "Updated title", "Updated description", "low", ["new", "tags"])

        # Verify the update was called with correct parameters
        assert result is True
        mock_repo.update.assert_called_once_with(1, "Updated title", "Updated description", None, "low", ["new", "tags"], None, None, None)

    def test_delete_task_use_case(self):
        """Test the DeleteTask use case."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.delete.return_value = True
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Delete a task
        result = service.delete_task(1)

        # Verify the delete was called with correct parameters
        assert result is True
        mock_repo.delete.assert_called_once_with(1)

    def test_complete_task_use_case(self):
        """Test the CompleteTask use case."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.get_by_id.return_value = Task(1, "Test", "Description", False, datetime.now())
        mock_repo.update.return_value = True
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Complete a task
        result = service.complete_task(1)

        # Verify the update was called to set status to True
        assert result is True
        mock_repo.update.assert_called_once_with(1, status=True)

    def test_list_tasks_use_case(self):
        """Test the ListTasks use case."""
        mock_repo = Mock()
        expected_tasks = [
            Task(1, "Task 1", "Description 1", False, datetime.now()),
            Task(2, "Task 2", "Description 2", True, datetime.now())
        ]
        mock_repo.get_all.return_value = expected_tasks
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # List tasks
        tasks = service.list_tasks()

        # Verify the correct tasks were returned
        assert tasks == expected_tasks
        mock_repo.get_all.assert_called_once()

    def test_search_tasks_use_case(self):
        """Test the SearchTasks use case."""
        mock_repo = Mock()
        expected_tasks = [
            Task(1, "Search Result", "Description", False, datetime.now(), priority="high", tags=["search"])
        ]
        mock_repo.search.return_value = expected_tasks
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Search tasks
        tasks = service.search_tasks(keyword="search", priority="high")

        # Verify the search was called with correct parameters
        mock_repo.search.assert_called_once_with("search", None, "high", None, None)
        assert tasks == expected_tasks