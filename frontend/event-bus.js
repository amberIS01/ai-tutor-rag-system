// Frontend event bus for component communication
class EventBus {
    constructor() {
        this.listeners = new Map();
        this.eventHistory = [];
        this.maxHistory = 100;
    }

    /**
     * Subscribe to event
     * @param {string} eventType - Event type
     * @param {Function} listener - Event listener
     * @returns {Function} Unsubscribe function
     */
    on(eventType, listener) {
        if (!this.listeners.has(eventType)) {
            this.listeners.set(eventType, []);
        }

        const listeners = this.listeners.get(eventType);
        listeners.push(listener);

        // Return unsubscribe function
        return () => {
            const index = listeners.indexOf(listener);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        };
    }

    /**
     * Subscribe to event (one-time)
     * @param {string} eventType - Event type
     * @param {Function} listener - Event listener
     */
    once(eventType, listener) {
        const unsubscribe = this.on(eventType, (data) => {
            listener(data);
            unsubscribe();
        });

        return unsubscribe;
    }

    /**
     * Emit event
     * @param {string} eventType - Event type
     * @param {*} data - Event data
     */
    emit(eventType, data = null) {
        const event = {
            type: eventType,
            data,
            timestamp: new Date().toISOString()
        };

        this.eventHistory.push(event);
        if (this.eventHistory.length > this.maxHistory) {
            this.eventHistory.shift();
        }

        if (this.listeners.has(eventType)) {
            const listeners = this.listeners.get(eventType);
            listeners.forEach(listener => {
                try {
                    listener(data);
                } catch (error) {
                    console.error(`Event listener error (${eventType}):`, error);
                }
            });
        }
    }

    /**
     * Remove all listeners for event
     * @param {string} eventType - Event type
     */
    off(eventType) {
        if (eventType) {
            this.listeners.delete(eventType);
        } else {
            this.listeners.clear();
        }
    }

    /**
     * Get listener count
     * @param {string} eventType - Event type
     */
    listenerCount(eventType) {
        if (!this.listeners.has(eventType)) {
            return 0;
        }
        return this.listeners.get(eventType).length;
    }

    /**
     * Get event history
     */
    getHistory() {
        return this.eventHistory;
    }

    /**
     * Clear event history
     */
    clearHistory() {
        this.eventHistory = [];
    }
}

// Global event bus
const eventBus = new EventBus();

// Common event types
const Events = {
    FILE_UPLOADED: 'file_uploaded',
    FILE_DELETED: 'file_deleted',
    CHAT_MESSAGE_SENT: 'chat_message_sent',
    CHAT_MESSAGE_RECEIVED: 'chat_message_received',
    API_ERROR: 'api_error',
    API_SUCCESS: 'api_success',
    UPLOAD_PROGRESS: 'upload_progress',
    THEME_CHANGED: 'theme_changed'
};
