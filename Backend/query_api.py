from flask import Flask, request, jsonify
from query_parser import parse_user_query
from semantic_search import find_similar_clauses
from answer_generator import generate_final_answer

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def handle_query():
    query = request.form['query']
    file = request.files['pdf']

    # (Optional) Save or parse file if needed
    file_path = f"./uploads/{file.filename}"
    file.save(file_path)

    # Step 1: Parse query
    metadata = parse_user_query(query)

    # Step 2: Semantic search
    top_matches = find_similar_clauses(query, metadata, top_k=3)

    # Step 3: Generate final answer
    clauses = [m['clause'] for m in top_matches]
    answer = generate_final_answer(query, metadata, clauses)

    return jsonify({
        "metadata": metadata,
        "top_matches": top_matches,
        "answer": answer
    })

if __name__ == '__main__':
    app.run(debug=True)
