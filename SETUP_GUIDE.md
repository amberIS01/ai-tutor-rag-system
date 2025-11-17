# 🚀 AI Tutor RAG System - Quick Setup Guide

## ✅ What's Already Done

- ✅ PDF extraction & chunking (46 chunks)
- ✅ Embeddings generated (all-MiniLM-L6-v2)
- ✅ FAISS vector database built
- ✅ Image metadata created (6 images)
- ✅ FastAPI backend complete
- ✅ RAG pipeline ready

## 📋 What You Need to Do (5 minutes)

### Step 1: Get API Key (2 minutes)

1. **Go to:** https://openrouter.ai/
2. **Click "Sign In"** (use Google/GitHub - no credit card needed)
3. **Go to:** https://openrouter.ai/keys
4. **Click "Create Key"**
5. **Copy the key** (starts with `sk-or-v1-...`)

### Step 2: Configure Backend (1 minute)

```bash
cd backend

# Create .env file (copy from template)
# On Windows PowerShell:
copy env.example.txt .env

# On Mac/Linux:
# cp env.example.txt .env
```

**Edit the `.env` file:**
```
OPENROUTER_API_KEY=sk-or-v1-PASTE-YOUR-KEY-HERE
MODEL_NAME=mistralai/mistral-small-3.2-24b-instruct:free
```

### Step 3: Start Server (1 minute)

```bash
python main.py
```

You should see:
```
🚀 Starting AI Tutor RAG System
✅ Configuration validated
✅ RAG service initialized
🌐 Server running on http://0.0.0.0:8000
```

### Step 4: Test It! (1 minute)

**Open another terminal:**

```bash
cd backend
python test_api.py
```

Or test in browser: http://localhost:8000

## 🧪 Quick API Test

**Using curl:**

```bash
# Test health
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "How does a bell produce sound?"}'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"question": "How does a bell produce sound?"}
)

print(response.json()["answer"])
```

## 📊 Project Status

### ✅ Completed (Backend)
1. PDF Processing ✅
2. Text Chunking ✅
3. Embedding Generation ✅
4. FAISS Vector Store ✅
5. Image Metadata ✅
6. FastAPI Backend ✅
7. RAG Pipeline ✅

### 🔄 Next (Frontend)
8. HTML/JS Chat Interface
9. File Upload UI
10. Image Display
11. Styling

### 📹 Final
12. End-to-end testing
13. Demo video (2-4 min)
14. GitHub README

## 🗂️ Project Structure

```
ai-tutor-rag-system/
├── backend/                      ✅ COMPLETE
│   ├── main.py                   # FastAPI app
│   ├── config.py                 # Configuration
│   ├── rag_service.py           # RAG pipeline
│   ├── embedding_generator.py   # Embeddings
│   ├── vector_store.py          # FAISS
│   ├── pdf_processor.py         # PDF handling
│   ├── test_api.py              # Testing
│   ├── requirements.txt         # Dependencies
│   ├── env.example.txt          # Config template
│   └── data/
│       ├── chunks.json          # 46 chunks
│       ├── image_metadata.json  # 6 images
│       └── embeddings/          # FAISS indices
│
├── pics/                        # 6 diagram images
├── Sound.pdf                    # Source material
└── README.md                    # Documentation
```

## 🎯 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| GET | `/health` | Detailed status |
| POST | `/upload` | Upload PDF |
| POST | `/chat` | Ask questions |
| GET | `/images/{id}` | Get image metadata |

## 🐛 Troubleshooting

**"OPENROUTER_API_KEY not set"**
→ Create `.env` file with your API key

**"Connection refused"**
→ Make sure server is running: `python main.py`

**"Module not found"**
→ Install dependencies: `pip install -r requirements.txt`

**Slow responses**
→ Normal for first request (loading model)
→ Subsequent requests are fast (~1-2 sec)

## 💡 Example Questions to Try

- "How does a bell produce sound?"
- "What are vocal cords and how do they work?"
- "Explain compression and rarefaction in sound waves"
- "How do musical instruments produce sound?"
- "What is the speed of sound?"

## 🎉 Success Criteria

Your backend is working if:
- ✅ Server starts without errors
- ✅ `/health` returns "healthy"
- ✅ `/chat` returns an answer with an image
- ✅ Answer is relevant to the question
- ✅ Image matches the topic

## 📚 Resources

- **OpenRouter Docs:** https://openrouter.ai/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **Assignment:** See `do.txt`

---

**Need help?** Check `backend/README_API.md` for detailed API documentation.

**Ready for frontend?** We'll build a simple HTML/JS chat interface next!

