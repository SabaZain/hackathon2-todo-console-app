import pytest
from datetime import datetime
from unittest.mock import Mock
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository


class TestTaskRepositoryInterface:
    """Test cases for TaskRepository interface."""

    def test_task_repository_interface_has_required_methods(self):
        """Test that TaskRepository interface has all required methods."""
        # Check if TaskRepository has the required methods
        assert hasattr(TaskRepository, 'create')
        assert hasattr(TaskRepository, 'get_by_id')
        assert hasattr(TaskRepository, 'get_all')
        assert hasattr(TaskRepository, 'update')
        assert hasattr(TaskRepository, 'delete')
        assert hasattr(TaskRepository, 'exists')

    def test_task_repository_cannot_be_instantiated(self):
        """Test that TaskRepository cannot be instantiated directly."""
        # Abstract classes cannot be instantiated
        with pytest.raises(TypeError):
            TaskRepository()