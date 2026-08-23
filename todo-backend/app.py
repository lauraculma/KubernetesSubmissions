import os
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 5000))
todos = ["Buy groceries", "Study Kubernetes"]

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json(silent=True) or {}
    todo = data.get("todo")
    if todo:
        todos.append(todo)
        return jsonify({"message": "Todo created", "todo": todo}), 201
    return jsonify({"error": "No todo provided"}), 400

if __name__ == '__main__':
    print(f"Backend started on port {PORT}", flush=True)
    app.run(host='0.0.0.0', port=PORT)
