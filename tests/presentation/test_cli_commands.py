import pytest
from unittest.mock import Mock, patch
from io import StringIO
from domain.entities.task import Task
from application.services.todo_service import TodoService
from presentation.formatters.task_formatter import TaskFormatter
from presentation.cli.cli_app import TodoCLI


class TestCLICommands:
    """Test cases for CLI commands."""

    def test_add_task_command(self):
        """Test adding a task via CLI command."""
        mock_service = Mock()
        mock_service.add_task.return_value = 1
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.add_task("Test title", "Test description")

        mock_service.add_task.assert_called_once_with("Test title", "Test description", "medium", None, None, None, None)
        assert result == "Task added with ID 1"

    def test_add_task_command_without_description(self):
        """Test adding a task without description via CLI command."""
        mock_service = Mock()
        mock_service.add_task.return_value = 1
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.add_task("Test title")

        mock_service.add_task.assert_called_once_with("Test title", None, "medium", None, None, None, None)
        assert result == "Task added with ID 1"

    def test_list_tasks_command(self):
        """Test listing tasks via CLI command."""
        mock_service = Mock()
        mock_tasks = [
            Task(1, "Task 1", "Description 1", False),
            Task(2, "Task 2", "Description 2", True)
        ]
        mock_service.list_tasks.return_value = mock_tasks
        mock_formatter = Mock()
        mock_formatter.format_task_list.return_value = "Formatted task list"

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.list_tasks()

        mock_service.list_tasks.assert_called_once()
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)
        assert result == "Formatted task list"

    def test_update_task_command(self):
        """Test updating a task via CLI command."""
        mock_service = Mock()
        mock_service.update_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.update_task(1, "Updated title", "Updated description")

        mock_service.update_task.assert_called_once_with(1, "Updated title", "Updated description", None, None, None, None, None)
        assert result is True

    def test_update_task_command_partial(self):
        """Test updating only title or description via CLI command."""
        mock_service = Mock()
        mock_service.update_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Update only title
        result = cli.update_task(1, "Updated title")

        mock_service.update_task.assert_called_once_with(1, "Updated title", None, None, None, None, None, None)
        assert result is True

    def test_complete_task_command(self):
        """Test completing a task via CLI command."""
        mock_service = Mock()
        mock_service.complete_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.complete_task(1)

        mock_service.complete_task.assert_called_once_with(1)
        assert result is True

    def test_delete_task_command(self):
        """Test deleting a task via CLI command."""
        mock_service = Mock()
        mock_service.delete_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.delete_task(1)

        mock_service.delete_task.assert_called_once_with(1)
        assert result is True

    def test_display_empty_task_list(self):
        """Test displaying an empty task list."""
        mock_service = Mock()
        mock_service.list_tasks.return_value = []
        mock_formatter = Mock()
        mock_formatter.format_task_list.return_value = "No tasks found."

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.list_tasks()

        assert result == "No tasks found."

    def test_restore_task_command_success(self):
        """Test restoring a task via CLI command successfully."""
        mock_service = Mock()
        mock_service.restore_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.restore_task(1)

        mock_service.restore_task.assert_called_once_with(1)
        assert result is True

    def test_restore_task_command_failure(self):
        """Test restoring a task via CLI command failure."""
        mock_service = Mock()
        mock_service.restore_task.return_value = False
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        result = cli.restore_task(999)

        mock_service.restore_task.assert_called_once_with(999)
        assert result is False

    def test_handle_complete_multiple_tasks(self, capsys):
        """Test handling complete command with multiple task IDs."""
        mock_service = Mock()
        mock_service.complete_task.side_effect = [True, False, True]  # Success, not found, success
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["complete", "1", "2", "3"]
        command = ["complete", "1", "2", "3"]
        cli._handle_complete(command)

        # Check that complete_task was called for each ID
        calls = [((1,),), ((2,),), ((3,),)]
        mock_service.complete_task.assert_has_calls(calls)
        assert mock_service.complete_task.call_count == 3

        # Capture output to verify messages
        captured = capsys.readouterr()
        output = captured.out
        assert "Task 1 marked as complete" in output
        assert "Task 2 not found" in output
        assert "Task 3 marked as complete" in output

    def test_handle_delete_multiple_tasks(self, capsys):
        """Test handling delete command with multiple task IDs."""
        mock_service = Mock()
        mock_service.delete_task.side_effect = [True, True, False]  # Success, success, not found
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["delete", "4", "5", "6"]
        command = ["delete", "4", "5", "6"]
        cli._handle_delete(command)

        # Check that delete_task was called for each ID
        calls = [((4,),), ((5,),), ((6,),)]
        mock_service.delete_task.assert_has_calls(calls)
        assert mock_service.delete_task.call_count == 3

        # Capture output to verify messages
        captured = capsys.readouterr()
        output = captured.out
        assert "Task 4 deleted successfully" in output
        assert "Task 5 deleted successfully" in output
        assert "Task 6 not found" in output

    def test_handle_restore_multiple_tasks(self, capsys):
        """Test handling restore command with multiple task IDs."""
        mock_service = Mock()
        mock_service.restore_task.side_effect = [True, False, True]  # Success, not found, success
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["restore", "2", "3", "7"]
        command = ["restore", "2", "3", "7"]
        cli._handle_restore(command)

        # Check that restore_task was called for each ID
        calls = [((2,),), ((3,),), ((7,),)]
        mock_service.restore_task.assert_has_calls(calls)
        assert mock_service.restore_task.call_count == 3

        # Capture output to verify messages
        captured = capsys.readouterr()
        output = captured.out
        assert "Task 2 restored successfully" in output
        assert "Task 3 not found or not deleted" in output
        assert "Task 7 restored successfully" in output

    def test_handle_complete_invalid_ids(self, capsys):
        """Test handling complete command with invalid task IDs."""
        mock_service = Mock()
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["complete", "1", "abc", "3"]
        command = ["complete", "1", "abc", "3"]
        cli._handle_complete(command)

        # Check that complete_task was called only for valid IDs
        calls = [((1,),), ((3,),)]
        mock_service.complete_task.assert_has_calls(calls)
        assert mock_service.complete_task.call_count == 2

        # Capture output to verify error message for invalid ID
        captured = capsys.readouterr()
        output = captured.out
        assert "Task ID 'abc' must be a number" in output
        assert "Task 1 marked as complete" in output
        assert "Task 3 marked as complete" in output

    def test_handle_single_task_still_works(self, capsys):
        """Test that single task operations still work as before."""
        mock_service = Mock()
        mock_service.complete_task.return_value = True
        mock_service.delete_task.return_value = True
        mock_service.restore_task.return_value = True
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Test single complete task
        command = ["complete", "5"]
        cli._handle_complete(command)
        mock_service.complete_task.assert_called_once_with(5)

        # Test single delete task
        command = ["delete", "6"]
        cli._handle_delete(command)
        mock_service.delete_task.assert_called_once_with(6)

        # Test single restore task
        command = ["restore", "7"]
        cli._handle_restore(command)
        mock_service.restore_task.assert_called_once_with(7)

        # Capture output to verify single task messages
        captured = capsys.readouterr()
        output = captured.out
        assert "Task 5 marked as complete" in output
        assert "Task 6 deleted successfully" in output
        assert "Task 7 restored successfully" in output