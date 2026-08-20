import os
import requests
from flask import Flask

app = Flask(__name__)
log_file_path = '/usr/src/app/files/log.txt'
PINGPONG_URL = os.environ.get("PINGPONG_URL", "http://pingpong-svc:5000/pings")

@app.route('/')
def read_log():
    log_content = ""
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            log_content = f.read().strip()

    pingpong_count = "0"
    try:
        response = requests.get(PINGPONG_URL, timeout=2)
        if response.status_code == 200:
            pingpong_count = response.text.strip()
    except Exception as e:
        pingpong_count = f"Error connecting: {e}"

    return f"{log_content}\nPing / Pongs: {pingpong_count}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
