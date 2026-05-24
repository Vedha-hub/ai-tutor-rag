import os
from dotenv import load_dotenv
from ingest import get_vectorstore

load_dotenv()

def ask_question(question: str) -> dict:
    """Retrieve relevant chunks and return as answer."""
    vectorstore = get_vectorstore()
    docs = vectorstore.similarity_search(question, k=3)
    
    context = "\n\n".join([doc.page_content for doc in docs])
    
    sources = []
    for doc in docs:
        sources.append({
            "page": doc.metadata.get("page", "unknown"),
            "source": doc.metadata.get("source", "unknown"),
            "snippet": doc.page_content[:150] + "..."
        })
    
    answer = f"Based on your course materials:\n\n{context[:500]}..."
    
    return {
        "answer": answer,
        "sources": sources
    }