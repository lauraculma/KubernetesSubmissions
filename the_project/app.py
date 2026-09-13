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
                content VARCHAR(140) NOT NULL,
                done BOOLEAN DEFAULT FALSE
            );
        """)
        # Asegurar la columna done si la tabla ya existía previamente
        cur.execute("""
            ALTER TABLE todos ADD COLUMN IF NOT EXISTS done BOOLEAN DEFAULT FALSE;
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
        body { font-family: sans-serif; display: flex; flex-direction: column; align-items: center; padding: 40px; background-color: #ffffff; color: #333; }
        h1 { margin-bottom: 20px; font-size: 2rem; }
        img { width: 220px; height: 160px; object-fit: cover; border-radius: 8px; margin-bottom: 25px; box-shadow: 0 2px 5px rgba(0,0,0,0.15); }
        .form-container { display: flex; gap: 10px; width: 100%; max-width: 550px; margin-bottom: 25px; }
        input[type="text"] { flex: 1; padding: 10px 14px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; }
        button.btn-send { background-color: #4CAF50; color: white; border: none; padding: 10px 22px; border-radius: 4px; cursor: pointer; font-size: 14px; }
        .todos-list { width: 100%; max-width: 550px; list-style: none; padding: 0; margin: 0; }
        .todo-item { display: flex; justify-content: space-between; align-items: center; background: #fdfdfd; border: 1px solid #e0e0e0; border-left: 4px solid #4CAF50; padding: 14px 18px; margin-bottom: 12px; border-radius: 4px; }
        .todo-item.done { border-left-color: #9e9e9e; color: #757575; }
        .todo-item.done .todo-text { text-decoration: line-through; }
        .btn-mark-done { background-color: #1976d2; color: white; border: none; padding: 6px 14px; border-radius: 4px; cursor: pointer; font-size: 13px; font-weight: 500; }
        .done-label { color: #2e7d32; font-weight: bold; font-size: 14px; }
        .break-btn { margin-top: 30px; background-color: #d9534f; color: white; border: none; padding: 10px 18px; border-radius: 4px; cursor: pointer; }
        .error-card { background: #ffebee; border: 1px solid #ffcdd2; color: #b71c1c; padding: 30px; border-radius: 8px; text-align: center; max-width: 500px; margin-top: 50px; }
        footer { margin-top: 40px; font-size: 12px; color: #777; }
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
        {% for id, content, done in todos %}
        <li class="todo-item {% if done %}done{% endif %}">
            <span class="todo-text">{{ content }}</span>
            {% if done %}
                <span class="done-label">Done</span>
            {% else %}
                <button class="btn-mark-done" onclick="markDone({{ id }})">Mark done</button>
            {% endif %}
        </li>
        {% endfor %}
    </ul>

    <form method="POST" action="/break">
        <button type="submit" class="break-btn">break the app</button>
    </form>

    <footer>DevOps with Kubernetes 2026</footer>

    <script>
        async function markDone(id) {
            const res = await fetch(`/todos/${id}`, { method: 'PUT' });
            if (res.ok) {
                window.location.reload();
            } else {
                alert('Failed to mark todo as done');
            }
        }
    </script>
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
        cur.execute("SELECT id, content, done FROM todos ORDER BY id ASC;")
        todos = cur.fetchall()
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
            cur.execute("INSERT INTO todos (content, done) VALUES (%s, %s);", (content, False))
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Error inserting todo: {e}")
    return redirect(url_for("index"))

@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE todos SET done = TRUE WHERE id = %s;", (todo_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"status": "updated", "id": todo_id}), 200
    except Exception as e:
        print(f"Error updating todo: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
