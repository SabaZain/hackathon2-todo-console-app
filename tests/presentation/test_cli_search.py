import pytest
from unittest.mock import Mock
from domain.entities.task import Task
from presentation.cli.cli_app import TodoCLI


class TestCLISearch:
    """Test cases for CLI search functionality."""

    def test_search_command_with_keyword(self):
        """Test the search command with keyword parameter."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [
            Task(1, "Read Python book", "Read Python programming book", False, None, priority="high", tags=["learning", "python"])
        ]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Formatted search results"

        cli = TodoCLI(mock_service, mock_formatter)

        # Execute search command
        result = cli.search_tasks(keyword="python")

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(keyword="python", status=None, priority=None, tags=None, sort_by=None)
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)
        assert result == "Formatted search results"

    def test_search_command_with_multiple_filters(self):
        """Test the search command with multiple filters."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [
            Task(1, "High priority task", "A high priority task", False, None, priority="high", tags=["urgent"])
        ]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Filtered results"

        cli = TodoCLI(mock_service, mock_formatter)

        # Execute search command with multiple filters
        result = cli.search_tasks(keyword="priority", status=False, priority="high", tags=["urgent"], sort_by="priority")

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(
            keyword="priority",
            status=False,
            priority="high",
            tags=["urgent"],
            sort_by="priority"
        )
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)
        assert result == "Filtered results"

    def test_list_command_with_filters(self):
        """Test the list command with filter parameters."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [
            Task(1, "Completed task", "A completed task", True, None, priority="medium", tags=["done"])
        ]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Filtered list"

        cli = TodoCLI(mock_service, mock_formatter)

        # Execute list command with filters
        result = cli.list_tasks(status="completed", priority="medium")

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(
            keyword=None,
            status=True,  # "completed" should convert to True
            priority="medium",
            tags=None,
            sort_by=None
        )
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)
        assert result == "Filtered list"

    def test_list_command_with_status_conversion(self):
        """Test the list command status parameter conversion."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [Task(1, "Test task", "Test description", True, None, priority="medium", tags=[])]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Results"

        cli = TodoCLI(mock_service, mock_formatter)

        # Test different status values that should convert to True
        cli.list_tasks(status="completed")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=True,
            priority=None,
            tags=None,
            sort_by=None
        )

        cli.list_tasks(status="true")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=True,
            priority=None,
            tags=None,
            sort_by=None
        )

        cli.list_tasks(status="1")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=True,
            priority=None,
            tags=None,
            sort_by=None
        )

        # Test different status values that should convert to False
        cli.list_tasks(status="pending")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=False,
            priority=None,
            tags=None,
            sort_by=None
        )

        cli.list_tasks(status="false")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=False,
            priority=None,
            tags=None,
            sort_by=None
        )

        cli.list_tasks(status="0")
        mock_service.search_tasks.assert_called_with(
            keyword=None,
            status=False,
            priority=None,
            tags=None,
            sort_by=None
        )

    def test_list_command_with_invalid_status(self):
        """Test the list command with invalid status parameter."""
        mock_service = Mock()
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Test invalid status value
        with pytest.raises(ValueError, match="Status must be 'completed', 'pending', 'true', 'false', '1', or '0'"):
            cli.list_tasks(status="invalid")

    def test_handle_search_command(self, capsys):
        """Test handling the search command via CLI."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [Task(1, "Search result", "Description", False, None, priority="high", tags=[])]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Search result output"

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["search", "keyword=python", "priority=high"]
        command = ["search", "keyword=python", "priority=high"]
        cli._handle_search(command)

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(
            keyword="python",
            status=None,
            priority="high",
            tags=None,
            sort_by=None
        )
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)

        # Capture and check output
        captured = capsys.readouterr()
        assert "Search result output" in captured.out

    def test_handle_list_command_with_filters(self, capsys):
        """Test handling the list command with filters via CLI."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [Task(1, "Filtered task", "Description", True, None, priority="medium", tags=[])]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Filtered task output"

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["list", "status=completed", "sort=priority"]
        command = ["list", "status=completed", "sort=priority"]
        cli._handle_list(command)

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(
            keyword=None,
            status=True,
            priority=None,
            tags=None,
            sort_by="priority"
        )
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)

        # Capture and check output
        captured = capsys.readouterr()
        assert "Filtered task output" in captured.out

    def test_handle_search_command_with_tags(self, capsys):
        """Test handling the search command with tags parameter."""
        mock_service = Mock()
        mock_formatter = Mock()

        # Mock the search results
        mock_tasks = [Task(1, "Tagged task", "Description", False, None, priority="low", tags=["work", "urgent"])]
        mock_service.search_tasks.return_value = mock_tasks
        mock_formatter.format_task_list.return_value = "Tagged results"

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["search", "tags=work,urgent"]
        command = ["search", "tags=work,urgent"]
        cli._handle_search(command)

        # Verify the service method was called with correct parameters
        mock_service.search_tasks.assert_called_once_with(
            keyword=None,
            status=None,
            priority=None,
            tags=["work", "urgent"],
            sort_by=None
        )
        mock_formatter.format_task_list.assert_called_once_with(mock_tasks)

        # Capture and check output
        captured = capsys.readouterr()
        assert "Tagged results" in captured.out

    def test_handle_search_command_with_unknown_parameter(self, capsys):
        """Test handling the search command with unknown parameter."""
        mock_service = Mock()
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["search", "unknown=param"]
        command = ["search", "unknown=param"]
        cli._handle_search(command)

        # Capture and check output - should show error message
        captured = capsys.readouterr()
        assert "Unknown parameter: unknown=param" in captured.out

    def test_handle_list_command_with_unknown_filter(self, capsys):
        """Test handling the list command with unknown filter."""
        mock_service = Mock()
        mock_formatter = Mock()

        cli = TodoCLI(mock_service, mock_formatter)

        # Simulate command input: ["list", "unknown=param"]
        command = ["list", "unknown=param"]
        cli._handle_list(command)

        # Capture and check output - should show error message
        captured = capsys.readouterr()
        assert "Unknown filter: unknown=param" in captured.out