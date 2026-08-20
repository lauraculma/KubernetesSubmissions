import os
from flask import Flask

app = Flask(__name__)
log_file_path = '/usr/src/app/files/log.txt'

@app.route('/')
def read_log():
    if os.path.exists(log_file_path):
        with open(log_file_path, 'r') as f:
            content = f.read()
        return content
    return "No logs generated yet.", 404

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    print(f"Reader server started on port {port}", flush=True)
    app.run(host='0.0.0.0', port=port)
