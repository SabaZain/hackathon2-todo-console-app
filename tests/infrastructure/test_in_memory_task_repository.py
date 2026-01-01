import pytest
from datetime import datetime
from domain.entities.task import Task
from domain.exceptions import TaskNotFoundError
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


class TestInMemoryTaskRepository:
    """Test cases for InMemoryTaskRepository."""

    def test_create_task(self):
        """Test creating a task in the repository."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )

        task_id = repo.create(task)

        assert task_id == 1
        assert repo.exists(1) is True

    def test_get_task_by_id(self):
        """Test retrieving a task by its ID."""
        repo = InMemoryTaskRepository()
        original_task = Task(
            id=1,
            title="Test task",
            description="Test description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(original_task)

        retrieved_task = repo.get_by_id(1)

        assert retrieved_task.id == 1
        assert retrieved_task.title == "Test task"
        assert retrieved_task.description == "Test description"

    def test_get_nonexistent_task_raises_exception(self):
        """Test that getting a non-existent task raises TaskNotFoundError."""
        repo = InMemoryTaskRepository()

        with pytest.raises(TaskNotFoundError):
            repo.get_by_id(999)

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when repository is empty."""
        repo = InMemoryTaskRepository()

        tasks = repo.get_all()

        assert len(tasks) == 0

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks when repository has tasks."""
        repo = InMemoryTaskRepository()
        task1 = Task(
            id=1,
            title="Task 1",
            description="Description 1",
            status=False,
            created_at=datetime.now()
        )
        task2 = Task(
            id=2,
            title="Task 2",
            description="Description 2",
            status=True,
            created_at=datetime.now()
        )
        repo.create(task1)
        repo.create(task2)

        tasks = repo.get_all()

        assert len(tasks) == 2
        task_ids = [task.id for task in tasks]
        assert 1 in task_ids
        assert 2 in task_ids

    def test_update_task(self):
        """Test updating a task's title and description."""
        repo = InMemoryTaskRepository()
        original_task = Task(
            id=1,
            title="Original title",
            description="Original description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(original_task)

        result = repo.update(1, "Updated title", "Updated description")

        assert result is True
        updated_task = repo.get_by_id(1)
        assert updated_task.title == "Updated title"
        assert updated_task.description == "Updated description"

    def test_update_task_with_status(self):
        """Test updating a task's status."""
        repo = InMemoryTaskRepository()
        original_task = Task(
            id=1,
            title="Original title",
            description="Original description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(original_task)

        result = repo.update(1, status=True)

        assert result is True
        updated_task = repo.get_by_id(1)
        assert updated_task.status is True

    def test_update_task_partial(self):
        """Test updating only title or only description."""
        repo = InMemoryTaskRepository()
        original_task = Task(
            id=1,
            title="Original title",
            description="Original description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(original_task)

        # Update only title
        result = repo.update(1, title="Updated title only")

        assert result is True
        updated_task = repo.get_by_id(1)
        assert updated_task.title == "Updated title only"
        assert updated_task.description == "Original description"

    def test_update_nonexistent_task(self):
        """Test that updating a non-existent task returns False."""
        repo = InMemoryTaskRepository()

        result = repo.update(999, "Updated title")

        assert result is False

    def test_delete_task(self):
        """Test deleting a task."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Task to delete",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        result = repo.delete(1)

        assert result is True
        assert repo.exists(1) is True  # Task still exists but is marked as deleted
        assert repo.get_by_id(1).deleted is True  # Task is marked as deleted
        # Verify get_all doesn't return deleted tasks
        all_tasks = repo.get_all()
        assert len(all_tasks) == 0

    def test_delete_nonexistent_task(self):
        """Test that deleting a non-existent task returns False."""
        repo = InMemoryTaskRepository()

        result = repo.delete(999)

        assert result is False

    def test_exists_with_existing_task(self):
        """Test that exists returns True for existing task."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Test task",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        result = repo.exists(1)

        assert result is True

    def test_exists_with_nonexistent_task(self):
        """Test that exists returns False for non-existent task."""
        repo = InMemoryTaskRepository()

        result = repo.exists(999)

        assert result is False

    def test_soft_delete_marks_task_as_deleted(self):
        """Test that deleting a task marks it as deleted instead of removing it."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Task to delete",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        result = repo.delete(1)

        assert result is True
        assert repo.exists(1) is True  # Task still exists but is marked as deleted
        assert repo.get_by_id(1).deleted is True  # Task is marked as deleted

        # Verify get_all doesn't return deleted tasks
        all_tasks = repo.get_all()
        assert len(all_tasks) == 0

    def test_get_by_id_returns_deleted_task(self):
        """Test that get_by_id still returns deleted tasks."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Task to delete",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        # Delete the task
        repo.delete(1)

        # Verify get_by_id still returns the task
        retrieved_task = repo.get_by_id(1)
        assert retrieved_task.id == 1
        assert retrieved_task.deleted is True

    def test_restore_marks_deleted_task_as_not_deleted(self):
        """Test that restore marks a deleted task as not deleted."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Task to restore",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        # Delete the task
        repo.delete(1)

        # Verify it's deleted
        all_tasks = repo.get_all()
        assert len(all_tasks) == 0

        # Restore the task
        result = repo.restore(1)

        assert result is True

        # Verify it's no longer deleted
        all_tasks = repo.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 1
        assert all_tasks[0].deleted is False

    def test_restore_nonexistent_task_returns_false(self):
        """Test that restoring a non-existent task returns False."""
        repo = InMemoryTaskRepository()

        result = repo.restore(999)

        assert result is False

    def test_restore_non_deleted_task_returns_false(self):
        """Test that restoring a non-deleted task returns False."""
        repo = InMemoryTaskRepository()
        task = Task(
            id=1,
            title="Task to restore",
            description="Description",
            status=False,
            created_at=datetime.now()
        )
        repo.create(task)

        # Try to restore a task that was never deleted
        result = repo.restore(1)

        assert result is False  # Cannot restore a task that was never deleted

    def test_get_all_excludes_deleted_tasks(self):
        """Test that get_all only returns non-deleted tasks."""
        repo = InMemoryTaskRepository()
        task1 = Task(
            id=1,
            title="Task 1",
            description="Description 1",
            status=False,
            created_at=datetime.now()
        )
        task2 = Task(
            id=2,
            title="Task 2",
            description="Description 2",
            status=True,
            created_at=datetime.now()
        )
        repo.create(task1)
        repo.create(task2)

        # Delete task 1
        repo.delete(1)

        # Verify only task 2 is returned by get_all
        all_tasks = repo.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 2
        assert all_tasks[0].title == "Task 2"