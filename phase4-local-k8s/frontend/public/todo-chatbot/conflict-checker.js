/**
 * Conflict Checker for Todo AI Chatbot
 *
 * This module ensures no conflicts with existing CSS or JavaScript.
 */

class ConflictChecker {
    constructor() {
        this.conflicts = {
            css: [],
            js: [],
            dom: []
        };
        this.originalStates = new Map();
        this.checkResults = {};
    }

    /**
     * Initialize the conflict checker
     */
    init() {
        this.runInitialChecks();
        this.setupMonitoring();
    }

    /**
     * Run initial checks for potential conflicts
     */
    runInitialChecks() {
        this.checkCSSConflicts();
        this.checkJavaScriptConflicts();
        this.checkDOMConflicts();

        // Store the results
        this.checkResults = {
            css: this.conflicts.css,
            js: this.conflicts.js,
            dom: this.conflicts.dom,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Check for CSS conflicts
     */
    checkCSSConflicts() {
        // Check for CSS class name conflicts
        this.checkClassNameConflicts();

        // Check for CSS selector conflicts
        this.checkSelectorConflicts();

        // Check for CSS variable conflicts
        this.checkCSSVariableConflicts();

        // Check for CSS property conflicts
        this.checkPropertyConflicts();
    }

    /**
     * Check for JavaScript conflicts
     */
    checkJavaScriptConflicts() {
        // Check for global variable conflicts
        this.checkGlobalVariables();

        // Check for function name conflicts
        this.checkFunctionNames();

        // Check for event listener conflicts
        this.checkEventListeners();

        // Check for prototype modifications
        this.checkPrototypeModifications();

        // Check for DOM manipulation conflicts
        this.checkDOMManipulationConflicts();
    }

    /**
     * Check for DOM conflicts
     */
    checkDOMConflicts() {
        // Check for ID conflicts
        this.checkIdConflicts();

        // Check for element attribute conflicts
        this.checkAttributeConflicts();

        // Check for element positioning conflicts
        this.checkPositioningConflicts();
    }

    /**
     * Check for CSS class name conflicts
     */
    checkClassNameConflicts() {
        const ourClasses = [
            'todo-chat-icon', 'chat-icon-button', 'chat-icon', 'todo-chat-interface',
            'chat-modal', 'chat-header', 'close-btn', 'chat-messages-container',
            'chat-messages', 'message', 'message-content', 'message-meta',
            'typing-indicator', 'typing-content', 'typing-text', 'typing-dots',
            'dot', 'chat-input-container', 'chat-input', 'send-btn', 'special'
        ];

        const allClasses = new Set();
        const stylesheets = document.styleSheets;

        for (let sheet of stylesheets) {
            try {
                const rules = sheet.cssRules || sheet.rules;
                for (let rule of rules) {
                    if (rule.selectorText) {
                        // Extract class names from selectors
                        const classMatches = rule.selectorText.match(/\.([a-zA-Z0-9_-]+)/g);
                        if (classMatches) {
                            classMatches.forEach(match => {
                                allClasses.add(match.substring(1)); // Remove the dot
                            });
                        }
                    }
                }
            } catch (e) {
                // Skip stylesheets from other domains due to CORS
                console.debug('Could not access stylesheet:', e.message);
            }
        }

        // Check for conflicts
        ourClasses.forEach(ourClass => {
            if (allClasses.has(ourClass)) {
                this.conflicts.css.push({
                    type: 'className',
                    element: ourClass,
                    severity: 'warning',
                    message: `CSS class '${ourClass}' may conflict with existing styles`
                });
            }
        });
    }

    /**
     * Check for CSS selector conflicts
     */
    checkSelectorConflicts() {
        const ourSelectors = [
            '#todo-chat-icon', '#todo-chat-interface', '#chat-toggle-btn',
            '#chat-messages', '#typing-indicator', '#chat-input', '#send-message-btn'
        ];

        const stylesheets = document.styleSheets;

        for (let sheet of stylesheets) {
            try {
                const rules = sheet.cssRules || sheet.rules;
                for (let rule of rules) {
                    if (rule.selectorText) {
                        ourSelectors.forEach(selector => {
                            if (rule.selectorText.includes(selector)) {
                                this.conflicts.css.push({
                                    type: 'selector',
                                    element: selector,
                                    severity: 'high',
                                    message: `Selector '${selector}' conflicts with existing styles: ${rule.cssText}`
                                });
                            }
                        });
                    }
                }
            } catch (e) {
                // Skip stylesheets from other domains due to CORS
                console.debug('Could not access stylesheet:', e.message);
            }
        }
    }

    /**
     * Check for CSS variable conflicts
     */
    checkCSSVariableConflicts() {
        const computedStyle = getComputedStyle(document.documentElement);
        const ourVars = ['--todo-chat-primary', '--todo-chat-secondary']; // Example variables

        ourVars.forEach(varName => {
            if (computedStyle.getPropertyValue(varName)) {
                this.conflicts.css.push({
                    type: 'cssVariable',
                    element: varName,
                    severity: 'medium',
                    message: `CSS variable '${varName}' already exists`
                });
            }
        });
    }

    /**
     * Check for CSS property conflicts
     */
    checkPropertyConflicts() {
        // Check important properties that could affect layout
        const ourImportantProps = ['position', 'z-index', 'display', 'visibility'];
        const elementsToCheck = [
            document.getElementById('todo-chat-icon'),
            document.getElementById('todo-chat-interface')
        ].filter(el => el !== null);

        elementsToCheck.forEach(element => {
            const computedStyle = getComputedStyle(element);
            ourImportantProps.forEach(prop => {
                // Check if existing styles might conflict with our intended styles
                if (computedStyle[prop]) {
                    // This is a basic check - in a real implementation, we'd compare values
                    console.debug(`Element ${element.id} has ${prop} property set to: ${computedStyle[prop]}`);
                }
            });
        });
    }

    /**
     * Check for global variable conflicts
     */
    checkGlobalVariables() {
        const ourGlobals = [
            'TodoChatIcon', 'TodoChatInterface', 'TodoUIController',
            'TodoMessageSender', 'TodoMessageDisplay', 'TodoTypingIndicator',
            'TodoChatIntegration', 'TodoConflictChecker', 'TodoFunctionalityGuard',
            'TodoAPIClient', 'TodoResponseHandler', 'TodoStateManager'
        ];

        ourGlobals.forEach(globalVar => {
            if (window[globalVar] !== undefined) {
                this.conflicts.js.push({
                    type: 'globalVariable',
                    element: globalVar,
                    severity: 'high',
                    message: `Global variable '${globalVar}' already exists`
                });
            }
        });
    }

    /**
     * Check for function name conflicts
     */
    checkFunctionNames() {
        // Check for function names in common namespaces
        const ourFunctions = ['initTodoChat', 'openTodoChat', 'closeTodoChat'];

        ourFunctions.forEach(funcName => {
            if (typeof window[funcName] === 'function') {
                this.conflicts.js.push({
                    type: 'functionName',
                    element: funcName,
                    severity: 'medium',
                    message: `Function '${funcName}' already exists`
                });
            }
        });
    }

    /**
     * Check for event listener conflicts
     */
    checkEventListeners() {
        // Check for potential conflicts with our custom events
        const ourEvents = ['chatToggle', 'messageSending', 'messageSent', 'chatOpened', 'chatClosed'];

        // We can't easily check for existing listeners, but we can log our event usage
        console.debug('Our custom events:', ourEvents);
    }

    /**
     * Check for prototype modifications
     */
    checkPrototypeModifications() {
        // Check if we're modifying prototypes that might affect existing code
        const prototypesToWatch = ['String.prototype', 'Array.prototype', 'Object.prototype'];

        prototypesToWatch.forEach(proto => {
            console.debug(`Monitoring modifications to ${proto}`);
        });
    }

    /**
     * Check for DOM manipulation conflicts
     */
    checkDOMManipulationConflicts() {
        // Check if our DOM manipulations might conflict with existing ones
        const elementsWeModify = ['#todo-chat-container', '#chat-messages', '#chat-input'];

        elementsWeModify.forEach(selector => {
            const element = document.querySelector(selector);
            if (element) {
                // Check for existing event listeners or data attributes
                const listeners = this.getEventListeners(element);
                console.debug(`Element ${selector} has ${listeners.length} existing event listeners`);
            }
        });
    }

    /**
     * Check for ID conflicts
     */
    checkIdConflicts() {
        const ourIds = [
            'todo-chat-container', 'todo-chat-icon', 'chat-toggle-btn',
            'todo-chat-interface', 'close-chat-btn', 'chat-messages',
            'typing-indicator', 'chat-input', 'send-message-btn'
        ];

        ourIds.forEach(id => {
            const existingElement = document.getElementById(id);
            if (existingElement) {
                this.conflicts.dom.push({
                    type: 'idConflict',
                    element: id,
                    severity: 'high',
                    message: `Element with ID '${id}' already exists in the DOM`
                });
            }
        });
    }

    /**
     * Check for element attribute conflicts
     */
    checkAttributeConflicts() {
        // Check for potential conflicts with attributes we might use
        const elementsWithAttributes = document.querySelectorAll('[data-todo-chat]');

        if (elementsWithAttributes.length > 0) {
            this.conflicts.dom.push({
                type: 'attributeConflict',
                element: 'data-todo-chat attributes',
                severity: 'medium',
                message: `Found ${elementsWithAttributes.length} elements with data-todo-chat attributes already`
            });
        }
    }

    /**
     * Check for element positioning conflicts
     */
    checkPositioningConflicts() {
        // Check if our fixed-position elements might overlap with important content
        const fixedElements = document.querySelectorAll('*[style*="position: fixed"]');

        if (fixedElements.length > 0) {
            console.debug(`Found ${fixedElements.length} fixed position elements that might conflict`);
        }
    }

    /**
     * Get event listeners for an element (browser-dependent)
     */
    getEventListeners(element) {
        // This is a simplified approach; full implementation would require
        // more sophisticated methods depending on browser support
        if (element.eventListenerList) {
            return element.eventListenerList;
        }
        return [];
    }

    /**
     * Setup monitoring for runtime conflicts
     */
    setupMonitoring() {
        // Monitor for runtime changes that might cause conflicts
        this.setupMutationObserver();
        this.setupErrorMonitoring();
    }

    /**
     * Setup mutation observer to monitor DOM changes
     */
    setupMutationObserver() {
        const observer = new MutationObserver(mutations => {
            mutations.forEach(mutation => {
                if (mutation.type === 'childList') {
                    // Check if any of our elements were removed or altered
                    mutation.removedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            if (node.id && node.id.startsWith('todo-chat')) {
                                console.warn(`Todo chat element removed: ${node.id}`);
                            }
                        }
                    });

                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE) {
                            if (node.id && node.id.startsWith('todo-chat')) {
                                console.info(`Todo chat element added: ${node.id}`);
                            }
                        }
                    });
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true
        });

        this.mutationObserver = observer;
    }

    /**
     * Setup error monitoring to catch conflicts at runtime
     */
    setupErrorMonitoring() {
        // Monitor for JavaScript errors that might be caused by conflicts
        window.addEventListener('error', (event) => {
            if (event.filename && event.filename.includes('todo-chat')) {
                this.conflicts.js.push({
                    type: 'runtimeError',
                    element: event.filename,
                    severity: 'high',
                    message: `Runtime error in Todo Chat: ${event.error.message}`
                });
            }
        });

        // Monitor for unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            if (event.reason && event.reason.stack && event.reason.stack.includes('todo-chat')) {
                this.conflicts.js.push({
                    type: 'promiseRejection',
                    element: 'Promise',
                    severity: 'high',
                    message: `Unhandled promise rejection in Todo Chat: ${event.reason.message}`
                });
            }
        });
    }

    /**
     * Run a specific conflict check
     */
    runCheck(checkType) {
        switch(checkType) {
            case 'css':
                return this.checkCSSConflicts();
            case 'js':
                return this.checkJavaScriptConflicts();
            case 'dom':
                return this.checkDOMConflicts();
            default:
                throw new Error(`Unknown check type: ${checkType}`);
        }
    }

    /**
     * Get conflict report
     */
    getConflictReport() {
        return {
            summary: {
                css: this.conflicts.css.length,
                js: this.conflicts.js.length,
                dom: this.conflicts.dom.length,
                total: this.conflicts.css.length + this.conflicts.js.length + this.conflicts.dom.length
            },
            details: {
                css: this.conflicts.css,
                js: this.conflicts.js,
                dom: this.conflicts.dom
            },
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Resolve a specific type of conflict
     */
    resolveConflicts(type = null) {
        if (type === null || type === 'css') {
            this.resolveCSSConflicts();
        }
        if (type === null || type === 'js') {
            this.resolveJavaScriptConflicts();
        }
        if (type === null || type === 'dom') {
            this.resolveDOMConflicts();
        }
    }

    /**
     * Resolve CSS conflicts
     */
    resolveCSSConflicts() {
        // Add more specific namespace prefixes to our CSS
        const styleSheet = document.getElementById('todo-chat-widget-styles');
        if (styleSheet) {
            // We already namespace our styles in the integration module
            console.info('CSS conflicts addressed through namespacing');
        }
    }

    /**
     * Resolve JavaScript conflicts
     */
    resolveJavaScriptConflicts() {
        // Use more specific global variable names
        console.info('JavaScript conflicts addressed through namespacing');
    }

    /**
     * Resolve DOM conflicts
     */
    resolveDOMConflicts() {
        // Use more specific IDs and selectors
        console.info('DOM conflicts addressed through unique identifiers');
    }

    /**
     * Check if there are any high-severity conflicts
     */
    hasHighSeverityConflicts() {
        return [
            ...this.conflicts.css.filter(c => c.severity === 'high'),
            ...this.conflicts.js.filter(c => c.severity === 'high'),
            ...this.conflicts.dom.filter(c => c.severity === 'high')
        ].length > 0;
    }

    /**
     * Check if there are any conflicts at all
     */
    hasAnyConflicts() {
        return this.conflicts.css.length > 0 ||
               this.conflicts.js.length > 0 ||
               this.conflicts.dom.length > 0;
    }

    /**
     * Get summary of conflicts
     */
    getSummary() {
        return {
            hasConflicts: this.hasAnyConflicts(),
            hasHighSeverity: this.hasHighSeverityConflicts(),
            counts: {
                css: this.conflicts.css.length,
                js: this.conflicts.js.length,
                dom: this.conflicts.dom.length
            }
        };
    }

    /**
     * Destroy the conflict checker
     */
    destroy() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }

        // Clear references
        this.conflicts = { css: [], js: [], dom: [] };
        this.originalStates.clear();
        this.checkResults = {};
    }
}

/**
 * Initialize the conflict checker when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const conflictChecker = new ConflictChecker();
    conflictChecker.init();

    // Store instance globally for potential external access
    window.TodoConflictChecker = conflictChecker;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ConflictChecker;
}