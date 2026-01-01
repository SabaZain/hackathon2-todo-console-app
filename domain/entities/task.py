from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


@dataclass
class Task:
    """Task entity with validation."""

    id: int
    title: str
    description: Optional[str] = None
    status: bool = False  # False = Pending, True = Completed
    created_at: datetime = None
    deleted: bool = False  # False = Not deleted, True = Deleted
    priority: str = "medium"  # high, medium, low
    tags: list = None  # List of strings
    due_date: Optional[datetime] = None  # Optional due date for sorting
    recurring: Optional[Dict[str, Any]] = None  # Recurring task configuration: {'interval': 'daily/weekly/monthly', 'count': int, 'next_due_date': datetime}
    reminder: Optional[datetime] = None  # Reminder datetime for notifications

    def __post_init__(self):
        """Validate the task after initialization."""
        if self.created_at is None:
            self.created_at = datetime.now()

        # Initialize tags to empty list if None
        if self.tags is None:
            self.tags = []

        # Initialize recurring to None if not provided
        if self.recurring is None:
            self.recurring = None

        # Validate that title is not empty or whitespace-only
        if self.title is None or not self.title.strip():
            raise ValueError("Title cannot be empty or contain only whitespace")

        # Validate that ID is a positive integer
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("ID must be a positive integer")

        # Validate that status is a boolean
        if not isinstance(self.status, bool):
            raise ValueError("Status must be a boolean value")

        # Validate that deleted is a boolean
        if not isinstance(self.deleted, bool):
            raise ValueError("Deleted must be a boolean value")

        # Validate that due_date is a datetime object or None
        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise ValueError("Due date must be a datetime object or None")

        # Validate that reminder is a datetime object or None
        if self.reminder is not None and not isinstance(self.reminder, datetime):
            raise ValueError("Reminder must be a datetime object or None")

        # Validate description length if provided
        if self.description is not None and len(self.description) > 1000:
            raise ValueError("Description length cannot exceed 1000 characters")

        # Validate priority value
        if self.priority not in ["high", "medium", "low"]:
            raise ValueError("Priority must be one of: high, medium, low")

        # Validate tags is a list and all elements are strings
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list of strings")
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("All tags must be strings")

        # Validate recurring configuration if provided
        if self.recurring is not None:
            if not isinstance(self.recurring, dict):
                raise ValueError("Recurring must be a dictionary or None")

            # Validate interval
            if 'interval' not in self.recurring or self.recurring['interval'] not in ['daily', 'weekly', 'monthly']:
                raise ValueError("Recurring interval must be one of: daily, weekly, monthly")

            # Validate count if provided
            if 'count' in self.recurring and (not isinstance(self.recurring['count'], int) or self.recurring['count'] <= 0):
                raise ValueError("Recurring count must be a positive integer or None")

            # Validate next_due_date if provided
            if 'next_due_date' in self.recurring and not isinstance(self.recurring['next_due_date'], datetime):
                raise ValueError("Recurring next_due_date must be a datetime object or None")

    def __str__(self):
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status={self.status}, deleted={self.deleted}, priority='{self.priority}', tags={self.tags}, due_date={self.due_date}, recurring={self.recurring}, reminder={self.reminder})"

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', description='{self.description}', status={self.status}, deleted={self.deleted}, priority='{self.priority}', tags={self.tags}, due_date={self.due_date}, recurring={self.recurring}, reminder={self.reminder})"