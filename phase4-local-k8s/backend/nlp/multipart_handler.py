"""
Multi-part Handler for Todo AI Chatbot

This module handles multi-part task creation like "Add a task to buy groceries tomorrow".
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import re


class MultiPartHandler:
    """Handles multi-part task creation and information collection."""

    def __init__(self):
        """Initialize the multi-part handler."""
        self.active_sessions = {}  # Stores ongoing multi-part interactions
        self.session_timeout = 600  # 10 minutes in seconds

    def process_multistep_request(self, user_input: str, user_id: str, conversation_id: str) -> Dict[str, Any]:
        """
        Process a potentially multi-part request.

        Args:
            user_input: The user's current input
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary with the response and next step information
        """
        session_key = f"{user_id}:{conversation_id}"

        # Check if this is a continuation of an existing multi-part session
        if session_key in self.active_sessions:
            return self._continue_session(session_key, user_input)

        # Check if this initiates a new multi-part session
        initiation_result = self._check_for_initiation(user_input)
        if initiation_result['is_initiating']:
            return self._start_new_session(session_key, user_input, initiation_result)

        # Otherwise, treat as single-part
        return {
            'is_complete': True,
            'action': 'process_single',
            'extracted_data': initiation_result['extracted_data'],
            'message': 'Task processed directly.'
        }

    def _check_for_initiation(self, user_input: str) -> Dict[str, Any]:
        """
        Check if the input starts a multi-part process.

        Args:
            user_input: The user's input

        Returns:
            Dictionary indicating if initiation occurred and extracted data
        """
        lower_input = user_input.lower()

        # Look for multi-part patterns that require additional information
        patterns = {
            'add_task_with_details': r'\b(add|create|make)\s+a?\s*(task|todo|to-do|item)\s+(to|for|about)\s+(?P<action>[^.!?]+)$',
            'update_task_details': r'\b(update|change|modify|edit)\s+(?P<task_ref>the|a)\s+(task|todo|to-do|item)\s+(?P<action>[^.!?]+)$',
            'incomplete_request': r'\b(remind\s+me|need\s+to|should\s+)(?P<action>[^.!?]+)$'
        }

        for pattern_name, pattern in patterns.items():
            match = re.search(pattern, lower_input)
            if match:
                extracted_data = {
                    'action': match.group('action').strip() if 'action' in match.groupdict() else '',
                    'task_ref': match.group('task_ref').strip() if 'task_ref' in match.groupdict() else None,
                    'pattern': pattern_name
                }

                # Check if the extracted action seems incomplete
                if self._is_incomplete_action(extracted_data['action']):
                    return {
                        'is_initiating': True,
                        'extracted_data': extracted_data,
                        'missing_info': self._determine_missing_info(extracted_data['action'])
                    }

        # If no multi-part pattern matched, extract what we can directly
        return {
            'is_initiating': False,
            'extracted_data': self._extract_basic_info(user_input)
        }

    def _is_incomplete_action(self, action_text: str) -> bool:
        """
        Determine if an action seems incomplete.

        Args:
            action_text: The action text to check

        Returns:
            Boolean indicating if the action is incomplete
        """
        if not action_text:
            return True

        # Actions that typically need more information
        incomplete_indicators = [
            'buy', 'purchase', 'get', 'go', 'visit', 'call', 'email',
            'schedule', 'plan', 'prepare', 'organize', 'arrange'
        ]

        words = action_text.lower().split()
        return any(indicator in words for indicator in incomplete_indicators)

    def _determine_missing_info(self, action_text: str) -> List[str]:
        """
        Determine what information is missing from an action.

        Args:
            action_text: The action text to analyze

        Returns:
            List of missing information types
        """
        missing_info = []

        # Check for missing location
        location_keywords = ['buy', 'purchase', 'get', 'go', 'visit']
        if any(keyword in action_text.lower() for keyword in location_keywords):
            missing_info.append('location')

        # Check for missing date/time
        if any(keyword in action_text.lower() for keyword in ['buy', 'visit', 'call', 'go', 'attend']):
            missing_info.append('timeframe')

        # Check for missing details
        if any(keyword in action_text.lower() for keyword in ['call', 'email', 'message']):
            missing_info.append('contact_details')

        # If no specific missing info identified, default to needing more details
        if not missing_info:
            missing_info.append('details')

        return missing_info

    def _extract_basic_info(self, user_input: str) -> Dict[str, Any]:
        """
        Extract basic information from a user input.

        Args:
            user_input: The user's input

        Returns:
            Dictionary with extracted basic information
        """
        # This is a simplified extraction - in a real implementation,
        # this would use more sophisticated NLP
        return {
            'raw_input': user_input,
            'text': user_input,
            'detected_action': self._detect_action(user_input),
            'contains_date': bool(re.search(r'\b(today|tomorrow|yesterday|next\s+\w+|\d{1,2}/\d{1,2}|\d{4}-\d{2}-\d{2})\b', user_input.lower())),
            'contains_priority': bool(re.search(r'\b(urgent|important|high|low|asap)\b', user_input.lower()))
        }

    def _detect_action(self, user_input: str) -> str:
        """
        Detect the main action in the user input.

        Args:
            user_input: The user's input

        Returns:
            Detected action string
        """
        lower_input = user_input.lower()

        if any(word in lower_input for word in ['add', 'create', 'make', 'new']):
            return 'create'
        elif any(word in lower_input for word in ['update', 'change', 'modify', 'edit']):
            return 'update'
        elif any(word in lower_input for word in ['delete', 'remove', 'erase', 'cancel']):
            return 'delete'
        elif any(word in lower_input for word in ['complete', 'finish', 'done', 'accomplish']):
            return 'complete'
        elif any(word in lower_input for word in ['list', 'show', 'display', 'view']):
            return 'list'
        else:
            return 'unknown'

    def _start_new_session(self, session_key: str, user_input: str, initiation_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Start a new multi-part session.

        Args:
            session_key: The session identifier
            user_input: The user's initial input
            initiation_result: Result from initiation check

        Returns:
            Dictionary with session information
        """
        session_data = {
            'created_at': datetime.now().timestamp(),
            'initial_input': user_input,
            'extracted_data': initiation_result['extracted_data'],
            'missing_info': initiation_result['missing_info'],
            'collected_info': {},
            'current_request': 'details'  # What we're asking for now
        }

        self.active_sessions[session_key] = session_data

        # Generate appropriate request for missing information
        request_message = self._generate_request_message(initiation_result['missing_info'])

        return {
            'is_complete': False,
            'action': 'request_more_info',
            'session_active': True,
            'request_message': request_message,
            'missing_info_types': initiation_result['missing_info']
        }

    def _continue_session(self, session_key: str, user_input: str) -> Dict[str, Any]:
        """
        Continue an existing multi-part session.

        Args:
            session_key: The session identifier
            user_input: The user's input to continue the session

        Returns:
            Dictionary with session continuation information
        """
        session_data = self.active_sessions[session_key]

        # Update collected info with the new input
        # In a real implementation, this would use proper NLP to extract specific details
        if session_data['current_request'] == 'details':
            session_data['collected_info']['details'] = user_input

        # Check if we have all needed information now
        if self._session_complete(session_data):
            # Session is complete, process the full task
            return self._finalize_session(session_key)
        else:
            # Still need more information
            remaining_info = [info for info in session_data['missing_info']
                             if info not in session_data['collected_info']]
            request_message = self._generate_request_message(remaining_info)

            return {
                'is_complete': False,
                'action': 'request_more_info',
                'session_active': True,
                'request_message': request_message,
                'missing_info_types': remaining_info
            }

    def _session_complete(self, session_data: Dict[str, Any]) -> bool:
        """
        Check if the session has collected all needed information.

        Args:
            session_data: The session data

        Returns:
            Boolean indicating if session is complete
        """
        # Check if all missing info has been collected
        for info_type in session_data['missing_info']:
            if info_type not in session_data['collected_info']:
                return False
        return True

    def _finalize_session(self, session_key: str) -> Dict[str, Any]:
        """
        Finalize a multi-part session and return complete data.

        Args:
            session_key: The session identifier

        Returns:
            Dictionary with final data and completion message
        """
        session_data = self.active_sessions[session_key]

        # Combine initial extracted data with collected info
        final_data = {
            **session_data['extracted_data'],
            **session_data['collected_info'],
            'full_completion': True
        }

        # Clean up session
        del self.active_sessions[session_key]

        return {
            'is_complete': True,
            'action': 'process_combined',
            'extracted_data': final_data,
            'message': 'Multi-part task created successfully.'
        }

    def _generate_request_message(self, missing_info_types: List[str]) -> str:
        """
        Generate a message asking for missing information.

        Args:
            missing_info_types: List of missing information types

        Returns:
            Request message string
        """
        if 'location' in missing_info_types:
            return "Where would you like to do this? For example, 'at the store' or 'at home'."
        elif 'timeframe' in missing_info_types:
            return "When would you like to do this? For example, 'tomorrow', 'next week', or 'by Friday'."
        elif 'contact_details' in missing_info_types:
            return "What are the contact details? For example, phone number or email address."
        else:
            return "Could you provide more details about what you need to do?"

    def cleanup_expired_sessions(self):
        """
        Clean up any sessions that have expired.
        """
        current_time = datetime.now().timestamp()
        expired_keys = []

        for session_key, session_data in self.active_sessions.items():
            if current_time - session_data['created_at'] > self.session_timeout:
                expired_keys.append(session_key)

        for key in expired_keys:
            del self.active_sessions[key]

    def get_session_status(self, session_key: str) -> Optional[Dict[str, Any]]:
        """
        Get the status of a specific session.

        Args:
            session_key: The session identifier

        Returns:
            Session status dictionary or None if not found
        """
        if session_key in self.active_sessions:
            return self.active_sessions[session_key]
        return None

    def cancel_session(self, session_key: str) -> bool:
        """
        Cancel a multi-part session.

        Args:
            session_key: The session identifier

        Returns:
            Boolean indicating if cancellation was successful
        """
        if session_key in self.active_sessions:
            del self.active_sessions[session_key]
            return True
        return False

    def get_active_sessions_count(self) -> int:
        """
        Get the number of active multi-part sessions.

        Returns:
            Count of active sessions
        """
        self.cleanup_expired_sessions()  # Clean up before counting
        return len(self.active_sessions)


def get_multip_part_handler() -> MultiPartHandler:
    """
    Get an instance of the multi-part handler.

    Returns:
        MultiPartHandler instance
    """
    return MultiPartHandler()