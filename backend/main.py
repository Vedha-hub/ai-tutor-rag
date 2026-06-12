import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routers import ingest, chat, quiz, memory,documents

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

# Register all routers
app.include_router(ingest.router)
app.include_router(chat.router)
app.include_router(quiz.router)
app.include_router(memory.router)
app.include_router(documents.router)

@app.get("/health")
async def health_check():
    return {"status": "ok", "message": "AI Tutor API is running"}