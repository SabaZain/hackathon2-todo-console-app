"""
Database utilities for MCP tools to avoid model re-import conflicts.
"""

from sqlmodel import Session, select
from typing import List, Dict, Union, Optional
import sys

import sys
import os

# Import models at module level to ensure they're registered once
# Use a single, consistent import path to avoid duplicate registrations
import sys
import os

# Get the correct path to import models consistently
current_dir = os.path.dirname(os.path.abspath(__file__))  # This is backend/mcp_tools/
backend_dir = os.path.dirname(os.path.dirname(current_dir))  # This is backend/

# Add backend to path if not already there
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import models using consistent path
from models import Task, User


def _get_engine():
    """Get engine dynamically to avoid circular imports."""
    try:
        from ..db import engine
    except (ImportError, ValueError):
        # Fallback for direct execution
        try:
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            if backend_dir not in sys.path:
                sys.path.insert(0, backend_dir)
            from db import engine
        except ImportError:
            # Last resort: try absolute import with backend prefix
            from backend.db import engine
    return engine


def _get_task_model():
    """Return the Task model - already imported at module level."""
    return Task


def _get_user_model():
    """Return the User model - already imported at module level."""
    return User


def create_task_db(user_id: int, title: str, description: str = None, completed: bool = False, session=None) -> Dict[str, Union[str, int, bool]]:
    """Create a task in the database."""
    task_model = _get_task_model()

    # Get engine dynamically to avoid circular imports
    engine = _get_engine()

    try:
        # Use provided session or create a new one
        own_session = False
        if session is None:
            session = Session(engine)
            own_session = True

        try:
            # Truncate title if too long
            safe_title = title[:200] if len(title) > 200 else title

            new_task = task_model(
                title=safe_title,
                description=description or title,
                completed=completed,
                owner_id=user_id
            )

            session.add(new_task)
            if own_session:
                session.commit()
                session.refresh(new_task)

            result = {
                "id": new_task.id,
                "status": "created",
                "description": description or title,
                "success": True
            }

            if own_session:
                session.close()

            return result
        except Exception as e:
            if own_session:
                session.rollback()
                session.close()
            raise e
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def list_tasks_db(user_id: int, status: Optional[str] = None, session=None) -> List[Dict[str, Union[int, str, bool]]]:
    """List tasks for a user from the database."""
    task_model = _get_task_model()

    # Get engine dynamically to avoid circular imports
    engine = _get_engine()

    try:
        # Use provided session or create a new one
        own_session = False
        if session is None:
            session = Session(engine)
            own_session = True

        try:
            query = select(task_model).where(task_model.owner_id == user_id)

            if status:
                if status == 'completed':
                    query = query.where(task_model.completed == True)
                elif status == 'pending':
                    query = query.where(task_model.completed == False)

            result = session.execute(query)
            tasks = result.scalars().all()

            formatted_tasks = []
            for task in tasks:
                task_status = 'completed' if task.completed else 'pending'

                formatted_tasks.append({
                    "id": task.id,
                    "description": task.description or task.title,
                    "status": task_status,
                    "priority": 'medium',
                    "due_date": None,
                    "category": 'general',
                    "tags": []
                })

            result = formatted_tasks

            if own_session:
                session.close()

            return result
        except Exception as e:
            if own_session:
                session.close()
            raise e
    except Exception as e:
        print(f"Error listing tasks: {e}")
        return []


def update_task_db(task_id: int, user_id: int, updates: Dict[str, any], session=None) -> Dict[str, Union[str, int, bool]]:
    """Update a task in the database."""
    task_model = _get_task_model()

    # Get engine dynamically to avoid circular imports
    engine = _get_engine()

    try:
        # Use provided session or create a new one
        own_session = False
        if session is None:
            session = Session(engine)
            own_session = True

        try:
            statement = select(task_model).where(
                task_model.id == task_id
            ).where(task_model.owner_id == user_id)

            result = session.execute(statement)
            task = result.first()

            if not task:
                if own_session:
                    session.close()
                return {
                    "status": "failed",
                    "message": "Task not found or user not authorized",
                    "success": False
                }

            # Apply updates
            if 'description' in updates:
                task.description = updates['description']
                task.title = updates['description'][:200] if len(updates['description']) > 200 else updates['description']

            if 'status' in updates:
                task.completed = (updates['status'] == 'completed')

            if 'title' in updates:
                task.title = updates['title'][:200] if len(updates['title']) > 200 else updates['title']

            if 'completed' in updates:
                task.completed = updates['completed']

            session.add(task)
            if own_session:
                session.commit()
                session.refresh(task)

            result = {
                "id": task.id,
                "status": "updated",
                "description": task.description or task.title,
                "success": True
            }

            if own_session:
                session.close()

            return result
        except Exception as e:
            if own_session:
                session.rollback()
                session.close()
            raise e
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def complete_task_db(user_id: int, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """Mark a task as completed in the database."""
    task_model = _get_task_model()

    # Get engine dynamically to avoid circular imports
    engine = _get_engine()

    try:
        # Use provided session or create a new one
        own_session = False
        if session is None:
            session = Session(engine)
            own_session = True

        try:
            statement = select(task_model).where(
                task_model.id == task_id
            ).where(task_model.owner_id == user_id)

            result = session.execute(statement)
            task = result.first()

            if not task:
                if own_session:
                    session.close()
                return {
                    "status": "failed",
                    "message": "Task not found or user not authorized",
                    "success": False
                }

            task.completed = True
            session.add(task)
            if own_session:
                session.commit()
                session.refresh(task)

            result = {
                "id": task.id,
                "status": "completed",
                "description": task.description or task.title,
                "success": True
            }

            if own_session:
                session.close()

            return result
        except Exception as e:
            if own_session:
                session.rollback()
                session.close()
            raise e
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }


def delete_task_db(user_id: int, task_id: int, session=None) -> Dict[str, Union[str, int, bool]]:
    """Delete a task from the database."""
    task_model = _get_task_model()

    # Get engine dynamically to avoid circular imports
    engine = _get_engine()

    try:
        # Use provided session or create a new one
        own_session = False
        if session is None:
            session = Session(engine)
            own_session = True

        try:
            statement = select(task_model).where(
                task_model.id == task_id
            ).where(task_model.owner_id == user_id)

            result = session.execute(statement)
            task = result.first()

            if not task:
                if own_session:
                    session.close()
                return {
                    "status": "failed",
                    "message": "Task not found or user not authorized",
                    "success": False
                }

            # Save task info before deletion
            task_title = task.title

            session.delete(task)
            if own_session:
                session.commit()

            result = {
                "id": task_id,
                "title": task_title,
                "status": "deleted",
                "success": True
            }

            if own_session:
                session.close()

            return result
        except Exception as e:
            if own_session:
                session.rollback()
                session.close()
            raise e
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "success": False
        }