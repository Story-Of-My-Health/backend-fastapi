from fastapi import Depends, FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from auth2.auth_schema import verify_token
from notifications import clients, notify_client
from routers.disease import router as disease_router
from routers.identity import router as identity_router
from routers.user import router as user_router
from schemas.notification import (
    NotificationAction,
    NotificationModel,
    NotificationSchema,
)

app = FastAPI()

origins = ["http://localhost:5173", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
            performer_id=5,
            action=NotificationAction.UPDATE.value,
            model=NotificationModel.IDENTITY.value,
        )
    )
    return {"ok": "ok"}


app.include_router(user_router)
app.include_router(
    disease_router,
    dependencies=[Depends(verify_token)],
)
app.include_router(
    identity_router,
    # Comment this to create identity for first time
    dependencies=[Depends(verify_token)],
)
