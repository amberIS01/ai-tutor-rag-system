"""
Input Validation Module
Validates user inputs and file uploads
"""

from typing import Tuple
import re


def validate_pdf_filename(filename: str) -> Tuple[bool, str]:
    """
    Validate PDF filename
    
    Args:
        filename: Name of the uploaded file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filename:
        return False, "Filename cannot be empty"
    
    if not filename.lower().endswith('.pdf'):
        return False, "Only PDF files are allowed"
    
    # Check for dangerous characters
    dangerous_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    if any(char in filename for char in dangerous_chars):
        return False, "Filename contains invalid characters"
    
    if len(filename) > 255:
        return False, "Filename too long (max 255 characters)"
    
    return True, ""


def validate_question(question: str) -> Tuple[bool, str]:
    """
    Validate user question
    
    Args:
        question: User's question text
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not question or not question.strip():
        return False, "Question cannot be empty"
    
    if len(question) > 1000:
        return False, "Question too long (max 1000 characters)"
    
    if len(question) < 3:
        return False, "Question too short (min 3 characters)"
    
    return True, ""


def validate_topic_id(topic_id: str) -> Tuple[bool, str]:
    """
    Validate topic ID format
    
    Args:
        topic_id: Topic identifier
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not topic_id:
        return False, "Topic ID cannot be empty"
    
    # Only allow alphanumeric and underscores
    if not re.match(r'^[a-z0-9_]+$', topic_id):
        return False, "Invalid topic ID format"
    
    if len(topic_id) > 100:
        return False, "Topic ID too long"
    
    return True, ""




