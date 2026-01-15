from db import engine, get_session
from models import Task
from sqlmodel import SQLModel, select
from auth import get_current_user_id

print("Testing database connection...")

try:
    # Test getting a session
    with next(get_session()) as session:
        print("Session created successfully")

        # Test querying tasks for user_id = 1 (our mocked user)
        statement = select(Task).where(Task.owner_id == 1)
        result = session.execute(statement)
        tasks = result.fetchall()
        print(f"Found {len(tasks)} tasks for user 1")

        # Test creating a task
        new_task = Task(title="Test from script", description="Test description", owner_id=1)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        print(f"Created task with ID: {new_task.id}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()