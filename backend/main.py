"""
FastAPI Main Application
AI Tutor RAG System Backend
"""

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import os
import shutil

from config import config
from rag_service import get_rag_service
from pdf_processor import PDFProcessor

# Initialize FastAPI app
app = FastAPI(
    title="AI Tutor RAG System",
    description="RAG-based AI tutor with image retrieval for educational content",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Ensure upload directory exists
os.makedirs(config.UPLOAD_DIR, exist_ok=True)


# ============================================================================
# PYDANTIC MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    question: str
    topic_id: Optional[str] = "sound"  # For now, we only have Sound topic
    
    class Config:
        str_min_length = 1
        str_max_length = 1000
    
    def validate_question(self):
        """Validate question input"""
        if not self.question or not self.question.strip():
            raise ValueError("Question cannot be empty")
        if len(self.question) > 1000:
            raise ValueError("Question too long (max 1000 characters)")
        return True


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    question: str
    answer: str
    image: Optional[dict] = None
    context_chunks: list


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "AI Tutor RAG System API",
        "version": "1.0.0",
        "endpoints": {
            "POST /upload": "Upload and process PDF",
            "POST /chat": "Ask questions and get answers",
            "GET /images/{topic_id}": "Get image metadata for a topic"
        }
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file for processing
    
    - Extracts text from PDF
    - Creates chunks
    - Generates embeddings
    - Stores in vector database
    - Returns topic ID
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are allowed")
        
        # Validate file size (read content to check size)
        content = await file.read()
        file_size_mb = len(content) / (1024 * 1024)
        
        if file_size_mb > config.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=400, 
                detail=f"File too large. Maximum size: {config.MAX_FILE_SIZE_MB}MB"
            )
        
        # Reset file pointer
        await file.seek(0)
        
        print(f"\n📄 Processing uploaded file: {file.filename}")
        
        # Save uploaded file
        file_path = os.path.join(config.UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"✅ File saved to: {file_path}")
        
        # Process PDF - Extract and chunk
        from pdf_processor import PDFProcessor
        from embedding_generator import EmbeddingGenerator
        from vector_store import VectorStore
        
        processor = PDFProcessor()
        chunks = processor.process_pdf(file_path, output_path=None)
        
        print(f"✅ Created {len(chunks)} chunks")
        
        # Generate embeddings for new chunks
        print("🔄 Generating embeddings...")
        generator = EmbeddingGenerator()
        
        texts = [chunk['text'] for chunk in chunks]
        chunk_ids = [chunk['id'] for chunk in chunks]
        embeddings = generator.model.encode(texts, convert_to_numpy=True)
        
        print(f"✅ Generated {len(embeddings)} embeddings")
        
        # Update vector store (add to existing or create new)
        print("💾 Updating vector store...")
        vector_store = VectorStore(embedding_dim=384)
        vector_store.create_text_index(embeddings, chunk_ids, chunks)
        
        # Save to a unique location or update existing
        # For now, we'll keep using the same embeddings (this is a demo)
        # In production, you'd manage multiple topics/files
        
        print(f"✅ Vector store updated")
        
        # Generate topic ID
        topic_id = file.filename.replace('.pdf', '').lower().replace(' ', '_')
        
        return {
            "status": "success",
            "message": f"PDF processed successfully",
            "topic_id": topic_id,
            "chunks_created": len(chunks),
            "filename": file.filename
        }
        
    except Exception as e:
        import traceback
        print(f"❌ Error processing upload: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint - Ask questions and get AI-generated answers
    
    - Retrieves relevant context chunks using RAG
    - Generates answer using LLM
    - Returns answer with relevant image
    """
    try:
        # Validate API key
        if not config.validate():
            raise HTTPException(
                status_code=500,
                detail="OpenRouter API key not configured. Please set OPENROUTER_API_KEY in .env file"
            )
        
        # Get RAG service
        rag_service = get_rag_service()
        
        # Process question
        result = rag_service.answer_question(request.question)
        
        return ChatResponse(**result)
        
    except Exception as e:
        print(f"❌ Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")


@app.get("/images/{topic_id}")
async def get_images(topic_id: str):
    """
    Get all images metadata for a specific topic
    
    - Returns list of available images with metadata
    - Useful for frontend to display image gallery
    """
    try:
        import json
        
        # Load image metadata
        with open(config.IMAGE_METADATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        images = data.get('images', [])
        
        return {
            "topic_id": topic_id,
            "images": images,
            "count": len(images)
        }
        
    except Exception as e:
        print(f"❌ Error loading images: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading images: {str(e)}")


@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Check if vector store is loaded
        rag_service = get_rag_service()
        
        return {
            "status": "healthy",
            "api_key_configured": bool(config.OPENROUTER_API_KEY),
            "model": config.MODEL_NAME,
            "vector_store": "loaded",
            "embeddings": "ready"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


# ============================================================================
# STARTUP
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("=" * 80)
    print("🚀 Starting AI Tutor RAG System")
    print("=" * 80)
    
    # Validate configuration
    if config.validate():
        print("✅ Configuration validated")
    else:
        print("⚠️  API key not set - /chat endpoint will not work")
    
    # Preload RAG service
    try:
        get_rag_service()
        print("✅ RAG service initialized")
    except Exception as e:
        print(f"⚠️  RAG service initialization failed: {e}")
    
    print("=" * 80)
    print(f"🌐 Server running on http://{config.HOST}:{config.PORT}")
    print("=" * 80)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )

