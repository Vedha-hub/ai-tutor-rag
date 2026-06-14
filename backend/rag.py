import os
import time
from dotenv import load_dotenv
import chromadb
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ── Two separate clients ───────────────────────────────────────────────────────
genai_client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

genai_client_gen = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"api_version": "v1beta"}
)

# ── ChromaDB ───────────────────────────────────────────────────────────────────
chroma_client = chromadb.PersistentClient(path="./chroma_db")

def get_collection():
    """Get collection lazily — only when needed."""
    return chroma_client.get_collection("course_docs")

# ── Prompt ─────────────────────────────────────────────────────────────────────
STRICT_PROMPT = """You are an expert academic tutor.
Answer ONLY using the context below.
If the answer is not in the context, say:
'I don't have information about that in your course materials.'
Do NOT use outside knowledge.

Context:
{context}

Question: {question}

Answer:"""


def get_query_embedding(text: str) -> list[float]:
    """Embed the user question using Gemini v1."""
    result = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text],
    )
    return result.embeddings[0].values


def retrieve_docs(question: str, k: int = 5) -> tuple[str, list[dict]]:
    """Query ChromaDB and return context string + sources."""
    query_embedding = get_query_embedding(question)

    results = get_collection().query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents", "metadatas"]
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    sources = []
    for doc, meta in zip(documents, metadatas):
        sources.append({
            "page": meta.get("page", "unknown"),
            "source": meta.get("source", "unknown"),
            "snippet": " ".join(doc[:150].split()) + "..."
        })

    return context, sources


def call_gemini(prompt_text: str) -> str:
    """Call Gemini 3.5 Flash with retry on quota errors."""
    for attempt in range(3):
        try:
            response = genai_client_gen.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt_text,
            )
            return response.text
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e) or "503" in str(e) or "UNAVAILABLE" in str(e):
                wait = 20 * (attempt + 1)
                print(f"Quota hit, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    return "Quota exceeded. Please wait a minute and try again."


def ask_question(question: str) -> dict:
    """Run question through Gemini RAG pipeline."""
    if not question or not question.strip():
        return {"answer": "Please ask a valid question.", "sources": []}

    try:
        context, sources = retrieve_docs(question, k=5)
        filled_prompt = STRICT_PROMPT.format(context=context, question=question)
        answer = call_gemini(filled_prompt)
        return {"answer": answer, "sources": sources}

    except Exception as e:
        return {"answer": f"Error generating answer: {str(e)}", "sources": []}


if __name__ == "__main__":
    print("RAG system ready. Type your question (or 'quit' to exit).\n")
    while True:
        q = input("Question: ").strip()
        if q.lower() in ("quit", "exit", "q"):
            break
        if not q:
            continue
        result = ask_question(q)
        print(f"\nAnswer: {result['answer']}")
        print("\nSources:")
        for s in result["sources"]:
            print(f"  • Page {s['page']}: {s['snippet']}")
        print()