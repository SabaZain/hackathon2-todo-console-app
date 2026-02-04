"""
Test script for MCP Task Tools
Tests all the MCP tools to ensure they work correctly with the existing backend system.
"""

import sys
import os
import pytest
from unittest.mock import patch, MagicMock
from sqlmodel import create_engine, SQLModel, Session
from sqlmodel.pool import StaticPool

# Add the backend directory to the path to access existing models and database functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

# Temporarily set DATABASE_URL to avoid the error during import
original_db_url = os.environ.get("DATABASE_URL")
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

try:
    from task_tools import add_task, list_tasks, complete_task, delete_task, update_task
    # Import Task model using the unique model factory to avoid duplicate registration
    from backend.models import get_unique_task_model
    Task = get_unique_task_model()
finally:
    # Restore original DATABASE_URL if it existed, or remove it if it didn't
    if original_db_url is not None:
        os.environ["DATABASE_URL"] = original_db_url
    else:
        os.environ.pop("DATABASE_URL", None)


def test_add_task():
    """Test the add_task function"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # Add a task
        result = add_task(user_id="1", title="Test Task", description="Test Description")

        assert result["status"] == "created"
        assert result["title"] == "Test Task"
        assert isinstance(result["task_id"], int)
        assert result["task_id"] > 0

        # Verify the task was added to the database
        with Session(engine) as session:
            task = session.get(Task, result["task_id"])
            assert task is not None
            assert task.title == "Test Task"
            assert task.description == "Test Description"
            assert task.completed is False
            assert task.owner_id == 1


def test_list_tasks():
    """Test the list_tasks function"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Add some test tasks to the database
    with Session(engine) as session:
        task1 = Task(title="Task 1", description="First task", completed=False, owner_id=1)
        task2 = Task(title="Task 2", description="Second task", completed=True, owner_id=1)
        task3 = Task(title="Task 3", description="Third task", completed=False, owner_id=2)  # Different user
        session.add(task1)
        session.add(task2)
        session.add(task3)
        session.commit()

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # List all tasks for user 1
        result = list_tasks(user_id="1")

        assert len(result) == 2  # Only 2 tasks belong to user 1
        titles = [task["title"] for task in result]
        assert "Task 1" in titles
        assert "Task 2" in titles

        # List pending tasks for user 1
        result = list_tasks(user_id="1", status="pending")
        assert len(result) == 1
        assert result[0]["title"] == "Task 1"
        assert result[0]["completed"] is False

        # List completed tasks for user 1
        result = list_tasks(user_id="1", status="completed")
        assert len(result) == 1
        assert result[0]["title"] == "Task 2"
        assert result[0]["completed"] is True


def test_complete_task():
    """Test the complete_task function"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Add a test task to the database
    with Session(engine) as session:
        task = Task(title="Incomplete Task", description="Will be completed", completed=False, owner_id=1)
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # Complete the task
        result = complete_task(user_id="1", task_id=task_id)

        assert result["status"] == "completed"
        assert result["task_id"] == task_id
        assert result["title"] == "Incomplete Task"

        # Verify the task was updated in the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is not None
            assert task.completed is True


def test_delete_task():
    """Test the delete_task function"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Add a test task to the database
    with Session(engine) as session:
        task = Task(title="Task to Delete", description="Will be deleted", completed=False, owner_id=1)
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # Delete the task
        result = delete_task(user_id="1", task_id=task_id)

        assert result["status"] == "deleted"
        assert result["task_id"] == task_id
        assert result["title"] == "Task to Delete"

        # Verify the task was deleted from the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is None


def test_update_task():
    """Test the update_task function"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Add a test task to the database
    with Session(engine) as session:
        task = Task(title="Old Title", description="Old Description", completed=False, owner_id=1)
        session.add(task)
        session.commit()
        task_id = task.id

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # Update the task
        result = update_task(
            user_id="1",
            task_id=task_id,
            title="New Title",
            description="New Description"
        )

        assert result["status"] == "updated"
        assert result["task_id"] == task_id
        assert result["title"] == "New Title"

        # Verify the task was updated in the database
        with Session(engine) as session:
            task = session.get(Task, task_id)
            assert task is not None
            assert task.title == "New Title"
            assert task.description == "New Description"


def test_error_handling():
    """Test error handling in the tools"""
    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Mock the global engine in task_tools
    with patch('task_tools.engine', engine):
        # Test invalid user_id
        try:
            add_task(user_id="invalid", title="Test", description="Desc")
            assert False, "Should have raised an exception"
        except ValueError as e:
            assert "Invalid user_id" in str(e)

        # Test non-existent task operations
        try:
            complete_task(user_id="1", task_id=999)
            assert False, "Should have raised an exception"
        except ValueError as e:
            assert "not found" in str(e)


if __name__ == "__main__":
    print("Running MCP Tools tests...")

    test_add_task()
    print("[PASS] add_task test passed")

    test_list_tasks()
    print("[PASS] list_tasks test passed")

    test_complete_task()
    print("[PASS] complete_task test passed")

    test_delete_task()
    print("[PASS] delete_task test passed")

    test_update_task()
    print("[PASS] update_task test passed")

    test_error_handling()
    print("[PASS] error handling test passed")

    print("\nAll tests passed! [SUCCESS]")