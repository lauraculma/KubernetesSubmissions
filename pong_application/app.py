import os
from flask import Flask

app = Flask(__name__)
counter = 0

@app.route('/pingpong')
def pingpong():
    global counter
    counter += 1
    return f"pong {counter}"

@app.route('/pings')
def pings():
    global counter
    return str(counter)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
