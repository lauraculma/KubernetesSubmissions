import os
import psycopg2
from flask import Flask, jsonify, Response

app = Flask(__name__)

DB_HOST = os.getenv("POSTGRES_HOST", "postgres-svc")
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
PORT = int(os.getenv("PORT", 8080))

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pings (
                id INT PRIMARY KEY,
                count INT NOT NULL
            );
        """)
        cur.execute("SELECT count FROM pings WHERE id = 1;")
        if cur.fetchone() is None:
            cur.execute("INSERT INTO pings (id, count) VALUES (1, 0);")
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error initializing DB: {e}")

init_db()

@app.route("/healthz", methods=["GET"])
def healthz():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.close()
        conn.close()
        return Response("OK", status=200)
    except Exception as e:
        return Response(f"DB not connected: {e}", status=500)

@app.route("/pingpong", methods=["GET"])
def pingpong():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE pings SET count = count + 1 WHERE id = 1 RETURNING count;")
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return f"Pong {count}"
    except Exception as e:
        return Response(f"Database error: {e}", status=500)

@app.route("/pings", methods=["GET"])
def pings():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT count FROM pings WHERE id = 1;")
        res = cur.fetchone()
        count = res[0] if res else 0
        cur.close()
        conn.close()
        return jsonify({"pings": count})
    except Exception as e:
        return Response(f"Database error: {e}", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
