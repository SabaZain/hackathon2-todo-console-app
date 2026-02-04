"""
MCP Server for Todo Task Management Tools
Exposes the task management tools as an MCP (Model Context Protocol) server
"""

import asyncio
import json
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import sys
import os

# Add the backend directory to the path to access existing models and database functions
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from .task_tools import create_task, list_tasks, complete_task, delete_task, update_task

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPTaskTool(BaseModel):
    """Base class for MCP task tools"""
    name: str
    description: str
    input_schema: Dict[str, Any]


class MCPServer:
    """MCP Server that exposes task management tools to AI agents"""

    def __init__(self):
        self.tools = {
            "add_task": MCPTaskTool(
                name="add_task",
                description="Create a new task for a user",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "title": {"type": "string", "description": "The task title"},
                        "description": {"type": "string", "description": "The task description (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            ),
            "list_tasks": MCPTaskTool(
                name="list_tasks",
                description="Retrieve tasks for a user",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "status": {
                            "type": "string",
                            "enum": ["all", "pending", "completed"],
                            "description": "Filter by status (optional, default: all)"
                        }
                    },
                    "required": ["user_id"]
                }
            ),
            "complete_task": MCPTaskTool(
                name="complete_task",
                description="Mark a task as completed",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            "delete_task": MCPTaskTool(
                name="delete_task",
                description="Delete a task",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            "update_task": MCPTaskTool(
                name="update_task",
                description="Update task title or description",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "The user's ID"},
                        "task_id": {"type": "integer", "description": "The ID of the task to update"},
                        "title": {"type": "string", "description": "New task title (optional)"},
                        "description": {"type": "string", "description": "New task description (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            )
        }

    def get_tool_list(self) -> List[Dict[str, Any]]:
        """Return the list of available tools"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "inputSchema": tool.input_schema
            }
            for tool in self.tools.values()
        ]

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific tool with the given arguments"""
        logger.info(f"Executing tool: {tool_name} with arguments: {arguments}")

        if tool_name not in self.tools:
            raise ValueError(f"Unknown tool: {tool_name}")

        try:
            if tool_name == "add_task":
                result = create_task(
                    user_id=arguments["user_id"],
                    description=arguments["title"]
                )
            elif tool_name == "list_tasks":
                result = list_tasks(
                    user_id=arguments["user_id"],
                    status=arguments.get("status")
                )
            elif tool_name == "complete_task":
                result = complete_task(
                    user_id=arguments["user_id"],
                    task_id=arguments["task_id"]
                )
            elif tool_name == "delete_task":
                result = delete_task(
                    user_id=arguments["user_id"],
                    task_id=arguments["task_id"]
                )
            elif tool_name == "update_task":
                # Prepare updates dictionary for update_task function
                updates = {}
                if "title" in arguments:
                    updates["title"] = arguments["title"]
                if "description" in arguments:
                    updates["description"] = arguments["description"]

                result = update_task(
                    task_id=arguments["task_id"],
                    user_id=arguments["user_id"],
                    updates=updates
                )
            else:
                raise ValueError(f"Unknown tool: {tool_name}")

            logger.info(f"Tool {tool_name} executed successfully. Result: {result}")
            return result

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "error": str(e),
                "status": "failed"
            }


async def handle_mcp_request(reader, writer):
    """Handle incoming MCP requests"""
    try:
        # Read the request
        data = await reader.read(1024)
        request_str = data.decode('utf-8').strip()

        if not request_str:
            return

        # Parse the request
        try:
            request = json.loads(request_str)
        except json.JSONDecodeError:
            response = {
                "error": "Invalid JSON in request",
                "status": "failed"
            }
            response_str = json.dumps(response)
            writer.write(response_str.encode('utf-8'))
            await writer.drain()
            return

        logger.info(f"Received request: {request}")

        # Initialize the server
        server = MCPServer()

        # Handle different types of requests
        if request.get("type") == "getTools":
            response = {
                "tools": server.get_tool_list(),
                "status": "success"
            }
        elif request.get("type") == "callTool":
            tool_name = request.get("name")
            arguments = request.get("arguments", {})

            result = server.execute_tool(tool_name, arguments)
            response = {
                "result": result,
                "status": "success"
            }
        else:
            response = {
                "error": "Unknown request type",
                "status": "failed"
            }

        # Send the response
        response_str = json.dumps(response)
        writer.write(response_str.encode('utf-8'))
        await writer.drain()

    except Exception as e:
        logger.error(f"Error handling request: {str(e)}")
        error_response = {
            "error": str(e),
            "status": "failed"
        }
        response_str = json.dumps(error_response)
        writer.write(response_str.encode('utf-8'))
        await writer.drain()

    finally:
        writer.close()
        await writer.wait_closed()


async def start_mcp_server(host='localhost', port=8001):
    """Start the MCP server"""
    logger.info(f"Starting MCP server on {host}:{port}")

    server = await asyncio.start_server(
        handle_mcp_request,
        host,
        port
    )

    addr = server.sockets[0].getsockname()
    logger.info(f"MCP server listening on {addr[0]}:{addr[1]}")

    async with server:
        await server.serve_forever()


def main():
    """Main entry point to start the MCP server"""
    try:
        # Start the server
        asyncio.run(start_mcp_server())
    except KeyboardInterrupt:
        logger.info("MCP server stopped by user")
    except Exception as e:
        logger.error(f"Error starting MCP server: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()