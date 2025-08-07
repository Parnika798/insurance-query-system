# embedandstore.py

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import pandas as pd

# ------------------- 2.1 Load Embedding Model -------------------

def get_embedder(model_name="all-MiniLM-L6-v2"):
    return SentenceTransformer(model_name)

# ------------------- 2.2 Prepare Embedding Records -------------------

def create_embedding_records(df, embedder, doc_type="insurance"):
    texts = df["clause_text"].tolist()
    embeddings = embedder.encode(texts, show_progress_bar=True)

    records = []
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        record = {
            "chunk_id": df["clause_id"].iloc[i],
            "text": text,
            "embedding": embedding.tolist(),
            "metadata": {
                "source": df["policy_name"].iloc[i],
                "section": df["section"].iloc[i],
                "doc_type": doc_type,
                "intent": "general"  # ✅ Added default intent
            }
        }
        records.append(record)
    return records

# ------------------- 2.3 Store in ChromaDB -------------------

def store_in_chromadb(records, collection_name="insurance_clauses", persist_path="./chroma"):
    client = chromadb.PersistentClient(path=persist_path)

    # Create or load collection
    collection = client.get_or_create_collection(name=collection_name)

    # Prepare fields
    ids = [rec["chunk_id"] for rec in records]
    texts = [rec["text"] for rec in records]
    embeddings = [rec["embedding"] for rec in records]
    metadatas = [rec["metadata"] for rec in records]

    # Add to collection
    collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    print(f"✅ Stored {len(records)} embeddings in ChromaDB → {collection_name}")

# ------------------- Main Execution (Optional Script Mode) -------------------

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("❌ Usage: python embedandstore.py path/to/chunked_output.csv")
        sys.exit(1)

    csv_path = sys.argv[1]
    df = pd.read_csv(csv_path)

    print("📥 Loaded chunked clauses:", len(df))

    embedder = get_embedder()
    records = create_embedding_records(df, embedder)
    store_in_chromadb(records)
