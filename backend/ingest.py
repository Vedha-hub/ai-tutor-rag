import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pinecone_store import store_in_pinecone
from document_registry import add_document

load_dotenv()


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


def ingest_pdf(pdf_path: str) -> dict:
    """Main entry point: load, chunk, embed, store in Pinecone."""
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env")
    if not os.getenv("PINECONE_API_KEY"):
        raise ValueError("PINECONE_API_KEY not found in .env")

    source_name = os.path.basename(pdf_path)

    chunks = load_and_chunk_pdf(pdf_path)
    result = store_in_pinecone(chunks, source_name=source_name)

    add_document(source_name, result["chunks_created"])

    print("🎉 Ingestion complete!")
    return result


if __name__ == "__main__":
    ingest_pdf("../course.pdf")