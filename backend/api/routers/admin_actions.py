from typing import Annotated

from fastapi import APIRouter

from fastapi import APIRouter, Header, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response

from ..internal.setup_db import setup_db, db_fill_starter_data
from ..internal import auth
from ..dependencies import DB_CONNECT_CONFIG

import json, pymysql

from collections import defaultdict

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

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 string
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return json.JSONEncoder.default(self, obj) # Let the base class handle other types

@router.get("/table/{table_name}", tags=["admin"])
async def view_table(
    table_name: str,
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    PRIVATE_COLUMNS_RESTRICTION_CONDITIONS = [
        "c.TABLE_NAME = 'User' AND (c.COLUMN_NAME = 'password_hash' OR c.COLUMN_NAME = 'email')"
    ]
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        if table_name in ADMIN_AUTHORIZED_TABLES_NAMES:
            with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT
                                c.COLUMN_NAME,
                                c.DATA_TYPE,
                                kcu.REFERENCED_TABLE_NAME
                            FROM
                                INFORMATION_SCHEMA.COLUMNS AS c
                            LEFT JOIN
                                INFORMATION_SCHEMA.KEY_COLUMN_USAGE AS kcu
                            ON
                                c.TABLE_SCHEMA = kcu.TABLE_SCHEMA
                                AND c.TABLE_NAME = kcu.TABLE_NAME
                                AND c.COLUMN_NAME = kcu.COLUMN_NAME
                                AND kcu.REFERENCED_TABLE_NAME IS NOT NULL -- Only joins for foreign keys
                            WHERE
                                c.TABLE_SCHEMA = %s AND c.TABLE_NAME = %s
                                {'\n'.join([f'AND NOT ({cond})' for cond in PRIVATE_COLUMNS_RESTRICTION_CONDITIONS])};
                        """,
                        (
                            DB_CONNECT_CONFIG["database"],
                            table_name,
                        ),
                    )
                    columns_infos = defaultdict(list)
                    reflection_result = cursor.fetchall()
                    for unlabeled_column_info in reflection_result:
                        columns_infos[
                            (unlabeled_column_info[0], unlabeled_column_info[1])
                        ].append(unlabeled_column_info[2])
                    columns_infos = [
                        {
                            "name": col_name,
                            "data_type": col_dtype,
                            "refs": [
                                ref_table_name
                                for ref_table_name in col_refs
                                if isinstance(ref_table_name, str)
                            ],
                        }
                        for (col_name, col_dtype), col_refs in columns_infos.items()
                    ]

                    sql = f"SELECT {','.join(f'`{col['name']}`' for col in columns_infos)} FROM {table_name};"
                    cursor.execute(sql)
                    results = (
                        cursor.fetchall()
                    )  # Fetches all results as a list of tuples
                return Response(
                    json.dumps({"columns": columns_infos, "rows": results}, cls=CustomEncoder),
                    media_type="application/json",
                )

    raise auth.UNAUTHORIZED_RESPONSE
