---
description: "Task list for Phase I Todo In-Memory Python Console App"
---

# Tasks: Phase I – Todo In-Memory Python Console App

**Input**: Design documents from `/specs/1-todo-console-app/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: Test-Driven Development (TDD) is required per the constitution - all tests will be written before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Project Structure**: Following the plan.md structure with domain, application, infrastructure, and presentation layers
- **Test Structure**: tests/ with subdirectories for each layer

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure per plan.md
- [ ] T002 Initialize Python project with requirements.txt including pytest
- [ ] T003 [P] Configure linting and formatting tools (flake8, black)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 [P] Create Task entity with validation in domain/entities/task.py
- [x] T005 [P] Create TaskRepository interface in domain/repositories/task_repository.py
- [x] T006 [P] Create ID generator service in application/services/id_generator.py
- [x] T007 Create base exceptions for domain errors in domain/exceptions.py
- [x] T008 Create TaskFormatter for display in presentation/formatters/task_formatter.py
- [x] T009 Configure pytest structure with conftest.py in tests/conftest.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add Task (Priority: P1) 🎯 MVP

**Goal**: Users can add tasks with title and optional description, with proper validation and error handling.

**Independent Test**: Verify that users can add tasks with title only, with title and description, and that attempts to add tasks with empty titles fail appropriately.

### Tests for User Story 1 (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Write tests for Task entity validation in tests/domain/test_task.py
- [ ] T011 [P] [US1] Write tests for AddTaskUseCase in tests/application/test_use_cases.py
- [ ] T012 [P] [US1] Write tests for in-memory repository create operation in tests/infrastructure/test_repositories.py

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create AddTaskUseCase in application/use_cases/add_task.py
- [ ] T014 [US1] Implement in-memory task repository in infrastructure/repositories/in_memory_task_repository.py
- [ ] T015 [US1] Implement AddTask command handler in presentation/cli/command_handlers.py
- [ ] T016 [US1] Add 'add' command to command parser in presentation/cli/command_parser.py
- [ ] T017 [US1] Add error handling for empty titles in domain/exceptions.py

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - List Tasks (Priority: P2)

**Goal**: Users can view all tasks with clear status indicators showing ID, status, title, and description.

**Independent Test**: Verify that users can see an empty list when no tasks exist, and can see properly formatted lists with all tasks showing their status indicators.

### Tests for User Story 2 (TDD approach) ⚠️

- [ ] T018 [P] [US2] Write tests for ListTasksUseCase in tests/application/test_use_cases.py
- [ ] T019 [P] [US2] Write tests for TaskFormatter in tests/presentation/test_cli.py

### Implementation for User Story 2

- [ ] T020 [P] [US2] Create ListTasksUseCase in application/use_cases/list_tasks.py
- [ ] T021 [US2] Implement ListTasks command handler in presentation/cli/command_handlers.py
- [ ] T022 [US2] Add 'list' command to command parser in presentation/cli/command_parser.py
- [ ] T023 [US2] Implement proper display formatting in presentation/formatters/task_formatter.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Delete Task (Priority: P3)

**Goal**: Users can remove a task by its unique ID with proper validation and error handling.

**Independent Test**: Verify that users can delete existing tasks and that attempts to delete non-existent tasks fail appropriately.

### Tests for User Story 3 (TDD approach) ⚠️

- [ ] T024 [P] [US3] Write tests for DeleteTaskUseCase in tests/application/test_use_cases.py
- [ ] T025 [P] [US3] Write tests for repository delete operation in tests/infrastructure/test_repositories.py

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create DeleteTaskUseCase in application/use_cases/delete_task.py
- [ ] T027 [US3] Implement DeleteTask command handler in presentation/cli/command_handlers.py
- [ ] T028 [US3] Add 'delete' command to command parser in presentation/cli/command_parser.py
- [ ] T029 [US3] Add error handling for non-existent tasks in domain/exceptions.py

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Update Task (Priority: P4)

**Goal**: Users can modify the title and/or description of an existing task with proper validation.

**Independent Test**: Verify that users can update task titles, descriptions, or both, and that attempts to update non-existent tasks or provide empty titles fail appropriately.

### Tests for User Story 4 (TDD approach) ⚠️

- [ ] T030 [P] [US4] Write tests for UpdateTaskUseCase in tests/application/test_use_cases.py
- [ ] T031 [P] [US4] Write tests for repository update operation in tests/infrastructure/test_repositories.py

### Implementation for User Story 4

- [ ] T032 [P] [US4] Create UpdateTaskUseCase in application/use_cases/update_task.py
- [ ] T033 [US4] Implement UpdateTask command handler in presentation/cli/command_handlers.py
- [ ] T034 [US4] Add 'update' command to command parser in presentation/cli/command_parser.py
- [ ] T035 [US4] Add validation for update operations in domain/exceptions.py

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Mark Task Complete/Incomplete (Priority: P5)

**Goal**: Users can toggle task state between pending and completed with proper validation.

**Independent Test**: Verify that users can mark pending tasks as complete, completed tasks as pending, and that attempts to toggle non-existent tasks fail appropriately.

### Tests for User Story 5 (TDD approach) ⚠️

- [ ] T036 [P] [US5] Write tests for ToggleTaskStatusUseCase in tests/application/test_use_cases.py
- [ ] T037 [P] [US5] Write tests for repository toggle operation in tests/infrastructure/test_repositories.py

### Implementation for User Story 5

- [ ] T038 [P] [US5] Create ToggleTaskStatusUseCase in application/use_cases/toggle_task_status.py
- [ ] T039 [US5] Implement ToggleTaskStatus command handler in presentation/cli/command_handlers.py
- [ ] T040 [US5] Add 'complete' and 'incomplete' commands to command parser in presentation/cli/command_parser.py
- [ ] T041 [US5] Add validation for toggle operations in domain/exceptions.py

**Checkpoint**: All user stories should now be independently functional

---

## Phase 8: CLI Interface Integration

**Goal**: Complete the command-line interface with help, quit, and error handling.

### Tests for CLI Interface

- [ ] T042 [P] Write integration tests for CLI commands in tests/presentation/test_cli.py
- [ ] T043 Write tests for main application flow in tests/presentation/test_cli_app.py

### Implementation for CLI Interface

- [ ] T044 Create main CLI application in presentation/cli/cli_app.py
- [ ] T045 Add 'help' command to command parser in presentation/cli/command_parser.py
- [ ] T046 Add 'quit' and 'exit' commands to command parser in presentation/cli/command_parser.py
- [ ] T047 Implement comprehensive error handling in presentation/cli/command_handlers.py
- [ ] T048 Create main.py entry point with proper CLI initialization

**Checkpoint**: Complete CLI application with all 5 core features available

---

## Phase 9: Feature Enhancement - Search, Filter, Sort Tasks

**Goal**: Enable users to search, filter, and sort tasks by various criteria (keyword, status, priority, tags, due date)

### Tests for Search/Filter/Sort Feature (TDD approach) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T049 [P] Write tests for Task entity with due_date field in tests/domain/test_task.py
- [x] T050 [P] Write tests for search/filter/sort methods in repository in tests/infrastructure/test_repositories.py
- [x] T051 [P] Write tests for search_tasks service method in tests/application/test_use_cases.py
- [x] T052 [P] Write tests for CLI search command in tests/presentation/test_cli.py

### Implementation for Search/Filter/Sort Feature

- [x] T053 Update Task entity to include optional due_date field in domain/entities/task.py
- [x] T054 Implement search/filter/sort logic in InMemoryTaskRepository in infrastructure/repositories/in_memory_task_repository.py
- [x] T055 Implement search/filter/sort logic in FileTaskRepository in infrastructure/repositories/file_task_repository.py
- [x] T056 Add search_tasks method to TodoService in application/services/todo_service.py
- [x] T057 Add search command to CLI in presentation/cli/cli_app.py
- [x] T058 Update list command to accept filter and sort parameters in presentation/cli/cli_app.py
- [x] T059 Update TaskFormatter to handle sorting display in presentation/formatters/task_formatter.py

**Checkpoint**: At this point, users should be able to search, filter, and sort tasks by keyword, status, priority, tags, and due date

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T060 [P] Add comprehensive docstrings to all modules and functions
- [ ] T061 [P] Add integration tests for complete user workflows in tests/integration/
- [ ] T062 Add performance validation for multiple tasks
- [ ] T063 [P] Add additional unit tests for edge cases in all layers
- [ ] T064 Run complete test suite and validate all functionality
- [ ] T065 Update README with usage instructions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **CLI Integration (Phase 8)**: Depends on all core feature user stories being complete
- **Polish (Phase 9)**: Depends on all desired user stories and CLI integration being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - No dependencies on other stories

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write tests for Task entity validation in tests/domain/test_task.py"
Task: "Write tests for AddTaskUseCase in tests/application/test_use_cases.py"
Task: "Write tests for in-memory repository create operation in tests/infrastructure/test_repositories.py"

# Launch all implementation tasks for User Story 1 together:
Task: "Create AddTaskUseCase in application/use_cases/add_task.py"
Task: "Implement in-memory task repository in infrastructure/repositories/in_memory_task_repository.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Add Task)
4. **STOP and VALIDATE**: Test Add Task functionality independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Complete CLI Integration → All features available
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
   - Developer E: User Story 5
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence