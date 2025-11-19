from fastapi import FastAPI

from fastapi import Depends, FastAPI
from fastapi_pagination import add_pagination
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import DB_CONNECT_CONFIG
from .internal import setup_db
from .routers import admin_actions, user_actions, tests, public_actions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://marketwatch-db.onrender.com",
        "localhost:5173",
        "http://localhost:5173",
        "https://localhost:5173",
    ],
    allow_credentials=True,  # Set to True if your frontend needs to send cookies or HTTP authentication
    allow_methods=["*"],  # Or specify a list of allowed methods, e.g., ["GET", "POST"]
    allow_headers=["*"],  # Or specify a list of allowed headers
)
add_pagination(app)

app.include_router(tests.router)
app.include_router(
    public_actions.router,
    tags=["public"],
)
app.include_router(
    admin_actions.router,
    prefix="/admin",
    tags=["admin"],
)
app.include_router(
    user_actions.router,
    tags=["users"],
)
