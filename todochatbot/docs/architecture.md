# Todo AI Chatbot Architecture

## Overview

The Todo AI Chatbot is designed as a modular, scalable system that integrates seamlessly with existing Todo functionality. The architecture follows a stateless design principle to ensure scalability and reliability while maintaining proper isolation between users.

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API    │    │   AI Agent      │
│   (Widget)      │◄──►│   (FastAPI)      │◄──►│   (OpenAI/LLM)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   MCP Tools      │
                    │   (Database)     │
                    └──────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Data Storage   │
                    │   (SQLite/DB)    │
                    └──────────────────┘
```

## Component Architecture

### 1. Frontend Components (`/todo-chatbot/frontend/`)

#### Core Components
- `chat-icon.js`: Floating chat icon that doesn't interfere with existing UI
- `chat-interface.js`: Modal/chat interface with message history display
- `ui-controller.js`: Handles opening/closing of chat interface functionality
- `message-sender.js`: Sends user messages to backend API
- `message-display.js`: Displays AI responses in conversation format
- `typing-indicator.js`: Shows typing indicators during AI processing
- `integration.js`: Embeds widget into existing Todo application layout
- `api-client.js`: Implements API calls to `/api/{user_id}/chat` endpoint
- `response-handler.js`: Handles response formatting and error states

#### Design Principles
- No conflicts with existing CSS or JavaScript
- Maintains existing Todo functionality when chat is closed
- Responsive design for different screen sizes

### 2. Backend API (`/todo-chatbot/api/`)

#### Core Components
- `chat_endpoint.py`: FastAPI/FastHTML route for chat communication
- `validation.py`: Request validation and sanitization
- `agent_connector.py`: Connects to AI agent for message processing
- `conversation_manager.py`: Handles conversation state management via database
- `error_handlers.py`: Implements graceful error handling for AI agent failures
- `fallback_handlers.py`: Handles MCP tool unavailability scenarios
- `user_messages.py`: Provides user-friendly error messages
- `persistence_handler.py`: Ensures conversations survive server restarts

#### Design Principles
- Stateless operation for scalability
- Proper request validation and sanitization
- Graceful degradation when services are unavailable

### 3. AI Agent (`/todo-chatbot/agent/`)

#### Core Components
- `chat_agent.py`: Main AI agent implementation
- `system_prompt.py`: System prompt for todo management
- `configuration.py`: Agent configuration
- `intent_mapper.py`: Maps recognized intents to appropriate MCP tools
- `multi_step_handler.py`: Handles multi-step operations (e.g., create task with details)
- `context_manager.py`: Implements context preservation across conversation turns
- `history_manager.py`: Conversation history management
- `reference_resolver.py`: Handles follow-up questions and references to previous statements
- `response_formatter.py`: Formats AI responses

#### Design Principles
- Intent recognition for task operations (add, list, update, complete, delete)
- Multi-step operation support
- Context preservation across conversation turns
- Proper integration with MCP tools

### 4. NLP Components (`/todo-chatbot/nlp/`)

#### Core Components
- `add_task_processor.py`: Natural language processing for "add task" commands
- `list_task_processor.py`: Natural language processing for "list tasks" commands
- `update_task_processor.py`: Natural language processing for "update task" commands
- `complete_task_processor.py`: Natural language processing for "complete task" commands
- `delete_task_processor.py`: Natural language processing for "delete task" commands
- `tool_mapper.py`: Maps natural language to appropriate MCP tool calls
- `validator.py`: Validates extracted task information
- `multipart_handler.py`: Handles multi-part task creation (e.g., "Add a task to buy groceries tomorrow")

#### Design Principles
- Natural language understanding for all task operations
- Proper validation of extracted information
- Support for complex multi-part interactions

### 5. Conversation Management (`/todo-chatbot/conversation/`)

#### Core Components
- `state_reconstructor.py`: Reconstructs conversation state from stored messages
- `storage.py`: Stores conversation history in database with proper indexing
- `retriever.py`: Retrieves conversation history for existing conversations
- `context_preserver.py`: Handles conversation context across multiple turns
- `resumer.py`: Supports conversation continuation after interruptions
- `stateless_handler.py`: Ensures each API request is stateless and self-contained
- `isolator.py`: Validates conversation isolation between users
- `cleanup.py`: Implements conversation cleanup for inactive sessions

#### Design Principles
- State reconstruction from persisted data
- Stateless API design
- User isolation and data privacy
- Automatic cleanup of inactive sessions

### 6. MCP Tools (`/todo-chatbot/mcp-tools/`)

#### Core Components
- `task_tools.py`: Stateful implementations for create, list, update, complete, delete operations

#### Design Principles
- Connection to existing database without bypassing business logic
- Proper validation for all input parameters
- Comprehensive error handling and user-friendly messages
- Stateless operation principle

### 7. Database Layer (`/todo-chatbot/database/`)

#### Core Components
- `conversations.py`: Functions to save/load conversation messages with proper persistence

#### Design Principles
- Proper indexing for conversation retrieval
- Efficient storage and retrieval of conversation history

## Security Architecture

### Security Components (`/todo-chatbot/security/`)
- `input_validation.py`: Input sanitization and validation for security
- `auth_handler.py`: Authentication and authorization
- `vulnerability_tests.py`: Testing against injection and other security vulnerabilities

#### Security Principles
- Input validation and sanitization at all entry points
- Authentication and authorization for all API endpoints
- Protection against common vulnerabilities (SQL injection, XSS, etc.)

## Performance Architecture

### Performance Components (`/todo-chatbot/performance/`)
- `query_optimizer.py`: Optimizes database queries for conversation history
- `response_optimizer.py`: Minimizes AI agent response times
- `resource_optimizer.js`: Optimizes frontend resource usage

#### Performance Principles
- Query optimization with caching and indexing
- Response time optimization for AI interactions
- Efficient resource usage in frontend

## Error Handling Architecture

### Error Handling Components (`/todo-chatbot/error_handling/`)
- `standardized_handlers.py`: Standardized error handling using skills

#### Error Handling Principles
- Consistent error responses across all components
- Graceful degradation when services are unavailable
- Proper logging for debugging and monitoring

## Formatting Architecture

### Formatting Components (`/todo-chatbot/formatting/`)
- `response_formatter.py`: Response formatting using skills

#### Formatting Principles
- Consistent response formatting
- User-friendly error messages

## Data Flow

### Typical Request Flow
1. **Frontend**: User enters message in chat interface
2. **API**: Request is validated and sanitized
3. **AI Agent**: Processes natural language and determines intent
4. **NLP**: Extracts task details and validates information
5. **MCP Tools**: Performs database operations
6. **Conversation**: Updates conversation state and context
7. **Response**: Formatted response sent back to frontend

### Conversation State Flow
1. **State Reconstruction**: Conversation state rebuilt from persisted data
2. **Context Preservation**: Context maintained across multiple turns
3. **State Update**: New messages and context stored
4. **Persistence**: Updated state saved to database

## Scalability Considerations

### Stateless Design
- Each API request is self-contained
- No server-side session state
- Horizontal scaling capability

### Caching Strategy
- Conversation state caching
- Response caching for repeated queries
- Database query result caching

### Resource Management
- Connection pooling for database access
- Thread-safe operations
- Efficient memory usage

## Deployment Architecture

### Environment Requirements
- Python 3.8+ for backend services
- Node.js for frontend asset processing
- Database (SQLite for development, PostgreSQL for production)
- AI provider API access (OpenAI, etc.)

### Containerization
- Docker containers for microservices
- Environment variable configuration
- Health check endpoints

## Integration Points

### With Existing Todo Application
- Non-intrusive integration
- Shared authentication system
- Independent data storage
- Compatible API contracts

### Third-Party Services
- AI platform integration (OpenAI, etc.)
- Monitoring and logging services
- Analytics platforms

## Testing Architecture

### Test Organization (`/todo-chatbot/tests/`)
- `e2e_flows.py`: Complete conversation flows from frontend to MCP tools
- `operation_tests.py`: All todo operations through chat interface
- `error_scenarios.py`: Error handling and recovery scenarios
- `regression_tests.py`: Existing Todo functionality integrity
- `performance_tests.py`: Performance verification
- `concurrency_tests.py`: Concurrent usage testing
- `persistence_tests.py`: Server restart survival
- `history_tests.py`: Conversation history retrieval
- `isolation_tests.py`: Multi-user isolation validation

### Testing Principles
- Comprehensive coverage of all components
- Isolation testing for each module
- Integration testing for complete flows
- Performance and security testing

## Monitoring and Observability

### Logging Strategy
- Structured logging for all components
- Performance metrics collection
- Error tracking and alerting
- Audit trails for security

### Health Checks
- Service availability monitoring
- Database connectivity checks
- External API health monitoring
- Resource utilization tracking

This architecture enables the Todo AI Chatbot to provide a seamless, secure, and scalable natural language interface while maintaining compatibility with existing Todo functionality.