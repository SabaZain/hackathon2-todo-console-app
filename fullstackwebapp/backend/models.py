from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Task(SQLModel, table=True):
    """
    Task model representing a todo item in the database.

    Fields:
    - id: Primary key, auto-incrementing integer
    - title: String, required title of the task (1-200 characters)
    - description: String, optional description of the task (max 1000 characters)
    - completed: Boolean, whether the task is completed (default: False)
    - owner_id: Integer, ID of the user who owns this task
    - created_at: DateTime, timestamp when the task was created
    """
    # Primary key field - automatically increments
    id: Optional[int] = Field(default=None, primary_key=True)

    # Required title of the task with validation constraints
    # Title must be between 1 and 200 characters
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Required title of the task (1-200 characters)"
    )

    # Optional description of the task with validation constraints
    # Description can be up to 1000 characters if provided
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Optional description of the task (max 1000 characters)"
    )

    # Whether the task is completed, defaults to False
    completed: bool = Field(
        default=False,
        description="Whether the task is completed"
    )

    # ID of the user who owns this task
    # This field ensures user isolation by linking tasks to specific users
    owner_id: int = Field(
        ...,
        description="ID of the user who owns this task",
        # Note: foreign_key should be defined differently in SQLModel
        # For now, we'll keep it as a regular field and define relationships separately if needed
    )

    # Timestamp when the task was created, defaults to current time
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Timestamp when the task was created"
    )

    # Note: Additional validation can be added using Pydantic v2 validation methods
    # For SQLModel compatibility, we rely on Field constraints for now