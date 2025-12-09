// API Service Module
// Centralized API calls

class APIService {
    constructor(baseURL = CONFIG.API_BASE_URL) {
        this.baseURL = baseURL;
        this.timeout = CONFIG.REQUEST_TIMEOUT_MS;
    }

    /**
     * Upload PDF file
     * @param {File} file - PDF file to upload
     * @returns {Promise<Object>} Upload response
     */
    async uploadPDF(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${this.baseURL}/upload`, {
                method: 'POST',
                body: formData,
                signal: AbortSignal.timeout(this.timeout)
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Upload error:', error);
            throw error;
        }
    }

    /**
     * Send chat message
     * @param {string} message - User message
     * @param {string} pdfFilename - PDF filename
     * @returns {Promise<Object>} Chat response
     */
    async sendMessage(message, pdfFilename) {
        try {
            const response = await fetch(`${this.baseURL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message,
                    pdf_filename: pdfFilename
                }),
                signal: AbortSignal.timeout(this.timeout)
            });

            if (!response.ok) {
                throw new Error(`Chat failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Chat error:', error);
            throw error;
        }
    }

    /**
     * Get health status
     * @returns {Promise<Object>} Health status
     */
    async getHealth() {
        try {
            const response = await fetch(`${this.baseURL}/health`, {
                signal: AbortSignal.timeout(this.timeout)
            });

            if (!response.ok) {
                throw new Error(`Health check failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Health check error:', error);
            throw error;
        }
    }

    /**
     * Get list of uploaded files
     * @returns {Promise<Object>} Files list
     */
    async getFiles() {
        try {
            const response = await fetch(`${this.baseURL}/files`, {
                signal: AbortSignal.timeout(this.timeout)
            });

            if (!response.ok) {
                throw new Error(`Failed to get files: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Get files error:', error);
            throw error;
        }
    }

    /**
     * Delete a file
     * @param {string} filename - Filename to delete
     * @returns {Promise<Object>} Delete response
     */
    async deleteFile(filename) {
        try {
            const response = await fetch(`${this.baseURL}/files/${filename}`, {
                method: 'DELETE',
                signal: AbortSignal.timeout(this.timeout)
            });

            if (!response.ok) {
                throw new Error(`Delete failed: ${response.statusText}`);
            }

            return await response.json();
        } catch (error) {
            console.error('Delete error:', error);
            throw error;
        }
    }
}

// Export API service
const apiService = new APIService();
