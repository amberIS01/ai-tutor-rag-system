# 🚀 AI Tutor RAG System - Backend API

## 📁 Project Structure

```
backend/
├── main.py                      # FastAPI application
├── config.py                    # Configuration & environment
├── rag_service.py              # RAG pipeline logic
├── embedding_generator.py      # Embedding creation
├── vector_store.py             # FAISS vector database
├── pdf_processor.py            # PDF extraction & chunking
├── test_api.py                 # API testing script
├── requirements.txt            # Python dependencies
├── env.example.txt            # Environment variables template
└── data/
    ├── chunks.json            # Text chunks
    ├── image_metadata.json    # Image descriptions
    └── embeddings/            # FAISS indices
        ├── text_vectors.index
        ├── image_vectors.index
        ├── chunk_mapping.json
        └── image_mapping.json
```

## 🔧 Setup Instructions

### 1. Get OpenRouter API Key

1. Go to https://openrouter.ai/
2. Sign up (free)
3. Go to https://openrouter.ai/keys
4. Create a new key
5. Copy the key (starts with `sk-or-v1-...`)

### 2. Configure Environment

Create a `.env` file in the `backend/` directory:

```bash
# Copy from template
cp env.example.txt .env

# Edit .env and add your API key
OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
MODEL_NAME=mistralai/mistral-small-3.2-24b-instruct:free
HOST=0.0.0.0
PORT=8000
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Server

```bash
python main.py
```

Or with auto-reload:

```bash
uvicorn main:app --reload --port 8000
```

Server will start at: http://localhost:8000

## 📡 API Endpoints

### 1. Health Check

**GET /**

```bash
curl http://localhost:8000/
```

Response:
```json
{
  "status": "online",
  "message": "AI Tutor RAG System API",
  "version": "1.0.0"
}
```

### 2. Upload PDF

**POST /upload**

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@Sound.pdf"
```

Response:
```json
{
  "status": "success",
  "topic_id": "sound",
  "chunks_created": 46,
  "filename": "Sound.pdf"
}
```

### 3. Chat (Ask Questions)

**POST /chat**

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How does a bell produce sound?"
  }'
```

Response:
```json
{
  "question": "How does a bell produce sound?",
  "answer": "A bell produces sound through vibration...",
  "image": {
    "filename": "SchoolBellVibration.png",
    "title": "School Bell Vibration",
    "description": "Diagram showing a school bell..."
  },
  "context_chunks": [...]
}
```

### 4. Get Images

**GET /images/{topic_id}**

```bash
curl http://localhost:8000/images/sound
```

Response:
```json
{
  "topic_id": "sound",
  "images": [...],
  "count": 6
}
```

## 🧪 Testing

Run the test script:

```bash
python test_api.py
```

This will test all endpoints and show example responses.

## 🔍 How It Works

1. **User asks a question** → POST /chat
2. **Question converted to embedding** (384-dim vector)
3. **FAISS searches** for similar chunks
4. **Retrieves top 3 relevant chunks** from PDF
5. **Selects best matching image**
6. **Sends chunks + question to LLM** (Mistral Small 24B)
7. **LLM generates educational answer**
8. **Returns answer + image** to user

## ⚙️ Configuration

Edit `config.py` or `.env` file:

- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `MODEL_NAME`: LLM model to use (default: Mistral Small 24B)
- `TOP_K_CHUNKS`: Number of chunks to retrieve (default: 3)
- `PORT`: Server port (default: 8000)

## 🐛 Troubleshooting

**API Key Not Set:**
```
⚠️  WARNING: OPENROUTER_API_KEY not set!
```
Solution: Create `.env` file with your API key

**Connection Error:**
```
Error calling OpenRouter API
```
Solution: Check internet connection and API key

**Model Not Found:**
```
Model not available
```
Solution: Check model name in `.env` file

## 📚 Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **OpenRouter**: LLM API gateway
- **Sentence-Transformers**: Embeddings
- **FAISS**: Vector database
- **PyMuPDF**: PDF processing
- **LangChain**: Text splitting

## 🚀 Next Steps

1. ✅ Backend complete
2. 🔄 Build frontend UI
3. 🔄 Connect frontend to API
4. 🔄 Test end-to-end
5. 🔄 Create demo video

---

**Made with ❤️ for educational AI tutoring**

