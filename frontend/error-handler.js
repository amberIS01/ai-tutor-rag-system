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
     * @param {Object} options - Additional options
     * @returns {string} User-friendly message
     */
    getUserMessage(error, options = {}) {
        const messageMap = {
            'NetworkError': 'Network error. Please check your internet connection and try again.',
            'TypeError': 'An unexpected error occurred. Please refresh the page and try again.',
            'SyntaxError': 'Invalid response from server. The server may be experiencing issues.',
            'AbortError': 'Request timed out. The server is taking too long to respond.',
            'RateLimitError': 'Too many requests. Please wait a moment and try again.',
            'ValidationError': 'Invalid input. Please check your input and try again.',
            'AuthenticationError': 'Authentication failed. Please log in again.',
            'ServerError': 'Server error. Please try again later.'
        };

        // Check for HTTP status codes
        if (options.statusCode) {
            if (options.statusCode === 429) return messageMap['RateLimitError'];
            if (options.statusCode === 401 || options.statusCode === 403) return messageMap['AuthenticationError'];
            if (options.statusCode >= 500) return messageMap['ServerError'];
        }

        return messageMap[error.constructor.name] || 
               error.message || 
               'An unexpected error occurred. Please try again.';
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
