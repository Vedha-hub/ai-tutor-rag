from ingest import get_vectorstore

# Load your active local ChromaDB index
db = get_vectorstore()

# Query the database to test the mathematical similarity matching
results = db.similarity_search("What is the exam pattern?", k=3)

print("--- STARTING LOCAL RETRIEVAL VERIFICATION ---")
for doc in results:
    print("\n--- CHUNK MATCH --- \n", doc.page_content)