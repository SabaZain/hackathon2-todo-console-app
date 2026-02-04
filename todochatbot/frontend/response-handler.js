/**
 * Response Handler for Todo AI Chatbot
 *
 * This module handles response formatting and error states.
 */

class ResponseHandler {
    constructor() {
        this.formatters = new Map();
        this.errorHandlers = new Map();
        this.responseValidators = new Map();
        this.setupDefaultFormatters();
        this.setupDefaultErrorHandlers();
        this.setupDefaultValidators();
    }

    /**
     * Initialize the response handler
     */
    init() {
        this.bindEvents();
    }

    /**
     * Bind events to handle responses
     */
    bindEvents() {
        // Listen for API responses to format and handle them
        document.addEventListener('apiResponse', (event) => {
            this.handleResponse(event.detail.data, event.detail.context);
        });

        // Listen for API errors to handle them
        document.addEventListener('apiError', (event) => {
            this.handleError(event.detail.error, event.detail.context);
        });

        // Listen for message sent events to process the response
        document.addEventListener('messageSent', (event) => {
            this.handleMessageResponse(event.detail.response, event.detail.conversationId);
        });
    }

    /**
     * Setup default formatters
     */
    setupDefaultFormatters() {
        // Default text formatter
        this.formatters.set('text', (data) => {
            if (typeof data === 'string') {
                return data;
            } else if (typeof data === 'object') {
                return JSON.stringify(data, null, 2);
            }
            return String(data);
        });

        // Default JSON formatter
        this.formatters.set('json', (data) => {
            if (typeof data === 'string') {
                try {
                    return JSON.parse(data);
                } catch (e) {
                    return { error: 'Invalid JSON', original: data };
                }
            }
            return data;
        });

        // Todo-specific formatter
        this.formatters.set('todo', (data) => {
            if (data && typeof data === 'object') {
                if (data.tasks && Array.isArray(data.tasks)) {
                    return this.formatTaskList(data.tasks);
                } else if (data.task) {
                    return this.formatSingleTask(data.task);
                }
                return data;
            }
            return { message: data };
        });
    }

    /**
     * Setup default error handlers
     */
    setupDefaultErrorHandlers() {
        // Network error handler
        this.errorHandlers.set('network', (error) => {
            return {
                type: 'network',
                message: 'Network error: Unable to reach the server. Please check your connection.',
                originalError: error,
                suggestedAction: 'Please check your internet connection and try again.'
            };
        });

        // Timeout error handler
        this.errorHandlers.set('timeout', (error) => {
            return {
                type: 'timeout',
                message: 'Request timed out: The server is taking too long to respond.',
                originalError: error,
                suggestedAction: 'Please try again in a moment.'
            };
        });

        // Validation error handler
        this.errorHandlers.set('validation', (error) => {
            return {
                type: 'validation',
                message: error.message || 'Validation error occurred',
                originalError: error,
                suggestedAction: 'Please check your input and try again.'
            };
        });

        // Server error handler
        this.errorHandlers.set('server', (error) => {
            return {
                type: 'server',
                message: 'Server error: The service encountered an issue.',
                originalError: error,
                suggestedAction: 'Our team has been notified. Please try again later.'
            };
        });
    }

    /**
     * Setup default validators
     */
    setupDefaultValidators() {
        // Response structure validator
        this.responseValidators.set('structure', (data) => {
            if (!data) {
                return { isValid: false, error: 'Empty response' };
            }

            if (typeof data !== 'object') {
                return { isValid: false, error: 'Response is not an object' };
            }

            // Check for required fields
            const requiredFields = ['success'];
            for (const field of requiredFields) {
                if (!(field in data)) {
                    return { isValid: false, error: `Missing required field: ${field}` };
                }
            }

            return { isValid: true };
        });

        // Todo response validator
        this.responseValidators.set('todo', (data) => {
            if (!data.success) {
                return { isValid: false, error: 'Operation failed' };
            }

            // Additional todo-specific validation
            if (data.tasks && !Array.isArray(data.tasks)) {
                return { isValid: false, error: 'Tasks should be an array' };
            }

            return { isValid: true };
        });
    }

    /**
     * Handle a response
     */
    handleResponse(responseData, context = {}) {
        try {
            // Validate the response
            const validation = this.validateResponse(responseData, context.validationType || 'structure');

            if (!validation.isValid) {
                const errorResponse = {
                    success: false,
                    error: validation.error,
                    originalData: responseData
                };

                this.dispatchError(errorResponse, context);
                return errorResponse;
            }

            // Format the response
            const formattedResponse = this.formatResponse(responseData, context.formatType || 'text');

            // Dispatch success event
            const successEvent = new CustomEvent('responseHandled', {
                detail: {
                    original: responseData,
                    formatted: formattedResponse,
                    context: context,
                    timestamp: new Date().toISOString()
                }
            });
            document.dispatchEvent(successEvent);

            return formattedResponse;
        } catch (error) {
            this.dispatchError(error, context);
            return { error: error.message, success: false };
        }
    }

    /**
     * Handle an error
     */
    handleError(error, context = {}) {
        try {
            // Determine error type
            const errorType = this.determineErrorType(error);

            // Process with appropriate handler
            const processedError = this.processError(error, errorType);

            // Dispatch error event
            const errorEvent = new CustomEvent('responseError', {
                detail: {
                    originalError: error,
                    processedError: processedError,
                    context: context,
                    timestamp: new Date().toISOString()
                }
            });
            document.dispatchEvent(errorEvent);

            return processedError;
        } catch (handlingError) {
            console.error('Error in error handling:', handlingError);
            return {
                type: 'handling_error',
                message: 'An error occurred while processing the error',
                originalError: error
            };
        }
    }

    /**
     * Handle message response specifically
     */
    handleMessageResponse(response, conversationId) {
        if (!response) {
            return this.handleError(new Error('Empty response received'), { conversationId });
        }

        // Special handling for message responses
        if (response.success) {
            // Format AI response for display
            const formattedResponse = {
                success: true,
                response: this.formatAiResponse(response.response || response.message || response),
                conversationId: response.conversation_id || conversationId,
                timestamp: new Date().toISOString()
            };

            // Dispatch event for other components
            const event = new CustomEvent('formattedResponse', {
                detail: formattedResponse
            });
            document.dispatchEvent(event);

            return formattedResponse;
        } else {
            // Handle error response
            return this.handleError(
                new Error(response.error || response.message || 'Unknown error'),
                { conversationId, originalResponse: response }
            );
        }
    }

    /**
     * Format a response using the specified formatter
     */
    formatResponse(data, formatType = 'text') {
        const formatter = this.formatters.get(formatType) || this.formatters.get('text');
        return formatter(data);
    }

    /**
     * Process an error using the appropriate handler
     */
    processError(error, errorType) {
        const errorHandler = this.errorHandlers.get(errorType) || this.errorHandlers.get('server');
        return errorHandler(error);
    }

    /**
     * Validate a response
     */
    validateResponse(data, validationType = 'structure') {
        const validator = this.responseValidators.get(validationType) || this.responseValidators.get('structure');
        return validator(data);
    }

    /**
     * Determine error type from error object
     */
    determineErrorType(error) {
        if (error.message && (
            error.message.includes('Failed to fetch') ||
            error.message.includes('NetworkError') ||
            error.message.includes('TypeError')
        )) {
            return 'network';
        }

        if (error.message && error.message.includes('timeout')) {
            return 'timeout';
        }

        if (error.message && (
            error.message.toLowerCase().includes('validation') ||
            error.message.toLowerCase().includes('invalid')
        )) {
            return 'validation';
        }

        if (error.status && (error.status >= 500 && error.status < 600)) {
            return 'server';
        }

        return 'generic';
    }

    /**
     * Format AI response for display
     */
    formatAiResponse(aiResponse) {
        if (typeof aiResponse === 'string') {
            // Handle markdown-like formatting
            return this.convertMarkdownToHtml(aiResponse);
        } else if (typeof aiResponse === 'object') {
            // If it's an object, convert to a readable format
            return JSON.stringify(aiResponse, null, 2);
        }
        return String(aiResponse);
    }

    /**
     * Convert markdown-like text to HTML
     */
    convertMarkdownToHtml(text) {
        // Convert headers
        text = text.replace(/^### (.*$)/gim, '<h3>$1</h3>');
        text = text.replace(/^## (.*$)/gim, '<h2>$1</h2>');
        text = text.replace(/^# (.*$)/gim, '<h1>$1</h1>');

        // Convert bold and italic
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');

        // Convert lists
        text = text.replace(/^\- (.*$)/gim, '<li>$1</li>');
        text = text.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');

        // Convert line breaks
        text = text.replace(/\n/g, '<br>');

        return text;
    }

    /**
     * Format a task list for display
     */
    formatTaskList(tasks) {
        if (!Array.isArray(tasks)) {
            return 'No tasks to display';
        }

        if (tasks.length === 0) {
            return 'No tasks found';
        }

        return tasks.map((task, index) => {
            const status = task.completed ? '✓' : '○';
            const priority = task.priority ? `[${task.priority}]` : '';
            return `${status} ${index + 1}. ${task.description || task.title || 'Untitled task'} ${priority}`;
        }).join('\n');
    }

    /**
     * Format a single task for display
     */
    formatSingleTask(task) {
        if (!task) {
            return 'No task to display';
        }

        const status = task.completed ? 'Completed' : 'Pending';
        const priority = task.priority ? `Priority: ${task.priority}` : '';
        const dueDate = task.due_date ? `Due: ${task.due_date}` : '';

        let result = `${task.description || task.title || 'Untitled task'} - ${status}`;
        if (priority) result += ` (${priority})`;
        if (dueDate) result += `, ${dueDate}`;

        return result;
    }

    /**
     * Add a custom formatter
     */
    addFormatter(name, formatterFn) {
        if (typeof formatterFn !== 'function') {
            throw new Error('Formatter must be a function');
        }
        this.formatters.set(name, formatterFn);
    }

    /**
     * Add a custom error handler
     */
    addErrorHandler(name, handlerFn) {
        if (typeof handlerFn !== 'function') {
            throw new Error('Error handler must be a function');
        }
        this.errorHandlers.set(name, handlerFn);
    }

    /**
     * Add a custom validator
     */
    addValidator(name, validatorFn) {
        if (typeof validatorFn !== 'function') {
            throw new Error('Validator must be a function');
        }
        this.responseValidators.set(name, validatorFn);
    }

    /**
     * Remove a formatter
     */
    removeFormatter(name) {
        this.formatters.delete(name);
    }

    /**
     * Remove an error handler
     */
    removeErrorHandler(name) {
        this.errorHandlers.delete(name);
    }

    /**
     * Remove a validator
     */
    removeValidator(name) {
        this.responseValidators.delete(name);
    }

    /**
     * Dispatch an error event
     */
    dispatchError(errorResponse, context) {
        const errorEvent = new CustomEvent('responseError', {
            detail: {
                error: errorResponse,
                context: context,
                timestamp: new Date().toISOString()
            }
        });
        document.dispatchEvent(errorEvent);
    }

    /**
     * Get available formatters
     */
    getAvailableFormatters() {
        return Array.from(this.formatters.keys());
    }

    /**
     * Get available error handlers
     */
    getAvailableErrorHandlers() {
        return Array.from(this.errorHandlers.keys());
    }

    /**
     * Get available validators
     */
    getAvailableValidators() {
        return Array.from(this.responseValidators.keys());
    }

    /**
     * Get response handling statistics
     */
    getStats() {
        return {
            formatters: this.getAvailableFormatters().length,
            errorHandlers: this.getAvailableErrorHandlers().length,
            validators: this.getAvailableValidators().length,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Destroy the response handler
     */
    destroy() {
        // Clear all maps
        this.formatters.clear();
        this.errorHandlers.clear();
        this.responseValidators.clear();
    }
}

/**
 * Initialize the response handler when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const responseHandler = new ResponseHandler();
    responseHandler.init();

    // Store instance globally for potential external access
    window.TodoResponseHandler = responseHandler;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ResponseHandler;
}