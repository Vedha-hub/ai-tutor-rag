              🎓 AI Tutor — RAG-Powered Learning Platform
Because students deserve answers from their actual syllabus, not hallucinations.
   
    Infotact Solutions · Technical Internship Program · Project 1 · Week 1
         Python · FastAPI · LangChain · ChromaDB · OpenAI · Streamlit

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

Why RAG?

Standard LLMs answer from general training data — they can confidently give wrong answers. RAG fixes this:

1. 📄 Your course PDF is broken into searchable chunks
2. 🔍 When a student asks something, the most relevant chunks are retrieved
3. 🤖 The LLM answers using **only** those chunks — nothing else

✅ Week 1 — What We Built
```
Goal: A PDF file can be uploaded via a FastAPI endpoint, the text is extracted, chunked, embedded, and stored in ChromaDB. Querying the database with a question returns relevant text chunks.
```

👥 Member Responsibilities

| Member A (`feature/rag-pipeline`)                          | Member B (`feature/frontend-memory`) |

| ✅ PDF loading using PyPDFLoader                          | ✅ FastAPI app skeleton in `main.py` |
| ✅ Text chunking with RecursiveCharacterTextSplitter      | ✅ `/health` endpoint |
| ✅ OpenAI embeddings integration                          | ✅ Streamlit file upload scaffold |
| ✅ ChromaDB vector storage + upsert                       | ✅ Wired upload form to `/ingest` endpoint |
| ✅ Similarity search test (`test_retrieval.py`)           | ✅ README project description |


#📅 Day-by-Day Progress

| Day         | Focus                                      | Key Commits |

| Day 1 (Mon) | Repo setup, folder structure, branching    | `feat: initialize project skeleton and virtual environment` |
| Day 2 (Tue) | PDF loading · FastAPI skeleton             | `feat: add pdf document loader using langchain pypdfloader` · `fix: add error handling for invalid                                                                  file types` |
| Day 3 (Wed) | Text chunking · Streamlit scaffold         | `feat: add recursive character text splitter with 500 chunk size` · `refactor: tune chunk_size to 500                                                               and overlap to 50` |
| Day 4 (Thu) | Embeddings + ChromaDB + `/ingest` endpoint | `feat: integrate openai text embeddings` · `feat: upsert embedded chunks to chromadb` · `feat: add                                                                  /ingest POST endpoint` |
| Day 5 (Fri) | Retrieval testing + PR + dashboard update  | `feat: add similarity search retrieval test script` · `feat: wire streamlit upload form to /ingest                                                                  endpoint` |

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

🗂️ Project Structure


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

Note:`rag.py`, `quiz.py`, and `memory.py` are created in Weeks 2–3. 
`chroma_db/` folder is auto-generated on first ingest and excluded from Git.


🌿 Git Workflow

```
main  (protected — merge via PR only)
  ├── feature/rag-pipeline        ← Member A
  └── feature/frontend-memory     ← Member B
```

Commit Message Format

```
feat:          New feature added
fix:           Bug corrected
prompt-tuning: System prompt or AI prompt changed
refactor:      Restructured code, no behavior change
docs:          README or documentation update
chore:         Setup, config, packages
test:          Test added or fixed
```

Week 1 Commit Targets — 15+ commits including:

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

🛡️ Security

- `.env` is in `.gitignore` — API keys never touch GitHub
- All secrets accessed via `os.getenv()` — nothing hardcoded
- `tmp/` folder for uploads is always cleaned up after each ingest (`finally` block)
- `chroma_db/` folder excluded from version control

---

## 🐛 Troubleshooting

| Problem                             | Fix |

| `ModuleNotFoundError`               | Activate venv: `venv\Scripts\activate` |
| `OPENAI_API_KEY not found`          | Check `backend/.env` exists and has your key |
| `git: not a repository`             | Run `cd ai-tutor-rag` first |
| ChromaDB returns empty results      | Re-run ingest — `chroma_db/` folder may be empty or missing |
| Port 8000 already in use            | `uvicorn main:app --reload --port 8001` |
| Merge conflict on git pull          | Open VS Code, resolve `<<<<` markers, then commit |
| Accidentally committed `.env`       | `git rm --cached .env` then `git commit -m "chore: remove .env from tracking"` |

---

🗺️ What's Next — Weeks 2–4

- [ ] **Week 2** — RAG chain + `/ask` endpoint + source citations per answer
- [ ] **Week 3** — Conversational memory + auto quiz generation
- [ ] **Week 4** — Token streaming + polished UI + final cleanup

---

👥 Team

| Member   | Branch                    | Week 1 Contribution |

| Member A | `feature/rag-pipeline`    | Ingestion pipeline, ChromaDB setup, retrieval testing |
| Member B | `feature/frontend-memory` | FastAPI skeleton, Streamlit upload UI, health endpoint |

---

<div align="center">

**Built during the Infotact Solutions Technical Internship Program**

[support@infotact.in](mailto:support@infotact.in) · [infotact.in](https://infotact.in)

*Commit early. Commit often. Never commit your API keys.*

</div>         
