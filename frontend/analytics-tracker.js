// Frontend analytics tracking
class AnalyticsTracker {
    constructor(apiBaseUrl = CONFIG.API_BASE_URL) {
        this.apiBaseUrl = apiBaseUrl;
        this.sessionId = this.generateSessionId();
        this.events = [];
        this.batchSize = 10;
        this.flushInterval = 30000; // 30 seconds

        this.startBatchFlush();
    }

    /**
     * Generate unique session ID
     */
    generateSessionId() {
        return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }

    /**
     * Track event
     * @param {string} eventType - Event type
     * @param {Object} data - Event data
     */
    track(eventType, data = {}) {
        const event = {
            type: eventType,
            timestamp: new Date().toISOString(),
            sessionId: this.sessionId,
            url: window.location.href,
            userAgent: navigator.userAgent,
            data
        };

        this.events.push(event);

        if (this.events.length >= this.batchSize) {
            this.flush();
        }
    }

    /**
     * Track page view
     */
    trackPageView() {
        this.track('pageview', {
            title: document.title,
            path: window.location.pathname
        });
    }

    /**
     * Track click event
     * @param {HTMLElement} element - Clicked element
     */
    trackClick(element) {
        this.track('click', {
            elementId: element.id,
            elementClass: element.className,
            elementText: element.textContent?.substring(0, 50)
        });
    }

    /**
     * Track form submission
     * @param {string} formId - Form ID
     */
    trackFormSubmit(formId) {
        this.track('form_submit', {
            formId
        });
    }

    /**
     * Track error
     * @param {string} message - Error message
     * @param {string} stack - Error stack
     */
    trackError(message, stack = '') {
        this.track('error', {
            message,
            stack: stack.substring(0, 500)
        });
    }

    /**
     * Flush events to server
     */
    async flush() {
        if (this.events.length === 0) return;

        const eventsToSend = this.events.slice();
        this.events = [];

        try {
            await fetch(`${this.apiBaseUrl}/analytics/events`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ events: eventsToSend })
            });
        } catch (error) {
            console.error('Failed to flush analytics:', error);
            // Re-add events if flush failed
            this.events = eventsToSend.concat(this.events);
        }
    }

    /**
     * Start batch flush interval
     */
    startBatchFlush() {
        setInterval(() => this.flush(), this.flushInterval);

        // Flush on page unload
        window.addEventListener('beforeunload', () => this.flush());
    }

    /**
     * Get session info
     */
    getSessionInfo() {
        return {
            sessionId: this.sessionId,
            eventsCount: this.events.length
        };
    }
}

// Global analytics tracker
const analyticsTracker = new AnalyticsTracker();
