import os
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi_pagination import Page, Params

import logging
from functools import lru_cache

DB_CONNECT_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASSWORD"],
    "database": os.environ["DB_NAME"],
    "port": int(os.environ["DB_PORT"]),
}

BAD_REQUEST_RESPONSE = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="The data you sent to the API is invalid.",
)


class DatabaseError(HTTPException):
    def __init__(self, sql_script_name: str | tuple):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database Error from Run SQL Script: {sql_script_name if isinstance(sql_script_name, str) else ','.join(sql_script_name)}",
        )
        self.sql_script_name = sql_script_name


# Configure logger (e.g., set level, add handlers)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


@lru_cache()  # Cache the logger instance for performance
def get_logger(name: str = "fastapi-app") -> logging.Logger:
    return logging.getLogger(name)


def pagination_augment(params: Params):
    params.start = (params.page - 1) * params.size  # type: ignore
    return params
