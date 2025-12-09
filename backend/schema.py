"""
Database Schema
Defines data models and database structure
"""

from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PDFMetadata:
    """PDF file metadata"""
    filename: str
    upload_time: datetime
    file_size: int
    page_count: int
    chunk_count: int
    status: str  # "processing", "completed", "failed"
    error_message: str = None


@dataclass
class TextChunk:
    """Text chunk from PDF"""
    chunk_id: str
    pdf_filename: str
    page_number: int
    content: str
    embedding_id: str = None


@dataclass
class ImageData:
    """Image metadata from PDF"""
    image_id: str
    pdf_filename: str
    page_number: int
    image_path: str
    related_text: str = None
    embedding_id: str = None


@dataclass
class ChatMessage:
    """Chat message in conversation"""
    message_id: str
    timestamp: datetime
    user_question: str
    ai_response: str
    relevant_chunks: List[str]
    retrieved_images: List[str]
    model: str


class DatabaseSchema:
    """Database schema definition"""
    
    TABLES = {
        "pdf_metadata": ["filename", "upload_time", "file_size", "page_count"],
        "text_chunks": ["chunk_id", "pdf_filename", "page_number", "content"],
        "images": ["image_id", "pdf_filename", "page_number", "image_path"],
        "chat_history": ["message_id", "timestamp", "user_question", "ai_response"],
        "embeddings": ["embedding_id", "chunk_id", "vector_data"]
    }
