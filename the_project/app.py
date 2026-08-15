import os
from flask import Flask

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))

@app.route('/')
def home():
    return "Todo App - Project v0.1"

if __name__ == '__main__':
    print(f"Server started in port {PORT}", flush=True)
    app.run(host='0.0.0.0', port=PORT)
