import pytest
from datetime import datetime
from domain.entities.task import Task


class TestTask:
    """Test cases for Task entity with validation."""

    def test_task_creation_with_valid_data(self):
        """Test creating a task with valid data."""
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.status is False
        assert isinstance(task.created_at, datetime)

    def test_task_creation_with_minimal_data(self):
        """Test creating a task with only required fields."""
        created_at = datetime.now()
        task = Task(
            id=1,
            title="Test task",
            description=None,
            status=False,
            created_at=created_at
        )

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description is None
        assert task.status is False
        assert task.created_at == created_at

    def test_task_creation_fails_with_empty_title(self):
        """Test that creating a task with empty title raises an error."""
        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            Task(
                id=1,
                title="",
                description="Test description",
                status=False,
                created_at=datetime.now()
            )

    def test_task_creation_fails_with_whitespace_only_title(self):
        """Test that creating a task with whitespace-only title raises an error."""
        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            Task(
                id=1,
                title="   ",
                description="Test description",
                status=False,
                created_at=datetime.now()
            )

    def test_task_creation_fails_with_none_title(self):
        """Test that creating a task with None title raises an error."""
        with pytest.raises(ValueError, match="Title cannot be empty or contain only whitespace"):
            Task(
                id=1,
                title=None,
                description="Test description",
                status=False,
                created_at=datetime.now()
            )

    def test_task_str_representation(self):
        """Test string representation of task."""
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )

        expected_str = f"Task(id=1, title='Test task', description='Test description', status=False, deleted=False, priority='medium', tags=[], due_date=None, recurring=None, reminder=None)"
        assert str(task) == expected_str

    def test_task_repr_representation(self):
        """Test repr representation of task."""
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )

        expected_repr = f"Task(id=1, title='Test task', description='Test description', status=False, deleted=False, priority='medium', tags=[], due_date=None, recurring=None, reminder=None)"
        assert repr(task) == expected_repr

    def test_task_creation_with_due_date(self):
        """Test creating a task with due date."""
        due_date = datetime(2025, 12, 31, 23, 59, 59)
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now(),
            due_date=due_date
        )

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.status is False
        assert task.due_date == due_date

    def test_task_creation_with_none_due_date(self):
        """Test creating a task with None due date."""
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now(),
            due_date=None
        )

        assert task.id == 1
        assert task.title == "Test task"
        assert task.description == "Test description"
        assert task.status is False
        assert task.due_date is None

    def test_task_creation_fails_with_invalid_due_date(self):
        """Test that creating a task with invalid due date raises an error."""
        with pytest.raises(ValueError, match="Due date must be a datetime object or None"):
            Task(
                id=1,
                title="Test task",
                description="Test description",
                status=False,
                created_at=datetime.now(),
                due_date="invalid_date"
            )