import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

CHROMA_DIR = "./chroma_db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def load_and_chunk_pdf(file_path: str) -> list:
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks.")
    return chunks

def store_in_chromadb(chunks: list) -> Chroma:
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings_model,
        persist_directory=CHROMA_DIR
    )
    vectorstore.persist()
    print(f"Stored chunks in ChromaDB at {CHROMA_DIR}")
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