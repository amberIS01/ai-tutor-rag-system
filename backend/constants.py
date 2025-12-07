"""
Application Constants
Centralized constants for the application
"""

# API Response Messages
MSG_PDF_UPLOAD_SUCCESS = "PDF processed successfully"
MSG_PDF_UPLOAD_ERROR = "Error processing PDF"
MSG_CHAT_ERROR = "Error generating response"
MSG_SERVER_ERROR = "Internal server error"
MSG_INVALID_FILE_TYPE = "Only PDF files are allowed"
MSG_FILE_TOO_LARGE = "File size exceeds maximum limit"

# File Processing
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_DIM = 384

# API Limits
MAX_RETRIES = 3
REQUEST_TIMEOUT = 60
MAX_TOKENS = 500

# Status Codes
STATUS_SUCCESS = "success"
STATUS_ERROR = "error"
STATUS_PROCESSING = "processing"



