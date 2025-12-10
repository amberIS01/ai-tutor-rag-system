// Frontend notification system
class NotificationManager {
    constructor() {
        this.notifications = [];
        this.container = null;
    }

    /**
     * Initialize notification container
     */
    init() {
        if (document.getElementById('notification-container')) return;

        this.container = document.createElement('div');
        this.container.id = 'notification-container';
        this.container.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 10000;
            max-width: 400px;
        `;
        document.body.appendChild(this.container);
    }

    /**
     * Show notification
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, info, warning)
     * @param {number} duration - Duration in milliseconds
     */
    show(message, type = 'info', duration = 5000) {
        if (!this.container) this.init();

        const notification = document.createElement('div');
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            info: '#3b82f6',
            warning: '#f59e0b'
        };

        notification.style.cssText = `
            background-color: ${colors[type] || colors.info};
            color: white;
            padding: 16px;
            margin-bottom: 10px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            animation: slideIn 0.3s ease-out;
        `;

        notification.textContent = message;
        this.container.appendChild(notification);

        if (duration > 0) {
            setTimeout(() => {
                notification.style.animation = 'slideOut 0.3s ease-out';
                setTimeout(() => notification.remove(), 300);
            }, duration);
        }

        return notification;
    }

    /**
     * Show success notification
     */
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    /**
     * Show error notification
     */
    error(message, duration = 5000) {
        return this.show(message, 'error', duration);
    }

    /**
     * Show info notification
     */
    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
    }

    /**
     * Show warning notification
     */
    warning(message, duration = 5000) {
        return this.show(message, 'warning', duration);
    }
}

// Global notification manager
const notificationManager = new NotificationManager();

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
