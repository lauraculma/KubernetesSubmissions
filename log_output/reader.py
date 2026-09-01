import os
import requests
from flask import Flask, Response

app = Flask(__name__)

PORT = int(os.getenv("PORT", 3000))
FILE_PATH = "/usr/src/app/files/timestamp.txt"
PINGPONG_URL = os.getenv("PINGPONG_URL", "http://pingpong-svc:8080/pings")
MESSAGE = os.getenv("MESSAGE", "")

@app.route("/healthz", methods=["GET"])
def healthz():
    try:
        res = requests.get(PINGPONG_URL, timeout=2)
        if res.status_code == 200:
            return Response("OK", status=200)
        return Response("Pingpong not ready", status=500)
    except Exception as e:
        return Response(f"Pingpong unreachable: {e}", status=500)

@app.route("/", methods=["GET"])
def index():
    timestamp = "No timestamp yet"
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            timestamp = f.read()

    ping_count = "N/A"
    try:
        res = requests.get(PINGPONG_URL, timeout=2)
        if res.status_code == 200:
            data = res.json()
            ping_count = data.get("pings", "N/A")
    except Exception:
        ping_count = "Ping-pong unreachable"

    return f"{MESSAGE}<br>{timestamp}<br>Ping / Pongs: {ping_count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
