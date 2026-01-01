import pytest
from unittest.mock import Mock
from datetime import datetime
from domain.entities.task import Task
from application.services.todo_service import TodoService


class TestTodoServiceSearch:
    """Test cases for TodoService search functionality."""

    def test_search_tasks_by_keyword_in_title(self):
        """Test searching tasks by keyword in title."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "Read book", "Read a programming book", False, datetime.now(), priority="high", tags=["learning"])
        task2 = Task(2, "Write code", "Write some Python code", False, datetime.now(), priority="medium", tags=["coding"])
        task3 = Task(3, "Clean room", "Clean the workspace", False, datetime.now(), priority="low", tags=["personal"])

        # Mock repository to return all tasks
        mock_repo.get_all.return_value = [task1, task2, task3]
        mock_repo.search.return_value = [task1]  # Only task with "Read" in title

        service = TodoService(mock_repo, mock_id_gen)

        # Search for tasks with "read" in title
        results = service.search_tasks(keyword="read")

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with("read", None, None, None, None)
        assert len(results) == 1
        assert results[0].title == "Read book"

    def test_search_tasks_by_keyword_in_description(self):
        """Test searching tasks by keyword in description."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "Read book", "Read a programming book", False, datetime.now(), priority="high", tags=["learning"])
        task2 = Task(2, "Write code", "Write some Python code", False, datetime.now(), priority="medium", tags=["coding"])
        task3 = Task(3, "Clean room", "Clean the workspace", False, datetime.now(), priority="low", tags=["personal"])

        # Mock repository to return matching tasks
        mock_repo.search.return_value = [task2]  # Only task with "Python" in description

        service = TodoService(mock_repo, mock_id_gen)

        # Search for tasks with "Python" in description
        results = service.search_tasks(keyword="Python")

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with("Python", None, None, None, None)
        assert len(results) == 1
        assert results[0].title == "Write code"

    def test_search_tasks_by_status(self):
        """Test searching tasks by status."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "Completed task", "A completed task", True, datetime.now(), priority="high", tags=["done"])
        task2 = Task(2, "Pending task", "A pending task", False, datetime.now(), priority="medium", tags=["todo"])

        # Mock repository to return matching tasks
        mock_repo.search.return_value = [task1]  # Only completed tasks

        service = TodoService(mock_repo, mock_id_gen)

        # Search for completed tasks
        results = service.search_tasks(status=True)

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with(None, True, None, None, None)
        assert len(results) == 1
        assert results[0].status is True

    def test_search_tasks_by_priority(self):
        """Test searching tasks by priority."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "High priority task", "A high priority task", False, datetime.now(), priority="high", tags=["urgent"])
        task2 = Task(2, "Medium priority task", "A medium priority task", False, datetime.now(), priority="medium", tags=["normal"])
        task3 = Task(3, "Low priority task", "A low priority task", False, datetime.now(), priority="low", tags=["later"])

        # Mock repository to return matching tasks
        mock_repo.search.return_value = [task1]  # Only high priority tasks

        service = TodoService(mock_repo, mock_id_gen)

        # Search for high priority tasks
        results = service.search_tasks(priority="high")

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with(None, None, "high", None, None)
        assert len(results) == 1
        assert results[0].priority == "high"

    def test_search_tasks_by_tags(self):
        """Test searching tasks by tags."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "Learning task", "Learning something new", False, datetime.now(), priority="high", tags=["learning", "python"])
        task2 = Task(2, "Coding task", "Working on code", False, datetime.now(), priority="medium", tags=["coding", "python"])
        task3 = Task(3, "Personal task", "Personal activity", False, datetime.now(), priority="low", tags=["personal"])

        # Mock repository to return matching tasks
        mock_repo.search.return_value = [task1, task2]  # Tasks with "python" tag

        service = TodoService(mock_repo, mock_id_gen)

        # Search for tasks with "python" tag
        results = service.search_tasks(tags=["python"])

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with(None, None, None, ["python"], None)
        assert len(results) == 2
        assert all("python" in task.tags for task in results)

    def test_search_tasks_by_sort_priority(self):
        """Test searching and sorting tasks by priority."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task_high = Task(1, "High priority", "High priority task", False, datetime.now(), priority="high", tags=[])
        task_low = Task(2, "Low priority", "Low priority task", False, datetime.now(), priority="low", tags=[])
        task_medium = Task(3, "Medium priority", "Medium priority task", False, datetime.now(), priority="medium", tags=[])

        # Mock repository to return tasks in specific order when sorted by priority
        mock_repo.search.return_value = [task_high, task_medium, task_low]

        service = TodoService(mock_repo, mock_id_gen)

        # Search and sort tasks by priority
        results = service.search_tasks(sort_by="priority")

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with(None, None, None, None, "priority")
        assert len(results) == 3
        # High priority should come first
        assert results[0].priority == "high"
        assert results[1].priority == "medium"
        assert results[2].priority == "low"

    def test_search_tasks_with_multiple_filters(self):
        """Test searching tasks with multiple filters."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        # Create test tasks
        task1 = Task(1, "Read Python book", "Read Python programming book", False, datetime.now(), priority="high", tags=["learning", "python"])
        task2 = Task(2, "Write Python code", "Write Python code", True, datetime.now(), priority="medium", tags=["coding", "python"])
        task3 = Task(3, "Clean room", "Clean the workspace", False, datetime.now(), priority="low", tags=["personal"])

        # Mock repository to return matching tasks
        mock_repo.search.return_value = [task1]  # Tasks with "python" in title/description AND high priority

        service = TodoService(mock_repo, mock_id_gen)

        # Search for tasks with keyword "python" and high priority
        results = service.search_tasks(keyword="python", priority="high")

        # Verify the search method was called with the correct parameters
        mock_repo.search.assert_called_once_with("python", None, "high", None, None)
        assert len(results) == 1
        assert results[0].title == "Read Python book"

    def test_search_tasks_validation_invalid_priority(self):
        """Test that searching with invalid priority raises an error."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Try to search with invalid priority
        with pytest.raises(ValueError, match="Priority must be one of: high, medium, low"):
            service.search_tasks(priority="invalid")

    def test_search_tasks_validation_invalid_sort_by(self):
        """Test that searching with invalid sort_by raises an error."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Try to search with invalid sort_by
        with pytest.raises(ValueError, match="Sort by must be one of: "):
            service.search_tasks(sort_by="invalid")

    def test_search_tasks_validation_invalid_tags(self):
        """Test that searching with invalid tags raises an error."""
        mock_repo = Mock()
        mock_id_gen = Mock()

        service = TodoService(mock_repo, mock_id_gen)

        # Try to search with invalid tags (not a list)
        with pytest.raises(ValueError, match="Tags must be a list of strings"):
            service.search_tasks(tags="not_a_list")

        # Try to search with invalid tags (list with non-strings)
        with pytest.raises(ValueError, match="All tags must be strings"):
            service.search_tasks(tags=["valid", 123])