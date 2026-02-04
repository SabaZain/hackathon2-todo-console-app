"""
Tool Mapper for Todo AI Chatbot

This module maps natural language to appropriate MCP tool calls.
"""

from typing import Dict, Any, Optional, List
from enum import Enum


class ToolType(Enum):
    """Enumeration of available MCP tools."""
    CREATE_TASK = "create_task"
    LIST_TASKS = "list_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"


class ToolMapper:
    """Maps natural language commands to appropriate MCP tools."""

    def __init__(self):
        """Initialize the tool mapper."""
        self.tool_mapping_rules = self._define_tool_mappings()

    def _define_tool_mappings(self) -> Dict[str, ToolType]:
        """
        Define rules for mapping natural language to tools.

        Returns:
            Dictionary of keyword-to-tool mappings
        """
        return {
            # Keywords for creating tasks
            'add': ToolType.CREATE_TASK,
            'create': ToolType.CREATE_TASK,
            'make': ToolType.CREATE_TASK,
            'new': ToolType.CREATE_TASK,
            'put in': ToolType.CREATE_TASK,
            'set up': ToolType.CREATE_TASK,
            'establish': ToolType.CREATE_TASK,
            'need to': ToolType.CREATE_TASK,
            'want to': ToolType.CREATE_TASK,
            'must': ToolType.CREATE_TASK,
            'should': ToolType.CREATE_TASK,
            'going to': ToolType.CREATE_TASK,
            'will': ToolType.CREATE_TASK,
            'remember to': ToolType.CREATE_TASK,

            # Keywords for listing tasks
            'list': ToolType.LIST_TASKS,
            'show': ToolType.LIST_TASKS,
            'display': ToolType.LIST_TASKS,
            'view': ToolType.LIST_TASKS,
            'see': ToolType.LIST_TASKS,
            'what are': ToolType.LIST_TASKS,
            'what is': ToolType.LIST_TASKS,
            'do i have': ToolType.LIST_TASKS,
            'what do i have': ToolType.LIST_TASKS,
            'what should i do': ToolType.LIST_TASKS,
            'what am i supposed to do': ToolType.LIST_TASKS,
            'what remains': ToolType.LIST_TASKS,
            'what is left': ToolType.LIST_TASKS,

            # Keywords for updating tasks
            'update': ToolType.UPDATE_TASK,
            'change': ToolType.UPDATE_TASK,
            'modify': ToolType.UPDATE_TASK,
            'edit': ToolType.UPDATE_TASK,
            'adjust': ToolType.UPDATE_TASK,
            'revise': ToolType.UPDATE_TASK,
            'alter': ToolType.UPDATE_TASK,
            'set': ToolType.UPDATE_TASK,
            'make': ToolType.UPDATE_TASK,

            # Keywords for completing tasks
            'mark': ToolType.COMPLETE_TASK,
            'complete': ToolType.COMPLETE_TASK,
            'finish': ToolType.COMPLETE_TASK,
            'done': ToolType.COMPLETE_TASK,
            'close': ToolType.COMPLETE_TASK,
            'accomplish': ToolType.COMPLETE_TASK,
            'achieve': ToolType.COMPLETE_TASK,
            'tick off': ToolType.COMPLETE_TASK,
            'check off': ToolType.COMPLETE_TASK,
            'completed': ToolType.COMPLETE_TASK,
            'finished': ToolType.COMPLETE_TASK,

            # Keywords for deleting tasks
            'remove': ToolType.DELETE_TASK,
            'delete': ToolType.DELETE_TASK,
            'erase': ToolType.DELETE_TASK,
            'cancel': ToolType.DELETE_TASK,
            'eliminate': ToolType.DELETE_TASK,
            'purge': ToolType.DELETE_TASK,
            'get rid of': ToolType.DELETE_TASK,
            'dispose of': ToolType.DELETE_TASK,
            'kill': ToolType.DELETE_TASK,
            'destroy': ToolType.DELETE_TASK,
        }

    def map_to_tool(self, command_type: str) -> Optional[ToolType]:
        """
        Map a command type to an appropriate tool.

        Args:
            command_type: The type of command to map

        Returns:
            ToolType if found, None otherwise
        """
        command_lower = command_type.lower()

        # Direct mapping
        for keyword, tool_type in self.tool_mapping_rules.items():
            if keyword in command_lower:
                return tool_type

        # More complex mapping based on context
        if self._is_create_command(command_lower):
            return ToolType.CREATE_TASK
        elif self._is_list_command(command_lower):
            return ToolType.LIST_TASKS
        elif self._is_update_command(command_lower):
            return ToolType.UPDATE_TASK
        elif self._is_complete_command(command_lower):
            return ToolType.COMPLETE_TASK
        elif self._is_delete_command(command_lower):
            return ToolType.DELETE_TASK

        return None

    def _is_create_command(self, text: str) -> bool:
        """
        Check if the text indicates a create command.

        Args:
            text: The text to check

        Returns:
            Boolean indicating if this is a create command
        """
        create_indicators = [
            'add', 'create', 'make', 'new', 'put in', 'set up', 'establish',
            'need to', 'want to', 'must', 'should', 'going to', 'will',
            'remember to', 'have to', 'ought to', 'shall', 'would like to'
        ]
        return any(indicator in text for indicator in create_indicators)

    def _is_list_command(self, text: str) -> bool:
        """
        Check if the text indicates a list command.

        Args:
            text: The text to check

        Returns:
            Boolean indicating if this is a list command
        """
        list_indicators = [
            'list', 'show', 'display', 'view', 'see', 'what are', 'what is',
            'do i have', 'what do i have', 'what should i do', 'what remains',
            'what is left', 'all', 'my tasks', 'my todos', 'my to-dos'
        ]
        return any(indicator in text for indicator in list_indicators)

    def _is_update_command(self, text: str) -> bool:
        """
        Check if the text indicates an update command.

        Args:
            text: The text to check

        Returns:
            Boolean indicating if this is an update command
        """
        update_indicators = [
            'update', 'change', 'modify', 'edit', 'adjust', 'revise', 'alter',
            'set', 'make', 'update the', 'change the', 'modify the'
        ]
        return any(indicator in text for indicator in update_indicators)

    def _is_complete_command(self, text: str) -> bool:
        """
        Check if the text indicates a complete command.

        Args:
            text: The text to check

        Returns:
            Boolean indicating if this is a complete command
        """
        complete_indicators = [
            'mark', 'complete', 'finish', 'done', 'close', 'accomplish',
            'achieve', 'tick off', 'check off', 'completed', 'finished',
            'i did', 'i finished', 'i completed', 'is done', 'was done'
        ]
        return any(indicator in text for indicator in complete_indicators)

    def _is_delete_command(self, text: str) -> bool:
        """
        Check if the text indicates a delete command.

        Args:
            text: The text to check

        Returns:
            Boolean indicating if this is a delete command
        """
        delete_indicators = [
            'remove', 'delete', 'erase', 'cancel', 'eliminate', 'purge',
            'get rid of', 'dispose of', 'kill', 'destroy', 'toss',
            'throw out', 'discard', 'bin', 'trash', 'dump', 'clear'
        ]
        return any(indicator in text for indicator in delete_indicators)

    def get_tool_parameters(self, command_type: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get appropriate parameters for an MCP tool call based on command type and extracted data.

        Args:
            command_type: The type of command
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for the tool call
        """
        tool_type = self.map_to_tool(command_type)

        if tool_type == ToolType.CREATE_TASK:
            return self._get_create_task_params(extracted_data)
        elif tool_type == ToolType.LIST_TASKS:
            return self._get_list_tasks_params(extracted_data)
        elif tool_type == ToolType.UPDATE_TASK:
            return self._get_update_task_params(extracted_data)
        elif tool_type == ToolType.COMPLETE_TASK:
            return self._get_complete_task_params(extracted_data)
        elif tool_type == ToolType.DELETE_TASK:
            return self._get_delete_task_params(extracted_data)
        else:
            return {}

    def _get_create_task_params(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameters for create task tool call.

        Args:
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for create task tool
        """
        params = {
            'description': extracted_data.get('description', ''),
            'due_date': extracted_data.get('due_date'),
            'priority': extracted_data.get('priority', 'medium'),
            'category': extracted_data.get('category', 'general'),
            'tags': extracted_data.get('tags', [])
        }

        # Ensure description is not empty
        if not params['description']:
            params['description'] = 'Untitled task'

        return params

    def _get_list_tasks_params(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameters for list tasks tool call.

        Args:
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for list tasks tool
        """
        return {
            'filter': extracted_data.get('filter', 'all'),
            'sort_by': extracted_data.get('sort_by', 'created'),
            'sort_order': extracted_data.get('sort_order', 'asc'),
            'limit': extracted_data.get('limit'),
            'category': extracted_data.get('category'),
            'priority': extracted_data.get('priority'),
            'search_term': extracted_data.get('search_term'),
            'include_overdue': extracted_data.get('include_overdue', True)
        }

    def _get_update_task_params(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameters for update task tool call.

        Args:
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for update task tool
        """
        return {
            'task_id': extracted_data.get('task_id'),
            'updates': extracted_data.get('updates', {}),
            'field_updates': extracted_data.get('field_updates', {})
        }

    def _get_complete_task_params(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameters for complete task tool call.

        Args:
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for complete task tool
        """
        return {
            'task_id': extracted_data.get('task_id'),
            'description': extracted_data.get('description')
        }

    def _get_delete_task_params(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get parameters for delete task tool call.

        Args:
            extracted_data: Data extracted from natural language

        Returns:
            Dictionary of parameters for delete task tool
        """
        return {
            'task_id': extracted_data.get('task_id'),
            'description': extracted_data.get('description')
        }

    def get_available_tools(self) -> List[ToolType]:
        """
        Get a list of available tools.

        Returns:
            List of available ToolType values
        """
        return list(ToolType)

    def get_tool_description(self, tool_type: ToolType) -> str:
        """
        Get a description of what a tool does.

        Args:
            tool_type: The tool type to describe

        Returns:
            Description of the tool
        """
        descriptions = {
            ToolType.CREATE_TASK: "Creates a new task with the specified details",
            ToolType.LIST_TASKS: "Lists tasks based on the specified filters and sorting options",
            ToolType.UPDATE_TASK: "Updates an existing task with new information",
            ToolType.COMPLETE_TASK: "Marks a task as completed",
            ToolType.DELETE_TASK: "Deletes a task permanently"
        }
        return descriptions.get(tool_type, "Unknown tool")

    def get_tool_schema(self, tool_type: ToolType) -> Dict[str, Any]:
        """
        Get the expected schema for a tool's parameters.

        Args:
            tool_type: The tool type to get schema for

        Returns:
            Schema definition for the tool's parameters
        """
        schemas = {
            ToolType.CREATE_TASK: {
                "type": "object",
                "properties": {
                    "description": {"type": "string", "description": "Task description"},
                    "due_date": {"type": "string", "format": "date", "description": "Due date in YYYY-MM-DD format"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Task priority"},
                    "category": {"type": "string", "description": "Task category"},
                    "tags": {"type": "array", "items": {"type": "string"}, "description": "Task tags"}
                },
                "required": ["description"]
            },
            ToolType.LIST_TASKS: {
                "type": "object",
                "properties": {
                    "filter": {"type": "string", "enum": ["all", "pending", "completed", "overdue"], "description": "Filter type"},
                    "sort_by": {"type": "string", "enum": ["created", "due_date", "priority", "name"], "description": "Sort by field"},
                    "sort_order": {"type": "string", "enum": ["asc", "desc"], "description": "Sort order"},
                    "limit": {"type": "integer", "description": "Maximum number of tasks to return"},
                    "category": {"type": "string", "description": "Category to filter by"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high"], "description": "Priority to filter by"},
                    "search_term": {"type": "string", "description": "Search term for filtering"},
                    "include_overdue": {"type": "boolean", "description": "Include overdue tasks in pending filter"}
                }
            },
            ToolType.UPDATE_TASK: {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to update"},
                    "updates": {"type": "object", "description": "Dictionary of fields to update"},
                    "field_updates": {"type": "object", "description": "Specific field updates"}
                },
                "required": ["task_id"]
            },
            ToolType.COMPLETE_TASK: {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to complete"},
                    "description": {"type": "string", "description": "Description of the task to complete"}
                }
            },
            ToolType.DELETE_TASK: {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string", "description": "ID of the task to delete"},
                    "description": {"type": "string", "description": "Description of the task to delete"}
                }
            }
        }
        return schemas.get(tool_type, {})


def get_tool_mapper() -> ToolMapper:
    """
    Get an instance of the tool mapper.

    Returns:
        ToolMapper instance
    """
    return ToolMapper()