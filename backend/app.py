
from flask import Flask, request, jsonify
from flask_cors import CORS
from llama_index.core import StorageContext, load_index_from_storage
from dotenv import load_dotenv
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/response": {"origins": "*"}})
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return 'Hello from Flask!'

@app.route('/response', methods=['POST'])
def get_response():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Load the index and create the query engine inside the route
    storage_context = StorageContext.from_defaults(persist_dir="KBot Storage")
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()

    response = query_engine.query(query)
    return jsonify({"response": str(response)})

if __name__ == '__main__':
    app.run(debug=True)