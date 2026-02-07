/**
 * API Client for Todo AI Chatbot
 *
 * This module implements API calls to the `/api/{user_id}/chat` endpoint with JWT authentication.
 */

class APIClient {
    constructor(baseURL = '/api', defaultTimeout = 30000) {
        this.baseURL = baseURL;
        this.defaultTimeout = defaultTimeout;
        this.requestQueue = [];
        this.isProcessing = false;
        this.retryAttempts = 3;
        this.connectionStatus = 'connected';
        this.authToken = null;
    }

    /**
     * Initialize the API client
     */
    init() {
        this.checkConnectionStatus();
        this.setupRetryMechanism();
    }

    /**
     * Send a message to the chat endpoint
     */
    async sendMessage(userId, message, conversationId = null) {
        const payload = {
            message: message,
            ...(conversationId && { conversation_id: conversationId })
        };

        return await this.makeRequest('POST', `${this.baseURL}/${userId}/chat`, payload);
    }

    /**
     * Get conversation history
     */
    async getConversationHistory(userId, conversationId) {
        return await this.makeRequest('GET', `${this.baseURL}/${userId}/conversations/${conversationId}`);
    }

    /**
     * Create a new conversation
     */
    async createConversation(userId, initialMessage = null) {
        const payload = initialMessage ? { message: initialMessage } : {};
        return await this.makeRequest('POST', `${this.baseURL}/${userId}/conversations`, payload);
    }

    /**
     * Get user's conversations
     */
    async getUserConversations(userId) {
        return await this.makeRequest('GET', `${this.baseURL}/${userId}/conversations`);
    }

    /**
     * Delete a conversation
     */
    async deleteConversation(userId, conversationId) {
        return await this.makeRequest('DELETE', `${this.baseURL}/${userId}/conversations/${conversationId}`);
    }

    /**
     * Update conversation metadata
     */
    async updateConversation(userId, conversationId, metadata) {
        return await this.makeRequest('PUT', `${this.baseURL}/${userId}/conversations/${conversationId}`, metadata);
    }

    /**
     * Make an API request with proper error handling
     */
    async makeRequest(method, url, data = null) {
        if (this.connectionStatus !== 'connected') {
            throw new Error(`Cannot make request: ${this.connectionStatus}`);
        }

        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
                ...this.getAuthHeaders()
            }
        };

        if (data !== null) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await this.fetchWithTimeout(url, options, this.defaultTimeout);

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Unauthorized: Please log in again');
                } else if (response.status === 403) {
                    throw new Error('Forbidden: Access denied');
                } else if (response.status === 429) {
                    throw new Error('Too many requests: Please try again later');
                } else {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
            }

            return await response.json();
        } catch (error) {
            console.error(`API request failed: ${error.message}`);

            // Check if it's a connection issue
            if (this.isConnectionError(error)) {
                this.setConnectionStatus('disconnected');

                // Dispatch event for other components
                const event = new CustomEvent('connectionLost', {
                    detail: { error: error.message, url: url }
                });
                document.dispatchEvent(event);
            }

            throw error;
        }
    }

    /**
     * Fetch with timeout
     */
    fetchWithTimeout(url, options, timeout) {
        return Promise.race([
            fetch(url, options),
            new Promise((_, reject) =>
                setTimeout(() => reject(new Error('Request timeout')), timeout)
            )
        ]);
    }

    /**
     * Get authentication headers
     */
    getAuthHeaders() {
        const headers = {};

        // Prioritize the authToken property if set, otherwise get from localStorage
        const token = this.authToken || localStorage.getItem('token');

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        return headers;
    }

    /**
     * Set authentication token
     */
    setAuthToken(token) {
        this.authToken = token;
    }

    /**
     * Check connection status
     */
    async checkConnectionStatus() {
        try {
            const userId = this.getCurrentUserId();
            const response = await this.fetchWithTimeout(
                `${this.baseURL}/${userId}/health`,
                { method: 'GET', headers: this.getAuthHeaders() },
                5000
            );

            if (response.ok) {
                this.setConnectionStatus('connected');
                return true;
            } else {
                this.setConnectionStatus('disconnected');
                return false;
            }
        } catch (error) {
            this.setConnectionStatus('disconnected');
            return false;
        }
    }

    /**
     * Set connection status
     */
    setConnectionStatus(status) {
        const prevStatus = this.connectionStatus;
        this.connectionStatus = status;

        if (prevStatus !== status) {
            // Dispatch event for other components
            const event = new CustomEvent('connectionStatusChange', {
                detail: { connected: status === 'connected', status: status }
            });
            document.dispatchEvent(event);
        }
    }

    /**
     * Check if error is a connection error
     */
    isConnectionError(error) {
        return error.message.includes('Failed to fetch') ||
               error.message.includes('NetworkError') ||
               error.message.includes('timeout') ||
               error.constructor.name === 'TypeError';
    }

    /**
     * Get current user ID (implement based on your auth system)
     */
    getCurrentUserId() {
        // Get user ID from localStorage (set by TodoChatbotWidget)
        return localStorage.getItem('todo_user_id') || 'anonymous';
    }

    /**
     * Queue a request for later processing
     */
    queueRequest(method, url, data = null) {
        const requestPromise = {
            method,
            url,
            data,
            resolve: null,
            reject: null,
            promise: null
        };

        // Create a promise that can be resolved later
        requestPromise.promise = new Promise((resolve, reject) => {
            requestPromise.resolve = resolve;
            requestPromise.reject = reject;
        });

        this.requestQueue.push(requestPromise);

        // Process the queue if not already processing
        if (!this.isProcessing) {
            this.processQueue();
        }

        return requestPromise.promise;
    }

    /**
     * Process the request queue
     */
    async processQueue() {
        if (this.requestQueue.length === 0) {
            this.isProcessing = false;
            return;
        }

        this.isProcessing = true;

        while (this.requestQueue.length > 0) {
            const request = this.requestQueue.shift();

            try {
                const result = await this.makeRequest(request.method, request.url, request.data);
                request.resolve(result);
            } catch (error) {
                // Retry mechanism
                if (this.shouldRetry(error, request)) {
                    // Add back to queue for retry
                    this.requestQueue.unshift(request);

                    // Wait before retrying
                    await this.delay(1000);
                } else {
                    request.reject(error);
                }
            }
        }

        this.isProcessing = false;
    }

    /**
     * Check if request should be retried
     */
    shouldRetry(error, request) {
        return this.isConnectionError(error) &&
               request.retryCount < this.retryAttempts;
    }

    /**
     * Delay helper function
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Setup retry mechanism
     */
    setupRetryMechanism() {
        // Listen for connection restored event to retry failed requests
        document.addEventListener('connectionRestored', async () => {
            if (this.requestQueue.length > 0 && !this.isProcessing) {
                await this.processQueue();
            }
        });
    }

    /**
     * Cancel all queued requests
     */
    cancelAllRequests() {
        while (this.requestQueue.length > 0) {
            const request = this.requestQueue.pop();
            request.reject(new Error('Request cancelled'));
        }
    }

    /**
     * Get request queue status
     */
    getQueueStatus() {
        return {
            length: this.requestQueue.length,
            processing: this.isProcessing,
            connectionStatus: this.connectionStatus
        };
    }

    /**
     * Upload file/data to the API
     */
    async uploadData(userId, formData, endpoint = 'upload') {
        const options = {
            method: 'POST',
            body: formData,
            headers: {
                ...this.getAuthHeaders()
                // Don't set Content-Type for FormData as it sets the boundary
            }
        };

        try {
            const response = await this.fetchWithTimeout(
                `${this.baseURL}/${userId}/${endpoint}`,
                options,
                this.defaultTimeout * 2 // Longer timeout for uploads
            );

            if (!response.ok) {
                if (response.status === 401) {
                    throw new Error('Unauthorized: Please log in again');
                } else if (response.status === 403) {
                    throw new Error('Forbidden: Access denied');
                } else {
                    throw new Error(`Upload failed with status: ${response.status}`);
                }
            }

            return await response.json();
        } catch (error) {
            console.error(`Upload failed: ${error.message}`);
            throw error;
        }
    }

    /**
     * Get API statistics
     */
    getStats() {
        return {
            baseURL: this.baseURL,
            timeout: this.defaultTimeout,
            queueSize: this.requestQueue.length,
            isProcessing: this.isProcessing,
            connectionStatus: this.connectionStatus,
            retryAttempts: this.retryAttempts,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Destroy the API client
     */
    destroy() {
        this.cancelAllRequests();

        // Clear any intervals or timeouts if present
        // In this implementation, we don't have any intervals to clear

        this.authToken = null;
    }
}

/**
 * Initialize the API client when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const apiClient = new APIClient();
    apiClient.init();

    // Store instance globally for potential external access
    window.TodoAPIClient = apiClient;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIClient;
}