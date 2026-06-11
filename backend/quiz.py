import os
import json
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

QUIZ_PROMPT = """
You are a quiz generator for an academic course.
Generate EXACTLY 5 multiple choice questions about: {topic}
Base questions ONLY on this context: {context}

Return ONLY valid JSON in this exact format, no other text:
[
  {{
    "question": "Question text here?",
    "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
    "answer": "A",
    "explanation": "Brief explanation why A is correct"
  }}
]
"""


def get_query_embedding(text: str) -> list[float]:
    """Embed the topic using Gemini v1."""
    result = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=[text],
    )
    return result.embeddings[0].values


def retrieve_context(topic: str, k: int = 4) -> str:
    """Query ChromaDB for relevant chunks."""
    query_embedding = get_query_embedding(topic)

    results = get_collection().query(
        query_embeddings=[query_embedding],
        n_results=k,
        include=["documents"]
    )

    documents = results["documents"][0]
    return "\n\n".join(documents)


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
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                wait = 20 * (attempt + 1)
                print(f"Quota hit, waiting {wait}s...")
                time.sleep(wait)
            else:
                raise
    return ""


def generate_quiz(topic: str) -> list:
    """Generate 5 MCQs using Gemini based on course content."""
    context = retrieve_context(topic, k=4)

    if not context.strip():
        return []

    filled_prompt = QUIZ_PROMPT.format(topic=topic, context=context)
    raw = call_gemini(filled_prompt).strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        questions = json.loads(raw)
        return questions[:5]
    except json.JSONDecodeError:
        return [
            {
                "question": f"What is {topic}?",
                "options": [
                    "A. A fundamental concept",
                    "B. An advanced technique",
                    "C. A practical application",
                    "D. All of the above"
                ],
                "answer": "D",
                "explanation": "All options describe aspects of this topic."
            }
        ] * 5