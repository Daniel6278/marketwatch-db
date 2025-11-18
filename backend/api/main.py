from fastapi import FastAPI

from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination, Page, Params

from .dependencies import DB_CONNECT_CONFIG
from .internal import setup_db
from .routers import admin_actions, user_actions, tests

app = FastAPI()
add_pagination(app)

app.include_router(tests.router)
app.include_router(
    admin_actions.router,
    prefix="/admin",
    tags=["admin"],
)
app.include_router(
    user_actions.router,
    tags=["users"],
)
