"""
Configuration for Todo AI Chatbot Agent.

This module handles the configuration of the AI agent, particularly
the connection to MCP tools for todo operations.
"""

import os
from typing import Dict, Any


class AgentConfig:
    """Configuration class for the chat agent."""

    def __init__(self):
        """Initialize agent configuration with default values."""
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:3000")
        self.mcp_timeout = int(os.getenv("MCP_TIMEOUT", "30"))
        self.max_retries = int(os.getenv("AGENT_MAX_RETRIES", "3"))
        self.model_name = os.getenv("AGENT_MODEL_NAME", "gpt-4")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))


def get_agent_config() -> AgentConfig:
    """
    Get the agent configuration instance.

    Returns:
        AgentConfig instance with loaded configuration
    """
    return AgentConfig()


def get_mcp_tool_config() -> Dict[str, Any]:
    """
    Get configuration specific to MCP tool connections.

    Returns:
        Dictionary containing MCP tool configuration
    """
    config = {
        "server_url": os.getenv("MCP_SERVER_URL", "http://localhost:3000"),
        "timeout": int(os.getenv("MCP_TIMEOUT", "30")),
        "retries": int(os.getenv("MCP_RETRIES", "3")),
        "available_tools": [
            "create_task",
            "list_tasks",
            "update_task",
            "complete_task",
            "delete_task"
        ]
    }
    return config


def get_agent_model_config() -> Dict[str, Any]:
    """
    Get configuration for the AI model used by the agent.

    Returns:
        Dictionary containing AI model configuration
    """
    config = {
        "model_name": os.getenv("AGENT_MODEL_NAME", "gpt-4"),
        "temperature": float(os.getenv("AGENT_TEMPERATURE", "0.7")),
        "max_tokens": int(os.getenv("AGENT_MAX_TOKENS", "1000")),
        "top_p": float(os.getenv("AGENT_TOP_P", "1.0")),
        "frequency_penalty": float(os.getenv("AGENT_FREQ_PENALTY", "0.0")),
        "presence_penalty": float(os.getenv("AGENT_PRESENCE_PENALTY", "0.0"))
    }
    return config