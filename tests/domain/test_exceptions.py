import pytest
from domain.exceptions import InvalidTaskTitleError, TaskNotFoundError, TaskValidationError


class TestDomainExceptions:
    """Test cases for domain exceptions."""

    def test_invalid_task_title_error_creation(self):
        """Test creating InvalidTaskTitleError with a message."""
        error = InvalidTaskTitleError("Title cannot be empty")
        assert str(error) == "Title cannot be empty"
        assert isinstance(error, Exception)

    def test_invalid_task_title_error_inheritance(self):
        """Test that InvalidTaskTitleError inherits from Exception."""
        error = InvalidTaskTitleError("Title cannot be empty")
        assert isinstance(error, Exception)
        assert isinstance(error, TaskValidationError)

    def test_task_not_found_error_creation(self):
        """Test creating TaskNotFoundError with a message."""
        error = TaskNotFoundError("Task with ID 5 does not exist")
        assert str(error) == "Task with ID 5 does not exist"
        assert isinstance(error, Exception)

    def test_task_not_found_error_inheritance(self):
        """Test that TaskNotFoundError inherits from Exception."""
        error = TaskNotFoundError("Task with ID 5 does not exist")
        assert isinstance(error, Exception)
        assert isinstance(error, TaskValidationError)

    def test_task_validation_error_creation(self):
        """Test creating TaskValidationError with a message."""
        error = TaskValidationError("Invalid task data")
        assert str(error) == "Invalid task data"
        assert isinstance(error, Exception)

    def test_exception_can_be_raised_and_caught(self):
        """Test that domain exceptions can be raised and caught."""
        with pytest.raises(InvalidTaskTitleError) as exc_info:
            raise InvalidTaskTitleError("Title validation failed")

        assert str(exc_info.value) == "Title validation failed"

    def test_task_not_found_error_can_be_raised_and_caught(self):
        """Test that TaskNotFoundError can be raised and caught."""
        with pytest.raises(TaskNotFoundError) as exc_info:
            raise TaskNotFoundError("Task not found")

        assert str(exc_info.value) == "Task not found"