# AI Tutor RAG System

A RAG-based AI tutor chatbot that answers questions from a Sound chapter PDF and displays relevant images during explanations.

## 🎯 Project Goal

Build an intelligent tutor that:
- Extracts and understands content from educational PDFs
- Answers student questions using RAG (Retrieval Augmented Generation)
- Automatically displays relevant diagrams and images
- Provides grounded, accurate answers based on the source material

## 🏗️ Architecture

### RAG Pipeline
1. **PDF Extraction** - PyMuPDF extracts text from Sound.pdf
2. **Text Chunking** - LangChain splits content into retrievable chunks
3. **Embeddings** - Sentence-transformers generates vector embeddings
4. **Vector Storage** - FAISS stores embeddings for fast retrieval
5. **Query & Retrieval** - User questions retrieve top K relevant chunks
6. **Answer Generation** - LLM generates grounded answers from retrieved context

### Image Retrieval
1. **Image Metadata** - JSON with descriptions and keywords for each diagram
2. **Image Embeddings** - Vector embeddings of image descriptions
3. **Semantic Matching** - Query matched against image embeddings
4. **Contextual Display** - Most relevant image shown with each answer

## 📁 Project Structure

```
ai-tutor-rag-system/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── pdf_processor.py     # PDF extraction & chunking
│   ├── requirements.txt     # Python dependencies
│   └── data/
│       ├── chunks.json      # Extracted text chunks
│       └── embeddings/      # FAISS vector index
├── pics/                    # Educational diagrams
│   ├── SchoolBellVibration.png
│   ├── VocalCordsDiagram.png
│   └── ...
├── Sound.pdf               # Source educational material
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip
- OpenRouter API key ([Get free key](https://openrouter.ai/keys))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-tutor-rag-system.git
cd ai-tutor-rag-system

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Configure environment
cp env.example.txt .env
# Edit .env and add your OPENROUTER_API_KEY

# 4. Run backend
python main.py
# Backend runs on http://localhost:8000

# 5. In a new terminal, run frontend
cd ../frontend
python -m http.server 5500
# Frontend runs on http://localhost:5500

# 6. Open browser
# Navigate to http://localhost:5500
```

### First Time Setup

1. **Get API Key** (2 minutes)
   - Visit: https://openrouter.ai/keys
   - Sign up (free, no credit card)
   - Create key and copy it

2. **Configure `.env`**
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   MODEL_NAME=mistralai/mistral-small-3.2-24b-instruct:free
   ```

3. **Start using!**
   - Upload a PDF
   - Ask questions
   - Get answers with images

### Quick Start with Docker (Alternative)

```bash
# Build and run with docker-compose
docker-compose up --build

# Access:
# Frontend: http://localhost:5500
# Backend: http://localhost:8000
```

## 🛠️ Technologies Used

- **PyMuPDF** - Fast PDF text extraction
- **LangChain** - Text splitting and RAG utilities
- **Sentence-Transformers** - Free embedding generation
- **FAISS** - Efficient vector similarity search
- **FastAPI** - Modern Python web framework
- **OpenRouter API** - LLM for answer generation

## 📚 API Examples

### Upload PDF
```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@Sound.pdf"
```

### Ask Question
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What causes sound?", "topic_id": "sound"}'
```

### Health Check
```bash
curl http://localhost:8000/health/readiness
```

## 🔧 Configuration

### Environment Variables
- `OPENROUTER_API_KEY` - Your OpenRouter API key (required)
- `MODEL_NAME` - LLM model to use (default: mistralai/mistral-small-3.2-24b-instruct:free)
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 8000)
- `REQUEST_TIMEOUT` - Request timeout in seconds (default: 30)
- `OPENROUTER_TIMEOUT` - OpenRouter API timeout (default: 60)

### Advanced Features
- **Rate Limiting**: 60 requests per minute per user
- **Request Timeout**: Configurable timeout for long-running operations
- **Health Checks**: `/health/readiness` and `/health/liveness` endpoints
- **Metrics**: `/metrics` endpoint for monitoring
- **API Versioning**: `/api/v1/` prefix for all endpoints

## 📝 Implementation Status

- [x] Project structure setup
- [x] PDF extraction with PyMuPDF
- [x] Text chunking with LangChain
- [x] Embedding generation
- [x] FAISS vector storage
- [x] Image metadata creation
- [x] FastAPI endpoints
- [x] Frontend interface
- [x] Demo video
- [x] File validation & size limits
- [x] Error handling & logging
- [x] Production optimizations

## 📹 Demo Video

[Link to demo video will be added here]

## ⭐ Features

- 🚀 Fast PDF processing with PyMuPDF
- 🧠 Semantic search using FAISS vector database
- 🤖 AI-powered answers with Mistral Small 24B
- 🖼️ Automatic image selection and display
- 📱 Responsive mobile-friendly design
- ✅ File validation and size limits
- 🔒 Secure API key management
- 📊 Real-time health monitoring
- ⚡ Sub-second query responses
- 🎯 Anti-hallucination measures

## 🤝 Contributing

This is an educational project. Feel free to fork and enhance!

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- OpenRouter for LLM API access
- Meta for FAISS vector database
- Sentence-Transformers team
- FastAPI framework

---

**Built for educational purposes**  
**Topic**: Sound Chapter - Physics Education

