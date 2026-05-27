import os
from dotenv import load_dotenv
from ingest import get_vectorstore

load_dotenv()

def ask_question(question: str) -> dict:
    """Retrieve relevant chunks and return as answer."""
    
    # Validate question
    if not question or not question.strip():
        return {
            "answer": "Please ask a valid question.",
            "sources": []
        }
    
    try:
        vectorstore = get_vectorstore()
        docs = vectorstore.similarity_search(question, k=3)
        
        if not docs:
            return {
                "answer": "I don't have information about that in your course materials.",
                "sources": []
            }
        
        context_parts = []
        for doc in docs:
            clean_text = " ".join(doc.page_content.split())
            context_parts.append(clean_text)
        
        context = "\n\n".join(context_parts)
        
        sources = []
        for doc in docs:
            sources.append({
                "page": doc.metadata.get("page", "unknown"),
                "source": doc.metadata.get("source", "unknown"),
                "snippet": " ".join(
                    doc.page_content[:150].split()
                ) + "..."
            })
        
        answer = (
            f"Based on your course materials:\n\n"
            f"{' '.join(context[:800].split())}..."
        )
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as e:
        return {
            "answer": f"Error retrieving answer: {str(e)}",
            "sources": []
        }