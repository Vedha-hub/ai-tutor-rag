import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

embeddings_model = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def load_and_chunk_pdf(pdf_path: str):
    """Load a PDF and split into chunks."""
    print(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"Total chunks created: {len(chunks)}")
    return chunks

def store_in_chromadb(chunks: list):
    """Embed chunks and store in ChromaDB using new API."""
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        client=client
    )
    print(f"Stored {len(chunks)} chunks in ChromaDB at {CHROMA_DIR}")
    return vectorstore

def ingest_pdf(file_path: str) -> dict:
    chunks = load_and_chunk_pdf(file_path)
    store_in_chromadb(chunks)
    return {"status": "success", "chunks_created": len(chunks)}

def get_vectorstore():
    """Load existing ChromaDB."""
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_DIR)
    return Chroma(
        embedding_function=embeddings_model,
        client=client
    )

if __name__ == "__main__":
    ingest_pdf("../course.pdf")