class TaskValidationError(Exception):
    """Base exception for task validation errors."""
    pass


class InvalidTaskTitleError(TaskValidationError):
    """Exception raised when a task title is invalid."""
    pass


class TaskNotFoundError(TaskValidationError):
    """Exception raised when a task is not found."""
    pass