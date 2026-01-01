from typing import List, Optional
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository
from application.services.id_generator import IDGenerator
from domain.exceptions import InvalidTaskTitleError, TaskNotFoundError


class TodoService:
    """Service for managing todo tasks with business logic."""

    def __init__(self, task_repository: TaskRepository, id_generator: IDGenerator):
        """Initialize the TodoService with dependencies."""
        self.task_repository = task_repository
        self.id_generator = id_generator

    def add_task(self, title: str, description: Optional[str] = None, priority: str = "medium", tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = None, reminder: Optional[str] = None) -> int:
        """Add a new task and return its ID."""
        from datetime import datetime

        # Validate title
        if title is None or not title.strip():
            raise InvalidTaskTitleError("Title cannot be empty or contain only whitespace")

        # Validate priority
        if priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate tags if provided
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list of strings")
            for tag in tags:
                if not isinstance(tag, str):
                    raise ValueError("All tags must be strings")

        # Validate due_date if provided
        parsed_due_date = None
        if due_date is not None:
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
            except ValueError:
                raise ValueError("Due date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

        # Validate recurring if provided
        parsed_recurring = None
        if recurring is not None:
            if not isinstance(recurring, dict):
                raise ValueError("Recurring must be a dictionary or None")

            # Validate interval
            if 'interval' not in recurring or recurring['interval'] not in ['daily', 'weekly', 'monthly']:
                raise ValueError("Recurring interval must be one of: daily, weekly, monthly")

            # Validate count if provided
            if 'count' in recurring and (not isinstance(recurring['count'], int) or recurring['count'] <= 0):
                raise ValueError("Recurring count must be a positive integer or None")

            # Validate next_due_date if provided
            if 'next_due_date' in recurring and not isinstance(recurring['next_due_date'], datetime):
                raise ValueError("Recurring next_due_date must be a datetime object or None")

            parsed_recurring = recurring

        # Validate reminder if provided
        parsed_reminder = None
        if reminder is not None:
            try:
                parsed_reminder = datetime.fromisoformat(reminder)
            except ValueError:
                raise ValueError("Reminder must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

        # Generate a new ID
        new_id = self.id_generator.generate_id()

        # Create a new task
        task = Task(
            id=new_id,
            title=title.strip(),
            description=description,
            status=False,  # Default to pending
            priority=priority,
            tags=tags if tags is not None else [],
            due_date=parsed_due_date,
            recurring=parsed_recurring,
            reminder=parsed_reminder
        )

        # Save the task to the repository
        return self.task_repository.create(task)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = None, reminder: Optional[str] = None) -> bool:
        """Update an existing task. Returns True if successful."""
        from datetime import datetime

        # Check if task exists
        if not self.task_repository.exists(task_id):
            return False

        # If a new title is provided, validate it
        if title is not None:
            if not title.strip():
                raise InvalidTaskTitleError("Title cannot be empty or contain only whitespace")
            title = title.strip()

        # Validate priority if provided
        if priority is not None:
            if priority not in ["high", "medium", "low"]:
                raise ValueError("Priority must be one of: high, medium, low")

        # Validate tags if provided
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list of strings")
            for tag in tags:
                if not isinstance(tag, str):
                    raise ValueError("All tags must be strings")

        # Validate due_date if provided
        parsed_due_date = None
        if due_date is not None:
            try:
                parsed_due_date = datetime.fromisoformat(due_date)
            except ValueError:
                raise ValueError("Due date must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

        # Validate recurring if provided
        parsed_recurring = None
        if recurring is not None:
            if not isinstance(recurring, dict):
                raise ValueError("Recurring must be a dictionary or None")

            # Validate interval
            if 'interval' not in recurring or recurring['interval'] not in ['daily', 'weekly', 'monthly']:
                raise ValueError("Recurring interval must be one of: daily, weekly, monthly")

            # Validate count if provided
            if 'count' in recurring and (not isinstance(recurring['count'], int) or recurring['count'] <= 0):
                raise ValueError("Recurring count must be a positive integer or None")

            # Validate next_due_date if provided
            if 'next_due_date' in recurring and not isinstance(recurring['next_due_date'], datetime):
                raise ValueError("Recurring next_due_date must be a datetime object or None")

            parsed_recurring = recurring

        # Validate reminder if provided
        # For the repository, we'll pass the original string since the repository handles parsing
        # but we validate it first to catch errors early
        if reminder is not None:
            try:
                datetime.fromisoformat(reminder)  # Validate that it's a valid ISO format
            except ValueError:
                raise ValueError("Reminder must be in ISO format (YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS)")

        # Update the task in the repository
        return self.task_repository.update(task_id, title, description, None, priority, tags, parsed_due_date, parsed_recurring, reminder)

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete. Returns True if successful."""
        # Check if task exists
        if not self.task_repository.exists(task_id):
            return False

        # Get the existing task
        task = self.task_repository.get_by_id(task_id)

        # Update the task status to completed
        result = self.task_repository.update(task_id, status=True)

        # If the task was successfully updated and it's recurring, schedule the next occurrence
        if result and task.recurring:
            self.schedule_next_occurrence(task_id)

        return result

    def delete_task(self, task_id: int) -> bool:
        """Delete a task. Returns True if successful."""
        # Check if task exists
        if not self.task_repository.exists(task_id):
            return False

        # Delete the task from the repository
        return self.task_repository.delete(task_id)

    def list_tasks(self) -> List[Task]:
        """List all tasks."""
        return self.task_repository.get_all()

    def restore_task(self, task_id: int) -> bool:
        """Restore a deleted task. Returns True if successful."""
        # Check if task exists
        if not self.task_repository.exists(task_id):
            return False

        # Get the task to check if it's deleted
        task = self.task_repository.get_by_id(task_id)
        if not task.deleted:
            # Task is not deleted, so there's nothing to restore
            return False

        # Restore the task in the repository
        return self.task_repository.restore(task_id)

    def search_tasks(self, keyword: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None) -> List[Task]:
        """Search, filter, and sort tasks based on criteria."""
        # Validate priority if provided
        if priority is not None and priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate tags if provided
        if tags is not None:
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list of strings")
            for tag in tags:
                if not isinstance(tag, str):
                    raise ValueError("All tags must be strings")

        # Validate sort_by if provided
        valid_sort_options = ["priority", "due_date", "title", "created_at", "status"]
        if sort_by is not None and sort_by not in valid_sort_options:
            raise ValueError(f"Sort by must be one of: {', '.join(valid_sort_options)}")

        # Search tasks in the repository
        return self.task_repository.search(keyword, status, priority, tags, sort_by)

    def schedule_next_occurrence(self, task_id: int) -> bool:
        """Schedule the next occurrence of a recurring task. Returns True if successful."""
        from datetime import datetime, timedelta

        # Check if task exists
        if not self.task_repository.exists(task_id):
            return False

        # Get the existing task
        task = self.task_repository.get_by_id(task_id)

        # Check if task is recurring
        if not task.recurring:
            return False

        # Get current count and interval
        current_count = task.recurring.get('count', 1)
        interval = task.recurring['interval']

        # If task has a count limit and we've reached it, don't create another occurrence
        # If current_count is 1, it means we're on the last occurrence, so we create a new one
        # and then remove the recurring config from the original task
        if 'count' in task.recurring and current_count <= 0:
            return False

        # Calculate next due date based on interval
        current_due_date = task.due_date if task.due_date else datetime.now()
        if interval == 'daily':
            next_due_date = current_due_date + timedelta(days=1)
        elif interval == 'weekly':
            next_due_date = current_due_date + timedelta(weeks=1)
        elif interval == 'monthly':
            # For monthly, we'll add 30 days as a simple approximation
            next_due_date = current_due_date + timedelta(days=30)
        else:
            return False

        # Create a new task with the same properties but updated due date
        new_id = self.id_generator.generate_id()

        # Update recurring count if present
        updated_recurring = task.recurring.copy()
        if 'count' in updated_recurring:
            new_count = updated_recurring['count'] - 1
            if new_count > 0:
                updated_recurring['count'] = new_count
            else:
                # If count is 0 or less, remove the count from the recurring config
                updated_recurring.pop('count', None)

        # Set the next due date
        updated_recurring['next_due_date'] = next_due_date

        new_task = Task(
            id=new_id,
            title=task.title,
            description=task.description,
            status=False,  # New occurrence starts as pending
            priority=task.priority,
            tags=task.tags,
            due_date=next_due_date,
            recurring=updated_recurring,
            reminder=task.reminder  # Keep the same reminder
        )

        # Save the new occurrence to the repository
        self.task_repository.create(new_task)

        # If the original task had count=1, we should remove the recurring config from it since we just created the final occurrence
        if 'count' in task.recurring and current_count == 1:
            # Remove recurring configuration from the original task
            self.task_repository.update(task_id, recurring=None)

        return True

    def check_reminders(self) -> List[Task]:
        """Check for tasks with upcoming reminders and return them."""
        from datetime import datetime

        # Search for tasks with reminders before or equal to current time
        current_time = datetime.now()
        return self.task_repository.search(reminder_before=current_time)