import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from ingest import get_vectorstore

load_dotenv()

STRICT_PROMPT = """
You are an expert academic tutor for this specific course.
You MUST follow these rules strictly:

1. Answer ONLY using the context provided below.
2. If the answer is not found in the context, say exactly:
   'I don't have information about that in your course materials.'
3. Do NOT use any knowledge from outside the provided context.
4. Give clear, educational, and helpful answers.
5. If relevant, suggest related topics to study.

Context:
{context}

Student's Question: {question}

Your Answer:
"""

def build_rag_chain():
    """Build RAG chain using Gemini."""
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )
    
    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=STRICT_PROMPT
    )
    
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )
    
    return chain

def ask_question(question: str) -> dict:
    """Run question through Gemini RAG chain."""
    
    if not question or not question.strip():
        return {
            "answer": "Please ask a valid question.",
            "sources": []
        }
    
    try:
        chain = build_rag_chain()
        result = chain.invoke({"query": question})
        
        sources = []
        for doc in result.get("source_documents", []):
            sources.append({
                "page": doc.metadata.get("page", "unknown"),
                "source": doc.metadata.get("source", "unknown"),
                "snippet": " ".join(
                    doc.page_content[:150].split()
                ) + "..."
            })
        
        return {
            "answer": result["result"],
            "sources": sources
        }
        
    except Exception as e:
        return {
            "answer": f"Error: {str(e)}",
            "sources": []
        }