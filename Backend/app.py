from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from query_parser import parse_query
from semantic_search import semantic_search
from answer_generator import generate_answer

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/api/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    user_query = data.get('query', '')
    selected_document = data.get('document', '')

    metadata = parse_query(user_query)
    top_matches = semantic_search(metadata, selected_document)
    final_answer = generate_answer(user_query, top_matches)

    return jsonify({
        'final_answer': final_answer,
        'matches': top_matches
    })

if __name__ == '__main__':
    app.run(debug=True)
