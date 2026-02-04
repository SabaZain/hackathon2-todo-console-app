/**
 * State Manager for Todo AI Chatbot
 *
 * This module manages conversation state in the frontend.
 */

class StateManager {
    constructor() {
        this.conversationState = new Map();
        this.globalState = new Map();
        this.stateHistory = [];
        this.maxHistorySize = 50;
        this.currentUser = null;
        this.currentConversationId = null;
        this.stateSubscribers = new Map();
    }

    /**
     * Initialize the state manager
     */
    init() {
        this.loadSavedState();
        this.setupStatePersistence();
    }

    /**
     * Load any saved state from localStorage
     */
    loadSavedState() {
        try {
            const savedState = localStorage.getItem('todoChatState');
            if (savedState) {
                const parsed = JSON.parse(savedState);

                // Restore conversation state
                if (parsed.conversationState) {
                    for (const [key, value] of Object.entries(parsed.conversationState)) {
                        this.conversationState.set(key, value);
                    }
                }

                // Restore global state
                if (parsed.globalState) {
                    for (const [key, value] of Object.entries(parsed.globalState)) {
                        this.globalState.set(key, value);
                    }
                }

                // Restore current user and conversation
                this.currentUser = parsed.currentUser || null;
                this.currentConversationId = parsed.currentConversationId || null;
            }
        } catch (error) {
            console.error('Error loading saved state:', error);
        }
    }

    /**
     * Setup state persistence to localStorage
     */
    setupStatePersistence() {
        // Save state before page unload
        window.addEventListener('beforeunload', () => {
            this.saveState();
        });

        // Also save periodically
        setInterval(() => {
            this.saveState();
        }, 30000); // Every 30 seconds
    }

    /**
     * Save current state to localStorage
     */
    saveState() {
        try {
            const stateToSave = {
                conversationState: Object.fromEntries(this.conversationState),
                globalState: Object.fromEntries(this.globalState),
                currentUser: this.currentUser,
                currentConversationId: this.currentConversationId,
                timestamp: new Date().toISOString()
            };

            localStorage.setItem('todoChatState', JSON.stringify(stateToSave));
        } catch (error) {
            console.error('Error saving state:', error);
        }
    }

    /**
     * Set the current user
     */
    setCurrentUser(userId) {
        this.currentUser = userId;
        this.notifySubscribers('currentUser', userId);
        this.saveState();
    }

    /**
     * Get the current user
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * Create a new conversation
     */
    createConversation(conversationId = null) {
        const id = conversationId || this.generateConversationId();

        const conversationData = {
            id: id,
            createdAt: new Date().toISOString(),
            lastActive: new Date().toISOString(),
            messages: [],
            context: {},
            isActive: true
        };

        this.conversationState.set(id, conversationData);
        this.currentConversationId = id;

        // Notify subscribers
        this.notifySubscribers('conversationCreated', { id, data: conversationData });

        // Add to history
        this.addToHistory('createConversation', { id });

        this.saveState();
        return id;
    }

    /**
     * Switch to an existing conversation
     */
    switchConversation(conversationId) {
        if (this.conversationState.has(conversationId)) {
            // Update last active for current conversation
            if (this.currentConversationId) {
                const currentConv = this.conversationState.get(this.currentConversationId);
                currentConv.lastActive = new Date().toISOString();
                this.conversationState.set(this.currentConversationId, currentConv);
            }

            this.currentConversationId = conversationId;

            // Update last active for new conversation
            const conv = this.conversationState.get(conversationId);
            conv.lastActive = new Date().toISOString();
            conv.isActive = true;

            // Deactivate other conversations
            for (const [id, data] of this.conversationState) {
                if (id !== conversationId) {
                    data.isActive = false;
                    this.conversationState.set(id, data);
                }
            }

            this.conversationState.set(conversationId, conv);

            // Notify subscribers
            this.notifySubscribers('conversationSwitched', { id: conversationId });

            this.saveState();
            return true;
        }

        return false;
    }

    /**
     * Add a message to the current conversation
     */
    addMessageToCurrent(messageData) {
        if (!this.currentConversationId) {
            this.createConversation();
        }

        return this.addMessage(this.currentConversationId, messageData);
    }

    /**
     * Add a message to a specific conversation
     */
    addMessage(conversationId, messageData) {
        if (!this.conversationState.has(conversationId)) {
            this.createConversation(conversationId);
        }

        const conversation = this.conversationState.get(conversationId);
        const message = {
            id: this.generateMessageId(),
            timestamp: new Date().toISOString(),
            ...messageData
        };

        conversation.messages.push(message);
        conversation.lastActive = new Date().toISOString();

        this.conversationState.set(conversationId, conversation);

        // Notify subscribers
        this.notifySubscribers('messageAdded', { conversationId, message });

        // Add to history
        this.addToHistory('addMessage', { conversationId, message });

        this.saveState();
        return message.id;
    }

    /**
     * Get messages for current conversation
     */
    getCurrentMessages(limit = null) {
        if (!this.currentConversationId) {
            return [];
        }
        return this.getMessages(this.currentConversationId, limit);
    }

    /**
     * Get messages for a specific conversation
     */
    getMessages(conversationId, limit = null) {
        if (!this.conversationState.has(conversationId)) {
            return [];
        }

        const conversation = this.conversationState.get(conversationId);
        const messages = conversation.messages;

        if (limit) {
            return messages.slice(-limit);
        }

        return messages;
    }

    /**
     * Update conversation context
     */
    updateContext(conversationId, contextUpdates) {
        if (!this.conversationState.has(conversationId)) {
            this.createConversation(conversationId);
        }

        const conversation = this.conversationState.get(conversationId);

        // Deep merge context updates
        conversation.context = { ...conversation.context, ...contextUpdates };
        conversation.lastActive = new Date().toISOString();

        this.conversationState.set(conversationId, conversation);

        // Notify subscribers
        this.notifySubscribers('contextUpdated', { conversationId, context: conversation.context });

        // Add to history
        this.addToHistory('updateContext', { conversationId, contextUpdates });

        this.saveState();
    }

    /**
     * Get conversation context
     */
    getContext(conversationId) {
        if (!this.conversationState.has(conversationId)) {
            return {};
        }

        return this.conversationState.get(conversationId).context;
    }

    /**
     * Set a global state value
     */
    setGlobalState(key, value) {
        this.globalState.set(key, value);

        // Notify subscribers
        this.notifySubscribers('globalStateUpdated', { key, value });

        // Add to history
        this.addToHistory('setGlobalState', { key, value });

        this.saveState();
    }

    /**
     * Get a global state value
     */
    getGlobalState(key, defaultValue = null) {
        return this.globalState.has(key) ? this.globalState.get(key) : defaultValue;
    }

    /**
     * Get all conversations
     */
    getAllConversations() {
        return Array.from(this.conversationState.entries()).map(([id, data]) => ({
            id,
            ...data
        }));
    }

    /**
     * Get active conversation
     */
    getActiveConversation() {
        if (!this.currentConversationId) {
            return null;
        }

        return this.conversationState.get(this.currentConversationId);
    }

    /**
     * Get conversation by ID
     */
    getConversation(conversationId) {
        return this.conversationState.get(conversationId) || null;
    }

    /**
     * Delete a conversation
     */
    deleteConversation(conversationId) {
        if (this.conversationState.has(conversationId)) {
            const conversation = this.conversationState.get(conversationId);

            this.conversationState.delete(conversationId);

            // If we deleted the current conversation, clear it
            if (this.currentConversationId === conversationId) {
                this.currentConversationId = null;
            }

            // Notify subscribers
            this.notifySubscribers('conversationDeleted', { id: conversationId, data: conversation });

            // Add to history
            this.addToHistory('deleteConversation', { id: conversationId });

            this.saveState();
            return true;
        }

        return false;
    }

    /**
     * Clear all conversations
     */
    clearAllConversations() {
        this.conversationState.clear();
        this.currentConversationId = null;

        // Notify subscribers
        this.notifySubscribers('allConversationsCleared');

        // Add to history
        this.addToHistory('clearAllConversations');

        this.saveState();
    }

    /**
     * Subscribe to state changes
     */
    subscribe(eventType, callback) {
        if (!this.stateSubscribers.has(eventType)) {
            this.stateSubscribers.set(eventType, []);
        }

        this.stateSubscribers.get(eventType).push(callback);

        // Return unsubscribe function
        return () => {
            this.unsubscribe(eventType, callback);
        };
    }

    /**
     * Unsubscribe from state changes
     */
    unsubscribe(eventType, callback) {
        if (this.stateSubscribers.has(eventType)) {
            const callbacks = this.stateSubscribers.get(eventType);
            const index = callbacks.indexOf(callback);
            if (index !== -1) {
                callbacks.splice(index, 1);
            }
        }
    }

    /**
     * Notify subscribers of a state change
     */
    notifySubscribers(eventType, data = null) {
        if (this.stateSubscribers.has(eventType)) {
            const callbacks = this.stateSubscribers.get(eventType);
            for (const callback of callbacks) {
                try {
                    callback(data);
                } catch (error) {
                    console.error(`Error in state subscriber for ${eventType}:`, error);
                }
            }
        }
    }

    /**
     * Add an entry to the state history
     */
    addToHistory(action, data) {
        const historyEntry = {
            action,
            data,
            timestamp: new Date().toISOString()
        };

        this.stateHistory.push(historyEntry);

        // Keep history size manageable
        if (this.stateHistory.length > this.maxHistorySize) {
            this.stateHistory = this.stateHistory.slice(-this.maxHistorySize);
        }
    }

    /**
     * Get state history
     */
    getHistory(limit = null) {
        if (limit) {
            return this.stateHistory.slice(-limit);
        }
        return this.stateHistory;
    }

    /**
     * Generate a unique conversation ID
     */
    generateConversationId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Generate a unique message ID
     */
    generateMessageId() {
        return 'msg_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Clear state history
     */
    clearHistory() {
        this.stateHistory = [];
    }

    /**
     * Export state for backup
     */
    exportState() {
        return {
            conversationState: Object.fromEntries(this.conversationState),
            globalState: Object.fromEntries(this.globalState),
            currentUser: this.currentUser,
            currentConversationId: this.currentConversationId,
            history: this.stateHistory,
            exportedAt: new Date().toISOString()
        };
    }

    /**
     * Import state from backup
     */
    importState(exportedState) {
        if (exportedState.conversationState) {
            this.conversationState = new Map(Object.entries(exportedState.conversationState));
        }

        if (exportedState.globalState) {
            this.globalState = new Map(Object.entries(exportedState.globalState));
        }

        this.currentUser = exportedState.currentUser || null;
        this.currentConversationId = exportedState.currentConversationId || null;
        this.stateHistory = exportedState.history || [];

        // Notify subscribers about the import
        this.notifySubscribers('stateImported', { importedAt: new Date().toISOString() });

        this.saveState();
    }

    /**
     * Get statistics about the state
     */
    getStats() {
        return {
            currentUser: this.currentUser,
            currentConversationId: this.currentConversationId,
            totalConversations: this.conversationState.size,
            totalMessages: Array.from(this.conversationState.values()).reduce((sum, conv) => sum + conv.messages.length, 0),
            globalStateKeys: this.globalState.size,
            historySize: this.stateHistory.length,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Reset the state manager to initial state
     */
    reset() {
        this.conversationState.clear();
        this.globalState.clear();
        this.stateHistory = [];
        this.currentUser = null;
        this.currentConversationId = null;

        // Notify subscribers
        this.notifySubscribers('stateReset');

        this.saveState();
    }

    /**
     * Destroy the state manager
     */
    destroy() {
        // Clear all state and history
        this.reset();

        // Clear subscribers
        this.stateSubscribers.clear();
    }
}

/**
 * Initialize the state manager when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', function() {
    const stateManager = new StateManager();
    stateManager.init();

    // Store instance globally for potential external access
    window.TodoStateManager = stateManager;
});

/**
 * Export for module systems (if needed)
 */
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StateManager;
}