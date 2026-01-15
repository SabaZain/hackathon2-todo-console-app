# Todo Domain Skill

This skill represents the core Todo domain knowledge. It defines the fundamental concepts and behaviors of the Todo application domain.

## Core Domain Concepts

### Task Definition
A Task is the fundamental unit of work in the Todo system. It represents a unit of work that a user intends to complete.

**Task Properties:**
- **ID**: Unique identifier for the task
- **Title**: Brief description of what needs to be done
- **Description**: Optional detailed explanation of the task
- **Created Date**: Timestamp when the task was created
- **Updated Date**: Timestamp when the task was last modified
- **Due Date**: Optional deadline for task completion
- **Priority**: Optional priority level (low, medium, high)
- **Status**: Current state of the task (pending, completed, archived)
- **Owner**: User who owns the task

### Task Lifecycle

The Task lifecycle encompasses the standard operations that can be performed on tasks:

1. **Create**: Initialize a new task with required properties
   - Assign unique ID
   - Set initial status to "pending"
   - Set creation timestamp
   - Associate with owner

2. **View**: Retrieve and display task information
   - Single task retrieval by ID
   - List multiple tasks with filtering options
   - Display all task properties

3. **Update**: Modify existing task properties
   - Change title, description, due date, priority
   - Update status (mark as completed, etc.)
   - Modify other properties as needed

4. **Delete**: Remove a task from the system
   - Permanent removal or soft delete to archive
   - Maintain data integrity

### Completion State

Tasks have distinct states that represent their completion status:

- **Pending**: Task has been created but not yet completed
- **Completed**: Task has been marked as finished
- **Archived**: Task is no longer active (completed or obsolete)

### User Ownership

- Each task is associated with a specific user who owns it
- Users can only view and modify their own tasks
- Ownership determines access permissions
- Users can share tasks (optional feature)

## Domain Rules

1. **Uniqueness**: Each task must have a unique identifier within the system
2. **Immutability**: Task ID cannot be changed after creation
3. **Ownership**: Only the task owner can modify or delete a task
4. **Status Transitions**: Tasks can transition from pending to completed, and completed to archived
5. **Completeness**: A task must have at least a title to be valid

## Reusability

This skill is designed to be reusable across multiple contexts:
- CLI app: Core logic for command-line task management
- Web frontend: Business logic for UI interactions
- Backend API: Domain validation and processing
- AI chatbot interactions: Understanding and processing task requests

## Implementation Constraints

This skill remains implementation-agnostic and free of:
- UI details or presentation logic
- Backend technology specifics
- Database schema details
- API endpoint definitions
- Framework-specific code
- Platform-specific implementations