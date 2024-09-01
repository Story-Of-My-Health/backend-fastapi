from typing import List

from fastapi import WebSocket

clients: List[WebSocket] = []


async def notify_client(message: str):
    for client in clients:
        await client.send_text(message)
