/**
 * Message Display for Todo AI Chatbot
 *
 * This module handles displaying AI responses in conversation format.
 */

class MessageDisplay {
    constructor() {
        this.messagesContainer = null;
        this.currentConversationId = null;
        this.displayedMessages = [];
    }

    /**
     * Initialize the message display component
     */
    init() {
        this.messagesContainer = document.getElementById('chat-messages');
        if (!this.messagesContainer) {
            console.warn('Chat messages container not found');
            return;
        }

        this.bindEvents();
    }

    /**
     * Bind events to handle message display
     */
    bindEvents() {
        // Listen for successful message sends to display responses
        document.addEventListener('messageSent', (event) => {
            this.handleResponse(event.detail.response, event.detail.conversationId);
        });

        // Listen for API responses to display AI replies
        document.addEventListener('apiResponse', (event) => {
            this.handleResponse(event.detail.data, event.detail.conversationId);
        });

        // Listen for system messages to display
        document.addEventListener('systemMessage', (event) => {
            this.addSystemMessage(event.detail.message);
        });

        // Listen for error messages
        document.addEventListener('messageError', (event) => {
            this.addErrorMessage(event.detail.error);
        });
    }

    /**
     * Handle an API response and display the AI message
     */
    handleResponse(response, conversationId) {
        if (!response) return;

        if (response.success && response.response) {
            // Add the AI response to the conversation
            this.addAIMessage(response.response, conversationId);

            // Update conversation ID if provided
            if (response.conversation_id) {
                this.currentConversationId = response.conversation_id;
            }
        } else if (!response.success && response.error) {
            this.addErrorMessage(response.error);
        }
    }

    /**
     * Add an AI message to the display
     */
    addAIMessage(message, conversationId = null) {
        const messageObj = {
            id: this.generateMessageId(),
            sender: 'ai',
            message: message,
            timestamp: new Date(),
            conversationId: conversationId || this.currentConversationId
        };

        this.displayedMessages.push(messageObj);
        this.renderMessage(messageObj);

        // Dispatch event for other components
        const event = new CustomEvent('aiMessageAdded', {
            detail: messageObj
        });
        document.dispatchEvent(event);
    }

    /**
     * Add a user message to the display
     */
    addUserMessage(message, conversationId = null) {
        const messageObj = {
            id: this.generateMessageId(),
            sender: 'user',
            message: message,
            timestamp: new Date(),
            conversationId: conversationId || this.currentConversationId
        };

        this.displayedMessages.push(messageObj);
        this.renderMessage(messageObj);

        // Dispatch event for other components
        const event = new CustomEvent('userMessageAdded', {
            detail: messageObj
        });
        document.dispatchEvent(event);
    }

    /**
     * Add a system message to the display
     */
    addSystemMessage(message) {
        const messageObj = {
            id: this.generateMessageId(),
            sender: 'system',
            message: message,
            timestamp: new Date(),
            conversationId: this.currentConversationId
        };

        this.displayedMessages.push(messageObj);
        this.renderMessage(messageObj, true); // System messages may have different styling

        // Dispatch event for other components
        const event = new CustomEvent('systemMessageAdded', {
            detail: messageObj
        });
        document.dispatchEvent(event);
    }

    /**
     * Add an error message to the display
     */
    addErrorMessage(errorMessage) {
        const messageObj = {
            id: this.generateMessageId(),
            sender: 'error',
            message: `Error: ${errorMessage}`,
            timestamp: new Date(),
            conversationId: this.currentConversationId
        };

        this.displayedMessages.push(messageObj);
        this.renderMessage(messageObj, true); // Error messages may have different styling

        // Dispatch event for other components
        const event = new CustomEvent('errorMessageAdded', {
            detail: messageObj
        });
        document.dispatchEvent(event);
    }

    /**
     * Render a message in the UI
     */
    renderMessage(messageObj, isSpecial = false) {
        if (!this.messagesContainer) return;

        const messageElement = document.createElement('div');
        messageElement.className = `message ${messageObj.sender}${isSpecial ? ' special' : ''}`;
        messageElement.dataset.messageId = messageObj.id;

        const timeString = messageObj.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageElement.innerHTML = `
            <div class="message-content">${this.formatMessageContent(messageObj.message)}</div>
            <div class="message-meta">
                ${timeString} - ${this.formatSenderName(messageObj.sender)}
            </div>
        `;

        this.messagesContainer.appendChild(messageElement);

        // Scroll to bottom to show the new message
        this.scrollToBottom();

        // Add fade-in animation
        setTimeout(() => {
            messageElement.style.opacity = '1';
            messageElement.style.transform = 'translateY(0)';
        }, 10);
    }

    /**
     * Format the message content for display (add any special formatting)
     */
    formatMessageContent(content) {
        // Escape HTML to prevent XSS
        const escapedContent = this.escapeHtml(content);

        // Format any special elements like lists, etc.
        return this.formatSpecialElements(escapedContent);
    }

    /**
     * Format special elements in the message
     */
    formatSpecialElements(content) {
        // Convert markdown-like lists to HTML
        let formattedContent = content.replace(/^(\d+)\.\s(.+)$/gm, '<div class="list-item">$1. $2</div>');
        formattedContent = formattedContent.replace(/^\-\s(.+)$/gm, '<div class="list-item">• $1</div>');

        // Convert bold text
        formattedContent = formattedContent.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convert italic text
        formattedContent = formattedContent.replace(/\*(.*?)\*/g, '<em>$1</em>');

        return formattedContent;
    }

    /**
     * Format sender name for display
     */
    formatSenderName(sender) {
        const nameMap = {
            'user': 'You',
            'ai': 'Todo Assistant',
            'system': 'System',
            'error': 'Error'
        };

        return nameMap[sender] || sender.charAt(0).toUpperCase() + sender.slice(1);
    }

    /**
     * Scroll to the bottom of the messages container
     */
    scrollToBottom() {
        if (this.messagesContainer) {
            this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
        }
    }

    /**
     * Clear all messages from the display
     */
    clearMessages() {
        if (this.messagesContainer) {
            this.messagesContainer.innerHTML = '';
        }
        this.displayedMessages = [];

        // Dispatch event for other components
        const event = new CustomEvent('messagesCleared');
        document.dispatchEvent(event);
    }

    /**
     * Load conversation history
     */
    async loadConversationHistory(conversationId) {
        this.currentConversationId = conversationId;

        // In a real implementation, this would fetch from an API
        // For now, we'll just clear and start fresh
        this.clearMessages();

        // Dispatch event for other components
        const event = new CustomEvent('conversationLoaded', {
            detail: { conversationId }
        });
        document.dispatchEvent(event);
    }

    /**
     * Get recent messages
     */
    getRecentMessages(count = 10) {
        return this.displayedMessages.slice(-count);
    }

    /**
     * Find a message by ID
     */
    getMessageById(messageId) {
        return this.displayedMessages.find(msg => msg.id === messageId);
    }

    /**
     * Update a message by ID
     */
    updateMessage(messageId, newContent) {
        const messageIndex = this.displayedMessages.findIndex(msg => msg.id === messageId);
        if (messageIndex !== -1) {
            this.displayedMessages[messageIndex].message = newContent;
            this.displayedMessages[messageIndex].timestamp = new Date();

            // Re-render the message
            const messageElement = document.querySelector(`[data-message-id="${messageId}"]`);
            if (messageElement) {
                const timeString = this.displayedMessages[messageIndex].timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                messageElement.innerHTML = `
                    <div class="message-content">${this.formatMessageContent(newContent)}</div>
                    <div class="message-meta">
                        ${timeString} - ${this.formatSenderName(this.displayedMessages[messageIndex].sender)}
                    </div>
                `;
            }
        }
    }

    /**
     * Generate a unique message ID
     */
    generateMessageId() {
        return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Get current conversation ID
     */
    getCurrentConversationId() {
        return this.currentConversationId;
    }

    /**
     * Get all displayed messages
     */
    getAllMessages() {
        return [...this.displayedMessages];
    }

    /**
     * Destroy the message display component
     */
    destroy() {
        // Clear references
        this.messagesContainer = null;
        this.displayedMessages = [];
    }
}

/**
 * Initialize the message display when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const messageDisplay = new MessageDisplay();
    messageDisplay.init();

    // Store instance globally for potential external access
    window.TodoMessageDisplay = messageDisplay;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = MessageDisplay;
}