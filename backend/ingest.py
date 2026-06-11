import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import chromadb

load_dotenv()

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Use HuggingFace for embeddings (free, no API needed)
embeddings_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def load_and_chunk_pdf(file_path: str) -> list:
    """Load PDF and split into chunks."""
    print(f"Loading PDF from: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

def store_in_chromadb(chunks: list):
    """Store chunks in ChromaDB."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        client=client
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DIR}")
    return vectorstore

def ingest_pdf(file_path: str) -> dict:
    """Full pipeline: load → chunk → embed → store."""
    chunks = load_and_chunk_pdf(file_path)
    store_in_chromadb(chunks)
    return {
        "status": "success",
        "chunks_created": len(chunks)
    }

def get_vectorstore() -> Chroma:
    """Load existing ChromaDB for retrieval."""
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return Chroma(
        embedding_function=embeddings_model,
        client=client
    )