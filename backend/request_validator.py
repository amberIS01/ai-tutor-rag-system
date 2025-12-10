"""
Request Validation Module
Comprehensive request validation
"""

from typing import Dict, Any, List, Tuple
from pydantic import BaseModel, Field, validator


class UploadRequest(BaseModel):
    """PDF upload request model"""
    filename: str = Field(..., min_length=1, max_length=255)
    file_size: int = Field(..., gt=0, le=52428800)  # Max 50MB


class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., min_length=1, max_length=1000)
    pdf_filename: str = Field(..., min_length=1, max_length=255)
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class UserRequest(BaseModel):
    """User request model"""
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class PaginationRequest(BaseModel):
    """Pagination request model"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1, le=100)


class RequestValidator:
    """Validate and sanitize requests"""
    
    @staticmethod
    def validate_file_extension(filename: str, allowed_extensions: List[str]) -> Tuple[bool, str]:
        """Validate file extension"""
        if not any(filename.lower().endswith(ext) for ext in allowed_extensions):
            return False, f"File type not allowed. Allowed: {', '.join(allowed_extensions)}"
        return True, ""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Validate email format"""
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, email):
            return False, "Invalid email format"
        return True, ""
    
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, List[str]]:
        """Validate password strength"""
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in password):
            issues.append("Password must contain uppercase letter")
        if not any(c.islower() for c in password):
            issues.append("Password must contain lowercase letter")
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain number")
        if not any(c in '!@#$%^&*' for c in password):
            issues.append("Password must contain special character")
        
        return len(issues) == 0, issues
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """Sanitize string input"""
        # Remove null bytes
        value = value.replace('\x00', '')
        # Trim to max length
        value = value[:max_length]
        return value.strip()
