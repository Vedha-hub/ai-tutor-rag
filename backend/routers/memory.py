from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ClearRequest(BaseModel):
    session_id: str = "default"

@router.post("/clear-memory")
async def clear_session(request: ClearRequest):
    from memory import clear_memory
    clear_memory(request.session_id)
    return {
        "status": "success",
        "message": f"Memory cleared for session {request.session_id}"
    }