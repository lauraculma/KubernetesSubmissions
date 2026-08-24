import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 3000))

DB_HOST = os.environ.get("POSTGRES_HOST", "postgres-svc")
DB_NAME = os.environ.get("POSTGRES_DB", "pingpong_db")
DB_USER = os.environ.get("POSTGRES_USER", "postgres")
DB_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "mysecretpassword")

def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            return conn
        except Exception as e:
            print(f"Waiting for database connection: {e}", flush=True)
            time.sleep(2)

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS counter_table (
            id SERIAL PRIMARY KEY,
            count INT NOT NULL
        );
    """)
    cur.execute("SELECT count FROM counter_table WHERE id = 1;")
    row = cur.fetchone()
    if row is None:
        cur.execute("INSERT INTO counter_table (id, count) VALUES (1, 0);")
    conn.commit()
    cur.close()
    conn.close()

init_db()

@app.route('/')
def health():
    return "OK", 200

@app.route('/pingpong')
def pingpong():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT count FROM counter_table WHERE id = 1;")
    current_count = cur.fetchone()[0]

    response = f"pong {current_count}"

    cur.execute("UPDATE counter_table SET count = count + 1 WHERE id = 1;")
    conn.commit()
    cur.close()
    conn.close()

    return response

if __name__ == '__main__':
    print(f"Ping-pong app started on port {PORT}", flush=True)
    app.run(host='0.0.0.0', port=PORT)
