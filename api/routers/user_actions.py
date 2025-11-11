from typing import Annotated

from ..internal import auth

from fastapi import APIRouter, Header, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import RedirectResponse

router = APIRouter()


def get_logged_in_user_id(
    credentials: Annotated[HTTPBasicCredentials, Depends(auth.security)],
) -> str | None:
    if not auth.verify_user_authentication(credentials.username, credentials.password):
        # treats unsuccessful auth as logged-out user = no username
        return None
    return credentials.username


@router.get("/me", tags=["users"])
async def user_me_shortcut(
    user_id: Annotated[str, Depends(get_logged_in_user_id)],
):
    if user_id:
        return RedirectResponse(url=f"/{user_id}", status_code=status.HTTP_302_FOUND)

    raise auth.UNAUTHORIZED_RESPONSE


@router.get("/users/{id}/portfolios", tags=["users"])
async def user_portfolios_details(
    id: int,
    logged_in_user_id: Annotated[str, Depends(get_logged_in_user_id)],
):
    if id == logged_in_user_id:
        return {"user_id": id}  # TODO
