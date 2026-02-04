"""
MCP Tools for Todo Task Management
Stateless tools for AI agents to manage todo tasks via the existing backend system.
"""

import sys
import os
from typing import Dict, List, Optional, Union
from datetime import datetime

# Add the backend directory to the path to access existing models and database functions
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)


def _get_db_functions():
    """Get database functions, importing them when first needed."""
    if not hasattr(_get_db_functions, '_functions'):
        from backend.mcp_tools.db_utils import (
            create_task_db,
            list_tasks_db,
            update_task_db,
            complete_task_db,
            delete_task_db
        )
        _get_db_functions._functions = (
            create_task_db, list_tasks_db, update_task_db, complete_task_db, delete_task_db
        )
    return _get_db_functions._functions


def create_task(user_id: str, description: str, status: str = 'pending', priority: str = 'medium',
                due_date: Optional[str] = None, category: str = 'general', tags: Optional[List[str]] = None,
                session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Create a new task for a user.

    Parameters:
    - user_id (str): The user's ID
    - description (str): The task description
    - status (str): The task status (default: 'pending')
    - priority (str): The task priority (default: 'medium')
    - due_date (str, optional): The due date in YYYY-MM-DD format
    - category (str): The task category (default: 'general')
    - tags (list, optional): List of tags
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task creation result with id, status, and description
    """
    create_task_db, _, _, _, _ = _get_db_functions()

    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        completed = (status == 'completed')
        return create_task_db(user_id=user_id_int, title=description, description=description,
                             completed=completed, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def list_tasks(user_id: str, status: Optional[str] = None, priority: Optional[str] = None,
               category: Optional[str] = None, session=None) -> List[Dict[str, Union[int, str, bool]]]:
    """
    Retrieve tasks for a user.

    Parameters:
    - user_id (str): The user's ID
    - status (str, optional): Filter by status ('all', 'pending', 'completed')
    - priority (str, optional): Filter by priority ('low', 'medium', 'high')
    - category (str, optional): Filter by category
    - session: Database session to use (if None, creates a new one)

    Returns:
    - list: List of task objects with id, description, status, priority, and due_date
    """
    _, list_tasks_db, _, _, _ = _get_db_functions()

    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return list_tasks_db(user_id=user_id_int, status=status, session=session)
    except Exception as e:
        print(f"Error listing tasks: {e}")
        return []


def update_task(task_id: int, user_id: str, updates: Dict[str, any], session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Update a task for a user.

    Parameters:
    - task_id (int): The ID of the task to update
    - user_id (str): The user's ID
    - updates (dict): Dictionary of fields to update
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task update result with id, status, and description
    """
    _, _, update_task_db, _, _ = _get_db_functions()

    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return update_task_db(task_id=task_id, user_id=user_id_int, updates=updates, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def complete_task(user_id: str, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Mark a task as completed.

    Parameters:
    - user_id (str): The user's ID
    - task_id (int): The ID of the task to complete
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task completion result with id, status, and description
    """
    _, _, _, complete_task_db, _ = _get_db_functions()

    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return complete_task_db(user_id=user_id_int, task_id=task_id, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def delete_task(user_id: str, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Delete a task.

    Parameters:
    - user_id (str): The user's ID
    - task_id (int): The ID of the task to delete
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task deletion result with id, status, and description
    """
    _, _, _, _, delete_task_db = _get_db_functions()

    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return delete_task_db(user_id=user_id_int, task_id=task_id, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


# Test function to demonstrate the tools
def test_tools():
    """Test function to demonstrate the MCP tools functionality."""
    print("Testing MCP Task Tools...")

    # Example of how the tools would be used
    try:
        # Example create task - note: user_id should be an integer in the actual system
        result = create_task(user_id="1", description="Test task from MCP tools")
        print(f"Create task result: {result}")

        # Example list tasks
        tasks = list_tasks(user_id="1")
        print(f"List tasks result: {tasks}")

        print("All tools defined successfully!")
    except Exception as e:
        print(f"Error in testing: {e}")


if __name__ == "__main__":
    test_tools()


def create_task(user_id: str, description: str, status: str = 'pending', priority: str = 'medium',
                due_date: Optional[str] = None, category: str = 'general', tags: Optional[List[str]] = None,
                session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Create a new task for a user.

    Parameters:
    - user_id (str): The user's ID
    - description (str): The task description
    - status (str): The task status (default: 'pending')
    - priority (str): The task priority (default: 'medium')
    - due_date (str, optional): The due date in YYYY-MM-DD format
    - category (str): The task category (default: 'general')
    - tags (list, optional): List of tags
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task creation result with id, status, and description
    """
    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        completed = (status == 'completed')
        return create_task_db(user_id=user_id_int, title=description, description=description,
                             completed=completed, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def list_tasks(user_id: str, status: Optional[str] = None, priority: Optional[str] = None,
               category: Optional[str] = None, session=None) -> List[Dict[str, Union[int, str, bool]]]:
    """
    Retrieve tasks for a user.

    Parameters:
    - user_id (str): The user's ID
    - status (str, optional): Filter by status ('all', 'pending', 'completed')
    - priority (str, optional): Filter by priority ('low', 'medium', 'high')
    - category (str, optional): Filter by category
    - session: Database session to use (if None, creates a new one)

    Returns:
    - list: List of task objects with id, description, status, priority, and due_date
    """
    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return list_tasks_db(user_id=user_id_int, status=status, session=session)
    except Exception as e:
        print(f"Error listing tasks: {e}")
        return []


def update_task(task_id: int, user_id: str, updates: Dict[str, any], session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Update a task for a user.

    Parameters:
    - task_id (int): The ID of the task to update
    - user_id (str): The user's ID
    - updates (dict): Dictionary of fields to update
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task update result with id, status, and description
    """
    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return update_task_db(task_id=task_id, user_id=user_id_int, updates=updates, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def complete_task(user_id: str, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Mark a task as completed.

    Parameters:
    - user_id (str): The user's ID
    - task_id (int): The ID of the task to complete
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task completion result with id, status, and description
    """
    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return complete_task_db(user_id=user_id_int, task_id=task_id, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def delete_task(user_id: str, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """
    Delete a task.

    Parameters:
    - user_id (str): The user's ID
    - task_id (int): The ID of the task to delete
    - session: Database session to use (if None, creates a new one)

    Returns:
    - dict: Task deletion result with id, status, and description
    """
    try:
        # Convert user_id to int since the existing system expects integer user IDs
        user_id_int = int(user_id)

        # Call the database utility function
        return delete_task_db(user_id=user_id_int, task_id=task_id, session=session)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


# Test function to demonstrate the tools
def test_tools():
    """Test function to demonstrate the MCP tools functionality."""
    print("Testing MCP Task Tools...")

    # Example of how the tools would be used
    try:
        # Example create task - note: user_id should be an integer in the actual system
        result = create_task(user_id="1", description="Test task from MCP tools")
        print(f"Create task result: {result}")

        # Example list tasks
        tasks = list_tasks(user_id="1")
        print(f"List tasks result: {tasks}")

        print("All tools defined successfully!")
    except Exception as e:
        print(f"Error in testing: {e}")


if __name__ == "__main__":
    test_tools()