# Phase I – Todo In-Memory Python Console App Specification

## Overview

This specification defines Phase I of the "Evolution of Todo" project: an in-memory Python console-based Todo application. The application will provide basic todo management functionality through a command-line interface with 5 core features: adding, deleting, updating, viewing, and marking tasks as complete.

## Domain Model

### Task Entity
- **ID**: A unique identifier for each task (auto-generated integer)
- **Title**: A required string representing the task description
- **Description**: An optional string with additional details about the task
- **Status**: A boolean indicating if the task is completed (True) or pending (False)
- **Created Timestamp**: The time when the task was created (auto-generated)

### Valid States
- **Pending**: Task exists but is not yet completed
- **Completed**: Task has been marked as done

### ID Rules
- Each task must have a unique integer ID
- IDs are auto-generated when a task is created
- IDs must be positive integers
- Deleted task IDs are not reused

## CLI Commands & UX

### Command Format
The application will use a simple command-line interface with the following commands:

- `add "title" ["description"]` - Add a new task
- `delete <id>` - Delete a task by its ID
- `update <id> "new_title" ["new_description"]` - Update task details
- `list` - Display all tasks with status indicators
- `complete <id>` - Mark a task as complete
- `incomplete <id>` - Mark a completed task as pending again
- `help` - Show available commands
- `quit` or `exit` - Exit the application

### User Interface Flow
1. Application starts and displays a prompt (e.g., `todo> `)
2. User enters a command
3. Application processes the command and displays results
4. Application returns to the prompt for the next command

### Display Format
- **List command output**: Show all tasks with ID, status indicator, title, and description
  - Format: `[ID] [Status] Title - Description`
  - Status indicators: `[ ]` for pending, `[x]` for completed
  - Example: `1 [ ] Buy groceries - Need to get milk and bread`
  - Example: `2 [x] Complete project - Submit final report`

## Functional Requirements

### FR-001: Add Task
**Requirement**: The system shall allow users to create new todo items with a required title and optional description.
- **Input**: Title (required string), Description (optional string)
- **Output**: Success message with the created task ID, or error message
- **Validation**: Title must not be empty
- **Post-condition**: New task is added to the in-memory store with a unique ID and pending status

### FR-002: Delete Task
**Requirement**: The system shall allow users to remove a task by its unique ID.
- **Input**: Task ID (integer)
- **Output**: Success confirmation or error message
- **Validation**: Task with the given ID must exist
- **Post-condition**: Task is removed from the in-memory store

### FR-003: Update Task
**Requirement**: The system shall allow users to modify the title and/or description of an existing task.
- **Input**: Task ID (integer), New title (optional string), New description (optional string)
- **Output**: Success confirmation or error message
- **Validation**: Task with the given ID must exist; if title is provided, it must not be empty
- **Post-condition**: Task details are updated in the in-memory store

### FR-004: View Task List
**Requirement**: The system shall display all tasks with clear status indicators.
- **Input**: None
- **Output**: List of all tasks showing ID, status, title, and description
- **Validation**: None required
- **Post-condition**: None; this is a read-only operation

### FR-005: Mark as Complete
**Requirement**: The system shall allow users to toggle task state between pending and completed.
- **Input**: Task ID (integer)
- **Output**: Success confirmation or error message
- **Validation**: Task with the given ID must exist
- **Post-condition**: Task status is toggled (pending↔completed) in the in-memory store

## Validation Rules

### Input Validation
- Task titles must not be empty or contain only whitespace
- Task IDs must be positive integers
- Commands must follow the expected format
- When updating, at least one of title or description must be provided

### Business Validation
- Task IDs must correspond to existing tasks
- Only valid commands should be accepted
- Commands should provide appropriate feedback for invalid inputs

## Error Handling

### Error Types and Messages
- **Invalid Command**: "Error: Unknown command. Type 'help' for available commands."
- **Missing Arguments**: "Error: Missing required arguments for command."
- **Invalid Task ID**: "Error: Task with ID [X] does not exist."
- **Empty Title**: "Error: Task title cannot be empty."
- **Invalid Format**: "Error: Invalid command format. Use 'help' for syntax."

### Error Recovery
- The application should continue running after displaying error messages
- Invalid commands should not affect the application state
- The user should be returned to the prompt after any error

## Acceptance Criteria

### Success Criteria
1. **Functionality**:
   - [ ] Users can add tasks with title and optional description
   - [ ] Users can delete tasks by ID
   - [ ] Users can update task title and/or description
   - [ ] Users can view all tasks with clear status indicators
   - [ ] Users can mark tasks as complete/incomplete
   - [ ] All operations work correctly with the in-memory storage

2. **User Experience**:
   - [ ] Command interface is intuitive and responsive
   - [ ] Error messages are clear and helpful
   - [ ] Status indicators clearly show task completion state
   - [ ] Help command provides useful information

3. **Quality**:
   - [ ] All validation rules are enforced
   - [ ] Error handling is comprehensive
   - [ ] The application handles edge cases gracefully
   - [ ] Performance is acceptable for typical usage

### Test Scenarios
1. **Add Task**:
   - Add task with title only
   - Add task with title and description
   - Attempt to add task with empty title (should fail)

2. **Delete Task**:
   - Delete existing task
   - Attempt to delete non-existent task (should fail)

3. **Update Task**:
   - Update task title only
   - Update task description only
   - Update both title and description
   - Attempt to update non-existent task (should fail)

4. **View Task List**:
   - View empty list
   - View list with pending tasks
   - View list with completed tasks
   - View list with mixed pending/completed tasks

5. **Mark as Complete**:
   - Mark pending task as complete
   - Mark completed task as pending
   - Attempt to mark non-existent task (should fail)

## Constraints and Limitations

- All data is stored in-memory only (no persistence)
- No concurrent users (single-user application)
- No authentication or authorization required
- No network connectivity required
- All operations are synchronous

## Assumptions

- The Python environment supports command-line input/output
- Users have basic familiarity with command-line interfaces
- The application will run on standard operating systems (Windows, macOS, Linux)
- Time-based operations use the system clock for timestamps