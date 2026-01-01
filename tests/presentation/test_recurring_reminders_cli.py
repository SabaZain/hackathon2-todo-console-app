import pytest
from datetime import datetime, timedelta
from presentation.cli.cli_app import TodoCLI
from application.services.todo_service import TodoService
from application.services.id_generator import IDGenerator
from presentation.formatters.task_formatter import TaskFormatter
from infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository


class TestRecurringRemindersCLI:
    """Tests for recurring tasks and reminders in CLI."""

    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.repository = InMemoryTaskRepository()
        self.id_generator = IDGenerator()
        self.service = TodoService(self.repository, self.id_generator)
        self.task_formatter = TaskFormatter()
        self.cli = TodoCLI(self.service, self.task_formatter)

    def test_add_task_with_recurring_parameter(self):
        """Test adding a task with recurring parameter via CLI."""
        recurring_config = {'interval': 'daily', 'count': 5}

        # Simulate CLI command: add "Daily Task" recurring=daily,5
        result = self.cli.add_task(
            title="Daily Task",
            recurring=recurring_config
        )

        # Verify the task was added
        assert "Task added with ID" in result

        # Verify the task has recurring configuration
        tasks = self.service.list_tasks()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.title == "Daily Task"
        assert task.recurring == recurring_config

    def test_add_task_with_reminder_parameter(self):
        """Test adding a task with reminder parameter via CLI."""
        future_time = datetime.now() + timedelta(hours=1)
        reminder_str = future_time.isoformat()

        # Simulate CLI command: add "Reminder Task" reminder=2023-12-31T14:30
        result = self.cli.add_task(
            title="Reminder Task",
            reminder=reminder_str
        )

        # Verify the task was added
        assert "Task added with ID" in result

        # Verify the task has reminder
        tasks = self.service.list_tasks()
        assert len(tasks) == 1
        task = tasks[0]
        assert task.title == "Reminder Task"
        assert task.reminder.isoformat().startswith(future_time.strftime('%Y-%m-%dT%H:%M'))

    def test_update_task_with_recurring_parameter(self):
        """Test updating a task with recurring parameter via CLI."""
        # Add a task first
        task_id = self.service.add_task(title="Original Task")

        # Update with recurring
        recurring_config = {'interval': 'weekly', 'count': 3}
        result = self.cli.update_task(
            task_id=task_id,
            recurring=recurring_config
        )

        assert result is True

        # Verify the task was updated
        updated_task = self.service.list_tasks()[0]
        assert updated_task.recurring == recurring_config

    def test_update_task_with_reminder_parameter(self):
        """Test updating a task with reminder parameter via CLI."""
        # Add a task first
        task_id = self.service.add_task(title="Original Task")

        # Update with reminder
        future_time = datetime.now() + timedelta(minutes=30)
        reminder_str = future_time.isoformat()
        result = self.cli.update_task(
            task_id=task_id,
            reminder=reminder_str
        )

        assert result is True

        # Verify the task was updated
        updated_task = self.service.list_tasks()[0]
        assert updated_task.reminder.isoformat().startswith(future_time.strftime('%Y-%m-%dT%H:%M'))

    def test_reminders_command_shows_upcoming_reminders(self):
        """Test that the reminders command shows tasks with upcoming reminders."""
        # Add a task with a past reminder
        past_reminder = datetime.now() - timedelta(minutes=5)
        self.service.add_task(
            title="Past Reminder Task",
            reminder=past_reminder.isoformat()
        )

        # Add a task with a future reminder
        future_reminder = datetime.now() + timedelta(hours=1)
        self.service.add_task(
            title="Future Reminder Task",
            reminder=future_reminder.isoformat()
        )

        # Call the reminders command
        result = self.cli.reminders()

        # Should contain the task with past reminder but not the future one
        assert "Past Reminder Task" in result
        assert "Future Reminder Task" not in result

    def test_reminders_command_with_multiple_past_reminders(self):
        """Test that the reminders command shows multiple tasks with past reminders."""
        # Add multiple tasks with past reminders
        past_reminder1 = datetime.now() - timedelta(minutes=10)
        past_reminder2 = datetime.now() - timedelta(minutes=5)

        self.service.add_task(
            title="Past Reminder Task 1",
            reminder=past_reminder1.isoformat()
        )
        self.service.add_task(
            title="Past Reminder Task 2",
            reminder=past_reminder2.isoformat()
        )

        # Add a task with future reminder
        future_reminder = datetime.now() + timedelta(hours=1)
        self.service.add_task(
            title="Future Reminder Task",
            reminder=future_reminder.isoformat()
        )

        # Call the reminders command
        result = self.cli.reminders()

        # Should contain both past reminder tasks but not the future one
        assert "Past Reminder Task 1" in result
        assert "Past Reminder Task 2" in result
        assert "Future Reminder Task" not in result

    def test_complete_task_creates_next_occurrence_for_recurring_task(self):
        """Test that completing a recurring task creates the next occurrence."""
        # Add a recurring task
        recurring_config = {
            'interval': 'daily',
            'count': 2
        }
        task_id = self.service.add_task(
            title="Daily Recurring Task",
            recurring=recurring_config
        )

        # Complete the task via CLI
        result = self.cli.complete_task(task_id)

        assert result is True

        # Verify that next occurrence was created
        all_tasks = self.service.list_tasks()
        assert len(all_tasks) == 2  # Original (completed) + new occurrence

        # Find the new occurrence (should be pending)
        original_task = self.service.list_tasks()[0]
        new_task = next((t for t in all_tasks if t.id != task_id), None)
        assert new_task is not None
        assert new_task.title == "Daily Recurring Task"
        assert new_task.status is False  # New occurrence starts as pending
        assert new_task.recurring['count'] == 1  # Count should be decremented

    def test_cli_add_handles_invalid_recurring_interval(self):
        """Test that CLI properly handles invalid recurring interval."""
        # This test is more about the validation in the service layer
        with pytest.raises(ValueError, match="Recurring interval must be one of: daily, weekly, monthly"):
            self.cli.add_task(
                title="Invalid Recurring Task",
                recurring={'interval': 'invalid_interval'}
            )

    def test_cli_add_handles_invalid_reminder_format(self):
        """Test that CLI properly handles invalid reminder format."""
        # This test is more about the validation in the service layer
        with pytest.raises(ValueError, match="Reminder must be in ISO format"):
            self.cli.add_task(
                title="Invalid Reminder Task",
                reminder="invalid_format"
            )