# Quickstart Guide: Phase I Todo In-Memory Python Console App

## Development Setup

### Prerequisites
- Python 3.13+ installed
- pip package manager

### Initial Setup
1. Create a new Python project:
   ```bash
   mkdir todo-app
   cd todo-app
   ```

2. Set up virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pytest  # For testing
   ```

## Project Structure
The project follows Clean Architecture principles with the following structure:
```
todo_app/
├── domain/                 # Business logic and entities
│   ├── entities/
│   │   └── task.py
│   └── repositories/
│       └── task_repository.py
├── application/            # Use cases and application logic
│   └── use_cases/
│       ├── add_task.py
│       ├── delete_task.py
│       ├── update_task.py
│       ├── list_tasks.py
│       └── toggle_task_status.py
├── infrastructure/         # External concerns (in-memory storage)
│   └── repositories/
│       └── in_memory_task_repository.py
├── presentation/           # User interface (CLI)
│   ├── cli/
│   │   ├── command_parser.py
│   │   ├── command_handlers.py
│   │   └── cli_app.py
│   └── formatters/
│       └── task_formatter.py
├── tests/                  # Test suite
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── presentation/
├── main.py                 # Application entry point
└── requirements.txt        # Project dependencies
```

## Running the Application
```bash
python main.py
```

## Running Tests
```bash
python -m pytest
```

## Key Implementation Notes

### Domain Layer
- The `Task` entity contains validation logic
- Repository interfaces are defined here
- Business rules are enforced at this layer

### Application Layer
- Use cases orchestrate business logic
- Input validation happens here
- Interacts with domain entities and repositories

### Infrastructure Layer
- In-memory repository implementation
- Task ID generation
- Data persistence during runtime

### Presentation Layer
- CLI command parsing
- User interaction handling
- Output formatting

## Testing Strategy
- Test each layer independently
- Use mocks for repository dependencies in use case tests
- Integration tests for CLI functionality
- Follow TDD approach: write tests first, then implement