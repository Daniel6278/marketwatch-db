from typing import Annotated

from ..internal import auth
from ..internal.demo_assignment import sql_code_return_wrapper
from ..dependencies import (
    DB_CONNECT_CONFIG,
    BAD_REQUEST_RESPONSE,
    DatabaseError,
    get_logger,
)

from fastapi import APIRouter, Header, status, HTTPException, Depends, Body
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse, Response

import pymysql, re, logging

router = APIRouter()


def get_logged_in_user_id(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
) -> str | None:
    if not auth.verify_user_authentication(credentials.username, credentials.password):
        # treats unsuccessful auth as logged-out user = no username
        return None
    return credentials.username


def is_valid_email_addr(email: str):
    """Check if the email is a valid format."""
    # Regular expression for validating an Email
    regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$"
    # If the string matches the regex, it is a valid email
    if re.match(regex, email):
        return True
    else:
        return False


@router.post("/register", tags=["users"])
async def register_new_user(
    first_name: str = Body(...),
    last_name: str = Body(...),
    email: str = Body(...),
    password: str = Body(...),
    logger: logging.Logger = Depends(get_logger),
):
    logger.info("start function register_new_user")
    password_hash = auth.hash_password(password)
    CONSTRAINTS = [
        len(first_name) > 0 and len(first_name) <= 100,
        len(last_name) > 0 and len(last_name) <= 100,
        len(email) > 0 and len(email) <= 255 and is_valid_email_addr(email),
        len(password_hash) > 0 and len(password_hash) <= 60,
    ]
    if not all(CONSTRAINTS):
        return BAD_REQUEST_RESPONSE

    try:
        with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(
                    "api/sql/crud_ops/create/create_a_user.sql", "r"
                ) as f_sql_create_a_user:
                    logger.info("db connected, got cursor, opened create_a_user.sql")
                    cursor.execute(
                        f_sql_create_a_user.read(),
                        {
                            "first_name": first_name,
                            "last_name": last_name,
                            "email": email,
                            "password_hash": password_hash,
                        },
                    )
                    logger.info("ran create_a_user.sql")

                cursor.execute("SELECT LAST_INSERT_ID() AS created_user_id;")
                logger.info("ran SELECT LAST_INSERT_ID()")

                (created_user_id,) = cursor.fetchone()

                conn.commit()

        return auth.user_state_json_dict(
            id=created_user_id,
            credentials_encoded=auth.credentials_b64(
                str(created_user_id), password_hash
            ),
        )
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="failed to create user account",
        )


@router.post("/signin", tags=["users"])
async def signin(
    email: str,
    password: str,
):
    password_hash = auth.hash_password(password)
    try:
        with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(
                    "api/sql/crud_ops/read/user_sign_in.sql", "r"
                ) as f_sql_user_sign_in:
                    cursor.execute(
                        f_sql_user_sign_in.read(),
                        {
                            "email_address": email,
                            "password_hash": password_hash,
                        },
                    )
                query_results = cursor.fetchall()

        is_auth_successful = len(query_results) > 0
        queried_user_id = query_results[0]

        if is_auth_successful:
            return auth.user_state_json_dict(
                id=queried_user_id,
                credentials_encoded=auth.credentials_b64(
                    str(queried_user_id), password_hash
                ),
            )

        raise auth.UNAUTHORIZED_RESPONSE

    except:
        raise DatabaseError("user_sign_in.sql")


@router.get("/me", tags=["users"])
async def user_me_shortcut(
    user_id: Annotated[str, Depends(get_logged_in_user_id)],
):
    if user_id:
        return RedirectResponse(
            url=f"/users/{user_id}", status_code=status.HTTP_302_FOUND
        )

    raise auth.UNAUTHORIZED_RESPONSE


@router.get("/users/{id}", tags=["users"])
async def user_profile_details(
    id: int,
    logged_in_user_id: Annotated[str, Depends(get_logged_in_user_id)],
):
    if logged_in_user_id:
        if id == logged_in_user_id:
            with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
                with conn.cursor() as cursor:
                    with open(
                        "api/sql/crud_ops/read/get_user_info_except_password.sql", "r"
                    ) as f_sql_get_user_info_except_password:
                        cursor.execute(
                            f_sql_get_user_info_except_password.read(),
                            {"id": id},
                        )
                        (
                            query_result__user_id,
                            query_result__first_name,
                            query_result__last_name,
                            query_result__email_address,
                            query_result__member_since,
                        ) = cursor.fetchone()

            return {
                "user_id": query_result__user_id,
                "first_name": query_result__first_name,
                "last_name": query_result__last_name,
                "email_address": query_result__email_address,
                "member_since": query_result__member_since,
            }

        raise auth.FORBIDDEN_RESPONSE

    raise auth.UNAUTHORIZED_RESPONSE


@router.get("/users/{id}/portfolios", tags=["users"])
async def user_portfolios_basic_info(
    id: int,
    logged_in_user_id: Annotated[str, Depends(get_logged_in_user_id)],
    return_descriptions: bool,
):
    if logged_in_user_id:
        if id == logged_in_user_id:
            return {"user_id": id}  # TODO

        raise auth.FORBIDDEN_RESPONSE

    raise auth.UNAUTHORIZED_RESPONSE


@router.get("/users/{id}/portfolios/holdings", tags=["users"])
async def user_portfolios_and_contained_holdings(
    id: int,
    logged_in_user_id: Annotated[str, Depends(get_logged_in_user_id)],
):
    if logged_in_user_id:
        if id == logged_in_user_id:
            return {"user_id": id}  # TODO

        raise auth.FORBIDDEN_RESPONSE

    raise auth.UNAUTHORIZED_RESPONSE


@router.post("/users/{id}/portfolios/new", tags=["users"])
async def create_portfolio(
    id: int,
    logged_in_user_id: Annotated[str, Depends(get_logged_in_user_id)],
    name: str,
    description: str,
    demo_mode: bool,
):
    CONSTRAINTS = [
        len(name) > 0 and len(name) <= 255,
        len(description) > 0 and len(description) <= 10000,
    ]

    def _task():
        with pymysql.connect(**DB_CONNECT_CONFIG) as conn:
            with conn.cursor() as cursor:
                with open(
                    "api/sql/crud_ops/create/create_a_portfolio.sql", "r"
                ) as f_sql_create_a_portfolio:
                    mogrified_sql_create_a_portfolio: str = cursor.mogrify(
                        f_sql_create_a_portfolio.read(),
                        {
                            "user_id": id,
                            "name": name,
                            "description": description,
                        },
                    )
                    cursor.execute(mogrified_sql_create_a_portfolio)

                cursor.execute("SELECT LAST_INSERT_ID() AS new_portfolio_id;")
                (new_portfolio_id,) = cursor.fetchone()

                conn.commit()

        return {"portfolio_id": new_portfolio_id}, mogrified_sql_create_a_portfolio

    if logged_in_user_id:
        if id == logged_in_user_id:
            if all(CONSTRAINTS):
                try:
                    return sql_code_return_wrapper(_task, demo_mode)
                except:
                    return Response(
                        "failed to create portfolio",
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            raise BAD_REQUEST_RESPONSE  # constraints violated

        raise auth.FORBIDDEN_RESPONSE  # not you

    raise auth.UNAUTHORIZED_RESPONSE  # user is not logged-in
