import pytest
from datetime import datetime
from domain.entities.task import Task
from presentation.formatters.task_formatter import TaskFormatter


class TestTaskFormatter:
    """Test cases for TaskFormatter."""

    def test_format_single_task_pending(self):
        """Test formatting a single pending task."""
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )
        formatter = TaskFormatter()
        formatted = formatter.format_task(task)

        assert "1" in formatted  # ID should be present
        assert "[ ]" in formatted  # Pending status indicator
        assert "Test task" in formatted  # Title should be present
        assert "Test description" in formatted  # Description should be present

    def test_format_single_task_completed(self):
        """Test formatting a single completed task."""
        task = Task(
            id=2,
            title="Completed task",
            description="Completed description",
            status=True,
            created_at=datetime.now()
        )
        formatter = TaskFormatter()
        formatted = formatter.format_task(task)

        assert "2" in formatted  # ID should be present
        assert "[x]" in formatted  # Completed status indicator
        assert "Completed task" in formatted  # Title should be present
        assert "Completed description" in formatted  # Description should be present

    def test_format_task_without_description(self):
        """Test formatting a task without description."""
        task = Task(
            id=3,
            title="Task without description",
            description=None,
            status=False,
            created_at=datetime.now()
        )
        formatter = TaskFormatter()
        formatted = formatter.format_task(task)

        assert "3" in formatted  # ID should be present
        assert "[ ]" in formatted  # Pending status indicator
        assert "Task without description" in formatted  # Title should be present
        # Should not show description if it's None

    def test_format_task_list_empty(self):
        """Test formatting an empty task list."""
        formatter = TaskFormatter()
        formatted = formatter.format_task_list([])

        assert formatted == "No tasks found."

    def test_format_task_list_with_multiple_tasks(self):
        """Test formatting a list with multiple tasks."""
        task1 = Task(
            id=1,
            title="First task",
            description="First description",
            status=False,
            created_at=datetime.now()
        )
        task2 = Task(
            id=2,
            title="Second task",
            description="Second description",
            status=True,
            created_at=datetime.now()
        )
        tasks = [task1, task2]
        formatter = TaskFormatter()
        formatted = formatter.format_task_list(tasks)

        # Should contain both tasks
        assert "1 [ ] First task - First description" in formatted
        assert "2 [x] Second task - Second description" in formatted

    def test_format_task_list_single_task(self):
        """Test formatting a list with a single task."""
        task = Task(
            id=1,
            title="Single task",
            description="Single description",
            status=False,
            created_at=datetime.now()
        )
        tasks = [task]
        formatter = TaskFormatter()
        formatted = formatter.format_task_list(tasks)

        assert "1 [ ] Single task - Single description" in formatted
        assert "No tasks found." not in formatted