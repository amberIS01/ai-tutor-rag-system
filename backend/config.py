"""
Configuration Module
Handles environment variables and app settings
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration"""
    
    # OpenRouter API
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    # Model settings
    MODEL_NAME = os.getenv(
        "MODEL_NAME", 
        "mistralai/mistral-small-3.2-24b-instruct:free"
    )
    
    # Server settings
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # CORS settings
    ALLOWED_ORIGINS = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5500"
    ).split(",")
    
    # Paths
    CHUNKS_FILE = "data/chunks.json"
    IMAGE_METADATA_FILE = "data/image_metadata.json"
    EMBEDDINGS_DIR = "data/embeddings"
    UPLOAD_DIR = "data/uploads"
    
    # RAG settings
    TOP_K_CHUNKS = 3  # Number of chunks to retrieve
    TOP_K_IMAGES = 1  # Number of images to retrieve
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENROUTER_API_KEY:
            print("⚠️  WARNING: OPENROUTER_API_KEY not set!")
            print("   Please create a .env file with your API key")
            print("   Get your key at: https://openrouter.ai/keys")
            return False
        return True


# Create config instance
config = Config()

