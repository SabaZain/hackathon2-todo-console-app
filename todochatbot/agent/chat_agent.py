"""
Chat Agent for Todo AI Chatbot.

This module implements the core AI agent that processes natural language
and invokes MCP tools for todo operations using Cohere NLP and JWT authentication.
"""

import os
import asyncio
import jwt
import cohere
from typing import Dict, Any, Optional
from .system_prompt import get_system_prompt
from .configuration import get_agent_config
import sys
import os

# Handle imports based on execution context
# Prevent re-importing SQLAlchemy models to avoid metadata conflicts
try:
    # Try relative imports first (for when running as part of the package)
    from ..nlp.tool_mapper import get_tool_mapper
    from ..mcp_tools.task_tools import (
        create_task, list_tasks, update_task, complete_task, delete_task
    )
    # Import session for potential injection
    from sqlmodel import Session
except (ImportError, ValueError):
    # Add the parent directory to the Python path to handle direct execution
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # This is the todochatbot directory

    # Add the grandparent directory (hackathontwo) to the path
    grandparent_dir = os.path.dirname(parent_dir)
    if grandparent_dir not in sys.path:
        sys.path.insert(0, grandparent_dir)

    # Now try to import with the updated path
    try:
        from todochatbot.nlp.tool_mapper import get_tool_mapper
        from todochatbot.mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )
        from sqlmodel import Session
    except ImportError:
        # Last resort: import directly from the relative path
        from nlp.tool_mapper import get_tool_mapper
        from mcp_tools.task_tools import (
            create_task, list_tasks, update_task, complete_task, delete_task
        )
        from sqlmodel import Session


class ChatAgent:
    """Main AI agent for processing natural language todo commands."""

    def __init__(self):
        """Initialize the chat agent with configuration and Cohere client."""
        self.config = get_agent_config()
        self.system_prompt = get_system_prompt()
        self.cohere_client = cohere.Client(os.getenv("COHERE_API_KEY"))
        self.jwt_secret = os.getenv("JWT_SECRET")
        self.tool_mapper = get_tool_mapper()

    async def process_message(self, user_id: str, conversation_id: str, message: str, session=None) -> Dict[str, Any]:
        """
        Process a user message using Cohere NLP and return AI response.

        Args:
            user_id: The ID of the user
            conversation_id: The ID of the conversation
            message: The user's message
            session: Optional database session to use for tool operations

        Returns:
            Dictionary containing the AI response and any tool invocations
        """
        try:
            # Use Cohere to classify the intent
            intent = await self._classify_intent_cohere(message)

            # Determine if the input is in Urdu for response language
            is_urdu = self._is_urdu_text(message)

            # Strict intent-based routing with proper tool-first behavior
            if intent in ['greeting', 'help', 'general']:
                # For greetings, help, and general questions, do not call any tools
                # Just return appropriate descriptive responses
                if intent == 'greeting':
                    # Check if the greeting includes identity questions
                    message_lower = message.lower()
                    if any(phrase in message_lower for phrase in ['who are you', 'what are you', 'introduce yourself', 'what is your name']):
                        # Always respond with the proper identity as specified in the system prompt
                        if is_urdu:
                            response_text = "Main aapka Todo AI Assistant hoon"
                        else:
                            response_text = "I am your Todo AI Assistant."
                    else:
                        if is_urdu:
                            response_text = "Namaste! Main aapka Todo AI Assistant hoon. Kaise madad kar sakta hoon?"
                        else:
                            response_text = "Hello! I'm your Todo AI Assistant. How can I help you?"
                elif intent == 'help':
                    # Check if the user is asking about the AI's identity
                    message_lower = message.lower()
                    if any(phrase in message_lower for phrase in ['who are you', 'what are you', 'introduce yourself', 'what is your name']):
                        # Always respond with the proper identity as specified in the system prompt
                        if is_urdu:
                            response_text = "Main aapka Todo AI Assistant hoon"
                        else:
                            response_text = "I am your Todo AI Assistant."
                    else:
                        # Provide help/capability description without hitting the database
                        if is_urdu:
                            response_text = "Main aapki task management mein madad kar sakta hoon. Aap mujhe kah sakte hain ki kya task add karna hai, aapke kya tasks hain, ya kisi task ko complete karna hai."
                        else:
                            response_text = "I can help you manage your tasks. You can ask me to add tasks, show your existing tasks, complete tasks, update tasks, or delete tasks."
                else:  # general
                    # For general questions, decide if they're capability-related or need tools
                    message_lower = message.lower()

                    # Check if it's asking about capabilities without requiring DB access
                    if any(phrase in message_lower for phrase in ['what can you', 'what do you', 'what are your', 'capabilities', 'features', 'can you do']):
                        if is_urdu:
                            response_text = "Main aapki task management mein madad kar sakta hoon. Aap mujhe kah sakte hain ki kya task add karna hai, aapke kya tasks hain, ya kisi task ko complete karna hai."
                        else:
                            response_text = "I can help you manage your tasks. You can ask me to add tasks, show your existing tasks, complete tasks, update tasks, or delete tasks."
                    else:
                        # For other general questions, use general response
                        response_text = await self._generate_general_response(message)

                # No tool calls for these intents
                response = {
                    "response_text": response_text,
                    "tool_calls": [],
                    "conversation_id": conversation_id,
                    "intent": intent
                }
            else:
                # For task-related intents, map to tools and execute them
                tool_type = self.tool_mapper.map_to_tool(intent)

                if tool_type:
                    # Prepare parameters for the tool based on the input
                    extracted_data = await self._extract_entities_cohere(message)
                    params = self.tool_mapper.get_tool_parameters(intent, extracted_data)

                    # Call the appropriate MCP tool (tool-first behavior)
                    if tool_type.name == 'CREATE_TASK':
                        result = create_task(
                            user_id=user_id,
                            description=params.get('description', message),
                            priority=params.get('priority', 'medium'),
                            due_date=params.get('due_date'),
                            category=params.get('category', 'general'),
                            tags=params.get('tags', []),
                            session=session  # Pass the session if available
                        )
                        if result.get('success', False):
                            response_text = f"I've created the task: {result.get('description', 'Task created successfully')}"
                        else:
                            if is_urdu:
                                response_text = "Mujhe task banane mein masla a raha hai. Kya aap details dobara bata sakte hain?"
                            else:
                                response_text = "I had trouble creating the task. Could you please provide the details again?"

                    elif tool_type.name == 'LIST_TASKS':
                        filter_param = params.get('filter', 'all')
                        tasks = list_tasks(user_id=user_id, status=filter_param if filter_param != 'all' else None, session=session)
                        if tasks:
                            task_list = "\n".join([f"- {task['description']}" for task in tasks])
                            if is_urdu:
                                response_text = f"Yeh aapke tasks hain:\n{task_list}"
                            else:
                                response_text = f"Here are your tasks:\n{task_list}"
                        else:
                            if is_urdu:
                                response_text = "Is user ke liye koi task maujood nahi."
                            else:
                                response_text = "You don't have any tasks."

                    elif tool_type.name == 'UPDATE_TASK':
                        task_id = params.get('task_id')
                        updates = params.get('updates', {})
                        if task_id and updates:
                            result = update_task(task_id, user_id, updates, session=session)
                            if result.get('success', False):
                                response_text = f"Task updated successfully: {result.get('description', '')}"
                            else:
                                if is_urdu:
                                    response_text = "Task update karna mushkil ho raha hai."
                                else:
                                    response_text = "I had trouble updating the task."
                        else:
                            if is_urdu:
                                response_text = "Mujhe zyada maloomat chahiye ta ke task update kar sakun. Kripya bataen konsa task aur kya update karna hai."
                            else:
                                response_text = "I need more information to update a task. Please specify which task and what to update."

                    elif tool_type.name == 'COMPLETE_TASK':
                        task_id = params.get('task_id')
                        if task_id:
                            result = complete_task(user_id, task_id, session=session)
                            if result.get('success', False):
                                if is_urdu:
                                    response_text = f"Task ko complete kiya gaya: {result.get('description', '')}"
                                else:
                                    response_text = f"Task marked as completed: {result.get('description', '')}"
                            else:
                                if is_urdu:
                                    response_text = "Task complete karna mushkil ho raha hai."
                                else:
                                    response_text = "I had trouble completing the task."
                        else:
                            if is_urdu:
                                response_text = " Mujhe batana hoga ke konsa task complete karna hai."
                            else:
                                response_text = "I need to know which task to mark as completed."

                    elif tool_type.name == 'DELETE_TASK':
                        task_id = params.get('task_id')
                        if task_id:
                            result = delete_task(user_id, task_id, session=session)
                            if result.get('success', False):
                                if is_urdu:
                                    response_text = f"Task delete kiya gaya: {result.get('id', task_id)}"
                                else:
                                    response_text = f"Task deleted: {result.get('id', task_id)}"
                            else:
                                if is_urdu:
                                    response_text = "Task delete karna mushkil ho raha hai."
                                else:
                                    response_text = "I had trouble deleting the task."
                        else:
                            if is_urdu:
                                response_text = "Mujhe batana hoga ke konsa task delete karna hai."
                            else:
                                response_text = "I need to know which task to delete."
                    else:
                        # Fallback to general response for unknown tool types
                        response_text = await self._generate_general_response(message)
                else:
                    # If intent is task-related but no tool mapping, use general response
                    response_text = await self._generate_general_response(message)

                response = {
                    "response_text": response_text,
                    "tool_calls": [{"name": tool_type.name, "arguments": params}] if tool_type else [],
                    "conversation_id": conversation_id,
                    "intent": intent
                }

            # Adjust response based on language detection
            if is_urdu and intent not in ['greeting', 'help', 'general']:
                if "don't have access" in response_text.lower() or "can't access" in response_text.lower():
                    response_text = "Mujhe aapke tasks tak poora access hai. Kripya bataen ke aap kya krna chahte hain?"

        except Exception as e:
            # Provide language-appropriate error handling
            is_urdu = self._is_urdu_text(message)
            if is_urdu:
                response_text = "Mujhe aapki request ko process karna mushkil ho raha hai. Kya aap usko dobara explain kar sakte hain?"
            else:
                response_text = f"I'm having trouble processing your request: {str(e)}. Could you try rephrasing it?"

            response = {
                "response_text": response_text,
                "tool_calls": [],
                "conversation_id": conversation_id,
                "intent": "error",
                "error": str(e)
            }

        return response

    def invoke_mcp_tool(self, tool_name: str, params: Dict[str, Any], session=None) -> Any:
        """
        Invoke an MCP tool with the given parameters.

        Args:
            tool_name: Name of the MCP tool to invoke
            params: Parameters for the tool call
            session: Optional database session to use

        Returns:
            Result from the MCP tool
        """
        # Map tool name to actual function
        tool_functions = {
            'create_task': create_task,
            'list_tasks': list_tasks,
            'update_task': update_task,
            'complete_task': complete_task,
            'delete_task': delete_task
        }

        if tool_name in tool_functions:
            tool_func = tool_functions[tool_name]
            # Add session parameter if available
            if session is not None:
                params['session'] = session
            return tool_func(**params)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    async def _classify_intent_cohere(self, user_input: str) -> str:
        """
        Use Cohere to classify the intent of the user input.

        Args:
            user_input: The user's message

        Returns:
            Classified intent string
        """
        try:
            # Use Cohere chat API to classify intent instead of classify API (which is deprecated)
            # Format the examples as few-shot examples in the prompt
            prompt = f"""Classify the intent of this user input. Choose from these categories:
- create_task: Adding a new task
- list_tasks: Showing existing tasks
- update_task: Changing an existing task
- complete_task: Marking a task as done
- delete_task: Removing a task
- greeting: Greetings like hello, hi
- help: Asking for assistance
- general: Other

Examples:
Input: "Add a task to buy groceries" -> create_task
Input: "Create a new task to call mom" -> create_task
Input: "Make a task to finish report" -> create_task
Input: "I need to add a task to schedule meeting" -> create_task
Input: "Show my tasks" -> list_tasks
Input: "List all my tasks" -> list_tasks
Input: "What tasks do I have?" -> list_tasks
Input: "Show pending tasks" -> list_tasks
Input: "Display completed tasks" -> list_tasks
Input: "Update task 1 to high priority" -> update_task
Input: "Change task 2 description" -> update_task
Input: "Modify task 3 due date" -> update_task
Input: "Edit task 4" -> update_task
Input: "Complete task 1" -> complete_task
Input: "Mark task 2 as done" -> complete_task
Input: "Finish task 3" -> complete_task
Input: "Complete the grocery task" -> complete_task
Input: "Delete task 1" -> delete_task
Input: "Remove task 2" -> delete_task
Input: "Cancel task 3" -> delete_task
Input: "Erase task 4" -> delete_task
Input: "Hello" -> greeting
Input: "Hi" -> greeting
Input: "How are you?" -> greeting
Input: "What can you do?" -> help
Input: "Help me" -> help
Input: "I need help" -> help

Input: "{user_input}" -> """

            # Try with the most basic available model
            response = self.cohere_client.chat(
                message=prompt,
                max_tokens=20,
                temperature=0.0  # Low temperature for consistent classification
            )

            # Extract the intent from the response
            intent = response.text.strip().lower().strip('.').strip('-').strip()

            # Validate that the intent is one of our expected values
            valid_intents = ['create_task', 'list_tasks', 'update_task', 'complete_task', 'delete_task', 'greeting', 'help', 'general']
            if intent in valid_intents:
                return intent
            else:
                # If the response is unexpected, try to match it to known patterns
                # Check the original user input instead of the Cohere response for better accuracy
                user_lower = user_input.lower()

                # Check for identity questions first (most specific patterns)
                if any(pattern in user_lower for pattern in ['who are you', 'what are you', 'introduce yourself', 'what is your name']):
                    return 'help'  # Identity questions are treated as help for consistency
                # Check for help/capability questions next
                elif any(pattern in user_lower for pattern in ['what can you', 'what do you', 'what are your', 'what is your', 'capabilities', 'features', 'can you do', 'help me', 'how can you']):
                    return 'help'
                elif any(pattern in user_lower for pattern in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
                    return 'greeting'
                elif 'create' in user_lower or 'add' in user_lower or 'make' in user_lower or 'new' in user_lower:
                    return 'create_task'
                elif 'list' in user_lower or 'show' in user_lower or 'display' in user_lower or ('what' in user_lower and 'task' in user_lower):
                    # Only 'what' + task-related words should trigger list_tasks
                    return 'list_tasks'
                elif 'update' in user_lower or 'change' in user_lower or 'edit' in user_lower or 'modify' in user_lower:
                    return 'update_task'
                elif 'complete' in user_lower or 'done' in user_lower or 'finish' in user_lower or 'mark' in user_lower:
                    return 'complete_task'
                elif 'delete' in user_lower or 'remove' in user_lower or 'cancel' in user_lower or 'erase' in user_lower:
                    return 'delete_task'
                else:
                    return 'general'

        except Exception:
            # Fallback to simple keyword matching if Cohere fails
            user_lower = user_input.lower()

            # Check for identity questions first (most specific patterns)
            if any(pattern in user_lower for pattern in ['who are you', 'what are you', 'introduce yourself', 'what is your name']):
                return 'help'  # Identity questions are treated as help for consistency
            # Check for help/capability questions next
            elif any(pattern in user_lower for pattern in ['what can you', 'what do you', 'what are your', 'what is your', 'capabilities', 'features', 'can you do', 'help me', 'how can you']):
                return 'help'
            elif any(pattern in user_lower for pattern in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
                return 'greeting'
            elif any(word in user_lower for word in ['add', 'create', 'new', 'make']):
                return 'create_task'
            elif any(word in user_lower for word in ['list', 'show', 'display', 'view']) or ('what' in user_lower and 'task' in user_lower):
                # Only 'what' + task-related words should trigger list_tasks
                return 'list_tasks'
            elif any(word in user_lower for word in ['update', 'change', 'modify', 'edit']):
                return 'update_task'
            elif any(word in user_lower for word in ['complete', 'done', 'finish', 'mark']):
                return 'complete_task'
            elif any(word in user_lower for word in ['delete', 'remove', 'cancel', 'erase']):
                return 'delete_task'
            else:
                return 'general'

    async def _extract_entities_cohere(self, user_input: str) -> Dict[str, Any]:
        """
        Use Cohere to extract entities from the user input.

        Args:
            user_input: The user's message

        Returns:
            Dictionary containing extracted entities
        """
        try:
            # This is a simplified entity extraction
            # In a real implementation, you would use Cohere's generative models
            # or other NLP techniques to extract specific entities

            entities = {}

            # Extract dates
            import re
            date_pattern = r'\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}[\/\-]\d{1,2}(?:[\/\-]\d{2,4})?\b|\b(today|tomorrow|yesterday|tonight)\b'
            date_matches = re.findall(date_pattern, user_input.lower())
            if date_matches:
                entities['due_date'] = date_matches[0]

            # Extract priority
            if 'high' in user_input.lower() or 'urgent' in user_input.lower() or 'asap' in user_input.lower():
                entities['priority'] = 'high'
            elif 'low' in user_input.lower():
                entities['priority'] = 'low'
            else:
                entities['priority'] = 'medium'

            # Extract task description (basic approach)
            # Remove common task verbs to isolate description
            common_verbs = ['add', 'create', 'make', 'list', 'show', 'update', 'change', 'complete', 'finish', 'delete', 'remove']
            words = user_input.split()
            desc_words = [word for word in words if word.lower() not in common_verbs]
            if len(desc_words) > 0:
                entities['description'] = ' '.join(desc_words)
            else:
                entities['description'] = user_input

            # Extract task ID if mentioned
            id_pattern = r'(?:task|number|#)\s*(\d+)'
            id_matches = re.findall(id_pattern, user_input, re.IGNORECASE)
            if id_matches:
                entities['task_id'] = int(id_matches[0])

            return entities
        except Exception:
            # Fallback to basic extraction
            return {
                'description': user_input,
                'priority': 'medium',
                'task_id': None
            }

    async def _generate_general_response(self, user_input: str) -> str:
        """
        Generate a general response when specific intent isn't clear.

        Args:
            user_input: The user's message

        Returns:
            Generated response string
        """
        try:
            # Detect if the input is in Urdu
            urdu_detected = self._is_urdu_text(user_input)

            # Check if the user is asking about the AI's identity
            if any(phrase in user_input.lower() for phrase in ['who are you', 'what are you', 'introduce yourself', 'what is your name', 'who are you?', 'what are you?']):
                # Always respond with the proper identity as specified in the system prompt
                if urdu_detected:
                    return "Main aapka Todo AI Assistant hoon"
                else:
                    return "I am your Todo AI Assistant."

            # Use Cohere to generate a contextual response - try chat first (current API)
            response = self.cohere_client.chat(
                message=user_input,
                max_tokens=100,
                temperature=0.7
            )

            result = response.text.strip()

            # If input was in Urdu, translate response to Urdu if needed
            if urdu_detected:
                # For this implementation, we'll just return the result, but in a real implementation
                # we'd translate to Urdu
                pass

            return result
        except Exception as e:
            # If chat fails, provide a friendly fallback message
            # Log error for debugging
            print(f"Cohere API error (chat method): {str(e)}")

            # Detect if the input was in Urdu and provide appropriate fallback
            if self._is_urdu_text(user_input):
                return "Mujhe aapki request ko process karna mushkil ho raha hai. Kya aap usko dobara explain kar sakte hain?"
            else:
                return f"I'm having trouble processing your request. Could you try rephrasing it?"


async def create_chat_agent() -> ChatAgent:
    """Factory function to create and initialize a chat agent."""
    return ChatAgent()