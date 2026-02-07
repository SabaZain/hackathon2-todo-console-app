"""
Stateless Handler for Todo AI Chatbot

This module ensures each API request is stateless and self-contained.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from .state_reconstructor import StateReconstructor
from .storage import StorageManager
from .retriever import Retriever
from .context_preserver import ContextPreserver
from .resumer import Resumer


class StatelessHandler:
    """
    Ensures each API request is stateless and self-contained by managing
    conversation state reconstruction on each request.
    """

    def __init__(
        self,
        state_reconstructor: StateReconstructor,
        storage_manager: StorageManager,
        retriever: Retriever,
        context_preserver: ContextPreserver,
        resumer: Resumer
    ):
        """
        Initialize the stateless handler.

        Args:
            state_reconstructor: Instance of StateReconstructor
            storage_manager: Instance of StorageManager
            retriever: Instance of Retriever
            context_preserver: Instance of ContextPreserver
            resumer: Instance of Resumer
        """
        self.state_reconstructor = state_reconstructor
        self.storage_manager = storage_manager
        self.retriever = retriever
        self.context_preserver = context_preserver
        self.resumer = resumer

    def handle_stateless_request(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Handle a stateless API request by reconstructing conversation state.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            user_message: The user's message
            additional_context: Additional context to include in the request

        Returns:
            Dictionary containing the response and updated state information
        """
        # Reconstruct full conversation state from persisted data
        conversation_state = self.state_reconstructor.reconstruct_conversation_state(
            user_id, conversation_id
        )

        # Check if conversation was interrupted and needs resuming
        resume_info = self.resumer.resume_conversation(
            user_id, conversation_id, user_message
        )

        # Prepare the complete request context
        request_context = {
            'conversation_state': conversation_state,
            'resume_info': resume_info,
            'additional_context': additional_context or {},
            'timestamp': datetime.now().isoformat(),
            'is_new_conversation': len(conversation_state['messages']) == 0
        }

        # Process the request (in a real implementation, this would involve calling
        # the AI agent and MCP tools)
        response = self._process_request(request_context)

        # Store the new messages in the database
        self._store_request_messages(user_id, conversation_id, user_message, response['ai_response'])

        # Update context preservation
        updated_context = self.context_preserver.preserve_context(
            user_id,
            conversation_id,
            {
                'role': 'user',
                'content': user_message,
                'timestamp': request_context['timestamp']
            },
            {
                'role': 'assistant',
                'content': response['ai_response'],
                'timestamp': datetime.now().isoformat()
            }
        )

        return {
            'response': response['ai_response'],
            'conversation_state': conversation_state,
            'request_context': request_context,
            'updated_context': updated_context,
            'success': True
        }

    def _process_request(self, request_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the request with the reconstructed state.

        Args:
            request_context: The complete request context

        Returns:
            Dictionary containing the AI response and processing information
        """
        # This is a placeholder for the actual AI processing
        # In a real implementation, this would call the AI agent with the context

        conversation_state = request_context['conversation_state']
        user_message = conversation_state['messages'][-1]['content'] if conversation_state['messages'] else ""

        # For demonstration purposes, return a simple response
        # In practice, this would involve calling the AI agent with full context
        ai_response = self._generate_response_with_context(
            user_message,
            conversation_state,
            request_context
        )

        return {
            'ai_response': ai_response,
            'processing_time': 0.1,  # Simulated processing time
            'tokens_used': len(user_message.split()) + len(ai_response.split())
        }

    def _generate_response_with_context(
        self,
        user_message: str,
        conversation_state: Dict[str, Any],
        request_context: Dict[str, Any]
    ) -> str:
        """
        Generate an AI response considering the full conversation context.

        Args:
            user_message: The user's message
            conversation_state: The reconstructed conversation state
            request_context: The full request context

        Returns:
            Generated AI response
        """
        # In a real implementation, this would call the actual AI agent
        # For this example, we'll simulate a response that considers context

        # Check if there's a greeting needed due to interruption
        resume_info = request_context['resume_info']
        greeting = ""
        if resume_info['was_interrupted']:
            greeting = self.resumer.handle_interruption_greeting(
                conversation_state['user_id'],
                conversation_state['conversation_id']
            ) + "\n\n"

        # Simulate AI response based on message content
        user_msg_lower = user_message.lower()

        if any(word in user_msg_lower for word in ['hello', 'hi', 'hey']):
            return greeting + "Hello! How can I help you with your tasks today?"
        elif any(word in user_msg_lower for word in ['add', 'create', 'new']):
            return greeting + "Sure, I can help you add a new task. What would you like to add?"
        elif any(word in user_msg_lower for word in ['list', 'show', 'display']):
            return greeting + "I'd be happy to show your tasks. Which tasks would you like to see?"
        elif any(word in user_msg_lower for word in ['update', 'change', 'modify']):
            return greeting + "I can help update a task. Which task would you like to modify?"
        elif any(word in user_msg_lower for word in ['complete', 'done', 'finish']):
            return greeting + "Which task would you like to mark as complete?"
        elif any(word in user_msg_lower for word in ['delete', 'remove']):
            return greeting + "Which task would you like to remove?"
        else:
            return greeting + f"I understand you said: '{user_message}'. How can I help you with your tasks?"

    def _store_request_messages(
        self,
        user_id: str,
        conversation_id: str,
        user_message: str,
        ai_response: str
    ):
        """
        Store the request messages in the database.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            user_message: The user's message
            ai_response: The AI's response
        """
        # Store user message
        self.storage_manager.store_message(
            user_id,
            conversation_id,
            'user',
            user_message
        )

        # Store AI response
        self.storage_manager.store_message(
            user_id,
            conversation_id,
            'assistant',
            ai_response
        )

    def validate_stateless_request(
        self,
        request_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Validate that a request has all required information to be stateless.

        Args:
            request_data: The request data to validate

        Returns:
            Dictionary containing validation results
        """
        required_fields = ['user_id', 'conversation_id', 'message']
        missing_fields = []

        for field in required_fields:
            if field not in request_data or request_data[field] is None:
                missing_fields.append(field)

        is_valid = len(missing_fields) == 0

        # Additional validation for user_id format
        user_id_valid = True
        if is_valid:
            user_id = request_data['user_id']
            if not isinstance(user_id, str) or len(user_id.strip()) == 0:
                user_id_valid = False
                missing_fields.append('user_id_format')

        # Additional validation for conversation_id format
        conversation_id_valid = True
        if is_valid:
            conversation_id = request_data['conversation_id']
            if not isinstance(conversation_id, str) or len(conversation_id.strip()) == 0:
                conversation_id_valid = False
                missing_fields.append('conversation_id_format')

        return {
            'is_valid': is_valid and user_id_valid and conversation_id_valid,
            'missing_fields': missing_fields,
            'user_id_valid': user_id_valid,
            'conversation_id_valid': conversation_id_valid,
            'validation_timestamp': datetime.now().isoformat()
        }

    def handle_batch_request(
        self,
        requests: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Handle multiple stateless requests in a batch.

        Args:
            requests: List of request dictionaries

        Returns:
            List of response dictionaries
        """
        responses = []

        for request in requests:
            # Validate each request individually
            validation = self.validate_stateless_request(request)

            if not validation['is_valid']:
                responses.append({
                    'success': False,
                    'error': f"Invalid request: missing fields {validation['missing_fields']}",
                    'request_id': request.get('request_id')
                })
                continue

            # Process the stateless request
            try:
                response = self.handle_stateless_request(
                    request['user_id'],
                    request['conversation_id'],
                    request['message'],
                    request.get('additional_context')
                )

                response['request_id'] = request.get('request_id')
                responses.append(response)
            except Exception as e:
                responses.append({
                    'success': False,
                    'error': str(e),
                    'request_id': request.get('request_id')
                })

        return responses

    def prepare_request_context(
        self,
        user_id: str,
        conversation_id: str,
        message: str,
        additional_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Prepare the full context for a stateless request.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID
            message: The user's message
            additional_context: Additional context to include

        Returns:
            Dictionary containing the complete request context
        """
        # Reconstruct conversation state
        conversation_state = self.state_reconstructor.reconstruct_conversation_state(
            user_id, conversation_id
        )

        # Get resume information if needed
        resume_info = self.resumer.resume_conversation(
            user_id, conversation_id, message
        )

        # Get context for continuation
        continuation_context = self.resumer.get_context_for_continuation(
            user_id, conversation_id
        )

        return {
            'user_id': user_id,
            'conversation_id': conversation_id,
            'message': message,
            'conversation_state': conversation_state,
            'resume_info': resume_info,
            'continuation_context': continuation_context,
            'additional_context': additional_context or {},
            'timestamp': datetime.now().isoformat()
        }

    def cleanup_request_resources(
        self,
        request_context: Dict[str, Any]
    ):
        """
        Cleanup any resources associated with a request.

        Args:
            request_context: The request context to cleanup
        """
        # In a real implementation, this might release locks, close connections, etc.
        # For this implementation, we'll just ensure context preservation
        user_id = request_context.get('user_id')
        conversation_id = request_context.get('conversation_id')

        if user_id and conversation_id:
            # Mark conversation as active to update its status
            self.resumer.mark_conversation_active(user_id, conversation_id)

    def get_request_efficiency_metrics(
        self,
        user_id: str,
        conversation_id: str
    ) -> Dict[str, Any]:
        """
        Get metrics about the efficiency of stateless request handling.

        Args:
            user_id: The user's ID
            conversation_id: The conversation ID

        Returns:
            Dictionary containing efficiency metrics
        """
        # Get conversation statistics
        stats = self.retriever.retrieve_conversation_statistics(user_id, conversation_id)

        # Calculate efficiency metrics
        total_messages = stats['message_count']
        if total_messages > 0:
            # Estimate state reconstruction overhead
            # In a real system, this would measure actual processing times
            avg_reconstruction_time_estimate = 0.05  # 50ms estimate
            total_estimated_overhead = avg_reconstruction_time_estimate * total_messages
        else:
            total_estimated_overhead = 0

        return {
            'total_messages': total_messages,
            'estimated_state_reconstruction_overhead_seconds': total_estimated_overhead,
            'average_overhead_per_message': total_estimated_overhead / total_messages if total_messages > 0 else 0,
            'messages_per_minute': stats['estimated_duration_minutes'] > 0 and stats['message_count'] / stats['estimated_duration_minutes'] or 0
        }


def get_stateless_handler(
    state_reconstructor: StateReconstructor,
    storage_manager: StorageManager,
    retriever: Retriever,
    context_preserver: ContextPreserver,
    resumer: Resumer
) -> StatelessHandler:
    """
    Get an instance of the stateless handler.

    Args:
        state_reconstructor: Instance of StateReconstructor
        storage_manager: Instance of StorageManager
        retriever: Instance of Retriever
        context_preserver: Instance of ContextPreserver
        resumer: Instance of Resumer

    Returns:
        StatelessHandler instance
    """
    return StatelessHandler(
        state_reconstructor,
        storage_manager,
        retriever,
        context_preserver,
        resumer
    )