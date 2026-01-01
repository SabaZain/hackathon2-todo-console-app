import pytest
from datetime import datetime, timedelta
from domain.entities.task import Task
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from infrastructure.repositories.file_task_repository import FileTaskRepository


class TestRecurringRemindersRepository:
    """Tests for recurring tasks and reminders in repositories."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.in_memory_repo = InMemoryTaskRepository()

        # Create a temporary file for file repository tests
        import tempfile
        import os
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.json')
        self.temp_file.close()
        self.file_repo = FileTaskRepository(file_path=self.temp_file.name)

    def teardown_method(self):
        """Clean up after each test method."""
        import os
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_in_memory_repository_stores_recurring_and_reminder_fields(self):
        """Test that in-memory repository properly stores recurring and reminder fields."""
        recurring_config = {
            'interval': 'weekly',
            'count': 5
        }
        reminder = datetime.now() + timedelta(hours=1)

        task = Task(
            id=1,
            title="Test Recurring Task",
            recurring=recurring_config,
            reminder=reminder
        )

        # Create the task
        result_id = self.in_memory_repo.create(task)
        assert result_id == 1

        # Retrieve the task
        retrieved_task = self.in_memory_repo.get_by_id(1)

        assert retrieved_task.recurring == recurring_config
        assert retrieved_task.reminder == reminder
        assert retrieved_task.title == "Test Recurring Task"

    def test_file_repository_stores_recurring_and_reminder_fields(self):
        """Test that file repository properly stores recurring and reminder fields."""
        recurring_config = {
            'interval': 'monthly',
            'count': 3
        }
        reminder = datetime.now() + timedelta(minutes=30)

        task = Task(
            id=2,
            title="Test Recurring Task in File",
            recurring=recurring_config,
            reminder=reminder
        )

        # Create the task
        result_id = self.file_repo.create(task)
        assert result_id == 2

        # Retrieve the task
        retrieved_task = self.file_repo.get_by_id(2)

        assert retrieved_task.recurring == recurring_config
        assert retrieved_task.reminder == reminder
        assert retrieved_task.title == "Test Recurring Task in File"

    def test_in_memory_repository_updates_recurring_and_reminder_fields(self):
        """Test that in-memory repository properly updates recurring and reminder fields."""
        # Create a task without recurring/reminder
        task = Task(id=3, title="Update Test Task")
        self.in_memory_repo.create(task)

        # Update with recurring and reminder
        recurring_config = {
            'interval': 'daily',
            'count': 7
        }
        reminder = datetime.now() + timedelta(hours=2)

        result = self.in_memory_repo.update(
            task_id=3,
            recurring=recurring_config,
            reminder=reminder.isoformat()
        )

        assert result is True

        # Retrieve and verify
        updated_task = self.in_memory_repo.get_by_id(3)
        assert updated_task.recurring == recurring_config
        assert updated_task.reminder.isoformat().startswith(reminder.strftime('%Y-%m-%dT%H:%M'))

    def test_file_repository_updates_recurring_and_reminder_fields(self):
        """Test that file repository properly updates recurring and reminder fields."""
        # Create a task without recurring/reminder
        task = Task(id=4, title="Update Test Task in File")
        self.file_repo.create(task)

        # Update with recurring and reminder
        recurring_config = {
            'interval': 'weekly',
            'count': 4
        }
        reminder = datetime.now() + timedelta(minutes=45)

        result = self.file_repo.update(
            task_id=4,
            recurring=recurring_config,
            reminder=reminder.isoformat()
        )

        assert result is True

        # Retrieve and verify
        updated_task = self.file_repo.get_by_id(4)
        assert updated_task.recurring == recurring_config
        assert updated_task.reminder.isoformat().startswith(reminder.strftime('%Y-%m-%dT%H:%M'))

    def test_in_memory_repository_search_by_reminder(self):
        """Test that in-memory repository can search by reminder."""
        # Add tasks with different reminder times
        past_reminder = datetime.now() - timedelta(minutes=10)
        future_reminder = datetime.now() + timedelta(hours=1)

        task1 = Task(
            id=5,
            title="Past Reminder Task",
            reminder=past_reminder
        )
        task2 = Task(
            id=6,
            title="Future Reminder Task",
            reminder=future_reminder
        )

        self.in_memory_repo.create(task1)
        self.in_memory_repo.create(task2)

        # Search for tasks with reminders before now (should find only the past one)
        current_time = datetime.now()
        reminder_tasks = self.in_memory_repo.search(reminder_before=current_time)

        assert len(reminder_tasks) == 1
        assert reminder_tasks[0].id == 5
        assert reminder_tasks[0].title == "Past Reminder Task"

    def test_file_repository_search_by_reminder(self):
        """Test that file repository can search by reminder."""
        # Add tasks with different reminder times
        past_reminder = datetime.now() - timedelta(minutes=5)
        future_reminder = datetime.now() + timedelta(hours=2)

        task1 = Task(
            id=7,
            title="Past Reminder Task File",
            reminder=past_reminder
        )
        task2 = Task(
            id=8,
            title="Future Reminder Task File",
            reminder=future_reminder
        )

        self.file_repo.create(task1)
        self.file_repo.create(task2)

        # Search for tasks with reminders before now (should find only the past one)
        current_time = datetime.now()
        reminder_tasks = self.file_repo.search(reminder_before=current_time)

        assert len(reminder_tasks) == 1
        assert reminder_tasks[0].id == 7
        assert reminder_tasks[0].title == "Past Reminder Task File"

    def test_in_memory_repository_sort_by_reminder(self):
        """Test that in-memory repository can sort by reminder."""
        # Add tasks with different reminder times
        reminder1 = datetime.now() + timedelta(hours=3)
        reminder2 = datetime.now() + timedelta(hours=1)
        reminder3 = datetime.now() + timedelta(hours=2)

        task1 = Task(id=9, title="Task 1", reminder=reminder1)
        task2 = Task(id=10, title="Task 2", reminder=reminder2)
        task3 = Task(id=11, title="Task 3", reminder=reminder3)

        self.in_memory_repo.create(task1)
        self.in_memory_repo.create(task2)
        self.in_memory_repo.create(task3)

        # Sort by reminder
        sorted_tasks = self.in_memory_repo.search(sort_by="reminder")

        # Should be sorted in ascending order by reminder time
        assert sorted_tasks[0].id == 10  # earliest reminder
        assert sorted_tasks[1].id == 11
        assert sorted_tasks[2].id == 9   # latest reminder

    def test_file_repository_sort_by_reminder(self):
        """Test that file repository can sort by reminder."""
        # Add tasks with different reminder times
        reminder1 = datetime.now() + timedelta(hours=3)
        reminder2 = datetime.now() + timedelta(hours=1)
        reminder3 = datetime.now() + timedelta(hours=2)

        task1 = Task(id=12, title="Task 1 File", reminder=reminder1)
        task2 = Task(id=13, title="Task 2 File", reminder=reminder2)
        task3 = Task(id=14, title="Task 3 File", reminder=reminder3)

        self.file_repo.create(task1)
        self.file_repo.create(task2)
        self.file_repo.create(task3)

        # Sort by reminder
        sorted_tasks = self.file_repo.search(sort_by="reminder")

        # Should be sorted in ascending order by reminder time
        assert sorted_tasks[0].id == 13  # earliest reminder
        assert sorted_tasks[1].id == 14
        assert sorted_tasks[2].id == 12  # latest reminder