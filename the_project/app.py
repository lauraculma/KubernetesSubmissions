import os
import requests
import psycopg2
from flask import Flask, request, jsonify, render_template_string, redirect, url_for, Response

app = Flask(__name__)
PORT = int(os.getenv("PORT", 5000))
DB_HOST = os.getenv("POSTGRES_HOST", "postgres-svc")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")

is_healthy = True

def get_db():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id SERIAL PRIMARY KEY,
                content VARCHAR(140) NOT NULL
            );
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing DB: {e}")

init_db()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
    <style>
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 40px; background-color: #f9f9f9; }
        h1 { margin-bottom: 20px; }
        img { width: 250px; height: 180px; object-fit: cover; border-radius: 8px; margin-bottom: 25px; }
        .form-container { display: flex; gap: 10px; width: 100%; max-width: 500px; margin-bottom: 30px; }
        input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button.btn-send { background-color: #4CAF50; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
        .todos-list { width: 100%; max-width: 500px; list-style: none; padding: 0; }
        .todo-item { background: white; border-left: 4px solid #4CAF50; padding: 12px 16px; margin-bottom: 10px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .break-btn { margin-top: 30px; background-color: #d9534f; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer; }
        .error-card { background: #ffebee; border: 1px solid #ffcdd2; color: #b71c1c; padding: 30px; border-radius: 8px; text-align: center; max-width: 500px; margin-top: 50px; }
    </style>
</head>
<body>
    {% if not is_healthy %}
    <div class="error-card">
        <h1>System Failure</h1>
        <p>The Todo App is currently unhealthy. Please wait for recovery.</p>
    </div>
    {% else %}
    <h1>Todo App</h1>
    <img src="https://picsum.photos/1200" alt="Daily Image">
    
    <form class="form-container" method="POST" action="/todos">
        <input type="text" name="content" maxlength="140" placeholder="Enter a new todo (max 140 characters)" required>
        <button type="submit" class="btn-send">Send</button>
    </form>

    <h2>Todos</h2>
    <ul class="todos-list">
        {% for todo in todos %}
        <li class="todo-item">{{ todo }}</li>
        {% endfor %}
    </ul>

    <form method="POST" action="/break">
        <button type="submit" class="break-btn">break the app</button>
    </form>
    {% endif %}
</body>
</html>
"""

@app.route("/healthz", methods=["GET"])
def healthz():
    global is_healthy
    if not is_healthy:
        return Response("Unhealthy", status=500)
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return Response("OK", status=200)
    except Exception as e:
        return Response(f"DB not ready: {e}", status=500)

@app.route("/break", methods=["POST"])
def break_app():
    global is_healthy
    is_healthy = False
    print("Application marked as UNHEALTHY via break button.")
    return redirect(url_for("index"))

@app.route("/", methods=["GET"])
def index():
    global is_healthy
    if not is_healthy:
        return render_template_string(HTML_TEMPLATE, is_healthy=False, todos=[])
    
    todos = []
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT content FROM todos ORDER BY id ASC;")
        todos = [row[0] for row in cur.fetchall()]
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error reading todos: {e}")
    
    return render_template_string(HTML_TEMPLATE, is_healthy=True, todos=todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    content = request.form.get("content", "").strip()
    if content and len(content) <= 140:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO todos (content) VALUES (%s);", (content,))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error inserting todo: {e}")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
