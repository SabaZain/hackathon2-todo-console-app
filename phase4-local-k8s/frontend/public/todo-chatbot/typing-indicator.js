/**
 * Typing Indicator for Todo AI Chatbot
 *
 * This module handles showing typing indicators during AI processing.
 */

class TypingIndicator {
    constructor() {
        this.indicatorElement = null;
        this.isVisible = false;
        this.animationInterval = null;
        this.timeoutId = null;
        this.typingUsers = new Set();
    }

    /**
     * Initialize the typing indicator component
     */
    init() {
        this.createIndicator();
        this.bindEvents();
    }

    /**
     * Create the typing indicator element
     */
    createIndicator() {
        // Find the messages container
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) {
            console.error('Chat messages container not found for typing indicator');
            return;
        }

        // Create the typing indicator element
        this.indicatorElement = document.createElement('div');
        this.indicatorElement.id = 'typing-indicator';
        this.indicatorElement.className = 'typing-indicator';
        this.indicatorElement.style.display = 'none';
        this.indicatorElement.innerHTML = `
            <div class="typing-content">
                <div class="typing-text">Todo Assistant is typing</div>
                <div class="typing-dots">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                </div>
            </div>
        `;

        // Insert the indicator at the end of the messages container
        messagesContainer.appendChild(this.indicatorElement);
    }

    /**
     * Bind events to handle typing indicator display
     */
    bindEvents() {
        // Listen for message sending events
        document.addEventListener('messageSending', () => {
            this.show();
        });

        // Listen for message sent events to hide the indicator
        document.addEventListener('messageSent', () => {
            this.scheduleHide();
        });

        // Listen for API responses to hide the indicator
        document.addEventListener('apiResponse', () => {
            this.hide();
        });

        // Listen for error events to hide the indicator
        document.addEventListener('messageError', () => {
            this.hide();
        });

        // Listen for AI message events to hide the indicator
        document.addEventListener('aiMessageAdded', () => {
            this.hide();
        });
    }

    /**
     * Show the typing indicator
     */
    show() {
        if (!this.indicatorElement) return;

        // Clear any scheduled hide
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }

        // Show the indicator
        this.indicatorElement.style.display = 'flex';
        this.isVisible = true;

        // Start the dot animation
        this.startAnimation();

        // Dispatch event for other components
        const event = new CustomEvent('typingIndicatorShown', {
            detail: { timestamp: new Date().toISOString() }
        });
        document.dispatchEvent(event);
    }

    /**
     * Hide the typing indicator
     */
    hide() {
        if (!this.indicatorElement || !this.isVisible) return;

        // Stop the animation
        this.stopAnimation();

        // Hide the indicator
        this.indicatorElement.style.display = 'none';
        this.isVisible = false;

        // Dispatch event for other components
        const event = new CustomEvent('typingIndicatorHidden', {
            detail: { timestamp: new Date().toISOString() }
        });
        document.dispatchEvent(event);
    }

    /**
     * Schedule hiding of the typing indicator after a delay
     */
    scheduleHide(delay = 1000) {
        // Clear any existing timeout
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }

        // Set new timeout
        this.timeoutId = setTimeout(() => {
            this.hide();
        }, delay);
    }

    /**
     * Start the dot animation
     */
    startAnimation() {
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
        }

        // Create pulsing effect for dots
        let dotIndex = 0;
        this.animationInterval = setInterval(() => {
            const dots = this.indicatorElement.querySelectorAll('.dot');
            if (dots.length > 0) {
                // Reset all dots
                dots.forEach(dot => dot.style.opacity = '0.4');

                // Highlight current dot
                dots[dotIndex].style.opacity = '1';

                // Move to next dot
                dotIndex = (dotIndex + 1) % dots.length;
            }
        }, 500);
    }

    /**
     * Stop the dot animation
     */
    stopAnimation() {
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
            this.animationInterval = null;

            // Reset dots to default state
            const dots = this.indicatorElement.querySelectorAll('.dot');
            dots.forEach(dot => dot.style.opacity = '0.4');
        }
    }

    /**
     * Add a typing user
     */
    addTypingUser(userId, userName = 'Someone') {
        if (!this.typingUsers.has(userId)) {
            this.typingUsers.add(userId);

            // Update the typing text to show who is typing
            this.updateTypingText();
        }
    }

    /**
     * Remove a typing user
     */
    removeTypingUser(userId) {
        if (this.typingUsers.has(userId)) {
            this.typingUsers.delete(userId);

            // Update the typing text
            this.updateTypingText();

            // Hide if no one is typing anymore
            if (this.typingUsers.size === 0) {
                this.hide();
            }
        }
    }

    /**
     * Update the typing text based on who is typing
     */
    updateTypingText() {
        if (!this.indicatorElement) return;

        const typingTextElement = this.indicatorElement.querySelector('.typing-text');
        if (!typingTextElement) return;

        if (this.typingUsers.size === 0) {
            typingTextElement.textContent = '';
        } else if (this.typingUsers.size === 1) {
            typingTextElement.textContent = 'Todo Assistant is typing';
        } else if (this.typingUsers.size === 2) {
            typingTextElement.textContent = 'Todo Assistant and another user are typing';
        } else {
            typingTextElement.textContent = `Todo Assistant and ${this.typingUsers.size - 1} others are typing`;
        }
    }

    /**
     * Set custom typing text
     */
    setCustomText(text) {
        if (!this.indicatorElement) return;

        const typingTextElement = this.indicatorElement.querySelector('.typing-text');
        if (typingTextElement) {
            typingTextElement.textContent = text;
        }
    }

    /**
     * Check if the typing indicator is currently visible
     */
    isTyping() {
        return this.isVisible;
    }

    /**
     * Get typing users
     */
    getTypingUsers() {
        return Array.from(this.typingUsers);
    }

    /**
     * Clear all typing users
     */
    clearTypingUsers() {
        this.typingUsers.clear();
        this.updateTypingText();
    }

    /**
     * Set a timeout to automatically hide the indicator
     */
    setTimeout(duration = 10000) {
        // Clear existing timeout
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }

        // Set new timeout
        this.timeoutId = setTimeout(() => {
            this.hide();
        }, duration);
    }

    /**
     * Reset the typing indicator state
     */
    reset() {
        this.clearTypingUsers();
        this.hide();

        // Clear any timeouts
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
    }

    /**
     * Destroy the typing indicator component
     */
    destroy() {
        // Clear intervals and timeouts
        if (this.animationInterval) {
            clearInterval(this.animationInterval);
        }
        if (this.timeoutId) {
            clearTimeout(this.timeoutId);
        }

        // Remove the indicator element
        if (this.indicatorElement && this.indicatorElement.parentNode) {
            this.indicatorElement.parentNode.removeChild(this.indicatorElement);
        }

        // Clear references
        this.indicatorElement = null;
        this.typingUsers.clear();
    }
}

/**
 * Initialize the typing indicator when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const typingIndicator = new TypingIndicator();
    typingIndicator.init();

    // Store instance globally for potential external access
    window.TodoTypingIndicator = typingIndicator;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TypingIndicator;
}