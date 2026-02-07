"""
Intent Recognition for Todo AI Chatbot Agent.

This module implements intent recognition functionality based on the
intent detection skill from .claude/skills/intent-detection-skill.md
"""

from enum import Enum
from typing import Dict, List, Optional
import re


class Intent(Enum):
    """Enumeration of possible intents for the todo chatbot."""
    ADD_TASK = "add_task"
    LIST_TASKS = "list_tasks"
    LIST_PENDING_TASKS = "list_pending_tasks"
    LIST_COMPLETED_TASKS = "list_completed_tasks"
    UPDATE_TASK = "update_task"
    COMPLETE_TASK = "complete_task"
    DELETE_TASK = "delete_task"
    UNKNOWN = "unknown"


class IntentRecognizer:
    """Class to recognize user intents from natural language input."""

    def __init__(self):
        """Initialize the intent recognizer with known patterns."""
        self.patterns = {
            Intent.ADD_TASK: [
                r"\b(add|create|make|new)\s+(a\s+)?task\b",
                r"\b(task|todo)\s+(to|for)\s+",
                r"\bneed\s+to\s+(do|finish|complete)\b",
                r"\bremember\s+to\b"
            ],
            Intent.LIST_TASKS: [
                r"\b(list|show|display|view)\s+(all\s+)?tasks?\b",
                r"\b(what|which)\s+(do\s+i\s+have|are\s+on\s+my\s+list)\b",
                r"\bmy\s+tasks?\b"
            ],
            Intent.LIST_PENDING_TASKS: [
                r"\b(list|show|display|view)\s+(pending|incomplete|open|remaining)\s+tasks?\b",
                r"\b(what|which)\s+(is\s+left|do\s+i\s+still\s+have)\b",
                r"\bpending\s+tasks?\b"
            ],
            Intent.LIST_COMPLETED_TASKS: [
                r"\b(list|show|display|view)\s+(completed|done|finished)\s+tasks?\b",
                r"\b(completed|done)\s+tasks?\b"
            ],
            Intent.UPDATE_TASK: [
                r"\b(update|change|modify|edit)\s+(a\s+)?task\b",
                r"\b(change|update)\s+(the\s+)?details?\b",
                r"\bmodify\s+(a\s+)?task\b"
            ],
            Intent.COMPLETE_TASK: [
                r"\b(mark|set|complete|finish|done)\s+(a\s+)?task\b",
                r"\bcomplete\s+(a\s+)?task\b",
                r"\bmark\s+(as\s+)?(done|completed|finished)\b"
            ],
            Intent.DELETE_TASK: [
                r"\b(delete|remove|erase|cancel)\s+(a\s+)?task\b",
                r"\bremove\s+(from\s+)?(list|todo)\b"
            ]
        }

    def recognize_intent(self, text: str) -> Intent:
        """
        Recognize the intent from the given text.

        Args:
            text: The user's input text

        Returns:
            The recognized Intent enum value
        """
        text_lower = text.lower().strip()

        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent

        return Intent.UNKNOWN

    def extract_entities(self, text: str) -> Dict[str, str]:
        """
        Extract entities from the text that might be relevant for the recognized intent.

        Args:
            text: The user's input text

        Returns:
            Dictionary of extracted entities
        """
        entities = {}

        # Extract task descriptions
        # Look for text after common task phrases
        task_match = re.search(r"(?:to|for|that|should)\s+(.+?)(?:\.|$|,|!|\?)", text.lower())
        if task_match:
            entities['task_description'] = task_match.group(1).strip()

        # Look for dates
        date_patterns = [
            r"\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",  # MM/DD or MM/DD/YYYY
            r"\b(?:today|tomorrow|yesterday|tonight)\b",  # Common day references
            r"\bnext\s+(?:week|month|year|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b",  # Future dates
            r"\b\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?\b",  # Times
        ]

        for pattern in date_patterns:
            date_match = re.search(pattern, text.lower())
            if date_match and 'due_date' not in entities:
                entities['due_date'] = date_match.group(0)

        # Look for priorities
        priority_patterns = [
            r"\b(?:high|low|medium)\s+priority\b",
            r"\b(?:urgent|important)\b",
            r"\b(?:low|medium|high)\b"
        ]

        for pattern in priority_patterns:
            priority_match = re.search(pattern, text.lower())
            if priority_match:
                entities['priority'] = priority_match.group(0)

        return entities


def get_intent_recognizer() -> IntentRecognizer:
    """
    Get an instance of the intent recognizer.

    Returns:
        IntentRecognizer instance
    """
    return IntentRecognizer()