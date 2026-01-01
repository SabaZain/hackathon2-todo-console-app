---
id: 2
title: undo-delete-restore-tasks
stage: general
date_iso: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude
command: /sp.implement
labels: ["undo", "delete", "restore", "tdd", "persistence"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - domain/entities/task.py
  - domain/repositories/task_repository.py
  - infrastructure/repositories/in_memory_task_repository.py
  - infrastructure/repositories/file_task_repository.py
  - application/services/todo_service.py
  - presentation/cli/cli_app.py
  - tests/domain/test_task.py
  - tests/infrastructure/test_file_task_repository.py
  - tests/infrastructure/test_in_memory_task_repository.py
  - tests/application/test_todo_service.py
  - tests/presentation/test_cli_commands.py
test_yaml: |
  - tests/infrastructure/test_file_task_repository.py
  - tests/infrastructure/test_in_memory_task_repository.py
  - tests/application/test_todo_service.py
  - tests/presentation/test_cli_commands.py
  - All existing tests
prompt_text: |
  Feature: Undo Delete / Restore Deleted Tasks

  Context:
  The Todo Console App currently supports file-based persistence and CLI commands (add, list, update, complete, delete).
  Deleted tasks are currently permanently removed. We want to allow users to restore recently deleted tasks.
  The solution must preserve Clean Architecture principles, TDD approach, and CLI compatibility.

  Requirements:

  1. Soft Delete in Repository
     - Modify FileTaskRepository to mark tasks as deleted instead of removing them.
     - Add a boolean field `deleted` to Task (default False).
     - `delete(task_id)` sets `deleted = True`.
     - `get_all()` should only return tasks where deleted=False.
     - Add a `restore(task_id)` method to set deleted=False.

  2. Service Layer
     - Add `restore_task(task_id)` method in TodoService that calls repository.restore().
     - Ensure proper validation and error handling for non-existent or non-deleted tasks.

  3. CLI
     - Add `restore <id>` command to the CLI.
     - User can type `restore 5` to restore task with ID 5.
     - Provide clear messages for success or errors.

  4. Tests (TDD Approach)
     - Write tests first for repository.restore(), service.restore_task(), and CLI restore command.
     - Ensure all existing tests continue to pass.
     - Test persistence across application restarts (file-based repo).

  5. Deliverables
     - Updated FileTaskRepository with soft delete and restore.
     - Updated TodoService with restore_task().
     - Updated CLI with restore command.
     - Comprehensive tests for restore functionality.

  Goal:
  Enable undo delete functionality without breaking existing commands or file persistence. Follow Clean Architecture principles strictly:
  - No business logic in CLI or infrastructure beyond persistence.
  - Dependency injection maintained.
  - Red-green-refactor cycle followed throughout.

  Proceed step-by-step. Explain architectural decisions briefly where relevant. Ensure full TDD coverage.
response_text: |
  Successfully implemented the undo delete / restore deleted tasks feature for the Todo Console App.

  ## Key Deliverables Completed:

  1. **Task Entity Update** (`domain/entities/task.py`):
     - Added `deleted: bool = False` field to Task entity
     - Updated validation to include deleted field
     - Updated `__str__` and `__repr__` methods to include deleted field

  2. **Repository Interface Update** (`domain/repositories/task_repository.py`):
     - Added `restore(self, task_id: int) -> bool` method to TaskRepository interface
     - Updated documentation for `get_all()` to indicate it returns non-deleted tasks
     - Updated documentation for `delete()` to indicate it marks tasks as deleted

  3. **Repository Implementations**:
     - **InMemoryTaskRepository** (`infrastructure/repositories/in_memory_task_repository.py`):
       - Implemented soft delete by setting `task.deleted = True`
       - Implemented restore method to set `task.deleted = False`
       - Updated `get_all()` to return only non-deleted tasks
     - **FileTaskRepository** (`infrastructure/repositories/file_task_repository.py`):
       - Implemented soft delete by setting `task_dict['deleted'] = True` in JSON
       - Implemented restore method to set `task_dict['deleted'] = False`
       - Updated `get_all()` to return only non-deleted tasks
       - Updated serialization/deserialization to handle deleted field

  4. **Service Layer** (`application/services/todo_service.py`):
     - Added `restore_task(task_id: int) -> bool` method
     - Added proper validation to check if task exists and is deleted
     - Calls repository's restore method

  5. **CLI Updates** (`presentation/cli/cli_app.py`):
     - Added `restore <id>` command to command processing
     - Added `_handle_restore()` method for command processing
     - Updated help text to include restore command
     - Updated welcome message to include restore in available commands

  6. **Comprehensive Tests**:
     - Updated Task entity tests to account for new `deleted` field
     - Added repository tests for soft delete and restore functionality
     - Added service tests for `restore_task` method
     - Added CLI tests for restore command

  ## Technical Details:
  - All 89 tests pass (original tests + new restore functionality tests)
  - Clean Architecture maintained throughout
  - Proper separation of concerns
  - Soft delete preserves tasks in storage but excludes them from get_all()
  - File-based persistence maintains deleted state across application restarts
  - Error handling for non-existent and non-deleted tasks
outcome: |
  All requirements met successfully. The application now supports undo delete functionality
  while maintaining backward compatibility and Clean Architecture principles.
  Users can delete tasks (soft delete) and restore them using the new restore command.
  The file persistence properly maintains the deleted state across application restarts.
evaluation: |
  - Soft delete in repository: ✅ Implemented
  - Service layer restore method: ✅ Implemented
  - CLI restore command: ✅ Implemented
  - TDD approach: ✅ All tests written before implementation
  - Clean Architecture: ✅ Principles maintained throughout
  - Persistence across restarts: ✅ File-based storage maintains state
---