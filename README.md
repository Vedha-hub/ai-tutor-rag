# 🎓 AI Tutor — RAG-Based Learning Assistant

An AI-powered tutoring system that answers questions 
from uploaded course PDFs using Retrieval-Augmented Generation (RAG).

## 🏗️ Architecture
PDF Upload → Text Chunking → HuggingFace Embeddings 
→ ChromaDB Storage → Retrieval → Answer Generation

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Backend API | Python + FastAPI |
| LLM Orchestration | LangChain |
| Vector Database | ChromaDB |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Frontend | Streamlit |

## ✅ Prerequisites
- Python 3.11.9
- OpenAI API key (for Week 3+)

## 🚀 Installation

### 1. Clone repository:
git clone https://github.com/Vedha-hub/ai-tutor-rag.git
cd ai-tutor-rag

### 2. Create virtual environment:
python -m venv venv
venv\Scripts\activate

### 3. Install dependencies:
pip install -r backend/requirements.txt --prefer-binary

### 4. Create .env file:
Create backend/.env and add:
OPENAI_API_KEY=your-key-here

## ▶️ How to Run

### Start Backend:
cd backend
uvicorn main:app --reload --port 8000

### Start Frontend:
cd frontend
streamlit run app.py

### Open browser:
http://localhost:8501

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | Check server status |
| POST | /ingest | Upload and process PDF |
| POST | /ask | Ask a question |

## 📁 Project Structure
ai-tutor-rag/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── ingest.py        # PDF ingestion pipeline
│   ├── rag.py           # RAG retrieval chain
│   ├── memory.py        # Conversation memory
│   ├── quiz.py          # Quiz generation
│   └── requirements.txt
├── frontend/
│   └── app.py           # Streamlit UI
└── README.md

## 👥 Team
- Member A (Vedha): RAG pipeline, ChromaDB, 
  embeddings, quiz generation
- Member B (Sirisha): Streamlit UI, FastAPI 
  endpoints, memory management

## 📊 Weekly Progress
- ✅ Week 1: PDF ingestion + ChromaDB storage
- ✅ Week 2: RAG retrieval + Chat UI
- 🔄 Week 3: Memory + Quiz generation
- 📅 Week 4: Streaming + Final polish
