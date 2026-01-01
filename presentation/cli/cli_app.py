from typing import Optional
from application.services.todo_service import TodoService
from presentation.formatters.task_formatter import TaskFormatter


class TodoCLI:
    """Command-line interface for the Todo application."""

    def __init__(self, todo_service: TodoService, task_formatter: TaskFormatter):
        """Initialize the CLI with dependencies."""
        self.todo_service = todo_service
        self.task_formatter = task_formatter

    def add_task(self, title: str, description: Optional[str] = None, priority: str = "medium", tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = None, reminder: Optional[str] = None) -> str:
        """Add a new task."""
        task_id = self.todo_service.add_task(title, description, priority, tags, due_date, recurring, reminder)
        tasks = self.todo_service.list_tasks()
        return f"Task added with ID {task_id}"

    def list_tasks(self, keyword: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None) -> str:
        """List tasks with optional filters."""
        # Convert status string to boolean if provided
        status_bool = None
        if status is not None:
            if isinstance(status, str):
                if status.lower() in ['completed', 'true', '1']:
                    status_bool = True
                elif status.lower() in ['pending', 'false', '0']:
                    status_bool = False
                else:
                    raise ValueError("Status must be 'completed', 'pending', 'true', 'false', '1', or '0'")
            else:
                # If status is already a boolean, use it directly
                status_bool = status

        try:
            # Use search if any filters are provided, otherwise use list
            if keyword or status_bool is not None or priority or tags or sort_by:
                tasks = self.todo_service.search_tasks(keyword=keyword, status=status_bool, priority=priority, tags=tags, sort_by=sort_by)
            else:
                tasks = self.todo_service.list_tasks()
        except ValueError as e:
            raise e

        return self.task_formatter.format_task_list(tasks)

    def search_tasks(self, keyword: Optional[str] = None, status: Optional[bool] = None, priority: Optional[str] = None, tags: Optional[list] = None, sort_by: Optional[str] = None) -> str:
        """Search tasks with filters."""
        # For search_tasks, we pass the status directly as a boolean to list_tasks
        return self.list_tasks(keyword=keyword, status=status, priority=priority, tags=tags, sort_by=sort_by)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None, tags: Optional[list] = None, due_date: Optional[str] = None, recurring: Optional[dict] = None, reminder: Optional[str] = None) -> bool:
        """Update an existing task."""
        return self.todo_service.update_task(task_id, title, description, priority, tags, due_date, recurring, reminder)

    def complete_task(self, task_id: int) -> bool:
        """Mark a task as complete."""
        return self.todo_service.complete_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return self.todo_service.delete_task(task_id)

    def restore_task(self, task_id: int) -> bool:
        """Restore a deleted task."""
        return self.todo_service.restore_task(task_id)

    def reminders(self) -> str:
        """List tasks with upcoming reminders."""
        tasks = self.todo_service.check_reminders()
        return self.task_formatter.format_task_list(tasks)

    def run_interactive(self):
        """Run the interactive CLI loop."""
        print("Welcome to the Todo CLI Application!")
        print("Available commands: add, list, update, complete, delete, restore, quit")
        print("Type 'help' for more information on commands.")

        while True:
            try:
                command = input("\ntodo> ").strip().split()

                if not command:
                    continue

                cmd = command[0].lower()

                if cmd == 'quit' or cmd == 'exit':
                    print("Goodbye!")
                    break
                elif cmd == 'help':
                    self._show_help()
                elif cmd == 'add':
                    self._handle_add(command)
                elif cmd == 'list':
                    self._handle_list(command)
                elif cmd == 'search':
                    self._handle_search(command)
                elif cmd == 'update':
                    self._handle_update(command)
                elif cmd == 'complete':
                    self._handle_complete(command)
                elif cmd == 'delete':
                    self._handle_delete(command)
                elif cmd == 'restore':
                    self._handle_restore(command)
                elif cmd == 'reminders':
                    self._handle_reminders(command)
                else:
                    print(f"Unknown command: {cmd}. Type 'help' for available commands.")

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {str(e)}")

    def _show_help(self):
        """Show help information."""
        help_text = """
BASIC COMMANDS:
  add <title> [description] [priority=high|medium|low] [tags=tag1,tag2] - Add a new task
  list [keyword=] [status=] [priority=] [tags=] [sort=] - List tasks with optional filters
  complete <id> [id2] [id3]...  - Mark one or more tasks as complete
  delete <id> [id2] [id3]...    - Delete one or more tasks
  quit/exit                     - Exit the application

INTERMEDIATE COMMANDS:
  search keyword= [status=] [priority=] [tags=] [sort=] - Search tasks by keyword with optional filters
  update <id> [title] [desc] [priority=high|medium|low] [tags=tag1,tag2] - Update a task (at least title or desc required)
  restore <id> [id2] [id3]...   - Restore one or more deleted tasks

ADVANCED COMMANDS:
  reminders                     - List tasks with upcoming reminders
  add [recurring=interval,count] [reminder=YYYY-MM-DDTHH:MM] - Add a recurring task with reminder
  update [recurring=interval,count] [reminder=YYYY-MM-DDTHH:MM] - Update a task with recurring and reminder settings

FILTER OPTIONS:
  keyword= - Search in title and description
  status=  - Filter by status (completed, pending, true, false, 1, 0)
  priority= - Filter by priority (high, medium, low)
  tags=    - Filter by tags (comma-separated list)
  sort=    - Sort by (priority, due_date, title, created_at, status)

ADVANCED OPTIONS:
  recurring= - Set recurring interval and count (e.g., daily,7 for daily recurring 7 times)
  reminder= - Set reminder datetime (e.g., 2023-12-31T14:30)
  interval - daily, weekly, monthly
  count - number of times to repeat (optional, defaults to 1)

For more information on any command, type the command without arguments.
        """
        print(help_text.strip())

    def _handle_add(self, command):
        """Handle the add command."""
        if len(command) < 2:
            print("Usage: add <title> [description] [priority=high|medium|low] [tags=tag1,tag2] [due_date=YYYY-MM-DD] [recurring=interval,count] [reminder=YYYY-MM-DDTHH:MM]")
            print("Examples:")
            print("  add 'Buy groceries' priority=high tags=shopping,food")
            print("  add 'Water plants' recurring=daily,7 reminder=2023-12-31T08:00")
            return

        title = command[1]
        description = None
        priority = "medium"
        tags = None
        due_date = None
        recurring = None
        reminder = None

        # Process remaining arguments to extract description, priority, tags, due_date, recurring, and reminder
        remaining_args = command[2:]
        desc_parts = []

        for arg in remaining_args:
            if arg.startswith("priority="):
                priority = arg.split("=", 1)[1]
                if priority not in ["high", "medium", "low"]:
                    print(f"Error: Invalid priority '{priority}'. Valid options: high, medium, low")
                    print("Example: add 'My task' priority=high")
                    return
            elif arg.startswith("tags="):
                tags_str = arg.split("=", 1)[1]
                # Validate tags format
                tags = [tag.strip() for tag in tags_str.split(",")]
                # Check for empty tags
                if any(tag == "" for tag in tags):
                    print("Error: Empty tag found. Tags cannot be empty strings.")
                    print("Example: add 'My task' tags=work,important")
                    return
            elif arg.startswith("due_date="):
                due_date = arg.split("=", 1)[1]
                # Validate date format
                try:
                    from datetime import datetime
                    datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                except ValueError:
                    print(f"Error: Invalid date format '{due_date}'. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format.")
                    print("Example: add 'My task' due_date=2023-12-31 or due_date=2023-12-31T14:30")
                    return
            elif arg.startswith("recurring="):
                recurring_str = arg.split("=", 1)[1]
                recurring_parts = recurring_str.split(",")
                if len(recurring_parts) >= 1:
                    interval = recurring_parts[0]
                    if interval not in ['daily', 'weekly', 'monthly']:
                        print(f"Error: Invalid recurring interval '{interval}'. Valid options: daily, weekly, monthly")
                        print("Example: add 'My task' recurring=daily,7")
                        return
                    recurring = {'interval': interval}
                    if len(recurring_parts) >= 2:
                        try:
                            count = int(recurring_parts[1])
                            if count <= 0:
                                print(f"Error: Recurring count must be a positive number, got {count}")
                                print("Example: add 'My task' recurring=daily,5")
                                return
                            recurring['count'] = count
                        except ValueError:
                            print(f"Error: Invalid recurring count '{recurring_parts[1]}'. Must be a number.")
                            print("Example: add 'My task' recurring=daily,5")
                            return
            elif arg.startswith("reminder="):
                reminder = arg.split("=", 1)[1]
                # Validate reminder format
                try:
                    from datetime import datetime
                    datetime.fromisoformat(reminder.replace("Z", "+00:00"))
                except ValueError:
                    print(f"Error: Invalid reminder format '{reminder}'. Use YYYY-MM-DDTHH:MM format.")
                    print("Example: add 'My task' reminder=2023-12-31T14:30")
                    return
            else:
                desc_parts.append(arg)

        # Join non-flag arguments as description
        if desc_parts:
            description = " ".join(desc_parts)

        try:
            result = self.add_task(title, description, priority, tags, due_date, recurring, reminder)
            print(result)
        except Exception as e:
            print(f"Error adding task: {str(e)}")

    def _handle_update(self, command):
        """Handle the update command."""
        if len(command) < 2:
            print("Usage: update <id> [title] [description] [priority=high|medium|low] [tags=tag1,tag2] [due_date=YYYY-MM-DD] [recurring=interval,count] [reminder=YYYY-MM-DDTHH:MM]")
            print("Examples:")
            print("  update 1 'New title' priority=high tags=work,urgent")
            print("  update 1 recurring=daily,7 reminder=2023-12-31T09:00")
            return

        try:
            task_id = int(command[1])
            title = None
            description = None
            priority = None
            tags = None
            due_date = None
            recurring = None
            reminder = None

            # Process remaining arguments to extract title, description, priority, tags, due_date, recurring, and reminder
            remaining_args = command[2:]
            desc_parts = []

            for arg in remaining_args:
                if arg.startswith("priority="):
                    priority = arg.split("=", 1)[1]
                    if priority not in ["high", "medium", "low"]:
                        print(f"Error: Invalid priority '{priority}'. Valid options: high, medium, low")
                        print("Example: update 1 priority=high")
                        return
                elif arg.startswith("tags="):
                    tags_str = arg.split("=", 1)[1]
                    # Validate tags format
                    tags = [tag.strip() for tag in tags_str.split(",")]
                    # Check for empty tags
                    if any(tag == "" for tag in tags):
                        print("Error: Empty tag found. Tags cannot be empty strings.")
                        print("Example: update 1 tags=work,important")
                        return
                elif arg.startswith("due_date="):
                    due_date = arg.split("=", 1)[1]
                    # Validate date format
                    try:
                        from datetime import datetime
                        datetime.fromisoformat(due_date.replace("Z", "+00:00"))
                    except ValueError:
                        print(f"Error: Invalid date format '{due_date}'. Use YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS format.")
                        print("Example: update 1 due_date=2023-12-31 or due_date=2023-12-31T14:30")
                        return
                elif arg.startswith("recurring="):
                    recurring_str = arg.split("=", 1)[1]
                    recurring_parts = recurring_str.split(",")
                    if len(recurring_parts) >= 1:
                        interval = recurring_parts[0]
                        if interval not in ['daily', 'weekly', 'monthly']:
                            print(f"Error: Invalid recurring interval '{interval}'. Valid options: daily, weekly, monthly")
                            print("Example: update 1 recurring=daily,7")
                            return
                        recurring = {'interval': interval}
                        if len(recurring_parts) >= 2:
                            try:
                                count = int(recurring_parts[1])
                                if count <= 0:
                                    print(f"Error: Recurring count must be a positive number, got {count}")
                                    print("Example: update 1 recurring=daily,5")
                                    return
                                recurring['count'] = count
                            except ValueError:
                                print(f"Error: Invalid recurring count '{recurring_parts[1]}'. Must be a number.")
                                print("Example: update 1 recurring=daily,5")
                                return
                elif arg.startswith("reminder="):
                    reminder = arg.split("=", 1)[1]
                    # Validate reminder format
                    try:
                        from datetime import datetime
                        datetime.fromisoformat(reminder.replace("Z", "+00:00"))
                    except ValueError:
                        print(f"Error: Invalid reminder format '{reminder}'. Use YYYY-MM-DDTHH:MM format.")
                        print("Example: update 1 reminder=2023-12-31T14:30")
                        return
                else:
                    desc_parts.append(arg)

            # Join non-flag arguments as title and description
            if desc_parts:
                if len(desc_parts) == 1:
                    title = desc_parts[0]
                else:
                    title = desc_parts[0]
                    description = " ".join(desc_parts[1:])

            result = self.update_task(task_id, title, description, priority, tags, due_date, recurring, reminder)
            if result:
                print(f"Task {task_id} updated successfully")
            else:
                print(f"Task {task_id} not found")
        except ValueError:
            print("Error: Task ID must be a number")
            print("Example: update 1 'New title' priority=high")
        except Exception as e:
            print(f"Error updating task: {str(e)}")

    def _handle_complete(self, command):
        """Handle the complete command."""
        if len(command) < 2:
            print("Usage: complete <id> [id2] [id3] ...")
            return

        # Process multiple task IDs
        task_ids = command[1:]  # Get all arguments after the command name
        for task_id_str in task_ids:
            try:
                task_id = int(task_id_str)
                result = self.complete_task(task_id)
                if result:
                    print(f"Task {task_id} marked as complete")
                else:
                    print(f"Task {task_id} not found")
            except ValueError:
                print(f"Task ID '{task_id_str}' must be a number")
            except Exception as e:
                print(f"Error completing task {task_id_str}: {str(e)}")

    def _handle_delete(self, command):
        """Handle the delete command."""
        if len(command) < 2:
            print("Usage: delete <id> [id2] [id3] ...")
            return

        # Process multiple task IDs
        task_ids = command[1:]  # Get all arguments after the command name
        for task_id_str in task_ids:
            try:
                task_id = int(task_id_str)
                result = self.delete_task(task_id)
                if result:
                    print(f"Task {task_id} deleted successfully")
                else:
                    print(f"Task {task_id} not found")
            except ValueError:
                print(f"Task ID '{task_id_str}' must be a number")
            except Exception as e:
                print(f"Error deleting task {task_id_str}: {str(e)}")

    def _handle_list(self, command):
        """Handle the list command with optional filters."""
        # Process arguments to extract filters
        keyword = None
        status = None
        priority = None
        tags = None
        sort_by = None

        # Process remaining arguments to extract filters
        remaining_args = command[1:]  # Skip the command name

        for arg in remaining_args:
            if arg.startswith("keyword="):
                keyword = arg.split("=", 1)[1]
            elif arg.startswith("status="):
                status = arg.split("=", 1)[1]
                # Validate status value
                if status.lower() not in ['completed', 'pending', 'true', 'false', '1', '0']:
                    print(f"Error: Invalid status '{status}'. Valid options: completed, pending, true, false, 1, 0")
                    print("Example: list status=completed")
                    return
            elif arg.startswith("priority="):
                priority = arg.split("=", 1)[1]
                # Validate priority value
                if priority not in ['high', 'medium', 'low']:
                    print(f"Error: Invalid priority '{priority}'. Valid options: high, medium, low")
                    print("Example: list priority=high")
                    return
            elif arg.startswith("tags="):
                tags_str = arg.split("=", 1)[1]
                tags = [tag.strip() for tag in tags_str.split(",")]
                # Check for empty tags
                if any(tag == "" for tag in tags):
                    print("Error: Empty tag found. Tags cannot be empty strings.")
                    print("Example: list tags=work,important")
                    return
            elif arg.startswith("sort="):
                sort_by = arg.split("=", 1)[1]
                # Validate sort options
                valid_sort_options = ['priority', 'due_date', 'title', 'created_at', 'status']
                if sort_by not in valid_sort_options:
                    print(f"Error: Invalid sort option '{sort_by}'. Valid options: {', '.join(valid_sort_options)}")
                    print("Example: list sort=priority")
                    return
            else:
                print(f"Error: Unknown filter: {arg}. Use keyword=, status=, priority=, tags=, or sort=")
                print("Example: list status=pending priority=high")
                return

        try:
            result = self.list_tasks(keyword=keyword, status=status, priority=priority, tags=tags, sort_by=sort_by)
            print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")

    def _handle_search(self, command):
        """Handle the search command."""
        # Process arguments to extract search parameters
        keyword = None
        status = None
        priority = None
        tags = None
        sort_by = None

        # Process remaining arguments to extract filters
        remaining_args = command[1:]  # Skip the command name

        for arg in remaining_args:
            if arg.startswith("keyword="):
                keyword = arg.split("=", 1)[1]
            elif arg.startswith("status="):
                status = arg.split("=", 1)[1]
                # Validate status value
                if status.lower() not in ['completed', 'pending', 'true', 'false', '1', '0']:
                    print(f"Error: Invalid status '{status}'. Valid options: completed, pending, true, false, 1, 0")
                    print("Example: search keyword=meeting status=completed")
                    return
            elif arg.startswith("priority="):
                priority = arg.split("=", 1)[1]
                # Validate priority value
                if priority not in ['high', 'medium', 'low']:
                    print(f"Error: Invalid priority '{priority}'. Valid options: high, medium, low")
                    print("Example: search keyword=meeting priority=high")
                    return
            elif arg.startswith("tags="):
                tags_str = arg.split("=", 1)[1]
                tags = [tag.strip() for tag in tags_str.split(",")]
                # Check for empty tags
                if any(tag == "" for tag in tags):
                    print("Error: Empty tag found. Tags cannot be empty strings.")
                    print("Example: search keyword=meeting tags=work,important")
                    return
            elif arg.startswith("sort="):
                sort_by = arg.split("=", 1)[1]
                # Validate sort options
                valid_sort_options = ['priority', 'due_date', 'title', 'created_at', 'status']
                if sort_by not in valid_sort_options:
                    print(f"Error: Invalid sort option '{sort_by}'. Valid options: {', '.join(valid_sort_options)}")
                    print("Example: search keyword=meeting sort=priority")
                    return
            else:
                print(f"Error: Unknown parameter: {arg}. Use keyword=, status=, priority=, tags=, or sort=")
                print("Example: search keyword=meeting status=pending priority=high")
                return

        try:
            result = self.search_tasks(keyword=keyword, status=status, priority=priority, tags=tags, sort_by=sort_by)
            print(result)
        except ValueError as e:
            print(f"Error: {str(e)}")
        except Exception as e:
            print(f"Error searching tasks: {str(e)}")

    def _handle_restore(self, command):
        """Handle the restore command."""
        if len(command) < 2:
            print("Usage: restore <id> [id2] [id3] ...")
            return

        # Process multiple task IDs
        task_ids = command[1:]  # Get all arguments after the command name
        for task_id_str in task_ids:
            try:
                task_id = int(task_id_str)
                result = self.restore_task(task_id)
                if result:
                    print(f"Task {task_id} restored successfully")
                else:
                    print(f"Task {task_id} not found or not deleted")
            except ValueError:
                print(f"Task ID '{task_id_str}' must be a number")
            except Exception as e:
                print(f"Error restoring task {task_id_str}: {str(e)}")

    def _handle_reminders(self, command):
        """Handle the reminders command."""
        try:
            result = self.reminders()
            print(result)
        except Exception as e:
            print(f"Error getting reminders: {str(e)}")