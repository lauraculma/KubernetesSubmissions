import os
import time
import psycopg2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

PORT = int(os.environ.get("PORT", 5000))
DB_HOST = os.environ.get("POSTGRES_HOST", "project-postgres-svc")
DB_NAME = os.environ.get("POSTGRES_DB", "tododb")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "todopassword")

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except Exception as e:
            print(f"Waiting for database: {e}", flush=True)
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            text VARCHAR(140) NOT NULL
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT text FROM todos ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    todos = [row[0] for row in rows]
    return jsonify(todos), 200

@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json(silent=True) or {}
    todo = data.get("todo")
    if not todo or len(todo) > 140:
        return jsonify({"error": "Todo text is invalid or exceeds 140 chars"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (text) VALUES (%s);", (todo,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Todo created", "todo": todo}), 201

if __name__ == '__main__':
    print(f"Backend started on port {PORT}", flush=True)
    app.run(host='0.0.0.0', port=PORT)
