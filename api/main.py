from fastapi import FastAPI

from fastapi import Depends, FastAPI

from .dependencies import get_DB_CONNECT_CONFIG
from .internal import setup_db
from .routers import admin_actions, user_actions, tests

app = FastAPI(dependencies=[Depends(get_DB_CONNECT_CONFIG)])

app.include_router(tests.router)
app.include_router(
    admin_actions.router,
    prefix="/admin",
    tags=["admin"],
)
app.include_router(
    user_actions.router,
    prefix="/user",
    tags=["users"],
)
