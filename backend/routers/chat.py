from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str
    session_id: str = "default"

@router.post("/ask")
async def ask_tutor(request: QuestionRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    try:
        from rag import ask_question
        result = ask_question(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))