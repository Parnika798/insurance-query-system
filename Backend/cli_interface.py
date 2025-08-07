import os
import sys
from query_parser import parse_query
from semantic_search import find_similar_clauses
from answer_generator import generate_final_answer
import pandas as pd

def load_chunked_clauses(csv_path="chunked_clauses.csv"):
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        sys.exit(1)
    return pd.read_csv(csv_path)

def main():
    print("📄 Insurance Query System CLI")
    
    # Step 1: Ask for document (for context, logging, or future use)
    doc_path = input("Enter the path to the insurance document (PDF): ").strip()
    if not os.path.exists(doc_path):
        print("Error: File not found.")
        return
    
    # Step 2: Ask for the user query
    query = input("🔍 Enter your query about the policy: ").strip()
    if not query:
        print("Error: Empty query.")
        return

    # Step 3: Parse the query using query_parser
    print("\n🧠 Parsing query...")
    metadata = parse_query(query)
    print(f"Parsed metadata: {metadata}")

    # Step 4: Perform semantic search
    print("\n🔎 Performing semantic search...")
    top_matches = find_similar_clauses(query, metadata, top_k=3)

    if not top_matches:
        print("No matching clauses found.")
        return

    print("\n📌 Top matching clauses:")
    for idx, match in enumerate(top_matches, 1):
        print(f"\n{idx}. Clause: {match['clause']}")
        print(f"   Similarity Score: {match['score']:.4f}")

    # Step 5: Generate final answer
    print("\n✍️ Generating final explanation...")
    clauses = [m['clause'] for m in top_matches]
    answer = generate_final_answer(query, metadata, clauses)

    print("\n✅ Final Answer:")
    print(answer)

if __name__ == "__main__":
    main()
