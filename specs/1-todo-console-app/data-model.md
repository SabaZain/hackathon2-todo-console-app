# Data Model: Phase I Todo In-Memory Python Console App

## Task Entity

### Attributes
- **id** (int): Unique identifier for the task
  - Auto-generated positive integer
  - Required, immutable after creation
- **title** (str): Task title/description
  - Required string (non-empty, no whitespace-only)
  - Minimum length: 1 character after trimming
- **description** (str): Optional additional details
  - Optional string, can be empty or None
  - Maximum length: 1000 characters (reasonable limit)
- **status** (bool): Completion status
  - True = Completed
  - False = Pending
  - Default: False (pending)
- **created_at** (datetime): Timestamp of task creation
  - Auto-generated when task is created
  - Format: ISO 8601 datetime string
  - Immutable after creation

### Validation Rules
- Title must not be empty or contain only whitespace
- ID must be a positive integer
- Status must be boolean
- Description length must not exceed 1000 characters

### State Transitions
- Initial state: status = False (pending)
- Toggle operation: status = !status (pending ↔ completed)

### Relationships
- None (standalone entity)

## Task Repository Interface

### Methods
- **create(task: Task) -> int**: Creates a new task and returns its ID
- **get_by_id(task_id: int) -> Task**: Retrieves a task by its ID, raises exception if not found
- **get_all() -> List[Task]**: Retrieves all tasks
- **update(task_id: int, title: str = None, description: str = None) -> bool**: Updates task details, returns True if successful
- **delete(task_id: int) -> bool**: Deletes a task by ID, returns True if successful
- **exists(task_id: int) -> bool**: Checks if a task exists by ID

## Use Cases

### AddTaskUseCase
- **Input**: title (str), description (str, optional)
- **Output**: task_id (int) or error
- **Validation**: Title must not be empty or whitespace-only
- **Success Path**: Creates new task with pending status and returns ID
- **Failure Path**: Raises exception if validation fails

### DeleteTaskUseCase
- **Input**: task_id (int)
- **Output**: success (bool) or error
- **Validation**: Task with ID must exist
- **Success Path**: Removes task from repository
- **Failure Path**: Raises exception if task doesn't exist

### UpdateTaskUseCase
- **Input**: task_id (int), title (str, optional), description (str, optional)
- **Output**: success (bool) or error
- **Validation**: Task with ID must exist; if title provided, must not be empty or whitespace-only
- **Success Path**: Updates specified fields of existing task
- **Failure Path**: Raises exception if task doesn't exist or validation fails

### ListTasksUseCase
- **Input**: None
- **Output**: List of all tasks
- **Validation**: None
- **Success Path**: Returns all tasks in repository
- **Failure Path**: None (read-only operation)

### ToggleTaskStatusUseCase
- **Input**: task_id (int)
- **Output**: success (bool) or error
- **Validation**: Task with ID must exist
- **Success Path**: Toggles the status of the task (pending ↔ completed)
- **Failure Path**: Raises exception if task doesn't exist