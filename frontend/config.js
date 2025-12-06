// Frontend Configuration
const CONFIG = {
    API_BASE_URL: 'http://localhost:8000',
    MAX_MESSAGE_LENGTH: 1000,
    MAX_FILE_SIZE_MB: 50,
    ALLOWED_FILE_TYPES: ['.pdf'],
    RETRY_ATTEMPTS: 3,
    RETRY_DELAY_MS: 1000,
    REQUEST_TIMEOUT_MS: 60000,
    AUTO_SCROLL_DELAY: 100,
    VERSION: '1.0.0'
};

// Export for use in app.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CONFIG;
}

