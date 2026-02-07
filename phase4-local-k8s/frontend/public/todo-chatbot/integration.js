/**
 * Integration Module for Todo AI Chatbot
 *
 * This module handles embedding the chat widget into existing Todo application layout
 * without interfering with existing functionality.
 */

class ChatWidgetIntegration {
    constructor() {
        this.widgetContainer = null;
        this.originalLayoutState = {};
        this.integrationComplete = false;
    }

    /**
     * Initialize the integration
     */
    init() {
        this.detectLayout();
        this.prepareContainer();
        this.bindEvents();

        // Check if integration should proceed
        if (this.shouldIntegrate()) {
            this.integrate();
        }
    }

    /**
     * Detect the current page layout and elements
     */
    detectLayout() {
        // Identify the main content area
        this.mainContentArea = document.querySelector('main') ||
                              document.querySelector('.main-content') ||
                              document.querySelector('#main') ||
                              document.body;

        // Identify header if present
        this.headerElement = document.querySelector('header') ||
                            document.querySelector('.header') ||
                            document.querySelector('#header');

        // Identify navigation if present
        this.navElement = document.querySelector('nav') ||
                         document.querySelector('.navigation') ||
                         document.querySelector('.nav');

        // Store original layout properties
        this.storeOriginalLayout();
    }

    /**
     * Store the original layout state before integration
     */
    storeOriginalLayout() {
        if (this.mainContentArea) {
            this.originalLayoutState.mainContent = {
                className: this.mainContentArea.className,
                style: this.mainContentArea.getAttribute('style') || '',
                position: this.mainContentArea.getBoundingClientRect()
            };
        }

        if (this.headerElement) {
            this.originalLayoutState.header = {
                className: this.headerElement.className,
                style: this.headerElement.getAttribute('style') || ''
            };
        }
    }

    /**
     * Prepare the container for the chat widget
     */
    prepareContainer() {
        // Create or identify the container for our chat widget
        let container = document.getElementById('todo-chat-container');

        if (!container) {
            // Create a container if it doesn't exist
            container = document.createElement('div');
            container.id = 'todo-chat-container';

            // Add it to the body to ensure it doesn't interfere with existing layout
            document.body.appendChild(container);
        }

        this.widgetContainer = container;

        // Add basic positioning styles without affecting existing layout
        Object.assign(this.widgetContainer.style, {
            'position': 'relative',
            'zIndex': '999',
            'pointerEvents': 'none' // Initially don't intercept clicks
        });
    }

    /**
     * Check if integration should proceed
     */
    shouldIntegrate() {
        // Only integrate on pages that seem to be part of the Todo app
        const pathname = window.location.pathname.toLowerCase();

        // Common paths for Todo application
        const todoPaths = ['/todo', '/todos', '/tasks', '/dashboard', '/', '/app'];

        return todoPaths.some(path => pathname.includes(path));
    }

    /**
     * Perform the integration
     */
    integrate() {
        if (this.integrationComplete) return;

        // Add our widget elements without disrupting existing layout
        this.addStyles();
        this.addAccessibilityFeatures();

        // Make container interactive
        if (this.widgetContainer) {
            this.widgetContainer.style.pointerEvents = 'auto';
        }

        // Notify that integration is complete
        this.integrationComplete = true;

        // Dispatch event for other components
        const event = new CustomEvent('widgetIntegrated', {
            detail: {
                timestamp: new Date().toISOString(),
                containerId: this.widgetContainer?.id
            }
        });
        document.dispatchEvent(event);
    }

    /**
     * Add necessary styles without conflicting with existing styles
     */
    addStyles() {
        // Create a unique style element to avoid conflicts
        const styleId = 'todo-chat-widget-styles';

        if (!document.getElementById(styleId)) {
            const style = document.createElement('style');
            style.id = styleId;
            style.type = 'text/css';
            style.textContent = `
                /* Namespace all styles to prevent conflicts */
                .todo-chat-icon, .todo-chat-interface {
                    all: initial; /* Reset inherited styles */
                    box-sizing: border-box;
                }

                /* Ensure our elements don't interfere with existing z-indexes */
                .todo-chat-icon {
                    z-index: 100000 !important; /* Very high to ensure visibility */
                }

                .todo-chat-interface {
                    z-index: 99999 !important;
                }

                /* Prevent our styles from affecting existing elements */
                .todo-chat-icon *,
                .todo-chat-interface * {
                    box-sizing: border-box;
                }
            `;

            document.head.appendChild(style);
        }
    }

    /**
     * Add accessibility features
     */
    addAccessibilityFeatures() {
        // Add ARIA labels and roles for accessibility
        if (this.widgetContainer) {
            this.widgetContainer.setAttribute('role', 'region');
            this.widgetContainer.setAttribute('aria-label', 'Todo AI Chat Assistant');
        }
    }

    /**
     * Bind events to handle integration-specific events
     */
    bindEvents() {
        // Listen for widget open/close events to adjust layout if needed
        document.addEventListener('chatOpened', () => {
            this.onWidgetOpen();
        });

        document.addEventListener('chatClosed', () => {
            this.onWidgetClose();
        });

        // Listen for resize events to adjust if needed
        window.addEventListener('resize', this.debounce(() => {
            this.onWindowResize();
        }, 250));

        // Listen for scroll events to adjust positioning if needed
        window.addEventListener('scroll', this.debounce(() => {
            this.onWindowScroll();
        }, 100));
    }

    /**
     * Handle widget opening
     */
    onWidgetOpen() {
        // Any special handling when widget opens
        // For example, reducing main content area if widget overlaps
    }

    /**
     * Handle widget closing
     */
    onWidgetClose() {
        // Any special handling when widget closes
        // Revert any layout adjustments made when opening
    }

    /**
     * Handle window resize
     */
    onWindowResize() {
        // Adjust widget positioning if needed based on new window size
        this.adjustWidgetPositioning();
    }

    /**
     * Handle window scroll
     */
    onWindowScroll() {
        // Adjust widget positioning if needed based on scroll position
        this.adjustWidgetPositioning();
    }

    /**
     * Adjust widget positioning based on current layout
     */
    adjustWidgetPositioning() {
        // Only adjust if widget is visible
        const interfaceEl = document.getElementById('todo-chat-interface');
        const iconEl = document.getElementById('todo-chat-icon');

        if (interfaceEl && window.getComputedStyle(interfaceEl).display !== 'none') {
            // Adjust position based on viewport and scrolling
            const rect = interfaceEl.getBoundingClientRect();

            // Ensure it stays within viewport
            if (rect.bottom > window.innerHeight) {
                interfaceEl.style.bottom = '20px';
            }

            if (rect.top < 0) {
                interfaceEl.style.top = '20px';
            }
        }
    }

    /**
     * Check if the widget is currently interfering with main content
     */
    isInterferingWithContent() {
        const interfaceEl = document.getElementById('todo-chat-interface');
        if (!interfaceEl || window.getComputedStyle(interfaceEl).display === 'none') {
            return false;
        }

        const interfaceRect = interfaceEl.getBoundingClientRect();
        const contentRect = this.mainContentArea?.getBoundingClientRect();

        if (!contentRect) return false;

        // Check if interface overlaps with main content
        return !(interfaceRect.right < contentRect.left ||
                 interfaceRect.left > contentRect.right ||
                 interfaceRect.bottom < contentRect.top ||
                 interfaceRect.top > contentRect.bottom);
    }

    /**
     * Resolve any conflicts with existing functionality
     */
    resolveConflicts() {
        // Check for common conflicts and resolve them
        this.resolveZIndexConflicts();
        this.resolveClickThroughIssues();
    }

    /**
     * Resolve z-index conflicts
     */
    resolveZIndexConflicts() {
        // Ensure our widget is always above other elements
        const iconEl = document.getElementById('todo-chat-icon');
        const interfaceEl = document.getElementById('todo-chat-interface');

        if (iconEl) {
            iconEl.style.zIndex = '100000';
        }

        if (interfaceEl) {
            interfaceEl.style.zIndex = '99999';
        }
    }

    /**
     * Resolve click-through issues
     */
    resolveClickThroughIssues() {
        // Ensure our container doesn't intercept clicks when invisible
        if (this.widgetContainer) {
            const interfaceEl = document.getElementById('todo-chat-interface');
            if (interfaceEl && window.getComputedStyle(interfaceEl).display === 'none') {
                this.widgetContainer.style.pointerEvents = 'none';
            } else {
                this.widgetContainer.style.pointerEvents = 'auto';
            }
        }
    }

    /**
     * Debounce utility function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    /**
     * Restore original layout state
     */
    restoreOriginalLayout() {
        if (this.mainContentArea && this.originalLayoutState.mainContent) {
            this.mainContentArea.className = this.originalLayoutState.mainContent.className;
            this.mainContentArea.setAttribute('style', this.originalLayoutState.mainContent.style);
        }

        if (this.headerElement && this.originalLayoutState.header) {
            this.headerElement.className = this.originalLayoutState.header.className;
            this.headerElement.setAttribute('style', this.originalLayoutState.header.style);
        }
    }

    /**
     * Get the current integration status
     */
    getStatus() {
        return {
            isIntegrated: this.integrationComplete,
            containerExists: !!this.widgetContainer,
            widgetElements: {
                icon: !!document.getElementById('todo-chat-icon'),
                interface: !!document.getElementById('todo-chat-interface')
            },
            originalLayoutState: { ...this.originalLayoutState }
        };
    }

    /**
     * Destroy the integration
     */
    destroy() {
        // Restore original layout
        this.restoreOriginalLayout();

        // Remove our container
        if (this.widgetContainer && this.widgetContainer.parentNode) {
            this.widgetContainer.parentNode.removeChild(this.widgetContainer);
        }

        // Remove styles
        const styleElement = document.getElementById('todo-chat-widget-styles');
        if (styleElement) {
            styleElement.parentNode.removeChild(styleElement);
        }

        // Clear references
        this.widgetContainer = null;
        this.originalLayoutState = {};
        this.integrationComplete = false;
    }
}

/**
 * Initialize the integration when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const integration = new ChatWidgetIntegration();
    integration.init();

    // Store instance globally for potential external access
    window.TodoChatIntegration = integration;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ChatWidgetIntegration;
}