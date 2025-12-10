// Frontend storage utilities
class StorageManager {
    constructor(prefix = 'ai-tutor') {
        this.prefix = prefix;
    }

    /**
     * Get storage key with prefix
     * @param {string} key - Storage key
     * @returns {string} Prefixed key
     */
    getKey(key) {
        return `${this.prefix}:${key}`;
    }

    /**
     * Save to localStorage
     * @param {string} key - Storage key
     * @param {*} value - Value to store
     */
    set(key, value) {
        try {
            const serialized = JSON.stringify(value);
            localStorage.setItem(this.getKey(key), serialized);
            return true;
        } catch (error) {
            console.error('Storage set error:', error);
            return false;
        }
    }

    /**
     * Get from localStorage
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if not found
     */
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(this.getKey(key));
            return item ? JSON.parse(item) : defaultValue;
        } catch (error) {
            console.error('Storage get error:', error);
            return defaultValue;
        }
    }

    /**
     * Remove from localStorage
     * @param {string} key - Storage key
     */
    remove(key) {
        try {
            localStorage.removeItem(this.getKey(key));
            return true;
        } catch (error) {
            console.error('Storage remove error:', error);
            return false;
        }
    }

    /**
     * Clear all stored data
     */
    clear() {
        try {
            const keys = Object.keys(localStorage);
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    localStorage.removeItem(key);
                }
            });
            return true;
        } catch (error) {
            console.error('Storage clear error:', error);
            return false;
        }
    }

    /**
     * Get all stored items
     */
    getAll() {
        const items = {};
        const keys = Object.keys(localStorage);
        
        keys.forEach(key => {
            if (key.startsWith(this.prefix)) {
                const cleanKey = key.replace(`${this.prefix}:`, '');
                items[cleanKey] = this.get(cleanKey);
            }
        });

        return items;
    }

    /**
     * Get storage size
     */
    getSize() {
        let size = 0;
        const items = this.getAll();
        
        Object.values(items).forEach(item => {
            size += JSON.stringify(item).length;
        });

        return size;
    }
}

// Global storage manager
const storageManager = new StorageManager('ai-tutor');
