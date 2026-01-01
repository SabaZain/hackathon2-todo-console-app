import json
import tempfile
import os
from datetime import datetime
from domain.entities.task import Task
from domain.exceptions import TaskNotFoundError
from infrastructure.repositories.file_task_repository import FileTaskRepository


class TestFileTaskRepository:
    """Test suite for FileTaskRepository following TDD approach."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.repository = FileTaskRepository(self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_create_task_persists_to_file(self):
        """Test that creating a task persists it to the JSON file."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)

        result_id = self.repository.create(task)

        assert result_id == 1

        # Check that the task was saved to the file
        with open(self.temp_file.name, 'r') as f:
            content = json.load(f)
            assert len(content) == 1
            saved_task = content[0]
            assert saved_task['id'] == 1
            assert saved_task['title'] == "Test Task"
            assert saved_task['description'] == "Test Description"
            assert saved_task['status'] is False
            assert saved_task['created_at'] is not None

    def test_get_by_id_retrieves_task_from_file(self):
        """Test that getting a task by ID retrieves it from the file."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        retrieved_task = self.repository.get_by_id(1)

        assert retrieved_task.id == 1
        assert retrieved_task.title == "Test Task"
        assert retrieved_task.description == "Test Description"
        assert retrieved_task.status is False
        assert isinstance(retrieved_task.created_at, datetime)

    def test_get_by_id_raises_exception_for_nonexistent_task(self):
        """Test that getting a non-existent task raises an exception."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        try:
            self.repository.get_by_id(999)
            assert False, "Expected TaskNotFoundError was not raised"
        except TaskNotFoundError:
            pass  # Expected exception was raised

    def test_get_all_retrieves_all_tasks_from_file(self):
        """Test that getting all tasks retrieves them from the file."""
        task1 = Task(id=1, title="Task 1", description="Description 1", status=False)
        task2 = Task(id=2, title="Task 2", description="Description 2", status=True)

        self.repository.create(task1)
        self.repository.create(task2)

        all_tasks = self.repository.get_all()

        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2
        assert all_tasks[0].title == "Task 1"
        assert all_tasks[1].title == "Task 2"

    def test_get_all_returns_empty_list_when_no_tasks(self):
        """Test that getting all tasks returns an empty list when there are no tasks."""
        all_tasks = self.repository.get_all()

        assert len(all_tasks) == 0

    def test_update_task_modifies_task_in_file(self):
        """Test that updating a task modifies it in the file."""
        task = Task(id=1, title="Original Title", description="Original Description", status=False)
        self.repository.create(task)

        result = self.repository.update(1, title="Updated Title", description="Updated Description", status=True)

        assert result is True

        # Verify the update was persisted to the file
        updated_task = self.repository.get_by_id(1)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"
        assert updated_task.status is True

    def test_update_nonexistent_task_returns_false(self):
        """Test that updating a non-existent task returns False."""
        result = self.repository.update(999, title="Updated Title")

        assert result is False

    def test_update_task_partial_updates(self):
        """Test that partial updates work correctly."""
        task = Task(id=1, title="Original Title", description="Original Description", status=False)
        self.repository.create(task)

        # Update only the title
        result = self.repository.update(1, title="Updated Title")

        assert result is True

        updated_task = self.repository.get_by_id(1)
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Original Description"  # Should remain unchanged
        assert updated_task.status is False  # Should remain unchanged

    def test_delete_task_removes_from_file(self):
        """Test that deleting a task removes it from the file."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        result = self.repository.delete(1)

        assert result is True

        # Verify the task was removed from the file
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 0

    def test_delete_nonexistent_task_returns_false(self):
        """Test that deleting a non-existent task returns False."""
        result = self.repository.delete(999)

        assert result is False

    def test_exists_returns_true_for_existing_task(self):
        """Test that exists returns True for existing tasks."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        result = self.repository.exists(1)

        assert result is True

    def test_exists_returns_false_for_nonexistent_task(self):
        """Test that exists returns False for non-existent tasks."""
        result = self.repository.exists(999)

        assert result is False

    def test_persistence_across_repository_instances(self):
        """Test that tasks persist across different repository instances."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)

        # Create and use first repository instance
        repo1 = FileTaskRepository(self.temp_file.name)
        repo1.create(task)

        # Create a new repository instance and verify the task is still there
        repo2 = FileTaskRepository(self.temp_file.name)
        retrieved_task = repo2.get_by_id(1)

        assert retrieved_task.id == 1
        assert retrieved_task.title == "Test Task"

    def test_soft_delete_marks_task_as_deleted(self):
        """Test that deleting a task marks it as deleted instead of removing it."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        result = self.repository.delete(1)

        assert result is True

        # Verify the task is still in the file but marked as deleted
        with open(self.temp_file.name, 'r') as f:
            content = json.load(f)
            assert len(content) == 1
            assert content[0]['id'] == 1
            assert content[0]['deleted'] is True

        # Verify get_all doesn't return deleted tasks
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 0

    def test_get_by_id_returns_deleted_task(self):
        """Test that get_by_id still returns deleted tasks."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        # Delete the task
        self.repository.delete(1)

        # Verify get_by_id still returns the task
        retrieved_task = self.repository.get_by_id(1)
        assert retrieved_task.id == 1
        assert retrieved_task.deleted is True

    def test_restore_marks_deleted_task_as_not_deleted(self):
        """Test that restore marks a deleted task as not deleted."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        # Delete the task
        self.repository.delete(1)

        # Verify it's deleted
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 0

        # Restore the task
        result = self.repository.restore(1)

        assert result is True

        # Verify it's no longer deleted
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 1
        assert all_tasks[0].deleted is False

    def test_restore_nonexistent_task_returns_false(self):
        """Test that restoring a non-existent task returns False."""
        result = self.repository.restore(999)

        assert result is False

    def test_restore_non_deleted_task_returns_false(self):
        """Test that restoring a non-deleted task returns False."""
        task = Task(id=1, title="Test Task", description="Test Description", status=False)
        self.repository.create(task)

        # Try to restore a task that was never deleted
        result = self.repository.restore(1)

        assert result is False

    def test_get_all_excludes_deleted_tasks(self):
        """Test that get_all only returns non-deleted tasks."""
        task1 = Task(id=1, title="Task 1", description="Description 1", status=False)
        task2 = Task(id=2, title="Task 2", description="Description 2", status=True)

        self.repository.create(task1)
        self.repository.create(task2)

        # Delete task 1
        self.repository.delete(1)

        # Verify only task 2 is returned by get_all
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 1
        assert all_tasks[0].id == 2
        assert all_tasks[0].title == "Task 2"