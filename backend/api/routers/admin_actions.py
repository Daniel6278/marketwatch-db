from typing import Annotated

from fastapi import APIRouter

from fastapi import APIRouter, Header, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response

from ..internal.setup_db import setup_db, db_fill_starter_data
from ..internal import auth
from ..dependencies import DB_CONNECT_CONFIG

import json, pymysql

router = APIRouter()


@router.post("/setup", tags=["admin"])
async def sitewide_setup(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        setup_db()
        return Response(status_code=status.HTTP_200_OK)

    raise auth.UNAUTHORIZED_RESPONSE


@router.put("/fill", tags=["admin"])
async def insert_static_data_into_db(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        db_fill_starter_data()
        return Response(status_code=status.HTTP_200_OK)

    raise auth.UNAUTHORIZED_RESPONSE


ADMIN_AUTHORIZED_TABLES_NAMES = [
    "Alert",
    "User",
    "Ticker",
    "Portfolio",
    "PriceHistory",
    "Holdings",
    "AuditLog",
]  # do not remove! this prevents SQL injection attacks


@router.get("/tables", tags=["admin"])
async def list_tables(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        return Response(
            json.dumps(ADMIN_AUTHORIZED_TABLES_NAMES), media_type="application/json"
        )


@router.get("/table/{table_name}", tags=["admin"])
async def view_table(
    table_name: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    PRIVATE_COLUMNS_RESTRICTION_CONDITIONS = [
        "TABLE_NAME = 'User' AND (COLUMN_NAME = 'password_hash' OR COLUMN_NAME = 'email')"
    ]
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        if table_name in ADMIN_AUTHORIZED_TABLES_NAMES:
            with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT
                            COLUMN_NAME,
                            DATA_TYPE
                        FROM
                            INFORMATION_SCHEMA.COLUMNS
                        WHERE
                            TABLE_SCHEMA = %s AND TABLE_NAME = %s
                            {'\n'.join([f'AND NOT ({cond})' for cond in PRIVATE_COLUMNS_RESTRICTION_CONDITIONS])};
                        """,
                        (
                            DB_CONNECT_CONFIG["database"],
                            table_name,
                        ),
                    )
                    columns_infos = []
                    reflection_result = cursor.fetchall()
                    for unlabeled_column_info in reflection_result:
                        columns_infos.append(
                            {
                                "name": unlabeled_column_info[0],
                                "data_type": unlabeled_column_info[1],
                            }
                        )

                    sql = f"SELECT {','.join(f'`{col['name']}`' for col in columns_infos)} FROM {table_name};"
                    cursor.execute(sql)
                    results = (
                        cursor.fetchall()
                    )  # Fetches all results as a list of tuples
                return Response(
                    json.dumps({"columns": columns_infos, "rows": results}),
                    media_type="application/json",
                )

    raise auth.UNAUTHORIZED_RESPONSE
