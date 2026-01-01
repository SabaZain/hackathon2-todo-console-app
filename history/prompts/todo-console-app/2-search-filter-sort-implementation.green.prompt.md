---
id: 2
title: Search Filter Sort Implementation
stage: green
date: 2025-12-31
surface: agent
model: Claude Sonnet 4.5
feature: todo-console-app
branch: master
user: Claude Code
command: Feature: Search, Filter, and Sort Tasks (Intermediate Level)
labels: [feature, search, filter, sort, tasks]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - domain/entities/task.py
 - domain/repositories/task_repository.py
 - infrastructure/repositories/in_memory_task_repository.py
 - infrastructure/repositories/file_task_repository.py
 - application/services/todo_service.py
 - presentation/cli/cli_app.py
 - presentation/formatters/task_formatter.py
 - tests/application/test_search_service.py
 - tests/presentation/test_cli_search.py
 - tests/application/test_use_cases.py
 - specs/1-todo-console-app/tasks.md
tests:
 - tests/application/test_search_service.py
 - tests/presentation/test_cli_search.py
 - tests/application/test_use_cases.py
---

## Prompt

Feature: Search, Filter, and Sort Tasks (Intermediate Level)

Context:
The Todo Console App currently supports file-based persistence, CLI commands (add, list, update, complete, delete, restore), and priorities/tags. The app follows Clean Architecture and TDD.
We want to enhance the app to allow users to:
- Search tasks by keyword (in title or description)
- Filter tasks by status (completed/pending), priority, or tags
- Sort tasks by due date, priority, or alphabetically

Requirements:

1. Domain Layer
   - Ensure Task entity has optional `due_date` (datetime) field for sorting
   - Ensure backward compatibility with existing tasks

2. Repository Layer
   - Update InMemoryTaskRepository and FileTaskRepository to:
       - Accept search keyword, filter options, and sort parameters in `get_all()` or a new method
       - Efficiently return filtered/sorted task lists
       - Maintain persistence and data integrity

3. Service Layer
   - Add `search_tasks(keyword=None, status=None, priority=None, tags=None, sort_by=None)` method in TodoService
   - Validate filter values and sort parameters
   - Return list of tasks matching criteria

4. CLI Layer
   - Add `search` command:
       - Example: `search keyword="read" status=pending priority=high tags=work sort=priority`
   - Update `list` command to accept optional filter and sort parameters
   - Display results in consistent format with priority/tags

5. Tests (TDD)
   - Write tests for repository search/filter/sort methods
   - Write tests for service layer method
   - Write tests for CLI search command
   - Ensure all existing tests continue to pass

Deliverables:
- Updated InMemoryTaskRepository and FileTaskRepository
- Updated TodoService with search/filter/sort
- Updated CLI commands for search and filtered list
- Comprehensive tests
- All tests passing

Goal:
Enable users to easily search, filter, and sort tasks without breaking existing functionality. Follow red-green-refactor step-by-step.

## Response snapshot

Successfully implemented the Search, Filter, and Sort Tasks feature for the Todo Console App. The implementation includes:

1. **Domain Layer**:
   - Added optional `due_date` field to the Task entity in `domain/entities/task.py`
   - Added validation for the due_date field
   - Updated string representations to include due_date

2. **Repository Layer**:
   - Updated `TaskRepository` interface with a new `search` method
   - Implemented search/filter/sort logic in `InMemoryTaskRepository`
   - Implemented search/filter/sort logic in `FileTaskRepository`
   - Added support for filtering by keyword, status, priority, tags
   - Added support for sorting by priority, due_date, title, created_at, status
   - Updated JSON serialization to properly handle due_date field in FileTaskRepository

3. **Service Layer**:
   - Enhanced `TodoService` with `search_tasks` method
   - Added validation for all filter parameters
   - Updated `add_task` and `update_task` methods to handle due_date parameter
   - Proper error handling for invalid parameters

4. **CLI Layer**:
   - Added `search` command with comprehensive filtering options
   - Updated `list` command to accept filter and sort parameters
   - Enhanced help text with new command documentation
   - Added support for keyword, status, priority, tags, and sort filters
   - Improved status string to boolean conversion

5. **Presentation Layer**:
   - Updated `TaskFormatter` to display due_date in task formatting
   - Enhanced display format to show due dates

6. **Testing**:
   - Created comprehensive tests for search functionality in `tests/application/test_search_service.py`
   - Created CLI search tests in `tests/presentation/test_cli_search.py`
   - Created use case tests in `tests/application/test_use_cases.py`
   - Updated existing tests to match new method signatures
   - All 123 tests pass, ensuring no regression

The feature allows users to:
- Search tasks by keyword in title or description
- Filter tasks by status (completed/pending), priority (high/medium/low), or tags
- Sort tasks by priority, due date, title, creation date, or status
- Use multiple filters simultaneously
- Use the new `search` command or enhanced `list` command with filters

## Outcome

- ✅ Impact: Full implementation of search, filter, and sort functionality
- 🧪 Tests: 123/123 tests passing, including 10 new search tests
- 📁 Files: 11 files modified to implement the feature
- 🔁 Next prompts: Ready for additional features or enhancements
- 🧠 Reflection: Clean architecture maintained with proper separation of concerns

## Evaluation notes (flywheel)

- Failure modes observed: None - All existing functionality preserved
- Graders run and results (PASS/FAIL): PASS - All tests pass
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Performance optimization for large task lists