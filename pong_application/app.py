import os
from flask import Flask

app = Flask(__name__)
data_dir = '/usr/src/app/files'
file_path = os.path.join(data_dir, 'pingpong.txt')

os.makedirs(data_dir, exist_ok=True)

def get_counter():
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                return int(f.read().strip())
            except ValueError:
                return 0
    return 0

def save_counter(count):
    with open(file_path, 'w') as f:
        f.write(str(count))

@app.route('/pingpong')
def pingpong():
    count = get_counter() + 1
    save_counter(count)
    return f"pong {count}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
