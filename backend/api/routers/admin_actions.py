from typing import Annotated

from fastapi import APIRouter, Body
from fastapi_pagination import LimitOffsetPage, Params, LimitOffsetParams

from fastapi import APIRouter, Header, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response, PlainTextResponse

from ..internal.setup_db import setup_db, db_fill_starter_data
from ..internal import auth
from ..dependencies import DB_CONNECT_CONFIG, get_logger

import json, pymysql, datetime, decimal, io, logging

from collections import defaultdict

router = APIRouter()


@router.post("/setup", tags=["admin"])
async def sitewide_setup(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
    logger: logging.Logger = Depends(get_logger),
):
    def _task():
        setup_db(logger)
        return Response(status_code=status.HTTP_200_OK)

    return auth.basic_admin_auth_wrapper(credentials, _task)


@router.put("/fill", tags=["admin"])
async def insert_static_data_into_db(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
    logger: logging.Logger = Depends(get_logger),
):
    def _task():
        db_fill_starter_data(logger)
        return Response(status_code=status.HTTP_200_OK)

    return auth.basic_admin_auth_wrapper(credentials, _task)


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
    def _task():
        return Response(
            json.dumps(ADMIN_AUTHORIZED_TABLES_NAMES), media_type="application/json"
        )

    return auth.basic_admin_auth_wrapper(credentials, _task)


class MysqlDataTypesJsonCompatableEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()  # Convert datetime to ISO 8601 string
        if isinstance(o, decimal.Decimal):
            return float(o)  # Convert Decimal to float
        return json.JSONEncoder.default(
            self, o
        )  # Let the base class handle other types


@router.get("/table/{table_name}", tags=["admin"])
async def view_table(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
    table_name: str,
    pagination_params: LimitOffsetParams = Depends(),
):
    def _task():
        MAX_PAGE_SIZE = 100
        PRIVATE_COLUMNS_RESTRICTION_CONDITIONS = [
            "c.TABLE_NAME = 'User' AND (c.COLUMN_NAME = 'password_hash' OR c.COLUMN_NAME = 'email')"
        ]
        if not (
            table_name in ADMIN_AUTHORIZED_TABLES_NAMES
            and pagination_params.limit < MAX_PAGE_SIZE
        ):
            raise (
                auth.FORBIDDEN_RESPONSE
            )  # should be FORBIDDEN_RESPONSE not ADMIN_FORBIDDEN_RESPONSE

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

                sql = f"""SELECT {','.join(f'`{col['name']}`' for col in columns_infos)} FROM {table_name}
                    LIMIT %d OFFSET %d;"""
                cursor.execute(sql, (pagination_params.limit, pagination_params.offset))  # type: ignore
                results = cursor.fetchall()  # Fetches all results as a list of tuples

        return Response(
            json.dumps(
                {"columns": columns_infos, "rows": results},
                cls=MysqlDataTypesJsonCompatableEncoder,
            ),
            media_type="application/json",
        )

    return auth.basic_admin_auth_wrapper(credentials, _task)


@router.get("/metrics/storage", response_class=PlainTextResponse, tags=["admin"])
async def check_db_size(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    def _task():
        response_text = io.StringIO()
        with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(
                    "api/sql/crud_ops/read/check_tables_sizes.sql", "r"
                ) as f_sql_check_tables_sizes:
                    # Gets size of each table
                    cursor.execute(
                        f_sql_check_tables_sizes.read(),
                        {"db_name": DB_CONNECT_CONFIG["database"]},
                    )

                print("=" * 60, file=response_text)
                print("DATABASE STORAGE BREAKDOWN", file=response_text)
                print("=" * 60, file=response_text)
                print(
                    f"{'Table':<20} {'Size (MB)':<12} {'Rows':<12}", file=response_text
                )
                print("-" * 60, file=response_text)

                total_size = 0
                for table, size, rows in cursor.fetchall():
                    total_size += size
                    print(
                        f"{table:<20} {size:>10.2f} MB {rows:>10}", file=response_text
                    )

                #

                print("-" * 60, file=response_text)
                print(f"{'TOTAL':<20} {total_size:>10.2f} MB", file=response_text)
                print("=" * 60, file=response_text)

                with open(
                    "api/sql/crud_ops/read/check_db_size.sql", "r"
                ) as f_sql_check_db_size:
                    # Get total database size
                    cursor.execute(
                        f_sql_check_db_size.read(),
                        {"db_name": DB_CONNECT_CONFIG["database"]},
                    )

                db_size = cursor.fetchone()[0]
                print(
                    f"\nTotal Database Size: {db_size:.2f} MB ({db_size/1024:.3f} GB)",
                    file=response_text,
                )

        return response_text.getvalue()

    return auth.basic_admin_auth_wrapper(credentials, _task)


@router.post("/signin", tags=["admin"])
async def signin(
    username: str = Body(...),
    password: str = Body(...),
    logger: logging.Logger = Depends(get_logger),
):
    if auth.verify_admin_authentication(username, password):
        logger.info("admin login successful")
        return auth.user_state_json_dict(
            id=-1,
            credentials_encoded=auth.credentials_b64(username, password),
        )

    raise auth.UNAUTHORIZED_RESPONSE
