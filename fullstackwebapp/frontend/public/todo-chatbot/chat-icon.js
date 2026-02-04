/**
 * Chat Icon Component for Todo AI Chatbot
 *
 * This module implements a floating chat icon that doesn't interfere with existing UI.
 */

class ChatIcon {
    constructor(containerId) {
        this.containerId = containerId;
        this.iconElement = null;
        this.isOpen = false;
    }

    /**
     * Initialize the chat icon component
     */
    init() {
        this.createIcon();
        this.bindEvents();
    }

    /**
     * Create the chat icon element
     */
    createIcon() {
        const container = document.getElementById(this.containerId);
        if (!container) {
            console.error(`Container with ID ${this.containerId} not found`);
            return;
        }

        this.iconElement = document.createElement('div');
        this.iconElement.id = 'todo-chat-icon';
        this.iconElement.className = 'todo-chat-icon';
        this.iconElement.innerHTML = `
            <button id="chat-toggle-btn" class="chat-icon-button" aria-label="Open chat">
                <span class="chat-icon">💬</span>
            </button>
        `;

        container.appendChild(this.iconElement);
    }

    /**
     * Bind event listeners to the chat icon
     */
    bindEvents() {
        const toggleBtn = document.getElementById('chat-toggle-btn');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
                this.toggleChatInterface();
            });
        }
    }

    /**
     * Toggle the chat interface visibility
     */
    toggleChatInterface() {
        this.isOpen = !this.isOpen;

        // Dispatch a custom event to communicate with other components
        const event = new CustomEvent('chatToggle', {
            detail: { isOpen: this.isOpen }
        });
        document.dispatchEvent(event);

        // Update UI state
        this.updateIconState();
    }

    /**
     * Update the icon's visual state based on open/close status
     */
    updateIconState() {
        if (this.iconElement) {
            const btn = this.iconElement.querySelector('.chat-icon-button');
            if (btn) {
                if (this.isOpen) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            }
        }
    }

    /**
     * Show the chat icon
     */
    show() {
        if (this.iconElement) {
            this.iconElement.style.display = 'block';
        }
    }

    /**
     * Hide the chat icon
     */
    hide() {
        if (this.iconElement) {
            this.iconElement.style.display = 'none';
        }
    }

    /**
     * Destroy the chat icon component
     */
    destroy() {
        if (this.iconElement && this.iconElement.parentNode) {
            this.iconElement.parentNode.removeChild(this.iconElement);
        }
    }
}

/**
 * Initialize the chat icon when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    // Only initialize if the container exists
    if (document.getElementById('todo-chat-container')) {
        const chatIcon = new ChatIcon('todo-chat-container');
        chatIcon.init();

        // Store instance globally for potential external access
        window.TodoChatIcon = chatIcon;
    }
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatIcon;
}