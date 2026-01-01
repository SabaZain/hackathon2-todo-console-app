#!/usr/bin/env python3
"""
Main entry point for the Todo CLI Application.

This application demonstrates the Clean Architecture implementation
with domain, application, infrastructure, and presentation layers.
"""

from infrastructure.repositories.repository_factory import TaskRepositoryFactory
from application.services.id_generator import IDGenerator
from application.services.todo_service import TodoService
from presentation.formatters.task_formatter import TaskFormatter
from presentation.cli.cli_app import TodoCLI


def main():
    """Main entry point for the application."""
    # Initialize dependencies following Clean Architecture
    # Use the repository factory to allow configuration-based repository selection
    task_repository = TaskRepositoryFactory.get_default_repository()
    id_generator = IDGenerator()
    todo_service = TodoService(task_repository, id_generator)
    task_formatter = TaskFormatter()
    cli = TodoCLI(todo_service, task_formatter)

    # Run the interactive CLI
    cli.run_interactive()


if __name__ == "__main__":
    main()