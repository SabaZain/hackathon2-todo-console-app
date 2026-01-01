import pytest
from datetime import datetime
from domain.entities.task import Task
from application.services.id_generator import IDGenerator
from domain.repositories.task_repository import TaskRepository


@pytest.fixture
def sample_task():
    """Create a sample task for testing."""
    return Task(
        id=1,
        title="Sample task",
        description="Sample description",
        status=False,
        created_at=datetime.now()
    )


@pytest.fixture
def sample_completed_task():
    """Create a sample completed task for testing."""
    return Task(
        id=2,
        title="Completed task",
        description="Completed description",
        status=True,
        created_at=datetime.now()
    )


@pytest.fixture
def id_generator():
    """Create an ID generator for testing."""
    return IDGenerator()


@pytest.fixture
def mock_repository():
    """Create a mock repository for testing."""
    class MockRepository(TaskRepository):
        def __init__(self):
            self.tasks = {}
            self.next_id = 1

        def create(self, task: Task) -> int:
            task.id = self.next_id
            self.tasks[self.next_id] = task
            self.next_id += 1
            return task.id

        def get_by_id(self, task_id: int) -> Task:
            if task_id not in self.tasks:
                from domain.exceptions import TaskNotFoundError
                raise TaskNotFoundError(f"Task with ID {task_id} not found")
            return self.tasks[task_id]

        def get_all(self) -> list:
            return list(self.tasks.values())

        def update(self, task_id: int, title: str = None, description: str = None) -> bool:
            if task_id not in self.tasks:
                return False

            task = self.tasks[task_id]
            if title is not None:
                task.title = title
            if description is not None:
                task.description = description
            return True

        def delete(self, task_id: int) -> bool:
            if task_id not in self.tasks:
                return False
            del self.tasks[task_id]
            return True

        def exists(self, task_id: int) -> bool:
            return task_id in self.tasks

    return MockRepository()


@pytest.fixture
def empty_mock_repository():
    """Create an empty mock repository for testing."""
    class EmptyMockRepository(TaskRepository):
        def create(self, task: Task) -> int:
            raise NotImplementedError

        def get_by_id(self, task_id: int) -> Task:
            raise NotImplementedError

        def get_all(self) -> list:
            return []

        def update(self, task_id: int, title: str = None, description: str = None) -> bool:
            raise NotImplementedError

        def delete(self, task_id: int) -> bool:
            raise NotImplementedError

        def exists(self, task_id: int) -> bool:
            return False

    return EmptyMockRepository()