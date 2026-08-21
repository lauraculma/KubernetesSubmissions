import os
from flask import Flask

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Todo App</title>
</head>
<body>
    <h1>Todo App</h1>
    <form id="todo-form">
        <input type="text" id="todo-input" placeholder="New todo..." required />
        <button type="submit">Create TODO</button>
    </form>
    <ul id="todos-list"></ul>

    <script>
        async function fetchTodos() {
            const res = await fetch('/todos');
            const todos = await res.json();
            const list = document.getElementById('todos-list');
            list.innerHTML = '';
            todos.forEach(todo => {
                const li = document.createElement('li');
                li.textContent = todo;
                list.appendChild(li);
            });
        }

        document.getElementById('todo-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = document.getElementById('todo-input');
            await fetch('/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ todo: input.value })
            });
            input.value = '';
            fetchTodos();
        });

        fetchTodos();
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML_TEMPLATE

if __name__ == '__main__':
    print(f"Server started in port {PORT}", flush=True)
    app.run(host='0.0.0.0', port=PORT)
