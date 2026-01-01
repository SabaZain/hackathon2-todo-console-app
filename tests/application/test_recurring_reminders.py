import pytest
from datetime import datetime, timedelta
from domain.entities.task import Task
from application.services.todo_service import TodoService
from application.services.id_generator import IDGenerator
from domain.exceptions import TaskNotFoundError
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


class TestRecurringTasksAndReminders:
    """Tests for recurring tasks and reminder functionality."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryTaskRepository()
        self.id_generator = IDGenerator()
        self.service = TodoService(self.repository, self.id_generator)

    def test_task_entity_with_recurring_and_reminder_fields(self):
        """Test that Task entity supports recurring and reminder fields."""
        # Create a task with recurring and reminder
        recurring_config = {
            'interval': 'daily',
            'count': 5,
            'next_due_date': datetime.now() + timedelta(days=1)
        }
        reminder = datetime.now() + timedelta(hours=1)

        task = Task(
            id=1,
            title="Test Recurring Task",
            recurring=recurring_config,
            reminder=reminder
        )

        assert task.recurring == recurring_config
        assert task.reminder == reminder
        assert task.title == "Test Recurring Task"

    def test_task_entity_validation_recurring_interval(self):
        """Test validation of recurring interval."""
        with pytest.raises(ValueError, match="Recurring interval must be one of: daily, weekly, monthly"):
            Task(
                id=1,
                title="Test Task",
                recurring={'interval': 'invalid_interval'}
            )

    def test_task_entity_validation_recurring_count(self):
        """Test validation of recurring count."""
        with pytest.raises(ValueError, match="Recurring count must be a positive integer or None"):
            Task(
                id=1,
                title="Test Task",
                recurring={'interval': 'daily', 'count': -1}
            )

    def test_task_entity_validation_reminder_datetime(self):
        """Test validation of reminder datetime."""
        with pytest.raises(ValueError, match="Reminder must be a datetime object or None"):
            Task(
                id=1,
                title="Test Task",
                reminder="invalid_datetime"
            )

    def test_add_task_with_recurring_and_reminder(self):
        """Test adding a task with recurring and reminder."""
        recurring_config = {
            'interval': 'weekly',
            'count': 3
        }
        reminder = datetime.now() + timedelta(hours=2)

        task_id = self.service.add_task(
            title="Recurring Task",
            recurring=recurring_config,
            reminder=reminder.isoformat()
        )

        task = self.repository.get_by_id(task_id)
        assert task.recurring == recurring_config
        assert task.reminder.isoformat().startswith(reminder.strftime('%Y-%m-%dT%H:%M'))

    def test_update_task_with_recurring_and_reminder(self):
        """Test updating a task with recurring and reminder."""
        # Add a task first
        original_task_id = self.service.add_task(title="Original Task")

        # Update with recurring and reminder
        recurring_config = {
            'interval': 'monthly',
            'count': 4
        }
        reminder = datetime.now() + timedelta(minutes=30)

        result = self.service.update_task(
            task_id=original_task_id,
            recurring=recurring_config,
            reminder=reminder.isoformat()
        )

        assert result is True

        updated_task = self.repository.get_by_id(original_task_id)
        assert updated_task.recurring == recurring_config
        assert updated_task.reminder.isoformat().startswith(reminder.strftime('%Y-%m-%dT%H:%M'))

    def test_schedule_next_occurrence_creates_new_task(self):
        """Test that scheduling next occurrence creates a new task."""
        # Create a recurring task
        recurring_config = {
            'interval': 'daily',
            'count': 3
        }
        task_id = self.service.add_task(
            title="Daily Recurring Task",
            recurring=recurring_config
        )

        # Schedule the next occurrence
        result = self.service.schedule_next_occurrence(task_id)

        assert result is True

        # Check that we now have 2 tasks (original + new occurrence)
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 2

        # Find the new occurrence (it should have a different ID)
        original_task = self.repository.get_by_id(task_id)
        new_occurrence = next(t for t in all_tasks if t.id != task_id)

        # New occurrence should have the same title but different due date
        assert new_occurrence.title == original_task.title
        assert new_occurrence.status is False  # New occurrence starts as pending
        assert new_occurrence.recurring['count'] == 2  # Count should be decremented

    def test_schedule_next_occurrence_with_count_limit(self):
        """Test that scheduling stops when count limit is reached."""
        # Create a recurring task with count = 1 (should only happen once more after completion)
        recurring_config = {
            'interval': 'daily',
            'count': 1
        }
        task_id = self.service.add_task(
            title="One-time Recurring Task",
            recurring=recurring_config
        )

        # Schedule the next occurrence (this should create one and remove recurring from original)
        result = self.service.schedule_next_occurrence(task_id)

        assert result is True

        # Check that we now have 2 tasks (original + new occurrence)
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 2

        # Get the original task again to check if recurring was removed
        original_task = self.repository.get_by_id(task_id)
        assert original_task.recurring is None  # Should be removed after last occurrence

    def test_check_reminders_finds_tasks_with_past_reminders(self):
        """Test that check_reminders finds tasks with past reminders."""
        # Add a task with a past reminder
        past_reminder = datetime.now() - timedelta(minutes=5)
        task_id = self.service.add_task(
            title="Past Reminder Task",
            reminder=past_reminder.isoformat()
        )

        # Add a task with a future reminder
        future_reminder = datetime.now() + timedelta(hours=1)
        self.service.add_task(
            title="Future Reminder Task",
            reminder=future_reminder.isoformat()
        )

        # Check reminders
        upcoming_tasks = self.service.check_reminders()

        # Should only return the task with past reminder
        assert len(upcoming_tasks) == 1
        assert upcoming_tasks[0].id == task_id
        assert upcoming_tasks[0].title == "Past Reminder Task"

    def test_complete_task_triggers_next_occurrence(self):
        """Test that completing a recurring task creates the next occurrence."""
        # Create a recurring task
        recurring_config = {
            'interval': 'daily',
            'count': 2
        }
        task_id = self.service.add_task(
            title="Recurring Task for Completion",
            recurring=recurring_config
        )

        # Complete the task
        result = self.service.complete_task(task_id)

        assert result is True

        # The completion should have triggered creation of next occurrence
        all_tasks = self.repository.get_all()
        assert len(all_tasks) == 2  # Original (completed) + new occurrence

        # Original task should be completed
        completed_task = self.repository.get_by_id(task_id)
        assert completed_task.status is True

        # There should be a new pending task with the same title
        new_task = next((t for t in all_tasks if t.id != task_id and t.status is False), None)
        assert new_task is not None
        assert new_task.title == "Recurring Task for Completion"
        assert new_task.recurring['count'] == 1  # Count should be decremented