// Frontend error handler
class ErrorHandler {
    constructor() {
        this.errorLog = [];
        this.maxLogSize = 100;
    }

    /**
     * Handle error
     * @param {Error} error - Error object
     * @param {string} context - Error context
     */
    handle(error, context = 'Unknown') {
        const errorEntry = {
            timestamp: new Date().toISOString(),
            context,
            message: error.message,
            stack: error.stack,
            type: error.constructor.name
        };

        this.errorLog.push(errorEntry);
        if (this.errorLog.length > this.maxLogSize) {
            this.errorLog.shift();
        }

        console.error(`[${context}] ${error.message}`, error);
        return errorEntry;
    }

    /**
     * Get user-friendly error message
     * @param {Error} error - Error object
     * @returns {string} User-friendly message
     */
    getUserMessage(error) {
        const messageMap = {
            'NetworkError': 'Network error. Please check your connection.',
            'TypeError': 'An unexpected error occurred. Please try again.',
            'SyntaxError': 'Invalid response from server. Please try again.',
            'AbortError': 'Request timeout. Please try again.'
        };

        return messageMap[error.constructor.name] || 
               error.message || 
               'An unexpected error occurred.';
    }

    /**
     * Get error log
     */
    getLog() {
        return this.errorLog;
    }

    /**
     * Clear error log
     */
    clearLog() {
        this.errorLog = [];
    }

    /**
     * Export error log
     */
    exportLog() {
        return JSON.stringify(this.errorLog, null, 2);
    }
}

// Global error handler
const errorHandler = new ErrorHandler();

// Global error event listeners
window.addEventListener('error', (event) => {
    errorHandler.handle(event.error, 'Uncaught Error');
});

window.addEventListener('unhandledrejection', (event) => {
    errorHandler.handle(event.reason, 'Unhandled Promise Rejection');
});
