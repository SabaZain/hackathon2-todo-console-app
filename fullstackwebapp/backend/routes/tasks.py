from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from ..db import get_session
from ..models import Task
from ..auth import get_current_user_id


"""
Task Ownership and User Isolation Principles:

This router implements strict ownership enforcement and user isolation:
1. Every endpoint receives user_id from JWT token (handled by authentication middleware)
2. All operations enforce ownership - users can only access their own tasks
3. Queries always filter by owner_id = user_id to ensure data isolation
4. Operations that fail ownership checks return 404 (not 403) to avoid revealing existence of other users' data
5. User isolation prevents data leakage between different users

Security Measures Implemented:
- Input validation for all parameters
- Ownership verification for all read/write operations
- Proper error handling that doesn't leak information
- Data filtering based on authenticated user identity

Testing & Integration Guidance:

Unit Testing Guidance:
- GET /api/tasks: Test input validation (user_id format), ownership enforcement (only user's tasks returned), error responses (400, 401, 403, 404), and empty list handling
- POST /api/tasks: Test input validation (title/description/length constraints), ownership assignment (user_id to owner_id), error responses (400, 401, 403), and response format
- GET /api/tasks/{id}: Test input validation (task_id/user_id format), ownership enforcement (404 for others' tasks), error responses (400, 404), and response format
- PUT /api/tasks/{id}: Test input validation (task_data constraints), ownership enforcement (404 for others' tasks), error responses (400, 404), and update behavior
- DELETE /api/tasks/{id}: Test input validation (task_id/user_id format), ownership enforcement (404 for others' tasks), error responses (400, 404), and deletion behavior
- PATCH /api/tasks/{id}/complete: Test input validation (task_id/user_id format), ownership enforcement (404 for others' tasks), completion toggling, error responses (400, 404), and response format

Integration Testing Guidance:
- Test how endpoints interact with the database layer (verify queries filter by owner_id = user_id)
- Verify data integrity (tasks are properly associated with users, completion status updates correctly)
- Test user isolation (users cannot access, modify, or delete other users' tasks)
- Verify response correctness (all required fields are returned in proper format)
- Test error response consistency across all endpoints
- Validate that authentication and authorization work properly with all endpoints
"""

# Create a router instance for task-related endpoints
router = APIRouter()


@router.get("/", response_model=List[Task])
def get_tasks(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Retrieve all tasks for a specific user.

    Args:
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        List of Task objects belonging to the user with fields:
        - id: integer, unique identifier
        - title: string, required task title
        - description: string, optional task description
        - completed: boolean, completion status (default: False)
        - owner_id: integer, ID of user who owns the task
        - created_at: datetime, timestamp when task was created

    HTTP Status Codes:
    - 200: Success - Returns list of tasks
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Access denied to user's tasks
    - 404: Not Found - User not found

    Ownership Rules:
    - Users can only access their own tasks (owner_id must match user_id)

    Business Rules:
    - Returns all tasks regardless of completion status
    - Tasks are sorted by creation date (newest first)
    """
    # Input validation: Verify user_id is valid (positive integer)
    if not isinstance(user_id, int) or user_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid user_id: must be a positive integer")

    # Query the database to fetch all tasks for the authenticated user
    # Filter by owner_id to ensure user isolation
    statement = select(Task).where(Task.owner_id == user_id).order_by(Task.created_at.desc())
    result = session.execute(statement)
    tasks = result.scalars().all()

    return tasks


@router.post("/", response_model=Task)
def create_task(task_data: Task, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Create a new task for a specific user.

    Args:
        task_data: Task object containing title, description, etc.
                 Expected fields:
                 - title: string, required task title (max 200 chars)
                 - description: string, optional task description (max 1000 chars)
                 - completed: boolean, completion status (will be set to False)
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        Created Task object with all fields including:
        - id: integer, unique identifier (auto-assigned)
        - title: string, required task title
        - description: string, optional task description
        - completed: boolean, completion status (default: False)
        - owner_id: integer, ID of user who owns the task (set from user_id)
        - created_at: datetime, timestamp when task was created (auto-assigned)

    HTTP Status Codes:
    - 201: Created - Task successfully created
    - 400: Bad Request - Invalid task data (missing title, invalid format)
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Access denied to user

    Input Validation:
    - title is required and must be a string between 1-200 characters
    - description is optional and must be a string up to 1000 characters if provided
    - completed is optional and defaults to False if not provided
    - owner_id is set from user_id parameter, not from task_data

    Ownership Rules:
    - The task's owner_id is automatically set to the authenticated user's ID
    - Users can only create tasks for themselves
    """
    # Input validation: Check that required fields are present
    # Validate title: required, string, 1-200 characters
    if not task_data.title:
        raise HTTPException(status_code=400, detail="Title is required")

    if not isinstance(task_data.title, str) or len(task_data.title) < 1 or len(task_data.title) > 200:
        raise HTTPException(status_code=400, detail="Title must be a string between 1 and 200 characters")

    # Validate description: optional, string, max 1000 characters if provided
    if task_data.description is not None and (not isinstance(task_data.description, str) or len(task_data.description) > 1000):
        raise HTTPException(status_code=400, detail="Description must be a string of maximum 1000 characters")

    # Validate completed field: boolean if provided
    if hasattr(task_data, 'completed') and task_data.completed is not None and not isinstance(task_data.completed, bool):
        raise HTTPException(status_code=400, detail="Completed field must be a boolean value")

    # Ensure that the task belongs to the authenticated user
    # Override any owner_id that might be in task_data with the authenticated user's ID
    # This enforces ownership rules and prevents users from creating tasks for others
    task_to_create = Task(
        title=task_data.title,
        description=task_data.description,
        completed=getattr(task_data, 'completed', False),
        owner_id=user_id
    )

    # Add the task to the database
    session.add(task_to_create)
    session.commit()
    session.refresh(task_to_create)

    return task_to_create


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Retrieve a specific task by ID for a specific user.

    Args:
        task_id: The ID of the task to retrieve (path parameter)
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        Task object with fields:
        - id: integer, unique identifier
        - title: string, required task title
        - description: string, optional task description
        - completed: boolean, completion status
        - owner_id: integer, ID of user who owns the task
        - created_at: datetime, timestamp when task was created

    HTTP Status Codes:
    - 200: Success - Task found and returned
    - 400: Bad Request - Invalid task_id format
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Task doesn't belong to user
    - 404: Not Found - Task not found

    Input Validation:
    - task_id must be a positive integer
    - user_id must be a positive integer

    Ownership Rules:
    - Users can only access tasks they own
    - Must verify that task.owner_id matches user_id
    """

    # Input validation: Verify task_id is valid (positive integer)
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task_id: must be a positive integer")

    # Query the database to fetch the specific task for the authenticated user
    # This ensures user isolation by checking both task ID and ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    # If the task doesn't exist or doesn't belong to the user, return 404
    # This combines both "not found" and "forbidden" into a single 404 response
    # to avoid revealing whether a task exists for other users
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task


@router.put("/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Update a specific task by ID for a specific user.

    Args:
        task_id: The ID of the task to update (path parameter)
        task_data: Task object containing updated data
                 Expected fields:
                 - title: string, required task title (max 200 chars)
                 - description: string, optional task description (max 1000 chars)
                 - completed: boolean, completion status
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        Updated Task object with all fields including:
        - id: integer, unique identifier
        - title: string, updated task title
        - description: string, updated task description
        - completed: boolean, updated completion status
        - owner_id: integer, ID of user who owns the task
        - created_at: datetime, timestamp when task was created (unchanged)

    HTTP Status Codes:
    - 200: Success - Task updated and returned
    - 400: Bad Request - Invalid task data or task_id format
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Task doesn't belong to user
    - 404: Not Found - Task not found

    Input Validation:
    - task_id must be a positive integer
    - user_id must be a positive integer
    - title is required and must be a string between 1-200 characters
    - description must be a string up to 1000 characters if provided
    - completed must be a boolean value

    Ownership Rules:
    - Users can only update tasks they own
    - Must verify that task.owner_id matches user_id before updating

    Business Rules:
    - The created_at field should remain unchanged
    - The owner_id field should remain unchanged
    - Only the title, description, and completed fields should be updated
    """

    # Input validation: Verify task_id is valid (positive integer)
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task_id: must be a positive integer")

    # Validate task_data fields
    # Validate title: required, string, 1-200 characters
    if not task_data.title:
        raise HTTPException(status_code=400, detail="Title is required")

    if not isinstance(task_data.title, str) or len(task_data.title) < 1 or len(task_data.title) > 200:
        raise HTTPException(status_code=400, detail="Title must be a string between 1 and 200 characters")

    # Validate description: optional, string, max 1000 characters if provided
    if task_data.description is not None and (not isinstance(task_data.description, str) or len(task_data.description) > 1000):
        raise HTTPException(status_code=400, detail="Description must be a string of maximum 1000 characters")

    # Validate completed field: boolean if provided
    if hasattr(task_data, 'completed') and task_data.completed is not None and not isinstance(task_data.completed, bool):
        raise HTTPException(status_code=400, detail="Completed field must be a boolean value")

    # Query the database to fetch the specific task for the authenticated user
    # This ensures user isolation by checking both task ID and ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    # If the task doesn't exist or doesn't belong to the user, return 404
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update the task with the new data
    # Preserve the original id, owner_id, and created_at values
    # Only update title, description, and completed fields
    task.title = task_data.title
    task.description = task_data.description
    task.completed = task_data.completed

    # Commit the changes to the database
    session.add(task)
    session.commit()
    session.refresh(task)

    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Delete a specific task by ID for a specific user.

    Args:
        task_id: The ID of the task to delete (path parameter)
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        Empty response with HTTP 204 status code on success

    HTTP Status Codes:
    - 204: No Content - Task successfully deleted
    - 400: Bad Request - Invalid task_id format
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Task doesn't belong to user
    - 404: Not Found - Task not found

    Input Validation:
    - task_id must be a positive integer
    - user_id must be a positive integer

    Ownership Rules:
    - Users can only delete tasks they own
    - Must verify that task.owner_id matches user_id before deletion

    Business Rules:
    - No response body is returned on successful deletion (HTTP 204)
    - The task is permanently removed from the database
    """

    # Input validation: Verify task_id is valid (positive integer)
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task_id: must be a positive integer")

    # Query the database to fetch the specific task for the authenticated user
    # This ensures user isolation by checking both task ID and ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    # If the task doesn't exist or doesn't belong to the user, return 404
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task from the database
    session.delete(task)
    session.commit()

    # Return 204 No Content for successful deletion
    return {"detail": "Task deleted successfully"}


@router.patch("/{task_id}/complete")
def toggle_task_completion(task_id: int, user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """
    Toggle the completion status of a specific task.

    Args:
        task_id: The ID of the task to update (path parameter)
        user_id: The current user's ID (obtained from authentication)
        session: Database session dependency

    Returns:
        Dictionary with updated completion status:
        {
            "task_id": integer, ID of the task
            "completed": boolean, new completion status
        }

    HTTP Status Codes:
    - 200: Success - Task completion status updated
    - 400: Bad Request - Invalid task_id format
    - 401: Unauthorized - Invalid authentication
    - 403: Forbidden - Task doesn't belong to user
    - 404: Not Found - Task not found

    Input Validation:
    - task_id must be a positive integer
    - user_id must be a positive integer

    Ownership Rules:
    - Users can only update tasks they own
    - Must verify that task.owner_id matches user_id before updating

    Business Rules:
    - Toggles the current completion status (True becomes False, False becomes True)
    - Only the completed field is changed
    - Returns the new completion status
    """

    # Input validation: Verify task_id is valid (positive integer)
    if not isinstance(task_id, int) or task_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid task_id: must be a positive integer")

    # Query the database to fetch the specific task for the authenticated user
    # This ensures user isolation by checking both task ID and ownership
    statement = select(Task).where(Task.id == task_id).where(Task.owner_id == user_id)
    result = session.execute(statement)
    task = result.scalar_one_or_none()

    # If the task doesn't exist or doesn't belong to the user, return 404
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Toggle the completion status (True becomes False, False becomes True)
    task.completed = not task.completed

    # Update the task in the database
    session.add(task)
    session.commit()
    session.refresh(task)

    # Return the updated completion status
    return {"task_id": task.id, "completed": task.completed}