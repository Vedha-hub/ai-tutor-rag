# 🎓 AI Tutor — RAG-Based Learning Assistant

An AI-powered tutoring system that lets students upload course PDFs and ask questions, get answers grounded strictly in their course material, and generate practice quizzes — powered by Google Gemini and Pinecone.

---

## 🚀 Features

- **PDF Ingestion** — Upload course materials (PDFs), automatically chunked and embedded
- **RAG-based Q&A** — Ask questions and get answers strictly from your course content (no hallucination)
- **Quiz Generation** — Auto-generate 5 MCQs on any topic from your uploaded material
- **Conversation Memory** — Session-based chat history for context-aware follow-up questions
- **Multi-PDF Support** — Ingest multiple documents; each tracked separately in Pinecone
- **Source Citations** — Every answer includes page numbers and snippets from the source

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│  Streamlit  │ ───▶ │   FastAPI    │ ───▶ │  Pinecone (Vector│
│  Frontend   │ ◀─── │   Backend    │ ◀─── │  Database)       │
└─────────────┘      └──────────────┘      └─────────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  Google       │
                     │  Gemini API   │
                     │ (embeddings + │
                     │  generation)  │
                     └──────────────┘
```

**Tech Stack:**
- **Frontend:** Streamlit
- **Backend:** FastAPI (modular routers)
- **Vector DB:** Pinecone (cloud, serverless)
- **LLM & Embeddings:** Google Gemini (`gemini-embedding-001`, `gemini-3.5-flash`) via `google-genai` SDK
- **PDF Processing:** LangChain document loaders + text splitters

---

## 📁 Project Structure

```
ai-tutor-rag/
├── backend/
│   ├── main.py                 # FastAPI app entrypoint
│   ├── ingest.py                # PDF loading + chunking
│   ├── rag.py                   # RAG Q&A pipeline
│   ├── quiz.py                  # Quiz generation
│   ├── memory.py                # Session-based conversation memory
│   ├── pinecone_store.py        # Pinecone embedding + retrieval logic
│   ├── document_registry.py     # Tracks ingested documents
│   ├── routers/
│   │   ├── ingest.py             # POST /ingest
│   │   ├── chat.py                # POST /ask
│   │   ├── quiz.py                # POST /generate-quiz
│   │   ├── memory.py              # POST /clear-memory
│   │   └── documents.py           # GET/DELETE /documents
│   ├── requirements.txt
│   └── .env                     # API keys (not committed)
├── frontend/
│   ├── app.py                   # Streamlit UI
│   └── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Vedha-hub/ai-tutor-rag.git
cd ai-tutor-rag
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
source venv/bin/activate       # macOS/Linux
```

### 3. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file inside `backend/` with:
```env
GOOGLE_API_KEY=your-gemini-api-key
PINECONE_API_KEY=your-pinecone-api-key
PINECONE_INDEX_NAME=ai-tutor
ANONYMIZED_TELEMETRY=False
CHROMA_TELEMETRY=False
```

- Get a Gemini API key: https://aistudio.google.com/app/apikey
- Get a Pinecone API key: https://app.pinecone.io (create a serverless index, dimension `3072`, metric `cosine`)

### 5. Install frontend dependencies
```bash
cd ../frontend
pip install -r requirements.txt
```

---

## ▶️ Running the App

**Terminal 1 — Start the backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```
API docs available at: `http://localhost:8000/docs`

**Terminal 2 — Start the frontend:**
```bash
cd frontend
streamlit run app.py
```
App available at: `http://localhost:8501`

---

## 📡 API Endpoints

| Method | Endpoint           | Description                              |
|--------|--------------------|--------------------------------------------|
| GET    | `/health`           | Health check                              |
| POST   | `/ingest`           | Upload and process a PDF                  |
| POST   | `/ask`              | Ask a question (with session memory)      |
| POST   | `/generate-quiz`    | Generate a 5-question MCQ quiz on a topic |
| POST   | `/clear-memory`     | Clear conversation history for a session  |
| GET    | `/documents`        | List all ingested documents               |
| DELETE | `/documents`        | Delete a document and its vectors         |

### Example: Ask a question
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is image processing?", "session_id": "user1"}'
```

---

## 🧠 How It Works

1. **Ingestion** — PDF is loaded, split into ~1000-character chunks with overlap, and each chunk is embedded using Gemini's `embedding-001` model
2. **Storage** — Embeddings are stored in Pinecone, with each vector ID prefixed by the source filename (supports multiple documents)
3. **Retrieval** — When a question is asked, it's embedded and matched against stored vectors using cosine similarity
4. **Generation** — Retrieved context + chat history + question are sent to `gemini-3.5-flash`, which answers strictly from the provided context
5. **Memory** — Each session's Q&A history is stored in-memory and included in future prompts for context-aware conversations

---

## 🛠️ Troubleshooting

- **404 model not found errors** — Ensure you're using `gemini-embedding-001` (v1) and `gemini-3.5-flash` (v1beta); check available models with `client.models.list()`
- **429 quota exceeded** — Free tier rate limits; the app automatically retries with backoff
- **Pinecone index errors** — Ensure index dimension is `3072` (matches Gemini embedding size) and metric is `cosine`
- **Telemetry warnings** — Harmless; suppressed via `ANONYMIZED_TELEMETRY=False` in `.env`

---

## 👥 Team

Built as part of a GenAI internship project — collaborative development using feature-branch Git workflow with FastAPI + Streamlit + Gemini + Pinecone.

---

## 📌 Future Improvements

- User authentication and per-user document spaces
- Support for additional file formats (DOCX, PPTX)
- Persistent chat history (database-backed instead of in-memory)
- Quiz difficulty levels and scoring history
- Deployment to cloud (Render/Railway + Streamlit Cloud)