/**
 * Message Sender for Todo AI Chatbot
 *
 * This module handles sending user messages to the backend API.
 */

class MessageSender {
    constructor(apiBaseUrl = '/api') {
        this.apiBaseUrl = apiBaseUrl;
        this.isSending = false;
        this.retryAttempts = 3;
        this.pendingMessages = [];
    }

    /**
     * Initialize the message sender
     */
    init() {
        this.bindEvents();
    }

    /**
     * Bind events to handle message sending
     */
    bindEvents() {
        // Listen for messages to send from the chat interface
        document.addEventListener('sendMessage', async (event) => {
            await this.sendMessage(event.detail.message);
        });

        // Listen for connection status changes
        document.addEventListener('connectionStatusChange', (event) => {
            if (event.detail.connected && this.pendingMessages.length > 0) {
                this.processPendingMessages();
            }
        });
    }

    /**
     * Send a message to the backend API
     */
    async sendMessage(message, userId = null, conversationId = null) {
        if (this.isSending) {
            // Queue the message if we're already sending
            this.pendingMessages.push({ message, userId, conversationId });
            return;
        }

        this.isSending = true;

        try {
            // Get user ID if not provided
            if (!userId) {
                userId = this.getCurrentUserId();
            }

            // Prepare the request payload
            const payload = {
                message: message,
                ...(conversationId && { conversation_id: conversationId })
            };

            // Dispatch event to indicate sending has started
            const sendingEvent = new CustomEvent('messageSending', {
                detail: { message, timestamp: new Date().toISOString() }
            });
            document.dispatchEvent(sendingEvent);

            // Make the API request
            const response = await this.makeApiRequest(userId, payload);

            // Handle the response
            if (response.success) {
                // Dispatch event for successful sending
                const successEvent = new CustomEvent('messageSent', {
                    detail: {
                        message,
                        response: response,
                        conversationId: response.conversation_id,
                        timestamp: new Date().toISOString()
                    }
                });
                document.dispatchEvent(successEvent);

                // Process any pending messages
                if (this.pendingMessages.length > 0) {
                    await this.processPendingMessages();
                }
            } else {
                throw new Error(response.error || 'Failed to send message');
            }

            return response;
        } catch (error) {
            console.error('Error sending message:', error);

            // Dispatch error event
            const errorEvent = new CustomEvent('messageError', {
                detail: {
                    message,
                    error: error.message,
                    timestamp: new Date().toISOString()
                }
            });
            document.dispatchEvent(errorEvent);

            // Add to pending messages if it's a connection issue
            if (this.isConnectionIssue(error)) {
                this.pendingMessages.unshift({ message, userId, conversationId });

                // Dispatch offline event
                const offlineEvent = new CustomEvent('connectionLost', {
                    detail: { reason: error.message }
                });
                document.dispatchEvent(offlineEvent);
            }

            return { success: false, error: error.message };
        } finally {
            this.isSending = false;
        }
    }

    /**
     * Make the actual API request
     */
    async makeApiRequest(userId, payload) {
        const url = `${this.apiBaseUrl}/${userId}/chat`;

        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...this.getAuthHeaders()
            },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        return await response.json();
    }

    /**
     * Process pending messages
     */
    async processPendingMessages() {
        while (this.pendingMessages.length > 0 && !this.isSending) {
            const { message, userId, conversationId } = this.pendingMessages.shift();

            // Add slight delay between messages to avoid overwhelming the server
            await new Promise(resolve => setTimeout(resolve, 500));

            await this.sendMessage(message, userId, conversationId);
        }
    }

    /**
     * Get current user ID (implement based on your auth system)
     */
    getCurrentUserId() {
        // This is a placeholder - implement based on your authentication system
        // For example, it might read from localStorage, cookies, or a global variable
        return localStorage.getItem('todo_user_id') || 'anonymous';
    }

    /**
     * Get authentication headers
     */
    getAuthHeaders() {
        // This is a placeholder - implement based on your auth system
        const token = localStorage.getItem('auth_token');
        if (token) {
            return { 'Authorization': `Bearer ${token}` };
        }
        return {};
    }

    /**
     * Check if an error indicates a connection issue
     */
    isConnectionIssue(error) {
        const errorMessage = error.message.toLowerCase();
        return errorMessage.includes('network') ||
               errorMessage.includes('fetch') ||
               errorMessage.includes('connection') ||
               errorMessage.includes('timeout') ||
               error instanceof TypeError; // Network errors often result in TypeError
    }

    /**
     * Retry sending failed messages
     */
    async retryFailedMessages() {
        if (this.pendingMessages.length === 0) return;

        const originalPending = [...this.pendingMessages];
        this.pendingMessages = [];

        for (const msgData of originalPending) {
            await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second between retries
            await this.sendMessage(msgData.message, msgData.userId, msgData.conversationId);
        }
    }

    /**
     * Clear all pending messages
     */
    clearPendingMessages() {
        this.pendingMessages = [];
    }

    /**
     * Get the number of pending messages
     */
    getPendingMessageCount() {
        return this.pendingMessages.length;
    }

    /**
     * Check if there are pending messages
     */
    hasPendingMessages() {
        return this.pendingMessages.length > 0;
    }

    /**
     * Get API status
     */
    async checkApiStatus(userId) {
        try {
            const response = await fetch(`${this.apiBaseUrl}/${userId}/health`, {
                method: 'GET',
                headers: this.getAuthHeaders()
            });

            return response.ok;
        } catch (error) {
            return false;
        }
    }

    /**
     * Destroy the message sender
     */
    destroy() {
        // Clear any pending timeouts or intervals
        this.clearPendingMessages();
    }
}

/**
 * Initialize the message sender when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const messageSender = new MessageSender();
    messageSender.init();

    // Store instance globally for potential external access
    window.TodoMessageSender = messageSender;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessageSender;
}