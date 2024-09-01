from typing import List

from fastapi import WebSocket

from schemas.notification import NotificationSchema

clients: List[WebSocket] = []


async def notify_client(message: NotificationSchema):
    for client in clients:
        await client.send_json(message.model_dump())
