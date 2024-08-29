from fastapi import FastAPI

from routers.identity import router as identity_touter
from routers.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(identity_touter)
