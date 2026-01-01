# Todo Console App

A feature-rich command-line interface (CLI) application for managing tasks and todos. Built with Clean Architecture principles, this application provides a complete task management solution through an intuitive command-line interface.

## Overview

The Todo Console App is a Python-based CLI application designed for efficient task management. It implements Clean Architecture with clear separation of concerns across domain, application, infrastructure, and presentation layers. The application supports basic, intermediate, and advanced task management features, making it suitable for both simple and complex productivity needs.

The application features in-memory storage for fast operations and includes file-based persistence. It supports both in-memory and file-based persistence, configurable via environment variables. It includes comprehensive support for recurring tasks, time-based reminders, and advanced search/filtering capabilities.

## Features

### Basic Features
- **Add Tasks**: Create new tasks with titles and optional descriptions
- **List Tasks**: View all tasks with clear status indicators
- **Complete Tasks**: Mark tasks as complete/pending
- **Delete Tasks**: Remove tasks from the system
- **Update Tasks**: Modify existing task details

### Intermediate Features
- **Task Priorities**: Assign priority levels (high, medium, low) to tasks
- **Task Tags**: Organize tasks with searchable tags
- **Due Dates**: Set deadlines for tasks
- **Advanced Filtering**: Search and filter tasks by keyword, status, priority, tags
- **Sorting**: Sort tasks by various criteria (priority, due date, title, etc.)

### Advanced Features
- **Recurring Tasks**: Create tasks that repeat daily, weekly, or monthly
- **Time Reminders**: Set specific datetime reminders for tasks
- **Automatic Scheduling**: Recurring tasks automatically generate next occurrence upon completion
- **Reminder Viewing**: View tasks with upcoming or past-due reminders via CLI

## CLI Usage Examples

### Basic Commands
```bash
# Add a new task
todo> add "Buy groceries" "Get milk, bread, and eggs" priority=high tags=shopping,food

# List all tasks
todo> list

# Mark a task as complete
todo> complete 1

# Update a task
todo> update 1 "Updated title" "New description" priority=medium

# Delete a task
todo> delete 1
```

### Advanced Commands
```bash
# Add a recurring task (daily, 7 occurrences)
todo> add "Take medication" "Take vitamins" recurring=daily,7

# Add a task with reminder
todo> add "Meeting prep" "Prepare slides" reminder=2026-01-02T09:00

# Search tasks by keyword
todo> search keyword=meeting status=pending priority=high

# Filter tasks with multiple criteria
todo> list status=pending priority=high sort=priority

# View upcoming reminders
todo> reminders
```

### Filtering and Sorting Options
- **Keyword**: `keyword=search_term` - Search in title and description
- **Status**: `status=completed|pending|true|false` - Filter by completion status
- **Priority**: `priority=high|medium|low` - Filter by priority level
- **Tags**: `tags=tag1,tag2` - Filter by tags
- **Sort**: `sort=priority|due_date|title|created_at|status` - Sort results

## Architecture Overview

The application follows Clean Architecture principles with four distinct layers:

### Domain Layer
- **Entities**: Core business objects (Task entity with validation)
- **Repositories**: Abstract interfaces defining data access contracts
- **Use Cases**: Business logic and rules

### Application Layer
- **Services**: Application-specific business rules (TodoService)
- **Use Cases**: Specific application operations
- **Interfaces**: Port definitions for external communication

### Infrastructure Layer
- **Repositories**: Concrete implementations (InMemoryTaskRepository, FileTaskRepository)
- **Frameworks**: External libraries and frameworks
- **Drivers**: Database connectors, web frameworks, etc.

### Presentation Layer
- **CLI**: Command-line interface components
- **Formatters**: Task display formatting
- **Controllers**: Handle user input and coordinate with services

## How to Run Locally

### Prerequisites
- Python 3.13 or higher
- pip (Python package installer)

### Installation
1. Clone the repository (if applicable) or navigate to the project directory
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
# Run the interactive CLI
python main.py
```

The application will start in interactive mode with a `todo> ` prompt where you can enter commands.

### Alternative: Running as Script
```bash
python main.py
```

## Testing Instructions

### Running All Tests
```bash
# Run all tests
python -m pytest tests/

# Run tests with verbose output
python -m pytest tests/ -v

# Run tests and show coverage
python -m pytest tests/ --cov=.
```

### Running Specific Test Categories
```bash
# Run domain tests
python -m pytest tests/domain/

# Run application service tests
python -m pytest tests/application/

# Run infrastructure tests
python -m pytest tests/infrastructure/

# Run presentation/UI tests
python -m pytest tests/presentation/
```

### Test Structure
- `tests/domain/` - Tests for domain entities and business rules
- `tests/application/` - Tests for application services and use cases
- `tests/infrastructure/` - Tests for repository implementations and infrastructure
- `tests/presentation/` - Tests for CLI interface and formatters

## Project Structure
```
todo_app/
├── application/           # Application layer (services, use cases)
│   ├── services/          # Application services (TodoService)
│   └── use_cases/         # Use case implementations
├── domain/                # Domain layer (entities, repositories, exceptions)
│   ├── entities/          # Domain entities (Task)
│   ├── repositories/      # Repository interfaces
│   └── exceptions/        # Domain exceptions
├── infrastructure/        # Infrastructure layer (repositories, frameworks)
│   └── repositories/      # Repository implementations
├── presentation/          # Presentation layer (CLI, formatters)
│   ├── cli/              # Command-line interface
│   └── formatters/       # Task display formatters
├── tests/                # Test suite
├── specs/                # Specification documents
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

## Key Design Decisions

1. **Clean Architecture**: Clear separation of concerns with dependency inversion
2. **Test-Driven Development**: Comprehensive test coverage for all layers
3. **Extensible CLI**: Flexible command system that supports advanced features
4. **Repository Pattern**: Abstraction over data storage allowing multiple implementations
5. **Validation at Every Layer**: Input validation from presentation to domain layer

## Contributing

This project follows a specification-driven development approach. New features should:
1. Begin with a clear specification document
2. Follow the Clean Architecture principles
3. Include comprehensive tests
4. Maintain backward compatibility where possible

## Development Methodology

This project follows modern software development practices:

- **Specification-driven development (SpecifyPlus)**: Features are developed based on detailed specifications before implementation
- **Red–Green–Refactor TDD**: Comprehensive test-driven development with red-green-refactor cycles
- **Prompt History Records (PHR)**: Complete history of development decisions and changes
- **Architecture Decision Records (ADR)**: Documented architectural decisions with rationale

## License

This project is licensed under the MIT License - see the LICENSE file for details.