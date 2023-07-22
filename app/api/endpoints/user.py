import os
import time

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response

from app.DAO.database import Session
from app.DAO.models.invitation_code import InvitationCode
from app.DAO.models.user import User
from app.api.request_body_models.user_request_body_models import ReqLogin, ReqSignUp, ReqAdjustStorageSize
from app.api.response_body_models.user_response_body_models import (
    RespLogin,
    RespSignUp,
    RespLogout,
    RespAdjustStorageSize,
)
from app.service.auth import unpack_invitation_code, Authentication
from app.service.utils import UtilService

router = APIRouter()


@router.post("/login", response_model=RespLogin)
def login(request: ReqLogin, response: Response):
    user_in_db = User.get_by_name(request.username)
    if user_in_db:
        if user_in_db.hashed_password == request.hashed_password:
            user_in_db.touch()
            response.set_cookie(
                "token",
                Authentication.create_access_token(user_id=str(user_in_db.id)),
                Authentication.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            )
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Wrong password!")
    else:
        raise HTTPException(status_code=400, detail="No such user, please sign up first!")


@router.post("/signup", response_model=RespSignUp)
def sign_up(request: ReqSignUp):
    new_user = User(
        name=request.username,
        email=request.email,
        hashed_password=request.hashed_password,
        storage_size=unpack_invitation_code(request.invitation_code) if request.invitation_code else 1024,
    )
    new_user.add_to_db()
    # Create storage folder for the new user
    os.mkdir(UtilService.get_storage_path() + str(new_user.id))
    return {"status": "ok"}


@router.post("/logout", response_model=RespLogout)
def logout(response: Response):
    response.delete_cookie("token")
    return {"status": "ok"}


@Authentication.refresh_token_in_cookie
@router.post("/adjustStorageSize", response_model=RespAdjustStorageSize)
def adjust_storage_size(
    request: ReqAdjustStorageSize,
    user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token),
):
    # Validate the invitation code
    invitation_code = InvitationCode.get_by_id(request.invitation_code)
    if invitation_code and invitation_code.expired_at is None:
        user = User.get_by_id(user_id_token_tuple[0])
        # Only enlarge the storage of user
        if user.storage_size < invitation_code.storage_size:
            user.storage_size = invitation_code.storage_size
            invitation_code.expired_at = time.time()
            with Session() as session:
                session.commit()
            return {"status": "Enlarged storage size!", "storage_size": user.storage_size}
        else:
            return {
                "status": "The invitation you entered can't enlarge your storage size because it has a smaller or equal size with the current size.",
                "storage_size": user.storage_size,
            }
    else:
        raise HTTPException(status_code=400, detail="Invalid invitation code!")
