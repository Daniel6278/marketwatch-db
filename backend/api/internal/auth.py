from typing import Annotated

from ..dependencies import DB_CONNECT_CONFIG

import pymysql

from hashlib import sha256
import base64

from fastapi import HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()

# default responses when fail authenticate as user
UNAUTHORIZED_RESPONSE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Basic"},
)
FORBIDDEN_RESPONSE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You do not have permission to do this.",
)

# default responses when fail authenticate as admin
ADMIN_UNAUTHORIZED_RESPONSE = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="You need to sign in as an admin to do this.",
    headers={"WWW-Authenticate": "Basic"},
)
ADMIN_FORBIDDEN_RESPONSE = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You are not an admin user, or the admin username and password you provided are incorrect credentials.",
)


def credentials_b64(username_no_colon, password_hash):
    return base64.b64encode(
        (username_no_colon + ":" + password_hash).encode("utf-8")
    ).decode("utf-8")


def hash_password(password: str):
    return base64.b64encode(sha256(password.encode("utf-8")).digest()).decode("utf-8")


def verify_user_authentication(user_id: str, password_hash: str):
    with pymysql.connect(**DB_CONNECT_CONFIG) as conn, open(
        "api/sql/crud_ops/read/authenticate_user.sql", "r"
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


def basic_admin_auth_wrapper(credentials, callback):
    if credentials.username and credentials.password:
        if verify_admin_authentication(credentials.username, credentials.password):
            return callback()
        raise ADMIN_FORBIDDEN_RESPONSE
    raise ADMIN_UNAUTHORIZED_RESPONSE
