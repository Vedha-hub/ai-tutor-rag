from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from document_registry import list_documents, remove_document
from pinecone_store import delete_document

router = APIRouter()


@router.get("/documents")
async def get_documents():
    """List all ingested documents."""
    docs = list_documents()
    return {"documents": docs, "count": len(docs)}


class DeleteDocumentRequest(BaseModel):
    filename: str


@router.delete("/documents")
async def delete_document_endpoint(request: DeleteDocumentRequest):
    """Delete a document and its vectors from Pinecone."""
    try:
        delete_document(request.filename)
        remove_document(request.filename)
        return {
            "status": "success",
            "message": f"Deleted '{request.filename}' and its vectors"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))