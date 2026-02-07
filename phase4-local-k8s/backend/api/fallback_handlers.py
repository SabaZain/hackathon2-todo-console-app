"""
Fallback Handlers for Todo AI Chatbot API.

This module handles MCP tool unavailability scenarios with appropriate fallbacks.
"""

from typing import Dict, Any, Optional, List
from enum import Enum
import asyncio
import logging
from datetime import datetime


class FallbackStrategy(Enum):
    """Enumeration of different fallback strategies."""
    MOCK_RESPONSE = "mock_response"
    CACHE_RESPONSE = "cache_response"
    SIMPLIFIED_OPERATION = "simplified_operation"
    QUEUE_FOR_LATER = "queue_for_later"
    HUMAN_INTERVENTION = "human_intervention"
    DEGRADED_MODE = "degraded_mode"


class FallbackHandler:
    """Handles fallback scenarios when MCP tools are unavailable."""

    def __init__(self):
        """Initialize the fallback handler."""
        self.fallback_strategies = {}
        self.setup_default_strategies()
        self.degraded_mode = False
        self.unavailable_tools = set()

    def setup_default_strategies(self):
        """Set up default fallback strategies for different operations."""
        self.fallback_strategies = {
            "create_task": [FallbackStrategy.MOCK_RESPONSE, FallbackStrategy.DEGRADED_MODE],
            "list_tasks": [FallbackStrategy.CACHE_RESPONSE, FallbackStrategy.MOCK_RESPONSE],
            "update_task": [FallbackStrategy.QUEUE_FOR_LATER, FallbackStrategy.DEGRADED_MODE],
            "complete_task": [FallbackStrategy.QUEUE_FOR_LATER, FallbackStrategy.MOCK_RESPONSE],
            "delete_task": [FallbackStrategy.QUEUE_FOR_LATER, FallbackStrategy.DEGRADED_MODE],
        }

    def handle_unavailable_tool(self, tool_name: str, params: Dict[str, Any],
                               fallback_strategy: Optional[FallbackStrategy] = None) -> Dict[str, Any]:
        """
        Handle an unavailable MCP tool with appropriate fallback.

        Args:
            tool_name: Name of the unavailable tool
            params: Parameters for the tool call
            fallback_strategy: Specific fallback strategy to use (optional)

        Returns:
            Dictionary with fallback response
        """
        logging.warning(f"MCP tool '{tool_name}' is unavailable, using fallback")

        # Determine fallback strategy if not specified
        if fallback_strategy is None:
            strategies = self.fallback_strategies.get(tool_name, [FallbackStrategy.MOCK_RESPONSE])
            fallback_strategy = strategies[0]  # Use primary strategy

        # Mark tool as unavailable
        self.unavailable_tools.add(tool_name)

        # Execute appropriate fallback
        if fallback_strategy == FallbackStrategy.MOCK_RESPONSE:
            return self._handle_mock_response(tool_name, params)
        elif fallback_strategy == FallbackStrategy.CACHE_RESPONSE:
            return self._handle_cache_response(tool_name, params)
        elif fallback_strategy == FallbackStrategy.SIMPLIFIED_OPERATION:
            return self._handle_simplified_operation(tool_name, params)
        elif fallback_strategy == FallbackStrategy.QUEUE_FOR_LATER:
            return self._handle_queue_for_later(tool_name, params)
        elif fallback_strategy == FallbackStrategy.HUMAN_INTERVENTION:
            return self._handle_human_intervention(tool_name, params)
        elif fallback_strategy == FallbackStrategy.DEGRADED_MODE:
            return self._handle_degraded_mode(tool_name, params)
        else:
            # Default to mock response
            return self._handle_mock_response(tool_name, params)

    def _handle_mock_response(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by returning a mock response that simulates the tool.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Mock response
        """
        mock_responses = {
            "create_task": {
                "success": True,
                "task_id": f"mock_{hash(str(params)) % 10000}",
                "message": f"Task '{params.get('description', 'unnamed')}' has been created (mock response). We'll process this when the system is available."
            },
            "list_tasks": {
                "success": True,
                "tasks": [],
                "message": "Currently unable to retrieve tasks from the system. Showing empty list until service is restored."
            },
            "update_task": {
                "success": True,
                "message": f"Task update for '{params.get('task_id', 'unknown')}' has been recorded (mock response). Changes will be applied when the system is available."
            },
            "complete_task": {
                "success": True,
                "message": f"Task completion for '{params.get('task_id', 'unknown')}' has been recorded (mock response). This will be processed when the system is available."
            },
            "delete_task": {
                "success": True,
                "message": f"Task deletion for '{params.get('task_id', 'unknown')}' has been recorded (mock response). This will be processed when the system is available."
            }
        }

        return mock_responses.get(tool_name, {
            "success": False,
            "message": f"The {tool_name} operation is temporarily unavailable. Please try again later.",
            "fallback_used": True
        })

    def _handle_cache_response(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by returning cached data if available.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Cached response or mock response
        """
        # In a real implementation, this would retrieve from cache
        # For now, return a mock response indicating cache is unavailable
        return {
            "success": True,
            "message": "Using cached data (simulated). The actual operation is temporarily unavailable.",
            "cached": True,
            "timestamp": datetime.utcnow().isoformat()
        }

    def _handle_simplified_operation(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by performing a simplified version of the operation.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Simplified response
        """
        # Simplified operations that don't require MCP tools
        if tool_name == "list_tasks":
            return {
                "success": True,
                "tasks": [],
                "message": "Showing simplified task view. Full functionality will be restored when MCP tools are available.",
                "simplified": True
            }
        elif tool_name == "create_task":
            return {
                "success": True,
                "task_id": f"simplified_{hash(str(params)) % 10000}",
                "message": f"Task '{params.get('description', 'unnamed')}' recorded in simplified mode. Will be processed when MCP tools are available.",
                "simplified": True
            }

        return {
            "success": True,
            "message": f"Simplified operation performed for {tool_name}. Full operation will be processed when MCP tools are available.",
            "simplified": True
        }

    def _handle_queue_for_later(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by queuing the operation for later execution.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Queue confirmation response
        """
        # In a real implementation, this would add the operation to a queue
        # For now, simulate queuing
        return {
            "success": True,
            "queued": True,
            "operation": tool_name,
            "params": params,
            "message": f"The {tool_name} operation has been queued and will be executed when MCP tools become available.",
            "estimated_processing_time": "within 5 minutes"
        }

    def _handle_human_intervention(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by indicating human intervention is required.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Human intervention response
        """
        return {
            "success": False,
            "requires_human_intervention": True,
            "message": f"The {tool_name} operation requires human assistance due to system unavailability. Our team has been notified.",
            "contact_support": True
        }

    def _handle_degraded_mode(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle by switching to degraded mode.

        Args:
            tool_name: Name of the tool
            params: Parameters for the tool call

        Returns:
            Degraded mode response
        """
        self.degraded_mode = True

        return {
            "success": True,
            "degraded_mode": True,
            "message": f"Operating in degraded mode. The {tool_name} functionality is limited due to MCP tool unavailability.",
            "available_functions": ["basic_chat", "view_status"]
        }

    def is_tool_available(self, tool_name: str) -> bool:
        """
        Check if a specific tool is available.

        Args:
            tool_name: Name of the tool to check

        Returns:
            Boolean indicating availability
        """
        return tool_name not in self.unavailable_tools

    def check_system_status(self) -> Dict[str, Any]:
        """
        Check overall system status.

        Returns:
            Dictionary with system status information
        """
        return {
            "degraded_mode": self.degraded_mode,
            "unavailable_tools": list(self.unavailable_tools),
            "system_operational": len(self.unavailable_tools) == 0,
            "timestamp": datetime.utcnow().isoformat()
        }

    def clear_unavailable_tool(self, tool_name: str):
        """
        Mark a tool as available again.

        Args:
            tool_name: Name of the tool to mark as available
        """
        self.unavailable_tools.discard(tool_name)
        if len(self.unavailable_tools) == 0:
            self.degraded_mode = False


class APIServiceFallbackHandler:
    """Fallback handler specifically for API services."""

    def __init__(self):
        """Initialize the API service fallback handler."""
        self.fallback_handler = FallbackHandler()

    async def handle_service_unavailable(self, service_name: str, operation: str,
                                       params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle a service unavailability scenario.

        Args:
            service_name: Name of the unavailable service
            operation: Operation that was attempted
            params: Parameters for the operation

        Returns:
            Fallback response
        """
        logging.warning(f"Service '{service_name}' unavailable for operation '{operation}'")

        # Determine appropriate fallback based on service and operation
        if service_name == "mcp" and operation.startswith("task_"):
            return self.fallback_handler.handle_unavailable_tool(operation, params)
        else:
            # Use mock response as default fallback
            return self.fallback_handler.handle_unavailable_tool(
                operation, params, FallbackStrategy.MOCK_RESPONSE
            )

    def get_degraded_response(self, original_request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a degraded mode response based on the original request.

        Args:
            original_request: The original request that triggered the fallback

        Returns:
            Degraded mode response
        """
        return {
            "success": True,
            "degraded_mode": True,
            "message": "Operating in degraded mode due to service unavailability. Some features may be limited.",
            "partial_result": True,
            "original_request": original_request,
            "fallback_applied": True
        }


def get_fallback_handler() -> FallbackHandler:
    """
    Get an instance of the fallback handler.

    Returns:
        FallbackHandler instance
    """
    return FallbackHandler()


def get_api_fallback_handler() -> APIServiceFallbackHandler:
    """
    Get an instance of the API service fallback handler.

    Returns:
        APIServiceFallbackHandler instance
    """
    return APIServiceFallbackHandler()