# ADR-1: Recurring Tasks and Reminder Architecture

## Status
Accepted

## Date
2025-12-31

## Context
The Todo Console App needs to support recurring tasks that repeat on a schedule (daily, weekly, monthly) and time-based reminders for tasks. This requires extending the existing domain model, repository layer, service layer, and CLI interface while maintaining backward compatibility and following clean architecture principles.

## Decision
We will implement recurring tasks and reminders using the following approach:

### Data Model
- Extend the Task entity with two optional fields:
  - `recurring: Optional[Dict[str, Any]]` - Contains interval ('daily', 'weekly', 'monthly'), count (number of occurrences), and next_due_date
  - `reminder: Optional[datetime]` - Time for notification

### Scheduling Mechanism
- Implement `schedule_next_occurrence` method in TodoService that creates new task instances when a recurring task is completed
- Use count-based limit system where each occurrence decrements the count
- Remove recurring configuration from original task when count reaches 0

### Reminder System
- Implement `check_reminders` method that returns tasks with reminder times before current time
- Support searching and sorting by reminder time in repositories

### Repository Support
- Update both InMemoryTaskRepository and FileTaskRepository to persist new fields
- Use sentinel values (...) to distinguish between not-provided and None parameters in update operations
- Add search functionality for filtering by reminder time

## Alternatives Considered

### Alternative 1: Separate RecurringTask Entity
Instead of extending Task, create a separate RecurringTask entity that inherits from Task or uses composition.

**Pros:** Better separation of concerns, cleaner domain model
**Cons:** More complex inheritance/composition hierarchy, requires separate repository and service methods

### Alternative 2: Cron-based Scheduling
Use external scheduling system or cron jobs to handle recurring tasks.

**Pros:** More robust scheduling, system handles timing automatically
**Cons:** Adds external dependencies, more complex deployment, doesn't fit CLI-only architecture

### Alternative 3: Event-driven Architecture
Use event system to trigger recurring task creation.

**Pros:** More flexible, decoupled architecture
**Cons:** Adds complexity to simple CLI app, over-engineering for current requirements

## Consequences

### Positive
- Maintains backward compatibility with existing tasks
- Simple implementation that follows existing patterns
- Clean extension of domain model without breaking changes
- Supports both in-memory and file-based persistence

### Negative
- Task entity becomes more complex with additional optional fields
- Scheduling only happens when tasks are completed (not time-based)
- Reminder checking requires manual invocation

## References
- plan.md: Clean Architecture implementation
- data-model.md: Task entity design
- spec.md: Requirements for recurring tasks and reminders