from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from memory import add_to_memory, get_chat_history

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

        # Get chat history for context
        history = get_chat_history(request.session_id)

        # Add history to question if exists
        full_question = request.question
        if history:
            full_question = f"Previous conversation:\n{history}\n\nNew question: {request.question}"

        result = ask_question(full_question)

        # Save to memory
        add_to_memory(
            request.session_id,
            request.question,
            result["answer"]
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))