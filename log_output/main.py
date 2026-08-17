import os
import uuid
from datetime import datetime
from flask import Flask

app = Flask(__name__)

# Generar la cadena aleatoria única al iniciar la aplicación
RANDOM_STRING = str(uuid.uuid4())

@app.route('/')
def status():
    current_time = datetime.now().isoformat()
    return f"{current_time}: {RANDOM_STRING}\n"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    print(f"Server started on port {port}", flush=True)
    app.run(host='0.0.0.0', port=port)
