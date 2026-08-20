import os
import time
import requests
from flask import Flask, send_from_directory, render_template_string

app = Flask(__name__)
image_dir = '/usr/src/app/files'
image_path = os.path.join(image_dir, 'image.jpg')

os.makedirs(image_dir, exist_ok=True)

def fetch_image():
    response = requests.get('https://picsum.photos/1200', stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

def get_image():
    if not os.path.exists(image_path):
        fetch_image()
    else:
        file_age = time.time() - os.path.getmtime(image_path)
        if file_age > 600:
            fetch_image()

@app.route('/image.jpg')
def serve_image():
    get_image()
    return send_from_directory(image_dir, 'image.jpg')

@app.route('/')
def index():
    todos = [
        "Learn Kubernetes basics",
        "Deploy application to cluster",
        "Configure persistent volumes"
    ]
    
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Todo App</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; text-align: center; color: #333; }
            h1 { font-size: 2.2rem; }
            .project-img { width: 300px; height: 300px; object-fit: cover; border-radius: 12px; margin-bottom: 25px; }
            .todo-form { display: flex; justify-content: center; gap: 10px; margin-bottom: 30px; }
            input[type="text"] { width: 70%; padding: 10px; font-size: 1rem; border: 2px solid #4CAF50; border-radius: 6px; outline: none; }
            button { padding: 10px 20px; font-size: 1rem; background-color: #4CAF50; color: white; border: none; border-radius: 6px; cursor: pointer; }
            button:hover { background-color: #45a049; }
            .todo-list { list-style: none; padding: 0; text-align: left; }
            .todo-item { background-color: #f9f9f9; padding: 12px 15px; margin-bottom: 10px; border-left: 5px solid #4CAF50; border-radius: 4px; font-size: 1.05rem; }
        </style>
    </head>
    <body>
        <h1>Todo App</h1>
        <img class="project-img" src="/image.jpg" alt="Random image">
        
        <form class="todo-form" onsubmit="event.preventDefault();">
            <input type="text" maxlength="140" placeholder="Enter a new todo (max 140 characters)">
            <button type="submit">Send</button>
        </form>

        <h2>Todos</h2>
        <ul class="todo-list">
            {% for todo in todos %}
                <li class="todo-item">{{ todo }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_content, todos=todos)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
