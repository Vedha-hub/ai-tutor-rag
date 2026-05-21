import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# Using local free HuggingFace embeddings instead of OpenAI
embeddings_model = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
def load_and_chunk_pdf(file_path: str) -> list:
    print(f"Loading PDF from: {file_path}")
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks (chunk size: {CHUNK_SIZE}, overlap: {CHUNK_OVERLAP}).")
    return chunks
def store_in_chromadb(chunks: list) -> Chroma:
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_DIR
    )
    print(f"Stored chunks in local ChromaDB index.")
    return vectorstore

def ingest_pdf(file_path: str) -> dict:
    chunks = load_and_chunk_pdf(file_path)
    store_in_chromadb(chunks)
    return {"status": "success", "chunks_created": len(chunks)}

def get_vectorstore() -> Chroma:
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