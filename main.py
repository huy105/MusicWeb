from fastapi import Depends, FastAPI
from .routers import items, users, login

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)
app.include_router(login.router)
