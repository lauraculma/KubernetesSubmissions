import os
import asyncio
import json
import requests
from nats.aio.client import Client as NATS

NATS_URL = os.getenv("NATS_URL", "nats://nats-svc:4222")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")

async def run():
    nc = NATS()
    print(f"Connecting to NATS at {NATS_URL}...")
    await nc.connect(NATS_URL)
    print("Connected to NATS.")

    async def message_handler(msg):
        data = msg.data.decode()
        print(f"Received message: {data}")
        
        # Enviar al servicio externo (Discord o Webhook genérico)
        if WEBHOOK_URL:
            try:
                # Payload compatible con Discord y Webhook genérico
                payload = {
                    "content": f"[Todo Bot] {data}",
                    "user": "bot",
                    "message": data
                }
                res = requests.post(WEBHOOK_URL, json=payload, timeout=5)
                print(f"Forwarded to webhook, response status: {res.status_code}")
            except Exception as e:
                print(f"Error forwarding message: {e}")
        else:
            print(f"[DRY-RUN - No WEBHOOK_URL set]: {data}")

    # queue="broadcaster-group" asegura que solo 1 réplica reciba cada mensaje
    await nc.subscribe("todos", queue="broadcaster-group", cb=message_handler)
    print("Subscribed to 'todos' subject with queue group 'broadcaster-group'.")

    while True:
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(run())
