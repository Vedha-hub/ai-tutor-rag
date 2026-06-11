import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from quiz import generate_quiz
from memory import get_memory, clear_memory

load_dotenv()

app = FastAPI(
    title="AI Tutor API",
    description="RAG-based tutoring system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Health ─────────────────────────────────────────────────────────────────────
@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Tutor API is running"}


# ── Ingest PDF ─────────────────────────────────────────────────────────────────
@app.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    os.makedirs("tmp", exist_ok=True)
    temp_path = f"tmp/{file.filename}"

    try:
        with open(temp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        from ingest import ingest_pdf
        result = ingest_pdf(temp_path)
        return {
        "status": "success",
        "message": "PDF ingested successfully",
        "chunks_created": result["chunks_created"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


# ── Ask Question ───────────────────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"


@app.post("/ask")
async def ask_tutor(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        from rag import ask_question
        result = ask_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Clear Memory ───────────────────────────────────────────────────────────────
class ClearRequest(BaseModel):
    session_id: str = "default"


@app.post("/clear-memory")
async def clear_session(request: ClearRequest):
    clear_memory(request.session_id)
    return {
        "status": "success",
        "message": f"Memory cleared for session {request.session_id}"
    }


# ── Generate Quiz ──────────────────────────────────────────────────────────────
class QuizRequest(BaseModel):
    topic: str


@app.post("/generate-quiz")
async def create_quiz(request: QuizRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    try:
        questions = generate_quiz(request.topic)
        return {
            "topic": request.topic,
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))