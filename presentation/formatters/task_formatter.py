from typing import List
from domain.entities.task import Task


class TaskFormatter:
    """Formatter for displaying tasks in CLI."""

    def format_task(self, task: Task) -> str:
        """Format a single task for display."""
        status_indicator = "[x]" if task.status else "[ ]"
        description = f" - {task.description}" if task.description else ""
        priority_indicator = f" [{task.priority}]"
        tags_indicator = f" #{' #'.join(task.tags)}" if task.tags else ""
        due_date_indicator = f" (due: {task.due_date.strftime('%Y-%m-%d')})" if task.due_date else ""

        # Add recurring information if present
        recurring_indicator = ""
        if task.recurring:
            interval = task.recurring.get('interval', 'unknown')
            count = task.recurring.get('count', 'unknown')
            if count is not None:
                recurring_indicator = f" (recurring: {interval}, {count} left)"
            else:
                recurring_indicator = f" (recurring: {interval})"

        # Add reminder information if present
        reminder_indicator = ""
        if task.reminder:
            reminder_indicator = f" (reminder: {task.reminder.strftime('%Y-%m-%d %H:%M')})"

        return f"{task.id} {status_indicator} {task.title}{description}{priority_indicator}{tags_indicator}{due_date_indicator}{recurring_indicator}{reminder_indicator}"

    def format_task_list(self, tasks: List[Task]) -> str:
        """Format a list of tasks for display."""
        if not tasks:
            return "No tasks found."

        formatted_tasks = []
        for task in tasks:
            formatted_tasks.append(self.format_task(task))

        return "\n".join(formatted_tasks)