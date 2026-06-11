import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/ingest")
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