import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()  # Load variables from .env file

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Using local free HuggingFace embeddings instead of OpenAI to bypass the quota limits
embeddings_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

def load_and_chunk_pdf(file_path: str) -> list:
    """Load a PDF and split into overlapping chunks."""
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    print(f"Loaded {len(pages)} pages from {file_path}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(pages)
    print(f"Created {len(chunks)} chunks")
    return chunks

def store_in_chromadb(chunks: list) -> Chroma:
    """Embed chunks and upsert into ChromaDB."""
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_DIR
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DIR}")
    return vectorstore

def ingest_pdf(file_path: str) -> dict:
    """Full pipeline: load → chunk → embed → store."""
    chunks = load_and_chunk_pdf(file_path)
    store_in_chromadb(chunks)
    return {"status": "success", "chunks_created": len(chunks)}

def get_vectorstore() -> Chroma:
    """Load existing ChromaDB for retrieval."""
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings_model
    )

if __name__ == "__main__":
    test_pdf_path = "../course.pdf" 
    print("--- Starting PDF Ingestion Pipeline Test ---")
    if os.path.exists(test_pdf_path):
        result = ingest_pdf(test_pdf_path)
        print("Pipeline Result Summary:", result)
    else:
        print(f"Error: Could not find '{test_pdf_path}'.")