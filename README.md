<div align="center">

# 🎓 AI Tutor — RAG-Powered Learning Platform

### *Because students deserve answers from their actual syllabus, not hallucinations.*

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.5-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://langchain.com)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.5-FF6B35?style=for-the-badge)](https://trychroma.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)

<br/>

> **Infotact Solutions · Technical Internship Program · Project 1 · Week 1**
> `Python` · `FastAPI` · `LangChain` · `ChromaDB` · `OpenAI` · `Streamlit`

</div>

---

## 🧠 What Is This?

**AI Tutor** is a Retrieval-Augmented Generation (RAG) system that turns any course PDF into a smart, conversational tutor. Unlike generic ChatGPT prompts, this system is *grounded* — it can only answer from the material your teacher uploaded. No guessing. No hallucinating. Just your syllabus, made interactive.

```
Teacher uploads PDF  →  AI indexes it  →  Student asks questions  →  AI answers from the syllabus
```

### Why RAG?

Standard LLMs answer from general training data — they can confidently give wrong answers. RAG fixes this:

1. 📄 Your course PDF is broken into searchable chunks
2. 🔍 When a student asks something, the most relevant chunks are retrieved
3. 🤖 The LLM answers using **only** those chunks — nothing else

---

## ✅ Week 1 — What We Built

> **Goal:** A PDF file can be uploaded via a FastAPI endpoint, the text is extracted, chunked, embedded, and stored in ChromaDB. Querying the database with a question returns relevant text chunks.

### 👥 Member Responsibilities

| Member A (`feature/rag-pipeline`) | Member B (`feature/frontend-memory`) |
|-----------------------------------|--------------------------------------|
| ✅ PDF loading using PyPDFLoader | ✅ FastAPI app skeleton in `main.py` |
| ✅ Text chunking with RecursiveCharacterTextSplitter | ✅ `/health` endpoint |
| ✅ OpenAI embeddings integration | ✅ Streamlit file upload scaffold |
| ✅ ChromaDB vector storage + upsert | ✅ Wired upload form to `/ingest` endpoint |
| ✅ Similarity search test (`test_retrieval.py`) | ✅ README project description |

### 📅 Day-by-Day Progress

| Day | Focus | Key Commits |
|-----|-------|-------------|
| Day 1 (Mon) | Repo setup, folder structure, branching | `feat: initialize project skeleton and virtual environment` |
| Day 2 (Tue) | PDF loading · FastAPI skeleton | `feat: add pdf document loader using langchain pypdfloader` · `fix: add error handling for invalid file types` |
| Day 3 (Wed) | Text chunking · Streamlit scaffold | `feat: add recursive character text splitter with 500 chunk size` · `refactor: tune chunk_size to 500 and overlap to 50` |
| Day 4 (Thu) | Embeddings + ChromaDB + `/ingest` endpoint | `feat: integrate openai text embeddings` · `feat: upsert embedded chunks to chromadb` · `feat: add /ingest POST endpoint` |
| Day 5 (Fri) | Retrieval testing + PR + dashboard update | `feat: add similarity search retrieval test script` · `feat: wire streamlit upload form to /ingest endpoint` |

---

## 🏗️ Architecture — Week 1 Pipeline

```
┌─────────────────────────────────────────────────────────────┐
│                      INGESTION FLOW                          │
│                                                              │
│   POST /ingest (PDF file)                                    │
│         ↓                                                    │
│   PyPDFLoader  →  extracts text + page metadata             │
│         ↓                                                    │
│   RecursiveCharacterTextSplitter                             │
│   chunk_size=500, chunk_overlap=50                           │
│         ↓                                                    │
│   OpenAI text-embedding-ada-002                              │
│   each chunk → 1536-dimensional vector                       │
│         ↓                                                    │
│   ChromaDB  →  persisted locally at ./chroma_db/            │
└─────────────────────────────────────────────────────────────┘
                          ↕
┌─────────────────────────────────────────────────────────────┐
│                     RETRIEVAL TEST                           │
│                                                              │
│   test_retrieval.py  →  sample question                      │
│         ↓                                                    │
│   ChromaDB similarity_search  →  top-3 relevant chunks      │
│         ↓                                                    │
│   Print chunks + verify relevance ✅                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Project Structure

```
ai-tutor-rag/
│
├── 📁 backend/
│   ├── main.py              # FastAPI app — /health and /ingest endpoints
│   ├── ingest.py            # Core pipeline: PDF → chunk → embed → ChromaDB
│   ├── test_retrieval.py    # Verify similarity search returns relevant chunks
│   ├── requirements.txt     # All Python dependencies
│   └── .env                 # 🔒 API keys (never committed to GitHub)
│
├── 📁 frontend/
│   └── app.py               # Streamlit UI — file upload wired to /ingest
│
├── .gitignore               # Excludes .env, chroma_db/, venv/, tmp/
└── README.md
```

> **Note:** `rag.py`, `quiz.py`, and `memory.py` are created in Weeks 2–3. `chroma_db/` folder is auto-generated on first ingest and excluded from Git.

---

## ⚡ Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR-USERNAME/ai-tutor-rag.git
cd ai-tutor-rag

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install all dependencies
pip install -r backend/requirements.txt
```

### 2. Set Up API Keys

Create `backend/.env` — **never commit this file:**

```env
OPENAI_API_KEY=sk-your-openai-key-here
PINECONE_API_KEY=your-pinecone-key-here      # optional — needed from Week 3+
PINECONE_ENVIRONMENT=us-east-1
PINECONE_INDEX_NAME=ai-tutor
```

### 3. Run the API

```bash
cd backend
uvicorn main:app --reload --port 8000
# → Open http://localhost:8000/docs  for Swagger UI (test endpoints in browser)
```

### 4. Run the Frontend

```bash
cd frontend
streamlit run app.py
```

---

## 📦 Dependencies (`requirements.txt`)

```txt
fastapi==0.111.0
uvicorn[standard]==0.29.0
langchain==0.2.5
langchain-openai==0.1.8
langchain-community==0.2.5
openai==1.30.0
chromadb==0.5.0
pypdf==4.2.0
python-multipart==0.0.9
python-dotenv==1.0.0
pydantic==2.7.0
streamlit==1.35.0
tiktoken==0.7.0
pinecone-client==3.2.2
```

---

## 🔌 API Endpoints — Week 1

### `GET /health`
Verify the server is live.

```json
// Response
{ "status": "ok", "message": "AI Tutor API is running" }
```

### `POST /ingest`
Upload a PDF — triggers the full ingestion pipeline.

```bash
curl -X POST http://localhost:8000/ingest \
  -F "file=@your-syllabus.pdf"
```

```json
// Response
{ "status": "success", "chunks_created": 47 }
```

---

## 🔬 Code Walkthrough

### `backend/ingest.py` — The Ingestion Pipeline

```python
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500      # tested 300 (too granular) and 700 (too broad) — 500 is optimal
CHUNK_OVERLAP = 50    # 10% overlap so context isn't lost at chunk boundaries

embeddings_model = OpenAIEmbeddings(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model="text-embedding-ada-002"
)

def load_and_chunk_pdf(file_path: str) -> list:
    """Load a PDF and split into overlapping chunks."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {file_path}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]  # tries paragraph → sentence → word
    )
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")
    return chunks

def store_in_chromadb(chunks: list) -> Chroma:
    """Embed chunks and upsert into ChromaDB."""
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_DIR
    )
    vectorstore.persist()  # save to disk — survives server restarts
    print(f"Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DIR}")
    return vectorstore

def ingest_pdf(file_path: str) -> dict:
    """Full pipeline: load → chunk → embed → store."""
    chunks = load_and_chunk_pdf(file_path)
    store_in_chromadb(chunks)
    return {"status": "success", "chunks_created": len(chunks)}

def get_vectorstore() -> Chroma:
    """Load existing ChromaDB for retrieval."""
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings_model
    )
```

**Why these choices?**
- `PyPDFLoader` preserves page number metadata — essential for source citations in Week 2
- `chunk_size=500` found through experimentation: 300 was too granular (split mid-sentence), 700 was too broad (chunks contained multiple unrelated concepts)
- `chunk_overlap=50` ensures a sentence at the edge of one chunk also appears at the start of the next — so no answer ever falls in the gap between chunks

---

### `backend/main.py` — FastAPI App

```python
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from ingest import ingest_pdf

load_dotenv()

app = FastAPI(
    title="AI Tutor API",
    description="RAG-based tutoring system using LangChain and ChromaDB",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Tutor API is running"}

@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    os.makedirs("tmp", exist_ok=True)
    temp_path = f"tmp/{file.filename}"
    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        result = ingest_pdf(temp_path)
        return result
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)  # always clean up temp files
```

---

### `backend/test_retrieval.py` — Verifying the Pipeline Works

This script is run after ingesting a PDF to confirm the vector store is returning relevant results. It tests 3 sample questions and prints the top matching chunks.

```python
from ingest import get_vectorstore

def test_similarity_search():
    vectorstore = get_vectorstore()

    test_questions = [
        "What is the main topic of this course?",
        "Explain the key concepts covered in chapter 1",
        "What are the assessment criteria?"
    ]

    for question in test_questions:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}")

        results = vectorstore.similarity_search(question, k=3)

        for i, doc in enumerate(results, 1):
            print(f"\n--- Chunk {i} (Page {doc.metadata.get('page', '?')}) ---")
            print(doc.page_content[:300])
            print("...")

if __name__ == "__main__":
    test_similarity_search()
```

**How to run:**
```bash
cd backend
python test_retrieval.py
```

Verify that: (a) chunks are returned, (b) they are actually relevant to the question asked, and (c) page numbers appear in metadata. If chunks look irrelevant, re-tune `CHUNK_SIZE` in `ingest.py` and re-ingest.

---

## 🌿 Git Workflow

```
main  (protected — merge via PR only)
  ├── feature/rag-pipeline        ← Member A
  └── feature/frontend-memory     ← Member B
```

### Commit Message Format

```
feat:          New feature added
fix:           Bug corrected
prompt-tuning: System prompt or AI prompt changed
refactor:      Restructured code, no behavior change
docs:          README or documentation update
chore:         Setup, config, packages
test:          Test added or fixed
```

### Week 1 Commit Targets — 15+ commits including:

```bash
feat: initialize project structure with fastapi and requirements
feat: add pdf document loader using langchain pypdfloader
fix: add error handling for invalid file types
feat: add recursive character text splitter with 500 chunk size
refactor: tune chunk_size to 500 and chunk_overlap to 50 after testing
feat: integrate openai text embeddings for each chunk
feat: upsert embedded chunks to chromadb local vector store
feat: add /ingest POST endpoint to fastapi for file upload
feat: add fastapi app skeleton with health check endpoint
feat: add streamlit file upload interface scaffold
feat: wire streamlit upload form to fastapi ingest endpoint
feat: add similarity search retrieval test script
docs: add week 1 readme with setup and architecture
```

---

## 🛡️ Security

- `.env` is in `.gitignore` — API keys never touch GitHub
- All secrets accessed via `os.getenv()` — nothing hardcoded
- `tmp/` folder for uploads is always cleaned up after each ingest (`finally` block)
- `chroma_db/` folder excluded from version control

---

## 🐛 Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError` | Activate venv: `venv\Scripts\activate` |
| `OPENAI_API_KEY not found` | Check `backend/.env` exists and has your key |
| `git: not a repository` | Run `cd ai-tutor-rag` first |
| ChromaDB returns empty results | Re-run ingest — `chroma_db/` folder may be empty or missing |
| Port 8000 already in use | `uvicorn main:app --reload --port 8001` |
| Merge conflict on git pull | Open VS Code, resolve `<<<<` markers, then commit |
| Accidentally committed `.env` | `git rm --cached .env` then `git commit -m "chore: remove .env from tracking"` |

---

## 🗺️ What's Next — Weeks 2–4

- [ ] **Week 2** — RAG chain + `/ask` endpoint + source citations per answer
- [ ] **Week 3** — Conversational memory + auto quiz generation
- [ ] **Week 4** — Token streaming + polished UI + final cleanup

---

## 👥 Team

| Member | Branch | Week 1 Contribution |
|--------|--------|---------------------|
| Member A | `feature/rag-pipeline` | Ingestion pipeline, ChromaDB setup, retrieval testing |
| Member B | `feature/frontend-memory` | FastAPI skeleton, Streamlit upload UI, health endpoint |

---

<div align="center">

**Built during the Infotact Solutions Technical Internship Program**

[support@infotact.in](mailto:support@infotact.in) · [infotact.in](https://infotact.in)

*Commit early. Commit often. Never commit your API keys.*

</div>
