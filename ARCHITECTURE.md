# 🏗️ System Architecture

## Overview

AI Tutor is a Retrieval Augmented Generation (RAG) system that provides grounded, context-aware answers from educational PDFs.

```
┌─────────────────────────────────────────────────────────┐
│                      USER                                │
│                    (Browser)                             │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (Port 5500)                        │
│  ┌──────────────────────────────────────────────────┐   │
│  │  - HTML/CSS/JavaScript                           │   │
│  │  - PDF Upload UI                                 │   │
│  │  - Chat Interface                                │   │
│  │  - Image Display                                 │   │
│  └──────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────┘
                     │ HTTP REST API
                     ↓
┌─────────────────────────────────────────────────────────┐
│              BACKEND (Port 8000)                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │  FastAPI Application (main.py)                   │   │
│  │  ├─ POST /upload                                 │   │
│  │  ├─ POST /chat                                   │   │
│  │  └─ GET /images/:topicId                         │   │
│  └──────────────────────────────────────────────────┘   │
│                     │                                    │
│  ┌──────────────────┴────────────────────────────────┐  │
│  │  RAG Pipeline (rag_service.py)                    │  │
│  │  ├─ Query Processing                              │  │
│  │  ├─ Context Retrieval                             │  │
│  │  └─ Answer Generation                             │  │
│  └───────────────────────────────────────────────────┘  │
│                     │                                    │
│          ┌──────────┴──────────┐                         │
│          ↓                     ↓                         │
│  ┌──────────────┐      ┌──────────────┐                 │
│  │  Embedding   │      │    Vector    │                 │
│  │  Generator   │      │    Store     │                 │
│  │              │      │   (FAISS)    │                 │
│  │ Sentence-    │      │              │                 │
│  │ Transformers │      │ - Text Index │                 │
│  │              │      │ - Image Index│                 │
│  │ 384-dim      │      │              │                 │
│  └──────────────┘      └──────────────┘                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────┐
│           EXTERNAL SERVICES                              │
│  ┌──────────────────────────────────────────────────┐   │
│  │  OpenRouter API                                   │   │
│  │  └─ Mistral Small 24B Instruct                    │   │
│  │     (Free Tier)                                   │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Data Flow

### 1. PDF Upload Flow

```
User uploads PDF
    ↓
Frontend sends file to /upload
    ↓
Backend (PDFProcessor)
    ├─ Extract text with PyMuPDF
    ├─ Chunk with LangChain (1000 chars, 200 overlap)
    └─ Generate embeddings (384-dim vectors)
    ↓
Store in FAISS index
    ↓
Return success with chunk count
```

### 2. Question Answering Flow

```
User asks question
    ↓
Frontend sends to /chat
    ↓
Backend (RAG Service)
    ├─ Convert question to embedding
    ├─ FAISS similarity search
    │   ├─ Retrieve top 3 text chunks
    │   └─ Retrieve top 1 image
    ├─ Build context from chunks
    ├─ Send to LLM with strict prompt
    │   └─ "Use ONLY provided context"
    └─ Return answer + image
    ↓
Frontend displays answer + image
```

---

## Components Detail

### Frontend (`frontend/`)

| File | Purpose |
|------|---------|
| `index.html` | UI structure, upload & chat interface |
| `styles.css` | Modern styling, responsive design |
| `app.js` | API communication, DOM manipulation |
| `pics/` | Copy of images for serving |

**Key Features:**
- File upload with drag-drop
- Real-time chat interface
- Inline image display
- Loading states
- Error handling

### Backend (`backend/`)

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app, API endpoints |
| `config.py` | Configuration, environment variables |
| `rag_service.py` | RAG pipeline orchestration |
| `embedding_generator.py` | Text → Vector conversion |
| `vector_store.py` | FAISS operations |
| `pdf_processor.py` | PDF extraction & chunking |

**Key Features:**
- RESTful API
- CORS enabled
- Async operations
- Error handling
- Fallback responses

### Data Storage (`backend/data/`)

| Directory/File | Content |
|----------------|---------|
| `chunks.json` | Processed text chunks |
| `image_metadata.json` | Image descriptions & keywords |
| `embeddings/text_vectors.index` | FAISS text index |
| `embeddings/image_vectors.index` | FAISS image index |
| `embeddings/chunk_mapping.json` | Index → Chunk mapping |
| `embeddings/image_mapping.json` | Index → Image mapping |
| `uploads/` | User uploaded PDFs |

---

## Technology Stack

### Core Technologies

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| **Frontend** | HTML/CSS/JS | - | User interface |
| **Backend** | FastAPI | 0.115+ | API framework |
| **Server** | Uvicorn | 0.32+ | ASGI server |
| **PDF** | PyMuPDF | 1.24+ | Text extraction |
| **Chunking** | LangChain | 0.3+ | Text splitting |
| **Embeddings** | Sentence-Transformers | 3.0+ | Vector generation |
| **Model** | all-MiniLM-L6-v2 | - | 384-dim embeddings |
| **Vector DB** | FAISS | 1.9+ | Similarity search |
| **LLM** | OpenRouter | - | API gateway |
| **Model** | Mistral Small 24B | - | Answer generation |

### Dependencies

**Python:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `pymupdf` - PDF processing
- `langchain` - Text utilities
- `sentence-transformers` - Embeddings
- `faiss-cpu` - Vector search
- `numpy` - Array operations
- `pydantic` - Data validation
- `python-multipart` - File uploads
- `python-dotenv` - Environment variables
- `requests` - HTTP client

---

## RAG Pipeline Details

### Embedding Generation

**Model:** `all-MiniLM-L6-v2`
- Input: Text string
- Output: 384-dimensional vector
- Time: ~0.02 seconds per sentence
- Quality: Good for semantic search

**Process:**
1. Tokenize text
2. Pass through transformer
3. Mean pooling
4. Normalize to unit vector

### Vector Search (FAISS)

**Index Type:** `IndexFlatL2`
- Distance metric: L2 (Euclidean)
- Accuracy: 100% (exhaustive search)
- Speed: <1ms for 46 vectors
- Memory: ~18KB per 46 vectors

**Search Process:**
1. Query embedding generated
2. Calculate distance to all vectors
3. Return top K smallest distances
4. Map indices to original chunks

### LLM Integration

**API:** OpenRouter
**Model:** Mistral Small 24B Instruct

**Prompt Structure:**
```
System: "Use ONLY provided context. Do not hallucinate."
User: "Context: [chunks]\nQuestion: [question]"
```

**Parameters:**
- Temperature: 0.7 (balanced)
- Max tokens: 500
- Top-p: Default

---

## Security Considerations

### API Key Protection
- ✅ Keys in `.env` (not committed)
- ✅ `.gitignore` configured
- ✅ Environment validation on startup

### CORS Configuration
- Development: `allow_origins=["*"]`
- Production: Specific domains only

### Input Validation
- File type checking (`.pdf` only)
- Size limits (implicit)
- Pydantic models for API requests

### Error Handling
- Try-catch blocks
- Fallback responses
- No sensitive info in errors

---

## Performance

### Metrics (Local Testing)

| Operation | Time | Notes |
|-----------|------|-------|
| PDF Upload (14 pages) | 5-10s | First time (includes embedding) |
| Chunk Generation | 1-2s | 46 chunks |
| Embedding Generation | 3-5s | 46 chunks |
| FAISS Index Creation | <0.1s | 46 vectors |
| Query Embedding | <0.1s | Single query |
| FAISS Search | <0.001s | Top 3 retrieval |
| LLM Response | 1-2s | API latency |
| **Total Query Time** | **1-2s** | End-to-end |

### Scalability

**Current System:**
- Good for: 1-100 PDFs
- Chunk limit: ~10,000 chunks
- Concurrent users: 10-50

**To Scale:**
- Use IVF index for >100K chunks
- Add Redis caching
- Deploy multiple backends
- Use async processing queue

---

## Future Enhancements

### Planned Features
1. Multi-PDF management
2. User authentication
3. Chat history
4. Export conversations
5. Custom model selection
6. Batch processing
7. API rate limiting
8. Advanced analytics

### Technical Improvements
1. Better chunking strategies
2. Re-ranking retrieved chunks
3. Hybrid search (keyword + vector)
4. Query expansion
5. Streaming responses
6. WebSocket support
7. Progressive image loading

---

## References

- [FAISS Documentation](https://github.com/facebookresearch/faiss)
- [Sentence-Transformers](https://www.sbert.net/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenRouter API](https://openrouter.ai/docs)
- [RAG Paper](https://arxiv.org/abs/2005.11401)

---

**For deployment guide, see [DEPLOYMENT.md](DEPLOYMENT.md)**

