from typing import List, Optional
from datetime import datetime
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository
from domain.exceptions import TaskNotFoundError


class InMemoryTaskRepository(TaskRepository):
    """Concrete implementation of TaskRepository using in-memory storage."""

    def __init__(self):
        """Initialize the in-memory repository."""
        self._tasks = {}  # Dictionary to store tasks with ID as key

    def create(self, task: Task) -> int:
        """Create a new task and return its ID."""
        self._tasks[task.id] = task
        return task.id

    def get_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its ID. Raises exception if not found."""
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        return self._tasks[task_id]

    def get_all(self) -> List[Task]:
        """Retrieve all non-deleted tasks."""
        return [task for task in self._tasks.values() if not task.deleted]

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = ..., reminder: Optional[str] = ...) -> bool:
        """Update task details. Returns True if successful."""
        from datetime import datetime

        if task_id not in self._tasks:
            return False

        task = self._tasks[task_id]
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            # Parse the due date string to datetime object
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
                task.due_date = parsed_due_date
            except ValueError:
                # If it's not a valid ISO format, try parsing as date only
                try:
                    parsed_due_date = datetime.fromisoformat(due_date + "T00:00:00")
                    task.due_date = parsed_due_date
                except ValueError:
                    raise ValueError("Due date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

        # Handle recurring - update only if parameter was explicitly provided (including None)
        if recurring is not ...:
            task.recurring = recurring
        # Handle reminder - update only if parameter was explicitly provided (including None)
        # The reminder parameter here comes as a string from the service layer
        if reminder is not ...:
            if reminder is not None:
                # Parse the reminder string to datetime object
                try:
                    parsed_reminder = datetime.fromisoformat(reminder)
                    task.reminder = parsed_reminder
                except ValueError:
                    # If it's not a valid ISO format, try parsing as date only
                    try:
                        parsed_reminder = datetime.fromisoformat(reminder + "T00:00:00")
                        task.reminder = parsed_reminder
                    except ValueError:
                        raise ValueError("Reminder must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
            else:
                # If reminder is explicitly set to None, clear it
                task.reminder = None

        return True

    def delete(self, task_id: int) -> bool:
        """Mark a task as deleted by ID. Returns True if successful."""
        if task_id not in self._tasks:
            return False

        self._tasks[task_id].deleted = True
        return True

    def restore(self, task_id: int) -> bool:
        """Restore a deleted task by ID. Returns True if successful."""
        if task_id not in self._tasks:
            return False

        # Only restore if the task is actually deleted
        if self._tasks[task_id].deleted:
            self._tasks[task_id].deleted = False
            return True
        else:
            # Task exists but is not deleted, so nothing to restore
            return False

    def exists(self, task_id: int) -> bool:
        """Check if a task exists by ID."""
        return task_id in self._tasks

    def search(self, keyword: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None, reminder_before: Optional[datetime] = None) -> List[Task]:
        """Search, filter, and sort tasks based on criteria."""
        # Start with all non-deleted tasks
        filtered_tasks = [task for task in self._tasks.values() if not task.deleted]

        # Apply keyword filter (search in title and description)
        if keyword is not None:
            keyword_lower = keyword.lower()
            filtered_tasks = [
                task for task in filtered_tasks
                if keyword_lower in task.title.lower() or
                (task.description and keyword_lower in task.description.lower())
            ]

        # Apply status filter
        if status is not None:
            filtered_tasks = [task for task in filtered_tasks if task.status == status]

        # Apply priority filter
        if priority is not None:
            filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

        # Apply tags filter (tasks that contain all specified tags)
        if tags is not None and len(tags) > 0:
            filtered_tasks = [
                task for task in filtered_tasks
                if all(tag in task.tags for tag in tags)
            ]

        # Apply reminder filter (tasks with reminder before specified datetime)
        if reminder_before is not None:
            filtered_tasks = [task for task in filtered_tasks if task.reminder is not None and task.reminder <= reminder_before]

        # Apply sorting
        if sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            filtered_tasks.sort(key=lambda task: priority_order.get(task.priority, 3))
        elif sort_by == "due_date":
            filtered_tasks.sort(key=lambda task: (task.due_date is None, task.due_date))
        elif sort_by == "title":
            filtered_tasks.sort(key=lambda task: task.title.lower())
        elif sort_by == "created_at":
            filtered_tasks.sort(key=lambda task: task.created_at)
        elif sort_by == "status":
            filtered_tasks.sort(key=lambda task: task.status)
        elif sort_by == "reminder":
            filtered_tasks.sort(key=lambda task: (task.reminder is None, task.reminder))

        return filtered_tasks