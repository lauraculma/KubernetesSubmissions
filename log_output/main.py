import os
import uuid
from datetime import datetime
import urllib.request
from flask import Flask

app = Flask(__name__)
RANDOM_STRING = str(uuid.uuid4())

CONFIG_FILE_PATH = "/config/information.txt"

def get_file_content():
    if os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "r") as f:
            return f.read().strip()
    return "file not found"

def get_pingpong_count():
    try:
        # Consulta al servicio pong-app-svc dentro del namespace exercises
        with urllib.request.urlopen("http://pong-app-svc:80/pingpong", timeout=2) as response:
            text = response.read().decode('utf-8')
            # Si responde "pong X", extraemos el número
            count = text.replace("pong", "").strip()
            return count
    except Exception:
        return "0"

@app.route('/')
def root():
    file_content = get_file_content()
    env_message = os.environ.get("MESSAGE", "No MESSAGE env set")
    current_time = datetime.utcnow().isoformat() + "Z"
    pongs = get_pingpong_count()

    output = (
        f"file content: {file_content}\n"
        f"env variable: MESSAGE={env_message}\n"
        f"{current_time}: {RANDOM_STRING}.\n"
        f"Ping / Pongs: {pongs}\n"
    )
    return output, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    print(f"Server started on port {port}", flush=True)
    app.run(host='0.0.0.0', port=port)
