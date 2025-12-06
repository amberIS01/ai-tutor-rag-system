"""
Custom Exceptions
Application-specific exception classes
"""


class PDFProcessingError(Exception):
    """Raised when PDF processing fails"""
    pass


class EmbeddingGenerationError(Exception):
    """Raised when embedding generation fails"""
    pass


class VectorStoreError(Exception):
    """Raised when vector store operations fail"""
    pass


class LLMAPIError(Exception):
    """Raised when LLM API call fails"""
    pass


class FileValidationError(Exception):
    """Raised when file validation fails"""
    pass

