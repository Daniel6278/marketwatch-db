from typing import Annotated

from ..dependencies import DB_CONNECT_CONFIG

import pymysql

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

UNAUTHORIZED_RESPONSE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Basic"},
)


def verify_user_authentication(user_id: str, password_hash: str):
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "api/sql/ops/authenticate_user.sql", "r"
    ) as query:
        cursor = conn.cursor()
        cursor.execute(
            query.read(),
            {
                "user_id": user_id,
                "password_hash": password_hash,
            },
        )
        conn.commit()

        is_auth_successful = cursor.fetchone()[0]

        if is_auth_successful:
            return True
    return False


def verify_admin_authentication(username: str, password: str):
    try:
        print(username, password, DB_CONNECT_CONFIG["host"])
        with pymysql.connect(
            host=DB_CONNECT_CONFIG["host"],
            port=DB_CONNECT_CONFIG["port"],
            database=DB_CONNECT_CONFIG["database"],
            user=username,
            password=password,
        ) as conn:
            return True
    except:
        pass
    return False
