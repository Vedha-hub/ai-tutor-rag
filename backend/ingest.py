import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import chromadb
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ── Gemini client using new google-genai SDK ───────────────────────────────────
client = genai.Client(
    api_key=GOOGLE_API_KEY,
    http_options={"api_version": "v1"}
)

def get_embedding(texts: list[str]) -> list[list[float]]:
    """Embed a list of strings using the new google-genai SDK."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=texts,
    )
    return [e.values for e in result.embeddings]


def load_and_chunk_pdf(pdf_path: str):
    """Load a PDF and split into chunks."""
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Total pages loaded: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks


def store_in_chromadb(chunks):
    """Embed chunks and store in ChromaDB using direct Chroma client."""

    # Use ChromaDB client directly — avoids langchain embedding wrapper issues
    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    # Delete collection if it exists (fresh start)
    try:
        chroma_client.delete_collection("course_docs")
    except Exception:
        pass

    collection = chroma_client.create_collection("course_docs")

    all_texts = [chunk.page_content for chunk in chunks]
    all_metadatas = [chunk.metadata for chunk in chunks]

    BATCH_SIZE = 10
    total_batches = (len(all_texts) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(all_texts), BATCH_SIZE):
        batch_texts = all_texts[i:i + BATCH_SIZE]
        batch_metadatas = all_metadatas[i:i + BATCH_SIZE]
        batch_ids = [f"chunk_{i + j}" for j in range(len(batch_texts))]
        batch_num = i // BATCH_SIZE + 1

        print(f"Embedding batch {batch_num}/{total_batches}...")

        for attempt in range(3):
            try:
                embeddings = get_embedding(batch_texts)

                collection.add(
                    documents=batch_texts,
                    embeddings=embeddings,
                    metadatas=batch_metadatas,
                    ids=batch_ids
                )
                break  # success

            except Exception as e:
                print(f"  Attempt {attempt + 1} failed: {e}")
                if attempt < 2:
                    print("  Retrying in 5 seconds...")
                    time.sleep(5)
                else:
                    raise RuntimeError(
                        f"Failed to embed batch {batch_num} after 3 attempts."
                    ) from e

        time.sleep(1)  # rate limit buffer between batches

    print(f"✅ All {len(all_texts)} chunks stored in ChromaDB!")
    return collection


def ingest_pdf(pdf_path: str):
    chunks = load_and_chunk_pdf(pdf_path)
    collection = store_in_chromadb(chunks)
    print("🎉 Ingestion complete! PDF is ready for Q&A.")
    return {"chunks_created": len(chunks)}


if __name__ == "__main__":
    ingest_pdf("../course.pdf")