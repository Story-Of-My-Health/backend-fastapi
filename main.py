from fastapi import FastAPI, WebSocket

from notifications import clients, notify_client
from routers.identity import router as identity_touter
from routers.user import router as user_router
from schemas.notification import (
    NotificationAction,
    NotificationModel,
    NotificationSchema,
)

app = FastAPI()


@app.websocket("/ws/notification")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        clients.remove(websocket)


@app.get("/test-ws", tags=["WS"])
async def test_ws():
    await notify_client(
        NotificationSchema(
            action=NotificationAction.UPDATE.value,
            model=NotificationModel.IDENTITY.value,
        )
    )
    return {"ok": "ok"}


app.include_router(user_router)
app.include_router(identity_touter)
