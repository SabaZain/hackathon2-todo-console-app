from typing import List, Optional
import json
import os
from datetime import datetime
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository
from domain.exceptions import TaskNotFoundError


class FileTaskRepository(TaskRepository):
    """Concrete implementation of TaskRepository using file-based storage."""

    def __init__(self, file_path: str = "tasks.json"):
        """Initialize the file-based repository."""
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensure the tasks file exists, create it with empty list if it doesn't."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _load_tasks(self) -> List[dict]:
        """Load tasks from the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return []
                return json.loads(content)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # If there's a JSON decode error, return an empty list
            return []

    def _save_tasks(self, tasks: List[dict]):
        """Save tasks to the JSON file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False, default=self._json_serializer)

    def _json_serializer(self, obj):
        """Custom serializer for datetime objects."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    def _dict_to_task(self, task_dict: dict) -> Task:
        """Convert a dictionary to a Task object."""
        # Convert ISO format datetime string back to datetime object
        created_at = datetime.fromisoformat(task_dict['created_at']) if task_dict.get('created_at') else None
        due_date = datetime.fromisoformat(task_dict['due_date']) if task_dict.get('due_date') else None
        reminder = datetime.fromisoformat(task_dict['reminder']) if task_dict.get('reminder') else None
        return Task(
            id=task_dict['id'],
            title=task_dict['title'],
            description=task_dict.get('description'),
            status=task_dict.get('status', False),
            created_at=created_at,
            deleted=task_dict.get('deleted', False),
            priority=task_dict.get('priority', 'medium'),
            tags=task_dict.get('tags', []),
            due_date=due_date,
            recurring=task_dict.get('recurring'),
            reminder=reminder
        )

    def _task_to_dict(self, task: Task) -> dict:
        """Convert a Task object to a dictionary."""
        return {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'status': task.status,
            'created_at': task.created_at.isoformat() if task.created_at else None,
            'deleted': task.deleted,
            'priority': task.priority,
            'tags': task.tags,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'recurring': task.recurring,
            'reminder': task.reminder.isoformat() if task.reminder else None
        }

    def create(self, task: Task) -> int:
        """Create a new task and return its ID."""
        tasks = self._load_tasks()

        # Check if task with this ID already exists
        for existing_task in tasks:
            if existing_task['id'] == task.id:
                # Replace existing task with the same ID
                for i, t in enumerate(tasks):
                    if t['id'] == task.id:
                        tasks[i] = self._task_to_dict(task)
                        break
                break
        else:
            # Task ID doesn't exist, add it to the list
            tasks.append(self._task_to_dict(task))

        self._save_tasks(tasks)
        return task.id

    def get_by_id(self, task_id: int) -> Task:
        """Retrieve a task by its ID. Raises exception if not found."""
        tasks = self._load_tasks()

        for task_dict in tasks:
            if task_dict['id'] == task_id:
                return self._dict_to_task(task_dict)

        raise TaskNotFoundError(f"Task with ID {task_id} not found")

    def get_all(self) -> List[Task]:
        """Retrieve all non-deleted tasks."""
        tasks = self._load_tasks()
        return [self._dict_to_task(task_dict) for task_dict in tasks if not task_dict.get('deleted', False)]

    def update(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = ..., reminder: Optional[str] = ...) -> bool:
        """Update task details. Returns True if successful."""
        from datetime import datetime

        tasks = self._load_tasks()

        for i, task_dict in enumerate(tasks):
            if task_dict['id'] == task_id:
                # Update the task dictionary with provided values
                if title is not None:
                    task_dict['title'] = title
                if description is not None:
                    task_dict['description'] = description
                if status is not None:
                    task_dict['status'] = status
                if priority is not None:
                    task_dict['priority'] = priority
                if tags is not None:
                    task_dict['tags'] = tags
                if due_date is not None:
                    # Validate and update the due date
                    try:
                        parsed_due_date = datetime.fromisoformat(due_date)
                        task_dict['due_date'] = parsed_due_date.isoformat()
                    except ValueError:
                        # If it's not a valid ISO format, try parsing as date only
                        try:
                            parsed_due_date = datetime.fromisoformat(due_date + "T00:00:00")
                            task_dict['due_date'] = parsed_due_date.isoformat()
                        except ValueError:
                            raise ValueError("Due date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                # Handle recurring - update only if parameter was explicitly provided (including None)
                if recurring is not ...:
                    task_dict['recurring'] = recurring
                # Handle reminder - update only if parameter was explicitly provided (including None)
                # The reminder parameter here comes as a string from the service layer
                if reminder is not ...:
                    if reminder is not None:
                        # Validate and update the reminder
                        try:
                            parsed_reminder = datetime.fromisoformat(reminder)
                            task_dict['reminder'] = parsed_reminder.isoformat()
                        except ValueError:
                            # If it's not a valid ISO format, try parsing as date only
                            try:
                                parsed_reminder = datetime.fromisoformat(reminder + "T00:00:00")
                                task_dict['reminder'] = parsed_reminder.isoformat()
                            except ValueError:
                                raise ValueError("Reminder must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")
                    else:
                        # If reminder is explicitly set to None, clear it
                        task_dict['reminder'] = None

                # Save the updated tasks list
                self._save_tasks(tasks)
                return True

        return False

    def delete(self, task_id: int) -> bool:
        """Mark a task as deleted by ID. Returns True if successful."""
        tasks = self._load_tasks()

        for i, task_dict in enumerate(tasks):
            if task_dict['id'] == task_id:
                # Mark the task as deleted instead of removing it
                task_dict['deleted'] = True
                self._save_tasks(tasks)
                return True

        return False

    def restore(self, task_id: int) -> bool:
        """Restore a deleted task by ID. Returns True if successful."""
        tasks = self._load_tasks()

        for i, task_dict in enumerate(tasks):
            if task_dict['id'] == task_id:
                if task_dict.get('deleted', False):
                    # Restore the task by marking it as not deleted
                    task_dict['deleted'] = False
                    self._save_tasks(tasks)
                    return True
                else:
                    # Task exists but is not deleted, so nothing to restore
                    return False

        return False

    def exists(self, task_id: int) -> bool:
        """Check if a task exists by ID."""
        tasks = self._load_tasks()

        for task_dict in tasks:
            if task_dict['id'] == task_id:
                return True

        return False

    def search(self, keyword: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None, reminder_before: Optional[datetime] = None) -> List[Task]:
        """Search, filter, and sort tasks based on criteria."""
        # Load all tasks from the file
        tasks = self._load_tasks()

        # Convert to Task objects
        task_objects = [self._dict_to_task(task_dict) for task_dict in tasks if not task_dict.get('deleted', False)]

        # Apply keyword filter (search in title and description)
        if keyword is not None:
            keyword_lower = keyword.lower()
            task_objects = [
                task for task in task_objects
                if keyword_lower in task.title.lower() or
                (task.description and keyword_lower in task.description.lower())
            ]

        # Apply status filter
        if status is not None:
            task_objects = [task for task in task_objects if task.status == status]

        # Apply priority filter
        if priority is not None:
            task_objects = [task for task in task_objects if task.priority == priority]

        # Apply tags filter (tasks that contain all specified tags)
        if tags is not None and len(tags) > 0:
            task_objects = [
                task for task in task_objects
                if all(tag in task.tags for tag in tags)
            ]

        # Apply reminder filter (tasks with reminder before specified datetime)
        if reminder_before is not None:
            task_objects = [task for task in task_objects if task.reminder is not None and task.reminder <= reminder_before]

        # Apply sorting
        if sort_by == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            task_objects.sort(key=lambda task: priority_order.get(task.priority, 3))
        elif sort_by == "due_date":
            task_objects.sort(key=lambda task: (task.due_date is None, task.due_date))
        elif sort_by == "title":
            task_objects.sort(key=lambda task: task.title.lower())
        elif sort_by == "created_at":
            task_objects.sort(key=lambda task: task.created_at)
        elif sort_by == "status":
            task_objects.sort(key=lambda task: task.status)
        elif sort_by == "reminder":
            task_objects.sort(key=lambda task: (task.reminder is None, task.reminder))

        return task_objects