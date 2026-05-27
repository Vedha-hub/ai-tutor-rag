from ingest import get_vectorstore

def test_retrieval():
    """Test similarity search retrieval."""
    vectorstore = get_vectorstore()
    
    questions = [
        "What is image processing?",
        "What are the course outcomes?",
        "What topics are covered?",
        "What are the reference books?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        docs = vectorstore.similarity_search(question, k=3)
        print(f"Retrieved {len(docs)} chunks:")
        for i, doc in enumerate(docs):
            print(f"  Chunk {i+1} (page {doc.metadata.get('page','?')}): {doc.page_content[:100]}...")

if __name__ == "__main__":
    test_retrieval()