from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.task import Task


class TaskRepository(ABC):
    """Abstract interface for task repository operations."""

    @abstractmethod
    def create(self, task: Task) -> int:
        """Create a new task and return its ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its ID. Raises exception if not found."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Task]:
        """Retrieve all non-deleted tasks."""
        raise NotImplementedError

    @abstractmethod
    def search(self, keyword: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None) -> List[Task]:
        """Search, filter, and sort tasks based on criteria."""
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, due_date: Optional[str] = None) -> bool:
        """Update task details. Returns True if successful."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Mark a task as deleted by ID. Returns True if successful."""
        raise NotImplementedError

    @abstractmethod
    def restore(self, task_id: int) -> bool:
        """Restore a deleted task by ID. Returns True if successful."""
        raise NotImplementedError

    @abstractmethod
    def exists(self, task_id: int) -> bool:
        """Check if a task exists by ID."""
        raise NotImplementedError