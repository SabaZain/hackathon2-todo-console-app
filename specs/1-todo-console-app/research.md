# Research Document: Phase I Todo In-Memory Python Console App

## Decision: CLI Framework Choice
**Rationale**: For a console-based application that needs to support both interactive mode and command-line arguments, Python's built-in `cmd` module is the most appropriate choice. It provides a framework for command interpreters with a command loop, making it ideal for interactive console applications. For command-line argument parsing when running non-interactively, `argparse` will be used.

**Alternatives considered**:
- `argparse` alone: Good for command-line arguments but doesn't provide interactive loop functionality
- `click`: More feature-rich but introduces external dependency
- Custom parser: Would require more implementation effort

## Decision: In-Memory Storage Implementation
**Rationale**: For Phase I with in-memory storage requirements, a simple Python dictionary will be used as the data store. The key will be the task ID (integer) and the value will be the Task entity object. This provides O(1) lookup performance and is simple to implement and maintain.

**Alternatives considered**:
- List-based storage: Would require searching for tasks by ID
- SQLite in-memory: Would introduce unnecessary complexity for Phase I
- Custom data structure: Would require more implementation effort

## Decision: Task ID Generation
**Rationale**: A simple counter-based ID generator will be implemented that starts at 1 and increments for each new task. The counter will be maintained in the application layer. When a task is deleted, its ID will not be reused to maintain consistency as specified in the domain model.

**Alternatives considered**:
- UUID: Would be overkill for this simple application
- Random integer: Could result in collisions
- Time-based: Could result in collisions with rapid task creation

## Decision: Testing Framework
**Rationale**: Pytest is the standard testing framework for Python applications. It provides simple syntax, powerful fixtures, and good integration with development tools. It supports both unit and integration testing, which is required for this multi-layered architecture.

**Alternatives considered**:
- unittest: Built-in but more verbose syntax
- nose: No longer actively maintained
- Custom testing: Would require significant implementation effort

## Decision: Date/Time Handling
**Rationale**: Python's built-in `datetime` module will be used to handle timestamps for task creation. The `datetime.now()` function will provide the required timestamp functionality in a standard format.

**Alternatives considered**:
- `time` module: Less feature-rich for date/time manipulation
- Third-party libraries like `arrow`: Would introduce unnecessary dependencies for Phase I

## Decision: Error Handling Strategy
**Rationale**: Custom exception classes will be created for each type of domain error (e.g., TaskNotFound, InvalidTaskTitle). This allows for specific error handling while maintaining clean separation of concerns in the architecture.

**Alternatives considered**:
- Generic exceptions: Would make error handling less precise
- Return codes: Would not follow Python conventions
- Boolean returns: Would not provide enough error information