import os
import time
import uuid
from datetime import datetime

# Crear el directorio compartido si no existe
os.makedirs('/usr/src/app/files', exist_ok=True)
log_file_path = '/usr/src/app/files/log.txt'

random_string = str(uuid.uuid4())

while True:
    current_time = datetime.now().isoformat()
    log_entry = f"{current_time}: {random_string}\n"
    
    with open(log_file_path, 'w') as f:
        f.write(log_entry)
        
    print(f"Wrote to file: {log_entry.strip()}", flush=True)
    time.sleep(5)
