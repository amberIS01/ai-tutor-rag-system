// Frontend storage utilities with caching support
class StorageManager {
    constructor(prefix = 'ai-tutor') {
        this.prefix = prefix;
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
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
     * Get from localStorage with caching
     * @param {string} key - Storage key
     * @param {*} defaultValue - Default value if not found
     * @param {boolean} useCache - Use in-memory cache
     */
    get(key, defaultValue = null, useCache = true) {
        try {
            // Check cache first
            if (useCache && this.cache.has(key)) {
                const cached = this.cache.get(key);
                if (Date.now() - cached.timestamp < this.cacheTimeout) {
                    return cached.value;
                }
                this.cache.delete(key);
            }

            const item = localStorage.getItem(this.getKey(key));
            const value = item ? JSON.parse(item) : defaultValue;

            // Update cache
            if (useCache && value !== defaultValue) {
                this.cache.set(key, {
                    value,
                    timestamp: Date.now()
                });
            }

            return value;
        } catch (error) {
            console.error('Storage get error:', error);
            return defaultValue;
        }
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
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
