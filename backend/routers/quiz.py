from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class QuizRequest(BaseModel):
    topic: str

@router.post("/generate-quiz")
async def create_quiz(request: QuizRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    try:
        from quiz import generate_quiz
        questions = generate_quiz(request.topic)
        return {
            "topic": request.topic,
            "questions": questions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))