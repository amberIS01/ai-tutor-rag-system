// ============================================================================
// AI Tutor Chat Application
// ============================================================================

const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('userInput');
const sendButton = document.getElementById('sendButton');
const loadingIndicator = document.getElementById('loadingIndicator');
const statusElement = document.getElementById('status');
const uploadSection = document.getElementById('uploadSection');
const inputContainer = document.getElementById('inputContainer');
const pdfInput = document.getElementById('pdfInput');
const selectPdfButton = document.getElementById('selectPdfButton');
const uploadPdfButton = document.getElementById('uploadPdfButton');
const selectedFileDiv = document.getElementById('selectedFile');
const uploadProgress = document.getElementById('uploadProgress');

// State
let currentTopicId = null;
let selectedFile = null;

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    checkServerStatus();
    setupEventListeners();
});

// ============================================================================
// Event Listeners
// ============================================================================

function setupEventListeners() {
    // Send button click
    sendButton.addEventListener('click', handleSendMessage);
    
    // Enter key press
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });
    
    // PDF upload listeners
    selectPdfButton.addEventListener('click', () => pdfInput.click());
    
    pdfInput.addEventListener('change', (e) => {
        selectedFile = e.target.files[0];
        if (selectedFile) {
            selectedFileDiv.innerHTML = `📄 ${selectedFile.name}`;
            selectedFileDiv.style.display = 'block';
            uploadPdfButton.style.display = 'inline-block';
        }
    });
    
    uploadPdfButton.addEventListener('click', handlePdfUpload);
}

// ============================================================================
// Server Status Check
// ============================================================================

async function checkServerStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        if (data.status === 'healthy') {
            updateStatus('online', 'Connected');
        } else {
            updateStatus('offline', 'Server Issue');
        }
    } catch (error) {
        updateStatus('offline', 'Offline');
        console.error('Server connection failed:', error);
    }
}

function updateStatus(status, text) {
    statusElement.className = `status ${status}`;
    statusElement.querySelector('.status-text').textContent = text;
}

// ============================================================================
// PDF Upload Handling
// ============================================================================

async function handlePdfUpload() {
    if (!selectedFile) return;
    
    // Show progress
    uploadProgress.style.display = 'block';
    selectPdfButton.disabled = true;
    uploadPdfButton.disabled = true;
    
    try {
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Upload failed: ${response.status}`);
        }
        
        const data = await response.json();
        currentTopicId = data.topic_id;
        
        // Hide upload section, show chat
        uploadSection.style.display = 'none';
        chatContainer.style.display = 'flex';
        inputContainer.style.display = 'block';
        
        // Enable chat
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
        
        // Add welcome message
        addWelcomeMessage(selectedFile.name, data.chunks_created);
        
    } catch (error) {
        console.error('Upload error:', error);
        alert('Failed to upload PDF. Please make sure the backend is running and try again.');
        
        // Reset UI
        uploadProgress.style.display = 'none';
        selectPdfButton.disabled = false;
        uploadPdfButton.disabled = false;
    }
}

function addWelcomeMessage(filename, chunkCount) {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    contentDiv.innerHTML = `
        <p><strong>✅ PDF Processed Successfully!</strong></p>
        <p><strong>File:</strong> ${filename}</p>
        <p><strong>Chunks created:</strong> ${chunkCount}</p>
        <p>I've analyzed your document and I'm ready to answer questions!</p>
        <p>Try asking me anything about the content...</p>
    `;
    
    messageDiv.appendChild(contentDiv);
    chatContainer.appendChild(messageDiv);
}

// ============================================================================
// Message Handling
// ============================================================================

async function handleSendMessage() {
    const question = userInput.value.trim();
    
    if (!question) return;
    
    // Disable input
    userInput.disabled = true;
    sendButton.disabled = true;
    
    // Add user message to chat
    addMessage('user', question);
    
    // Clear input
    userInput.value = '';
    
    // Show loading
    showLoading(true);
    
    try {
        // Call API
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add bot response with image
        addMessage('bot', data.answer, data.image);
        
    } catch (error) {
        console.error('Error:', error);
        addMessage('bot', 
            '❌ Sorry, I encountered an error. Please make sure the backend server is running and try again.', 
            null, 
            true
        );
    } finally {
        // Re-enable input
        showLoading(false);
        userInput.disabled = false;
        sendButton.disabled = false;
        userInput.focus();
    }
}

// ============================================================================
// UI Functions
// ============================================================================

function addMessage(type, text, image = null, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = `message-content ${isError ? 'error-message' : ''}`;
    
    // Format text (convert newlines to paragraphs)
    const paragraphs = text.split('\n\n').filter(p => p.trim());
    paragraphs.forEach(paragraph => {
        const p = document.createElement('p');
        p.textContent = paragraph.trim();
        contentDiv.appendChild(p);
    });
    
    messageDiv.appendChild(contentDiv);
    
    // Add image if provided
    if (image && type === 'bot') {
        const imageDiv = document.createElement('div');
        imageDiv.className = 'message-image';
        
        const img = document.createElement('img');
        img.src = `pics/${image.filename}`;
        img.alt = image.title;
        img.onerror = () => {
            img.style.display = 'none';
            console.error('Image not found:', image.filename);
        };
        
        const caption = document.createElement('div');
        caption.className = 'image-caption';
        caption.textContent = `📊 ${image.title}`;
        
        imageDiv.appendChild(img);
        imageDiv.appendChild(caption);
        contentDiv.appendChild(imageDiv);
    }
    
    chatContainer.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollToBottom();
}

function showLoading(show) {
    if (show) {
        loadingIndicator.classList.add('active');
    } else {
        loadingIndicator.classList.remove('active');
    }
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ============================================================================
// Utility Functions
// ============================================================================

// Format timestamps (if needed)
function getTimestamp() {
    const now = new Date();
    return now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Log for debugging
function log(message, data = null) {
    console.log(`[AI Tutor] ${message}`, data || '');
}

