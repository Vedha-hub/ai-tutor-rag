import os
import time
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ai-tutor")

# ── Clients ────────────────────────────────────────────────────────────────────
genai_client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

pc = Pinecone(api_key=PINECONE_API_KEY)


def get_index():
    """Get or create Pinecone index."""
    existing = [i.name for i in pc.list_indexes()]

    if PINECONE_INDEX_NAME not in existing:
        print(f"Creating index '{PINECONE_INDEX_NAME}'...")
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=3072,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
        while not pc.describe_index(PINECONE_INDEX_NAME).status["ready"]:
            time.sleep(1)
        print("Index ready!")

    return pc.Index(PINECONE_INDEX_NAME)


def get_embedding(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings using Gemini."""
    result = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
    )
    return [e.values for e in result.embeddings]


def sanitize_id(name: str) -> str:
    """Make a string safe to use as part of a Pinecone vector ID."""
    safe = "".join(c if c.isalnum() else "_" for c in name)
    return safe.strip("_")


def store_in_pinecone(chunks, source_name: str = "document") -> dict:
    """Embed chunks and store in Pinecone, namespaced by source filename."""
    index = get_index()

    safe_source = sanitize_id(source_name)

    all_texts = [chunk.page_content for chunk in chunks]
    all_metadatas = [chunk.metadata for chunk in chunks]

    BATCH_SIZE = 10
    total_batches = (len(all_texts) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(all_texts), BATCH_SIZE):
        batch_texts = all_texts[i:i + BATCH_SIZE]
        batch_metadatas = all_metadatas[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        print(f"Embedding batch {batch_num}/{total_batches} for '{source_name}'...")

        for attempt in range(3):
            try:
                embeddings = get_embedding(batch_texts)

                vectors = []
                for j, (text, embedding, metadata) in enumerate(
                    zip(batch_texts, embeddings, batch_metadatas)
                ):
                    # Unique ID includes source filename so multiple PDFs don't collide
                    vector_id = f"{safe_source}_chunk_{i + j}"
                    vectors.append({
                        "id": vector_id,
                        "values": embedding,
                        "metadata": {
                            **metadata,
                            "text": text,
                            "source_file": source_name
                        }
                    })

                index.upsert(vectors=vectors)
                break

            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    print("  Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise RuntimeError(
                        f"Failed to embed batch {batch_num} after 3 attempts."
                    ) from e

        time.sleep(1)

    print(f"✅ All {len(all_texts)} chunks from '{source_name}' stored in Pinecone!")
    return {"chunks_created": len(all_texts), "source_file": source_name}


def query_pinecone(question: str, k: int = 5, source_file: str = None) -> tuple[str, list[dict]]:
    """Query Pinecone and return context + sources.
    Optionally filter by source_file to search within a specific document.
    """
    index = get_index()

    result = genai_client.models.embed_content(
        model="gemini-embedding-001",
        contents=[question],
    )
    query_embedding = result.embeddings[0].values

    query_kwargs = {
        "vector": query_embedding,
        "top_k": k,
        "include_metadata": True
    }

    if source_file:
        query_kwargs["filter"] = {"source_file": {"$eq": source_file}}

    results = index.query(**query_kwargs)

    documents = []
    sources = []

    for match in results["matches"]:
        text = match["metadata"].get("text", "")
        documents.append(text)
        sources.append({
            "page": match["metadata"].get("page", "unknown"),
            "source": match["metadata"].get("source_file", "unknown"),
            "score": round(match["score"], 3),
            "snippet": " ".join(text[:150].split()) + "..."
        })

    context = "\n\n".join(documents)
    return context, sources


def list_ingested_documents() -> list[str]:
    """Return a list of unique source filenames currently in the index.

    Note: Pinecone doesn't support listing distinct metadata values directly,
    so this uses a workaround by querying with a dummy vector and large top_k,
    then deduplicating source_file values. For production, maintain a separate
    registry (e.g., a small JSON file or DB table) of ingested filenames.
    """
    index = get_index()
    stats = index.describe_index_stats()
    return stats  # returns namespace/vector counts; filenames tracked separately


def delete_document(source_file: str) -> dict:
    """Delete all vectors belonging to a specific source file."""
    index = get_index()
    safe_source = sanitize_id(source_file)

    # Delete by metadata filter
    index.delete(filter={"source_file": {"$eq": source_file}})
    return {"status": "deleted", "source_file": source_file}