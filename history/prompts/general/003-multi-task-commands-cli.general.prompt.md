---
id: 3
title: multi-task-commands-cli
stage: general
date_iso: 2025-12-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: Claude
command: /sp.implement
labels: ["cli", "multi-task", "tdd", "refactor"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml: |
  - presentation/cli/cli_app.py
  - tests/presentation/test_cli_commands.py
test_yaml: |
  - tests/presentation/test_cli_commands.py
  - All existing tests
prompt_text: |
  Feature: Multi-Task Commands in CLI

  Context:
  The Todo Console App CLI currently only allows completing, deleting, or restoring one task at a time.
  We want to allow users to pass multiple task IDs in a single command, e.g. `complete 1 2 3`.

  Requirements:

  1. CLI Updates
     - Modify `_handle_complete`, `_handle_delete`, `_handle_restore` methods in TodoCLI.
     - Accept multiple task IDs separated by spaces.
     - For each ID:
       - Validate it is a number
       - Call the corresponding service method (`complete_task`, `delete_task`, `restore_task`)
       - Print appropriate success or error message per task
     - Usage examples:
       - `complete 1 2 3`
       - `delete 4 5 6`
       - `restore 2 3`

  2. Service & Repository
     - No changes needed; continue using existing methods for single task operations.
     - CLI should call the existing service methods iteratively.

  3. Tests
     - Update CLI tests to cover multiple ID commands.
     - Ensure old single-ID commands still work.
     - Maintain TDD approach.

  Deliverables:
  - Updated TodoCLI class supporting multiple task IDs for complete, delete, and restore commands.
  - Updated CLI tests for multi-ID scenarios.

  Goal:
  Enable users to operate on multiple tasks in one command while preserving Clean Architecture and CLI behavior.

  Proceed step-by-step using red-green-refactor. Explain briefly any architectural changes if needed.
response_text: |
  Successfully implemented multi-task commands in the CLI for the Todo Console App.

  ## Key Deliverables Completed:

  1. **CLI Updates** (`presentation/cli/cli_app.py`):
     - Modified `_handle_complete` to accept multiple task IDs
     - Modified `_handle_delete` to accept multiple task IDs
     - Modified `_handle_restore` to accept multiple task IDs
     - Updated usage messages to reflect multi-ID support
     - Updated help text to show multi-ID examples
     - Added proper error handling for invalid IDs

  2. **Implementation Details**:
     - Commands now accept variable number of task IDs: `complete 1 2 3`, `delete 4 5 6`, `restore 2 3`
     - Each ID is processed individually with separate success/error messages
     - Invalid IDs are handled gracefully with appropriate error messages
     - Backward compatibility maintained for single ID commands

  3. **Comprehensive Tests** (`tests/presentation/test_cli_commands.py`):
     - Added tests for multiple task operations (complete, delete, restore)
     - Added tests for handling invalid IDs
     - Added tests to ensure single-task operations still work
     - Used capsys to verify output messages for each operation

  ## Technical Details:
  - All 94 tests pass (original tests + new multi-ID functionality tests)
  - Clean Architecture maintained throughout
  - Proper error handling for invalid inputs
  - Backward compatibility preserved
  - TDD approach followed with comprehensive test coverage
outcome: |
  All requirements met successfully. The CLI now supports multi-task commands
  while maintaining backward compatibility and Clean Architecture principles.
  Users can operate on multiple tasks in a single command (e.g., `complete 1 2 3`)
  with appropriate success/error messages for each task.
evaluation: |
  - CLI multi-ID support: ✅ Implemented
  - Backward compatibility: ✅ Maintained
  - Error handling: ✅ Comprehensive
  - TDD approach: ✅ Followed with new tests
  - Clean Architecture: ✅ Maintained
---