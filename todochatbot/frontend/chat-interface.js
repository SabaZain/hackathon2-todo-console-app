/**
 * Chat Interface Component for Todo AI Chatbot
 *
 * This module implements the modal/chat interface with message history display.
 */

class ChatInterface {
    constructor(containerId) {
        this.containerId = containerId;
        this.interfaceElement = null;
        this.isOpen = false;
        this.messages = [];
    }

    /**
     * Initialize the chat interface component
     */
    init() {
        this.createInterface();
        this.bindEvents();
        this.hide(); // Start hidden
    }

    /**
     * Create the chat interface element
     */
    createInterface() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`Container with ID ${this.containerId} not found`);
            return;
        }

        this.interfaceElement = document.createElement('div');
        this.interfaceElement.id = 'todo-chat-interface';
        this.interfaceElement.className = 'todo-chat-interface';
        this.interfaceElement.innerHTML = `
            <div class="chat-modal">
                <div class="chat-header">
                    <h3>Todo Assistant</h3>
                    <button id="close-chat-btn" class="close-btn" aria-label="Close chat">&times;</button>
                </div>
                <div class="chat-messages-container">
                    <div id="chat-messages" class="chat-messages"></div>
                    <div id="typing-indicator" class="typing-indicator" style="display: none;">
                        <span>AI is typing...</span>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input
                        type="text"
                        id="chat-input"
                        class="chat-input"
                        placeholder="Type your message..."
                        autocomplete="off"
                    >
                    <button id="send-message-btn" class="send-btn" aria-label="Send message">
                        <span>➤</span>
                    </button>
                </div>
            </div>
        `;

        container.appendChild(this.interfaceElement);
    }

    /**
     * Bind event listeners to the chat interface
     */
    bindEvents() {
        // Close button
        const closeBtn = document.getElementById('close-chat-btn');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                this.close();
            });
        }

        // Send message button
        const sendBtn = document.getElementById('send-message-btn');
        if (sendBtn) {
            sendBtn.addEventListener('click', () => {
                this.sendMessage();
            });
        }

        // Input field (Enter key)
        const inputField = document.getElementById('chat-input');
        if (inputField) {
            inputField.addEventListener('keypress', (event) => {
                if (event.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }

        // Listen for chat toggle events from the icon
        document.addEventListener('chatToggle', (event) => {
            if (event.detail.isOpen) {
                this.open();
            } else {
                this.close();
            }
        });
    }

    /**
     * Open the chat interface
     */
    open() {
        this.isOpen = true;
        this.show();

        // Focus on input field when opened
        const inputField = document.getElementById('chat-input');
        if (inputField) {
            setTimeout(() => inputField.focus(), 100);
        }
    }

    /**
     * Close the chat interface
     */
    close() {
        this.isOpen = false;
        this.hide();
    }

    /**
     * Show the chat interface
     */
    show() {
        if (this.interfaceElement) {
            this.interfaceElement.style.display = 'block';
        }
    }

    /**
     * Hide the chat interface
     */
    hide() {
        if (this.interfaceElement) {
            this.interfaceElement.style.display = 'none';
        }
    }

    /**
     * Add a message to the chat history
     */
    addMessage(sender, message, timestamp = new Date()) {
        this.messages.push({
            sender,
            message,
            timestamp
        });

        this.renderMessages();
    }

    /**
     * Render all messages in the chat interface
     */
    renderMessages() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;

        messagesContainer.innerHTML = '';

        this.messages.forEach((msg, index) => {
            const messageElement = document.createElement('div');
            messageElement.className = `message ${msg.sender}`;

            const timeString = msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

            messageElement.innerHTML = `
                <div class="message-content">${this.escapeHtml(msg.message)}</div>
                <div class="message-meta">${timeString} - ${msg.sender}</div>
            `;

            messagesContainer.appendChild(messageElement);
        });

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    /**
     * Show typing indicator
     */
    showTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'block';
        }
    }

    /**
     * Hide typing indicator
     */
    hideTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.style.display = 'none';
        }
    }

    /**
     * Send message to backend
     */
    sendMessage() {
        const inputField = document.getElementById('chat-input');
        if (!inputField || !inputField.value.trim()) return;

        const message = inputField.value.trim();

        // Add user message to UI
        this.addMessage('user', message);

        // Clear input
        inputField.value = '';

        // Dispatch event to be handled by message sender
        const event = new CustomEvent('sendMessage', {
            detail: { message: message }
        });
        document.dispatchEvent(event);
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
     * Destroy the chat interface component
     */
    destroy() {
        if (this.interfaceElement && this.interfaceElement.parentNode) {
            this.interfaceElement.parentNode.removeChild(this.interfaceElement);
        }
    }
}

/**
 * Initialize the chat interface when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if the container exists
    if (document.getElementById('todo-chat-container')) {
        const chatInterface = new ChatInterface('todo-chat-container');
        chatInterface.init();

        // Store instance globally for potential external access
        window.TodoChatInterface = chatInterface;
    }
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatInterface;
}