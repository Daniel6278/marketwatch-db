from typing import Annotated

from fastapi import APIRouter

from fastapi import APIRouter, Header, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import Response

from ..internal.setup_db import setup_db
from ..internal import auth

router = APIRouter()


@router.post("/setup", tags=["admin"])
async def sitewide_setup(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
):
    if auth.verify_admin_authentication(credentials.username, credentials.password):
        setup_db()
        return Response(status_code=status.HTTP_200_OK)

    raise auth.UNAUTHORIZED_RESPONSE


@router.get("/table/{table_name}", tags=["admin"])
async def view_table(table_name: str):
    return table_name
