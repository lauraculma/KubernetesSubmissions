import os
from flask import Flask

app = Flask(__name__)
log_file_path = '/usr/src/app/files/log.txt'
pingpong_file_path = '/usr/src/app/files/pingpong.txt'

@app.route('/')
def read_log():
    log_content = ""
    pingpong_count = 0

    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            log_content = f.read().strip()

    if os.path.exists(pingpong_file_path):
        with open(pingpong_file_path, 'r') as f:
            try:
                pingpong_count = int(f.read().strip())
            except ValueError:
                pingpong_count = 0

    return f"{log_content}\nPing / Pongs: {pingpong_count}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)
