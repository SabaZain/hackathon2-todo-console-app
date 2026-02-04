"""
Example usage of MCP Tools for Todo AI Chatbot
This script demonstrates how to use the MCP tools for task management.
"""

import os
import sys
from unittest.mock import patch

# Add the backend directory to the path to access existing models and database functions
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Add the todochatbot directory to the path to access mcp_tools
todochatbot_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if todochatbot_path not in sys.path:
    sys.path.insert(0, todochatbot_path)

# Temporarily set DATABASE_URL to avoid the error during import
original_db_url = os.environ.get("DATABASE_URL")
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

try:
    # Import the tools after setting the environment variable
    from sqlmodel import create_engine, SQLModel, Session
    from sqlmodel.pool import StaticPool

    # Import Task model using the unique model factory to avoid duplicate registration
    from backend.models import get_unique_task_model
    Task = get_unique_task_model()

    # Import the task tools functions directly
    from task_tools import create_task, list_tasks, complete_task, delete_task, update_task
finally:
    # Restore original DATABASE_URL if it existed, or remove it if it didn't
    if original_db_url is not None:
        os.environ["DATABASE_URL"] = original_db_url
    else:
        os.environ.pop("DATABASE_URL", None)


def example_usage():
    """Demonstrate the usage of MCP tools"""

    # Create an in-memory SQLite database for the example
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # Mock the global engine in task_tools for this example
    with patch('task_tools.engine', engine):
        print("=== MCP Tools Example Usage ===\n")

        # Example 1: Add a task
        print("1. Adding a new task:")
        result = create_task(
            user_id="1",
            description="Buy groceries",
            status="pending"
        )
        task_id = result["id"]
        print(f"   Added task: {result['description']} (ID: {task_id})\n")

        # Example 2: Add another task
        print("2. Adding another task:")
        result = create_task(
            user_id="1",
            description="Complete project proposal - Finish the project proposal document and send to manager"
        )
        task_id2 = result["id"]  # Changed from "task_id" to "id" based on actual function
        print(f"   Added task: {result['description']} (ID: {task_id2})\n")

        # Example 3: List all tasks
        print("3. Listing all tasks for user 1:")
        tasks = list_tasks(user_id="1")
        for task in tasks:
            status = "[DONE]" if task["status"] == "completed" else "[TODO]"
            print(f"   {status} [{task['id']}] {task['description']}")
        print()

        # Example 4: Update a task
        print("4. Updating task description:")
        result = update_task(
            task_id=task_id2,
            user_id="1",
            updates={
                "title": "Complete urgent project proposal",
                "description": "Finish the high-priority project proposal and send to manager by EOD"
            }
        )
        print(f"   Updated task: {result['description']} (ID: {result['id']})\n")

        # Example 5: Complete a task
        print("5. Completing a task:")
        result = complete_task(user_id="1", task_id=task_id)
        print(f"   Completed task: {result['description']} (ID: {result['id']})\n")

        # Example 6: List pending tasks
        print("6. Listing pending tasks for user 1:")
        pending_tasks = list_tasks(user_id="1", status="pending")
        for task in pending_tasks:
            print(f"   [TODO] [{task['id']}] {task['description']}")
        print()

        # Example 7: List completed tasks
        print("7. Listing completed tasks for user 1:")
        completed_tasks = list_tasks(user_id="1", status="completed")
        for task in completed_tasks:
            print(f"   [DONE] [{task['id']}] {task['description']}")
        print()

        # Example 8: Delete a task
        print("8. Deleting a task:")
        result = delete_task(user_id="1", task_id=task_id2)
        print(f"   Deleted task: {result['title']} (ID: {result['id']})\n")

        # Example 9: Final list of tasks
        print("9. Final list of tasks for user 1:")
        final_tasks = list_tasks(user_id="1")
        if final_tasks:
            for task in final_tasks:
                status = "[DONE]" if task["completed"] else "[TODO]"
                print(f"   {status} [{task['id']}] {task['title']}")
        else:
            print("   No tasks remaining")
        print()

        print("=== Example completed successfully ===")


if __name__ == "__main__":
    example_usage()