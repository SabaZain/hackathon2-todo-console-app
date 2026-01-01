import os
from typing import Type
from domain.repositories.task_repository import TaskRepository
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from infrastructure.repositories.file_task_repository import FileTaskRepository


class TaskRepositoryFactory:
    """Factory for creating task repository instances based on configuration."""

    @staticmethod
    def create_repository(repository_type: str = None, **kwargs) -> TaskRepository:
        """
        Create a task repository instance based on the specified type.

        Args:
            repository_type: 'in_memory', 'file', or None (defaults to file)
            **kwargs: Additional arguments passed to repository constructor

        Returns:
            TaskRepository: An instance of the requested repository type
        """
        if repository_type is None:
            # Default to file-based repository
            repository_type = os.getenv('TASK_REPOSITORY_TYPE', 'file')

        if repository_type.lower() == 'in_memory':
            return InMemoryTaskRepository()
        elif repository_type.lower() == 'file':
            file_path = kwargs.get('file_path') or os.getenv('TASKS_FILE_PATH', 'tasks.json')
            return FileTaskRepository(file_path=file_path)
        else:
            raise ValueError(f"Unknown repository type: {repository_type}")

    @staticmethod
    def get_default_repository() -> TaskRepository:
        """Get the default repository based on environment configuration."""
        return TaskRepositoryFactory.create_repository()