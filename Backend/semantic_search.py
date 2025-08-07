from sentence_transformers import SentenceTransformer
import chromadb
import json
import sys

# Load embedding model
def get_embedder(model_name="all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)

# Perform semantic search
def semantic_search(query, top_k=3, model_name="all-MiniLM-L6-v2", chroma_path="./chroma", collection_name="insurance_clauses"):
    # Step 1: Encode the query
    embedder = get_embedder(model_name)
    query_embedding = embedder.encode([query])[0]  # Single query

    # Step 2: Load ChromaDB
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection(collection_name)

    # Step 3: Query top-k matches
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# Command-line run
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python semantic_search.py \"your full query\"")
        sys.exit(1)

    query = sys.argv[1]
    print("🔍 Running semantic search on query:", query)

    search_results = semantic_search(query)

    print("\n📄 Top Matching Clauses:\n")
    for i, text in enumerate(search_results['documents'][0]):
        print(f"{i+1}. {text}\n")
