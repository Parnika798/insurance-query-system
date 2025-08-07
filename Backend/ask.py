import sys
from Backend.query_parser import parse_query
from Backend.semantic_search import semantic_search
from Backend.answer_generator import generate_answer

def main():
    if len(sys.argv) < 2:
        print("Usage: python ask.py \"<your insurance-related question>\"")
        return

    query = sys.argv[1]

    print("\n🔎 Parsing user query...")
    query_dict = parse_query(query)
    print(query_dict)

    print("\n🔍 Running semantic search...")
    filters = {
        "doc_type": "insurance",
        "intent": query_dict.get("intent")
    }
    results = semantic_search(query)

    print("\n📄 Top Matching Clauses:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")


    print("\n🧠 Generating Explanation...\n")
    final_response = generate_answer(query_dict, results)
    print(final_response)

if __name__ == "__main__":
    main()
