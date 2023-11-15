from fastapi import Depends, FastAPI
from .routers import audio, users, login

app = FastAPI()

app.include_router(users.router)
app.include_router(audio.router)
app.include_router(login.router)
