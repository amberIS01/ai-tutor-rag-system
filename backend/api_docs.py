"""
API Documentation
Enhanced API documentation with examples
"""

from typing import Dict, Any


API_ENDPOINTS = {
    "POST /upload": {
        "description": "Upload a PDF file for processing",
        "request_body": {
            "file": "PDF file (multipart/form-data)"
        },
        "response": {
            "success": bool,
            "data": {
                "filename": str,
                "status": "processing"
            }
        },
        "status_codes": [200, 400, 413, 415]
    },
    "POST /chat": {
        "description": "Send a chat message and get AI response",
        "request_body": {
            "message": str,
            "pdf_filename": str
        },
        "response": {
            "success": bool,
            "data": {
                "response": str,
                "relevant_chunks": list,
                "images": list
            }
        },
        "status_codes": [200, 400, 404, 500]
    },
    "GET /health": {
        "description": "Check API health status",
        "response": {
            "status": "healthy|degraded|unhealthy",
            "resources": dict
        },
        "status_codes": [200]
    },
    "GET /files": {
        "description": "List all uploaded PDF files",
        "response": {
            "success": bool,
            "data": list
        },
        "status_codes": [200]
    },
    "DELETE /files/{filename}": {
        "description": "Delete a PDF file and associated data",
        "response": {
            "success": bool,
            "message": str
        },
        "status_codes": [200, 404]
    }
}


RESPONSE_STATUS_CODES = {
    200: "Request successful",
    400: "Bad request - invalid parameters",
    404: "Resource not found",
    413: "File too large",
    415: "Unsupported media type",
    429: "Rate limit exceeded",
    500: "Internal server error"
}


def get_api_documentation() -> Dict[str, Any]:
    """Get complete API documentation"""
    return {
        "title": "AI Tutor RAG System API",
        "version": "1.0.0",
        "description": "API for PDF-based learning with RAG",
        "endpoints": API_ENDPOINTS,
        "status_codes": RESPONSE_STATUS_CODES
    }
