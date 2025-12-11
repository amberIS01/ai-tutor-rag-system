// Frontend state management
class StateManager {
    constructor() {
        this.state = {
            currentFile: null,
            uploadProgress: 0,
            isProcessing: false,
            isLoading: false,
            loadingMessage: '',
            chatHistory: [],
            uploadedFiles: [],
            apiStatus: 'unknown',
            userPreferences: this.loadPreferences()
        };
        this.subscribers = [];
    }

    /**
     * Subscribe to state changes
     * @param {Function} callback - Callback function
     */
    subscribe(callback) {
        this.subscribers.push(callback);
        return () => {
            this.subscribers = this.subscribers.filter(sub => sub !== callback);
        };
    }

    /**
     * Notify all subscribers of state change
     */
    notifySubscribers() {
        this.subscribers.forEach(callback => callback(this.state));
    }

    /**
     * Update state
     * @param {Object} updates - State updates
     */
    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.notifySubscribers();
    }

    /**
     * Add chat message
     * @param {string} role - Message role (user/assistant)
     * @param {string} content - Message content
     */
    addChatMessage(role, content) {
        const message = {
            id: Date.now(),
            role,
            content,
            timestamp: new Date().toISOString()
        };
        const updated = [...this.state.chatHistory, message];
        this.setState({ chatHistory: updated });
        return message;
    }

    /**
     * Clear chat history
     */
    clearChatHistory() {
        this.setState({ chatHistory: [] });
    }

    /**
     * Load user preferences from localStorage
     */
    loadPreferences() {
        const stored = localStorage.getItem('userPreferences');
        return stored ? JSON.parse(stored) : {
            theme: 'light',
            autoScroll: true,
            notifications: true
        };
    }

    /**
     * Save user preferences
     * @param {Object} preferences - User preferences
     */
    savePreferences(preferences) {
        const updated = { ...this.state.userPreferences, ...preferences };
        localStorage.setItem('userPreferences', JSON.stringify(updated));
        this.setState({ userPreferences: updated });
    }

    /**
     * Set loading state
     * @param {boolean} isLoading - Loading state
     * @param {string} message - Loading message
     */
    setLoading(isLoading, message = '') {
        this.setState({ 
            isLoading, 
            loadingMessage: message 
        });
    }

    /**
     * Get current state
     */
    getState() {
        return this.state;
    }
}

// Global state manager instance
const stateManager = new StateManager();
