/**
 * Functionality Guard for Todo AI Chatbot
 *
 * This module ensures existing Todo functionality remains intact when chat is closed.
 */

class FunctionalityGuard {
    constructor() {
        this.originalStates = new Map();
        this.protectedElements = new Set();
        this.functionalityStatus = {
            todoList: true,
            todoCreation: true,
            todoEditing: true,
            todoDeletion: true,
            navigation: true,
            authentication: true
        };
        this.observers = [];
    }

    /**
     * Initialize the functionality guard
     */
    init() {
        this.protectOriginalFunctionality();
        this.setupMonitoring();
    }

    /**
     * Protect original functionality by preserving initial states
     */
    protectOriginalFunctionality() {
        // Store original event handlers for important elements
        this.storeOriginalEventHandlers();

        // Store original element properties
        this.storeOriginalElementProperties();

        // Monitor key functionality areas
        this.monitorTodoFunctionality();
    }

    /**
     * Store original event handlers for protected elements
     */
    storeOriginalEventHandlers() {
        const elementsToProtect = [
            // Common Todo app elements
            'form[action*="todo"]',
            'form[action*="task"]',
            'button[data-action="add-todo"]',
            'button[data-action="complete-todo"]',
            'button[data-action="delete-todo"]',
            '.todo-list',
            '.todo-item',
            '#todo-input',
            '[data-todo]',
            '[data-task]'
        ];

        elementsToProtect.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                if (!this.protectedElements.has(element)) {
                    this.protectedElements.add(element);

                    // Store original event listeners
                    this.storeElementEventListeners(element);

                    // Store original click handlers
                    if (element.onclick) {
                        this.originalStates.set(`${element.tagName}-${element.id || element.className}-onclick`, element.onclick);
                    }
                }
            });
        });
    }

    /**
     * Store event listeners for an element
     */
    storeElementEventListeners(element) {
        const eventType = 'click';
        const key = `${element.tagName}-${element.id || element.className}-${eventType}`;

        if (!this.originalStates.has(key)) {
            // In a real implementation, we would need to use a more sophisticated approach
            // to store the original listeners, possibly using a WeakMap or similar
            console.debug(`Storing original listeners for ${key}`);
        }
    }

    /**
     * Store original element properties
     */
    storeOriginalElementProperties() {
        const elements = document.querySelectorAll('[data-todo], [data-task], .todo-item, .todo-list');

        elements.forEach(element => {
            const key = `element-${element.tagName}-${element.id || element.className}`;

            // Store important properties that we shouldn't override
            this.originalStates.set(`${key}-display`, window.getComputedStyle(element).display);
            this.originalStates.set(`${key}-visibility`, window.getComputedStyle(element).visibility);
            this.originalStates.set(`${key}-zIndex`, window.getComputedStyle(element).zIndex);
            this.originalStates.set(`${key}-pointerEvents`, window.getComputedStyle(element).pointerEvents);
        });
    }

    /**
     * Monitor key Todo functionality
     */
    monitorTodoFunctionality() {
        // Monitor form submissions
        document.addEventListener('submit', (event) => {
            if (this.isTodoRelatedForm(event.target)) {
                this.verifyFunctionality(event.target);
            }
        }, true); // Use capture phase to intercept first

        // Monitor button clicks
        document.addEventListener('click', (event) => {
            if (this.isTodoRelatedElement(event.target)) {
                this.verifyFunctionality(event.target);
            }
        }, true);

        // Monitor input changes
        document.addEventListener('input', (event) => {
            if (this.isTodoRelatedInput(event.target)) {
                this.verifyFunctionality(event.target);
            }
        }, true);
    }

    /**
     * Check if an element is related to Todo functionality
     */
    isTodoRelatedElement(element) {
        const todoKeywords = ['todo', 'task', 'item', 'list', 'add', 'complete', 'delete', 'edit'];
        const elementText = element.textContent.toLowerCase();
        const elementId = (element.id || '').toLowerCase();
        const elementClass = (element.className || '').toLowerCase();
        const elementTag = element.tagName.toLowerCase();

        return todoKeywords.some(keyword =>
            elementText.includes(keyword) ||
            elementId.includes(keyword) ||
            elementClass.includes(keyword) ||
            elementTag.includes(keyword)
        );
    }

    /**
     * Check if a form is related to Todo functionality
     */
    isTodoRelatedForm(form) {
        if (!(form instanceof HTMLFormElement)) return false;

        const action = form.getAttribute('action') || '';
        const formId = (form.id || '').toLowerCase();
        const formClass = (form.className || '').toLowerCase();

        const todoKeywords = ['todo', 'task', 'item', 'add', 'create', 'update', 'delete'];

        return todoKeywords.some(keyword =>
            action.includes(keyword) ||
            formId.includes(keyword) ||
            formClass.includes(keyword)
        );
    }

    /**
     * Check if an input is related to Todo functionality
     */
    isTodoRelatedInput(input) {
        if (!(input instanceof HTMLInputElement || input instanceof HTMLTextAreaElement)) return false;

        const inputId = (input.id || '').toLowerCase();
        const inputClass = (input.className || '').toLowerCase();
        const inputName = (input.name || '').toLowerCase();
        const inputPlaceholder = (input.placeholder || '').toLowerCase();

        const todoKeywords = ['todo', 'task', 'item', 'title', 'description', 'notes', 'name'];

        return todoKeywords.some(keyword =>
            inputId.includes(keyword) ||
            inputClass.includes(keyword) ||
            inputName.includes(keyword) ||
            inputPlaceholder.includes(keyword)
        );
    }

    /**
     * Verify that functionality is still working as expected
     */
    verifyFunctionality(element) {
        // Check if the element still behaves as expected
        if (this.isTodoRelatedElement(element)) {
            // Verify that event handlers are still attached
            this.verifyEventHandlers(element);

            // Verify that the element is still visible and interactive
            this.verifyElementVisibility(element);
        }
    }

    /**
     * Verify that event handlers are still attached to an element
     */
    verifyEventHandlers(element) {
        // In a real implementation, we would verify that the original handlers are still present
        // This is a simplified check
        if (element.onclick === null) {
            console.warn(`Original onclick handler may have been removed from ${element.tagName}`);
        }
    }

    /**
     * Verify that an element is still visible and interactive
     */
    verifyElementVisibility(element) {
        const computedStyle = window.getComputedStyle(element);

        if (computedStyle.display === 'none' || computedStyle.visibility === 'hidden') {
            console.warn(`Todo element ${element.tagName} may be hidden by chat widget`);
            this.functionalityStatus.todoList = false;
        }

        if (computedStyle.pointerEvents === 'none') {
            console.warn(`Todo element ${element.tagName} may be non-interactive due to chat widget`);
        }
    }

    /**
     * Setup monitoring for changes to protected functionality
     */
    setupMonitoring() {
        // Monitor DOM changes that might affect Todo functionality
        this.setupDOMChangeMonitoring();

        // Monitor for style changes that might affect Todo functionality
        this.setupStyleChangeMonitoring();
    }

    /**
     * Setup monitoring for DOM changes
     */
    setupDOMChangeMonitoring() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList') {
                    // Check if any Todo-related elements were removed
                    mutation.removedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE && this.isTodoRelatedElement(node)) {
                            console.error(`Todo-related element was removed: ${node.tagName}`);
                            this.reportFunctionalityImpact('elementRemoved', node);
                        }
                    });

                    // Check if any Todo-related elements were added
                    mutation.addedNodes.forEach(node => {
                        if (node.nodeType === Node.ELEMENT_NODE && this.isTodoRelatedElement(node)) {
                            console.info(`Todo-related element was added: ${node.tagName}`);
                        }
                    });
                } else if (mutation.type === 'attributes') {
                    // Check if attributes of Todo-related elements were changed
                    if (this.isTodoRelatedElement(mutation.target)) {
                        console.debug(`Attribute changed on Todo element: ${mutation.attributeName}`);
                    }
                }
            });
        });

        observer.observe(document.body, {
            childList: true,
            subtree: true,
            attributes: true,
            attributeFilter: ['style', 'class', 'id', 'data-todo', 'data-task']
        });

        this.mutationObserver = observer;
    }

    /**
     * Setup monitoring for style changes
     */
    setupStyleChangeMonitoring() {
        // Monitor for changes to styles that might affect Todo functionality
        const styleObserver = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
                    const element = mutation.target;
                    if (this.isTodoRelatedElement(element)) {
                        const computedStyle = window.getComputedStyle(element);

                        // Check if visibility or interactivity has been affected
                        if (computedStyle.display === 'none' ||
                            computedStyle.visibility === 'hidden' ||
                            computedStyle.pointerEvents === 'none') {

                            console.warn(`Style change may affect Todo functionality on ${element.tagName}`);
                            this.reportFunctionalityImpact('styleChanged', element);
                        }
                    }
                }
            });
        });

        // Observe all elements that might be affected
        const allElements = document.querySelectorAll('*');
        allElements.forEach(element => {
            styleObserver.observe(element, { attributes: true, attributeFilter: ['style'] });
        });

        this.styleObserver = styleObserver;
    }

    /**
     * Report functionality impact
     */
    reportFunctionalityImpact(type, element) {
        const report = {
            type: type,
            element: element.tagName,
            id: element.id || 'no-id',
            className: element.className || 'no-class',
            timestamp: new Date().toISOString(),
            description: this.getImpactDescription(type, element)
        };

        // Trigger an event for other modules to handle
        const event = new CustomEvent('functionalityImpacted', {
            detail: report
        });
        document.dispatchEvent(event);
    }

    /**
     * Get impact description for reporting
     */
    getImpactDescription(type, element) {
        switch(type) {
            case 'elementRemoved':
                return `Todo-related element ${element.tagName} was removed from the DOM`;
            case 'styleChanged':
                return `Style changes to ${element.tagName} may affect Todo functionality`;
            default:
                return `Unknown impact to ${element.tagName}`;
        }
    }

    /**
     * Restore original functionality if compromised
     */
    restoreFunctionality() {
        // Restore original event handlers
        this.restoreEventHandlers();

        // Restore original element properties
        this.restoreElementProperties();

        // Re-enable any disabled functionality
        this.reenableFunctionality();
    }

    /**
     * Restore original event handlers
     */
    restoreEventHandlers() {
        // Iterate through stored original handlers and restore them
        for (let [key, originalHandler] of this.originalStates.entries()) {
            if (key.endsWith('-onclick')) {
                const [tag, idOrClass] = key.replace('-onclick', '').split('-');

                // Find the element and restore the handler
                let element;
                if (idOrClass.startsWith('undefined')) {
                    element = document.getElementsByTagName(tag)[0]; // Rough approximation
                } else {
                    element = document.getElementById(idOrClass) ||
                             document.querySelector(`.${idOrClass.split(' ')[0]}`);
                }

                if (element && typeof originalHandler === 'function') {
                    element.onclick = originalHandler;
                }
            }
        }
    }

    /**
     * Restore original element properties
     */
    restoreElementProperties() {
        // This is a simplified approach - in reality, we'd need more sophisticated tracking
        const elements = document.querySelectorAll('[data-todo], [data-task], .todo-item, .todo-list');

        elements.forEach(element => {
            const key = `element-${element.tagName}-${element.id || element.className}`;

            // Restore display if it was changed
            const originalDisplay = this.originalStates.get(`${key}-display`);
            if (originalDisplay && window.getComputedStyle(element).display !== originalDisplay) {
                element.style.display = originalDisplay;
            }

            // Restore visibility if it was changed
            const originalVisibility = this.originalStates.get(`${key}-visibility`);
            if (originalVisibility && window.getComputedStyle(element).visibility !== originalVisibility) {
                element.style.visibility = originalVisibility;
            }

            // Restore z-index if it was changed
            const originalZIndex = this.originalStates.get(`${key}-zIndex`);
            if (originalZIndex && window.getComputedStyle(element).zIndex !== originalZIndex) {
                element.style.zIndex = originalZIndex;
            }

            // Restore pointer events if they were changed
            const originalPointerEvents = this.originalStates.get(`${key}-pointerEvents`);
            if (originalPointerEvents && window.getComputedStyle(element).pointerEvents !== originalPointerEvents) {
                element.style.pointerEvents = originalPointerEvents;
            }
        });
    }

    /**
     * Re-enable functionality if it was disabled
     */
    reenableFunctionality() {
        // Reset functionality status flags
        Object.keys(this.functionalityStatus).forEach(key => {
            this.functionalityStatus[key] = true;
        });
    }

    /**
     * Check if Todo functionality is intact
     */
    isTodoFunctionalityIntact() {
        // Check if all functionality status flags are true
        return Object.values(this.functionalityStatus).every(status => status === true);
    }

    /**
     * Get current functionality status
     */
    getFunctionalityStatus() {
        return {
            ...this.functionalityStatus,
            intact: this.isTodoFunctionalityIntact(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Add an observer function to be called when functionality is impacted
     */
    addObserver(observerFn) {
        if (typeof observerFn === 'function') {
            this.observers.push(observerFn);
        }
    }

    /**
     * Remove an observer function
     */
    removeObserver(observerFn) {
        const index = this.observers.indexOf(observerFn);
        if (index !== -1) {
            this.observers.splice(index, 1);
        }
    }

    /**
     * Notify observers of functionality status changes
     */
    notifyObservers(status) {
        this.observers.forEach(observer => {
            try {
                observer(status);
            } catch (error) {
                console.error('Error in functionality observer:', error);
            }
        });
    }

    /**
     * Destroy the functionality guard
     */
    destroy() {
        if (this.mutationObserver) {
            this.mutationObserver.disconnect();
        }

        if (this.styleObserver) {
            this.styleObserver.disconnect();
        }

        // Clear stored states and protected elements
        this.originalStates.clear();
        this.protectedElements.clear();
        this.observers = [];
    }
}

/**
 * Initialize the functionality guard when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const functionalityGuard = new FunctionalityGuard();
    functionalityGuard.init();

    // Store instance globally for potential external access
    window.TodoFunctionalityGuard = functionalityGuard;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FunctionalityGuard;
}