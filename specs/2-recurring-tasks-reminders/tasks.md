---
description: "Task list for Phase II - Recurring Tasks & Time Reminders"
---

# Tasks: Phase II – Recurring Tasks & Time Reminders

**Input**: Design documents from `/specs/2-recurring-tasks-reminders/`
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

## Phase 1: Domain Layer Updates (Blocking Prerequisites)

**Purpose**: Update core Task entity and related domain components to support recurring tasks and reminders

**⚠️ CRITICAL**: No other work can begin until this phase is complete

- [ ] T101 [P] Update Task entity with recurring field in domain/entities/task.py
- [ ] T102 [P] Update Task entity with reminder field in domain/entities/task.py
- [ ] T103 [P] Add validation for recurring intervals in domain/entities/task.py
- [ ] T104 [P] Add validation for reminder datetime in domain/entities/task.py
- [ ] T105 Update Task __str__ and __repr__ methods to include new fields

**Checkpoint**: Domain layer ready with recurring and reminder support

---

## Phase 2: Repository Layer Updates

**Purpose**: Update repository implementations to persist recurring and reminder data

### Tests for Repository Updates (TDD approach) ⚠️

- [ ] T106 [P] Write tests for InMemoryTaskRepository with recurring data in tests/infrastructure/test_repositories.py
- [ ] T107 [P] Write tests for FileTaskRepository with recurring data in tests/infrastructure/test_repositories.py
- [ ] T108 [P] Write tests for InMemoryTaskRepository with reminder data in tests/infrastructure/test_repositories.py
- [ ] T109 [P] Write tests for FileTaskRepository with reminder data in tests/infrastructure/test_repositories.py

### Implementation for Repository Updates

- [ ] T110 Update InMemoryTaskRepository to store recurring field in infrastructure/repositories/in_memory_task_repository.py
- [ ] T111 Update InMemoryTaskRepository to store reminder field in infrastructure/repositories/in_memory_task_repository.py
- [ ] T112 Update FileTaskRepository to store recurring field in infrastructure/repositories/file_task_repository.py
- [ ] T113 Update FileTaskRepository to store reminder field in infrastructure/repositories/file_task_repository.py
- [ ] T114 Update FileTaskRepository JSON serialization to include new fields
- [ ] T115 Update FileTaskRepository JSON deserialization to handle new fields

**Checkpoint**: Both repository implementations support recurring and reminder data

---

## Phase 3: Service Layer Updates

**Purpose**: Update TodoService with recurring task scheduling and reminder checking functionality

### Tests for Service Updates (TDD approach) ⚠️

- [ ] T116 [P] Write tests for schedule_next_occurrence in tests/application/test_services.py
- [ ] T117 [P] Write tests for check_reminders in tests/application/test_services.py
- [ ] T118 [P] Write tests for add_task with recurring parameter in tests/application/test_services.py
- [ ] T119 [P] Write tests for add_task with reminder parameter in tests/application/test_services.py
- [ ] T120 [P] Write tests for update_task with recurring parameter in tests/application/test_services.py
- [ ] T121 [P] Write tests for update_task with reminder parameter in tests/application/test_services.py

### Implementation for Service Updates

- [ ] T122 Add schedule_next_occurrence method to TodoService in application/services/todo_service.py
- [ ] T123 Add check_reminders method to TodoService in application/services/todo_service.py
- [ ] T124 Update add_task method to accept recurring parameter in application/services/todo_service.py
- [ ] T125 Update add_task method to accept reminder parameter in application/services/todo_service.py
- [ ] T126 Update update_task method to accept recurring parameter in application/services/todo_service.py
- [ ] T127 Update update_task method to accept reminder parameter in application/services/todo_service.py
- [ ] T128 Add validation for recurring intervals in TodoService
- [ ] T129 Add validation for reminder datetime in TodoService

**Checkpoint**: Service layer supports recurring tasks and reminders

---

## Phase 4: CLI Layer Updates

**Purpose**: Update CLI to support recurring tasks and reminder functionality

### Tests for CLI Updates (TDD approach) ⚠️

- [ ] T130 [P] Write tests for CLI add command with recurring parameter in tests/presentation/test_cli.py
- [ ] T131 [P] Write tests for CLI add command with reminder parameter in tests/presentation/test_cli.py
- [ ] T132 [P] Write tests for CLI update command with recurring parameter in tests/presentation/test_cli.py
- [ ] T133 [P] Write tests for CLI update command with reminder parameter in tests/presentation/test_cli.py
- [ ] T134 [P] Write tests for new reminders command in tests/presentation/test_cli.py

### Implementation for CLI Updates

- [ ] T135 Update CLI add command to accept recurring parameter in presentation/cli/cli_app.py
- [ ] T136 Update CLI add command to accept reminder parameter in presentation/cli/cli_app.py
- [ ] T137 Update CLI update command to accept recurring parameter in presentation/cli/cli_app.py
- [ ] T138 Update CLI update command to accept reminder parameter in presentation/cli/cli_app.py
- [ ] T139 Add new reminders command to list upcoming reminders in presentation/cli/cli_app.py
- [ ] T140 Update task display formatting to show recurring and reminder info in presentation/formatters/task_formatter.py
- [ ] T141 Update help documentation to include new recurring and reminder features

**Checkpoint**: CLI supports recurring tasks and reminders

---

## Phase 5: Integration & Testing

**Purpose**: Complete integration and ensure all components work together

- [ ] T142 Run all existing tests to ensure backward compatibility
- [ ] T143 Write integration tests for recurring task workflow
- [ ] T144 Write integration tests for reminder checking workflow
- [ ] T145 Test automatic scheduling of next occurrence after completion
- [ ] T146 Test reminder functionality with various datetime formats
- [ ] T147 Verify JSON persistence works correctly with new fields

**Checkpoint**: Complete integration with all functionality working

---

## Dependencies & Execution Order

### Phase Dependencies

- **Domain Updates (Phase 1)**: No dependencies - can start immediately
- **Repository Updates (Phase 2)**: Depends on Domain Updates completion
- **Service Updates (Phase 3)**: Depends on Repository Updates completion
- **CLI Updates (Phase 4)**: Depends on Service Updates completion
- **Integration (Phase 5)**: Depends on all previous phases

### Within Each Phase

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Phase 1 tasks marked [P] can run in parallel
- All Phase 2 tests marked [P] can run in parallel
- All Phase 3 tests marked [P] can run in parallel
- All Phase 4 tests marked [P] can run in parallel

---