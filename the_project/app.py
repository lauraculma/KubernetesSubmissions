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
        if file_age > 600:  # 10 minutos (600 segundos)
            fetch_image()

@app.route('/image.jpg')
def serve_image():
    get_image()
    return send_from_directory(image_dir, 'image.jpg')

@app.route('/')
def index():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Todo App</title>
        <style>
            body { font-family: sans-serif; text-align: center; margin-top: 40px; }
            img { width: 400px; height: 400px; object-fit: cover; border-radius: 8px; }
        </style>
    </head>
    <body>
        <h1>Todo App</h1>
        <img src="/image.jpg" alt="Random Image">
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
