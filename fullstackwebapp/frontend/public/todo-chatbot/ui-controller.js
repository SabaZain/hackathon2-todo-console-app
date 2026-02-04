/**
 * UI Controller for Todo AI Chatbot
 *
 * This module handles opening/closing of chat interface functionality.
 */

class UIController {
    constructor() {
        this.chatIcon = null;
        this.chatInterface = null;
        this.isOpen = false;

        // State management
        this.state = {
            isVisible: false,
            isMinimized: false,
            isAnimating: false
        };
    }

    /**
     * Initialize the UI controller
     */
    init() {
        this.bindEvents();
        this.setupKeyboardShortcuts();
    }

    /**
     * Bind global UI events
     */
    bindEvents() {
        // Listen for chat toggle events
        document.addEventListener('chatToggle', (event) => {
            if (event.detail.isOpen) {
                this.openChat();
            } else {
                this.closeChat();
            }
        });

        // Listen for global keyboard shortcuts
        document.addEventListener('keydown', (event) => {
            // ESC to close chat
            if (event.key === 'Escape' && this.state.isVisible) {
                this.closeChat();
            }
        });

        // Listen for clicks outside the chat to close it
        document.addEventListener('click', (event) => {
            if (this.state.isVisible &&
                !event.target.closest('#todo-chat-interface') &&
                !event.target.closest('#todo-chat-icon')) {

                // Don't close if clicking on other interactive elements
                if (!event.target.closest('button, input, textarea, select, a')) {
                    this.closeChat();
                }
            }
        });

        // Listen for resize events to handle responsive adjustments
        window.addEventListener('resize', () => {
            this.handleResize();
        });

        // Listen for orientation changes on mobile devices
        window.addEventListener('orientationchange', () => {
            setTimeout(() => {
                this.handleResize();
            }, 100);
        });
    }

    /**
     * Setup keyboard shortcuts
     */
    setupKeyboardShortcuts() {
        // Ctrl/Cmd + Shift + C to toggle chat
        document.addEventListener('keydown', (event) => {
            if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() === 'c') {
                event.preventDefault();
                this.toggleChat();
            }
        });
    }

    /**
     * Open the chat interface
     */
    openChat() {
        if (this.state.isAnimating) return;

        this.state.isAnimating = true;
        this.state.isVisible = true;
        this.state.isMinimized = false;

        // Show the chat interface with animation
        this.animateIn(() => {
            this.state.isAnimating = false;

            // Dispatch event for other components
            const event = new CustomEvent('chatOpened', {
                detail: { timestamp: new Date().toISOString() }
            });
            document.dispatchEvent(event);
        });

        this.isOpen = true;
    }

    /**
     * Close the chat interface
     */
    closeChat() {
        if (this.state.isAnimating) return;

        this.state.isAnimating = true;

        // Hide the chat interface with animation
        this.animateOut(() => {
            this.state.isVisible = false;
            this.state.isAnimating = false;

            // Dispatch event for other components
            const event = new CustomEvent('chatClosed', {
                detail: { timestamp: new Date().toISOString() }
            });
            document.dispatchEvent(event);
        });

        this.isOpen = false;
    }

    /**
     * Toggle the chat interface open/close state
     */
    toggleChat() {
        if (this.state.isVisible) {
            this.closeChat();
        } else {
            this.openChat();
        }
    }

    /**
     * Minimize the chat interface
     */
    minimizeChat() {
        if (!this.state.isVisible || this.state.isAnimating) return;

        this.state.isMinimized = true;
        this.state.isAnimating = true;

        const interfaceEl = document.getElementById('todo-chat-interface');
        if (interfaceEl) {
            interfaceEl.style.height = 'auto';
            interfaceEl.style.overflow = 'hidden';
            interfaceEl.querySelector('.chat-messages-container').style.display = 'none';
            interfaceEl.querySelector('.chat-input-container').style.display = 'none';
        }

        this.state.isAnimating = false;

        // Dispatch event for other components
        const event = new CustomEvent('chatMinimized', {
            detail: { timestamp: new Date().toISOString() }
        });
        document.dispatchEvent(event);
    }

    /**
     * Maximize the chat interface
     */
    maximizeChat() {
        if (!this.state.isVisible || this.state.isAnimating || !this.state.isMinimized) return;

        this.state.isMinimized = false;
        this.state.isAnimating = true;

        const interfaceEl = document.getElementById('todo-chat-interface');
        if (interfaceEl) {
            interfaceEl.style.height = '';
            interfaceEl.style.overflow = '';
            interfaceEl.querySelector('.chat-messages-container').style.display = '';
            interfaceEl.querySelector('.chat-input-container').style.display = '';
        }

        this.state.isAnimating = false;

        // Dispatch event for other components
        const event = new CustomEvent('chatMaximized', {
            detail: { timestamp: new Date().toISOString() }
        });
        document.dispatchEvent(event);
    }

    /**
     * Animate the chat interface in (show)
     */
    animateIn(callback) {
        const interfaceEl = document.getElementById('todo-chat-interface');
        if (!interfaceEl) {
            if (callback) callback();
            return;
        }

        // Initial state for animation
        interfaceEl.style.opacity = '0';
        interfaceEl.style.transform = 'translateY(20px) scale(0.95)';
        interfaceEl.style.display = 'block';

        // Trigger reflow
        void interfaceEl.offsetWidth;

        // Apply animation
        interfaceEl.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        interfaceEl.style.opacity = '1';
        interfaceEl.style.transform = 'translateY(0) scale(1)';

        // Call callback after animation
        setTimeout(() => {
            if (callback) callback();
        }, 300);
    }

    /**
     * Animate the chat interface out (hide)
     */
    animateOut(callback) {
        const interfaceEl = document.getElementById('todo-chat-interface');
        if (!interfaceEl) {
            if (callback) callback();
            return;
        }

        // Apply animation
        interfaceEl.style.transition = 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)';
        interfaceEl.style.opacity = '0';
        interfaceEl.style.transform = 'translateY(20px) scale(0.95)';

        // Hide after animation
        setTimeout(() => {
            interfaceEl.style.display = 'none';
            if (callback) callback();
        }, 200);
    }

    /**
     * Handle window resize events for responsive adjustments
     */
    handleResize() {
        // Adjust positioning based on viewport size
        const interfaceEl = document.getElementById('todo-chat-interface');
        const iconEl = document.getElementById('todo-chat-icon');

        if (window.innerWidth < 768) {
            // Mobile adjustments
            if (interfaceEl) {
                interfaceEl.style.bottom = '70px';
                interfaceEl.style.right = '10px';
                interfaceEl.style.left = '10px';
                interfaceEl.style.width = 'calc(100% - 20px)';
            }

            if (iconEl) {
                iconEl.style.bottom = '15px';
                iconEl.style.right = '15px';
            }
        } else {
            // Desktop adjustments
            if (interfaceEl) {
                interfaceEl.style.bottom = '90px';
                interfaceEl.style.right = '20px';
                interfaceEl.style.left = '';
                interfaceEl.style.width = '400px';
            }

            if (iconEl) {
                iconEl.style.bottom = '20px';
                iconEl.style.right = '20px';
            }
        }
    }

    /**
     * Check if chat is currently open
     */
    isChatOpen() {
        return this.state.isVisible && !this.state.isMinimized;
    }

    /**
     * Get current UI state
     */
    getState() {
        return { ...this.state };
    }

    /**
     * Focus on the chat input field
     */
    focusInput() {
        const inputField = document.getElementById('chat-input');
        if (inputField && this.state.isVisible) {
            setTimeout(() => inputField.focus(), 100);
        }
    }

    /**
     * Destroy the UI controller
     */
    destroy() {
        // Clean up event listeners
        document.removeEventListener('keydown', this.handleKeyDown);
        window.removeEventListener('resize', this.handleResize);
        window.removeEventListener('orientationchange', this.handleOrientationChange);
    }
}

/**
 * Initialize the UI controller when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const uiController = new UIController();
    uiController.init();

    // Store instance globally for potential external access
    window.TodoUIController = uiController;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIController;
}