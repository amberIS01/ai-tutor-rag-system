# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-11-17

### Added
- Initial release of AI Tutor RAG System
- PDF upload and processing functionality
- Vector embeddings with FAISS
- Semantic search for text chunks
- Automatic image retrieval and display
- Chat interface with real-time responses
- Anti-hallucination prompts for grounded answers
- File size validation (50MB limit)
- Request timeout handling
- Centralized logging system
- Health monitoring system
- Utility functions for file handling
- Comprehensive documentation
- Mobile-responsive design

### Features
- Dynamic PDF processing (not hardcoded)
- Retrieval Augmented Generation (RAG) pipeline
- 384-dimensional embeddings using Sentence-Transformers
- Fast similarity search with FAISS
- Integration with Mistral Small 24B via OpenRouter
- Beautiful, modern UI with smooth animations
- Real-time status indicators
- Error handling with fallback responses

### Technical
- Backend: FastAPI + Python
- Frontend: HTML/CSS/JavaScript
- Vector DB: FAISS
- LLM: Mistral Small 24B (via OpenRouter)
- Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)

### Security
- API keys in environment variables
- File type and size validation
- Proper .gitignore configuration
- CORS protection

## [Unreleased]

### Planned
- Multi-PDF management
- User authentication
- Chat history persistence
- Export conversations
- Custom model selection
- Batch processing
- Advanced analytics





