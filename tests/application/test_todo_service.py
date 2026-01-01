import pytest
from unittest.mock import Mock
from datetime import datetime
from domain.entities.task import Task
from domain.exceptions import InvalidTaskTitleError, TaskNotFoundError
from application.services.todo_service import TodoService
from application.services.id_generator import IDGenerator


class TestTodoService:
    """Test cases for TodoService."""

    def test_add_task_success(self):
        """Test adding a task successfully."""
        mock_repo = Mock()
        mock_repo.create.return_value = 1  # Mock the return value of create
        mock_id_gen = Mock()
        mock_id_gen.generate_id.return_value = 1

        service = TodoService(mock_repo, mock_id_gen)

        task_id = service.add_task("Test title", "Test description")

        assert task_id == 1
        mock_repo.create.assert_called_once()
        # Verify that create was called with a task that has the right properties
        created_task = mock_repo.create.call_args[0][0]
        assert created_task.title == "Test title"
        assert created_task.description == "Test description"
        assert created_task.status is False  # Default status is pending

    def test_add_task_without_description(self):
        """Test adding a task without description."""
        mock_repo = Mock()
        mock_repo.create.return_value = 1  # Mock the return value of create
        mock_id_gen = Mock()
        mock_id_gen.generate_id.return_value = 1

        service = TodoService(mock_repo, mock_id_gen)

        task_id = service.add_task("Test title")

        assert task_id == 1
        created_task = mock_repo.create.call_args[0][0]
        assert created_task.title == "Test title"
        assert created_task.description is None

    def test_add_task_invalid_title_raises_exception(self):
        """Test that adding a task with invalid title raises exception."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        with pytest.raises(InvalidTaskTitleError):
            service.add_task("")  # Empty title

        with pytest.raises(InvalidTaskTitleError):
            service.add_task("   ")  # Whitespace-only title

    def test_update_task_success(self):
        """Test updating a task successfully."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.update.return_value = True  # Mock the return value of update
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.update_task(1, "Updated title", "Updated description")

        assert result is True
        mock_repo.update.assert_called_once_with(1, "Updated title", "Updated description", None, None, None, None, None, None)

    def test_update_task_partial(self):
        """Test updating only title or only description."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.update.return_value = True  # Mock the return value of update
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Update only title
        result = service.update_task(1, "Updated title")

        assert result is True
        mock_repo.update.assert_called_once_with(1, "Updated title", None, None, None, None, None, None, None)

    def test_update_nonexistent_task(self):
        """Test that updating a non-existent task returns False."""
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.update_task(999, "Updated title")

        assert result is False
        mock_repo.update.assert_not_called()

    def test_update_task_invalid_title(self):
        """Test that updating a task with invalid title raises exception."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        with pytest.raises(InvalidTaskTitleError):
            service.update_task(1, "")  # Empty title

    def test_complete_task_success(self):
        """Test completing a task successfully."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_task = Mock(title="Test", description="Test", status=False)
        mock_task.recurring = None  # Mock the recurring attribute to be None
        mock_repo.get_by_id.return_value = mock_task  # Mock the task
        mock_repo.update.return_value = True  # Mock the return value of update
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.complete_task(1)

        assert result is True
        mock_repo.update.assert_called_once_with(1, status=True)

    def test_complete_nonexistent_task(self):
        """Test that completing a non-existent task returns False."""
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.complete_task(999)

        assert result is False
        mock_repo.update.assert_not_called()

    def test_delete_task_success(self):
        """Test deleting a task successfully."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        mock_repo.delete.return_value = True  # Mock the return value of delete
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.delete_task(1)

        assert result is True
        mock_repo.delete.assert_called_once_with(1)

    def test_delete_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.delete_task(999)

        assert result is False
        mock_repo.delete.assert_not_called()

    def test_list_tasks(self):
        """Test listing all tasks."""
        mock_repo = Mock()
        expected_tasks = [
            Task(1, "Task 1", "Description 1", False, datetime.now()),
            Task(2, "Task 2", "Description 2", True, datetime.now())
        ]
        mock_repo.get_all.return_value = expected_tasks
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        tasks = service.list_tasks()

        assert tasks == expected_tasks
        mock_repo.get_all.assert_called_once()

    def test_restore_task_success(self):
        """Test restoring a deleted task successfully."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        deleted_task = Task(1, "Task 1", "Description 1", False, datetime.now(), deleted=True)
        mock_repo.get_by_id.return_value = deleted_task
        mock_repo.restore.return_value = True
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.restore_task(1)

        assert result is True
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.restore.assert_called_once_with(1)

    def test_restore_nonexistent_task(self):
        """Test that restoring a non-existent task returns False."""
        mock_repo = Mock()
        mock_repo.exists.return_value = False
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.restore_task(999)

        assert result is False
        mock_repo.exists.assert_called_once_with(999)
        mock_repo.restore.assert_not_called()

    def test_restore_non_deleted_task(self):
        """Test that restoring a non-deleted task returns False."""
        mock_repo = Mock()
        mock_repo.exists.return_value = True
        non_deleted_task = Task(1, "Task 1", "Description 1", False, datetime.now(), deleted=False)
        mock_repo.get_by_id.return_value = non_deleted_task
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        result = service.restore_task(1)

        assert result is False
        mock_repo.get_by_id.assert_called_once_with(1)
        mock_repo.restore.assert_not_called()