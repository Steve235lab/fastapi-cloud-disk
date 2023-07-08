from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from app.api.response_body_models.user_response_body_models import RespLogin, RespSignUp, RespLogout
from app.api.request_body_models.user_request_body_models import ReqLogin, ReqSignUp
from app.DAO.models.user import User
from app.service.auth import unpack_invitation_code, Authentication

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
                Authentication.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Wrong password!")
    else:
        raise HTTPException(status_code=400, detail="No such user, please sign up first!")


@router.post("/sign_up", response_model=RespSignUp)
def sign_up(request: ReqSignUp):
    new_user = User(
        name=request.username,
        email=request.email,
        hashed_password=request.hashed_password,
        storage_size=unpack_invitation_code(request.invitation_code) if request.invitation_code else 1024
    )
    new_user.add_to_db()
    return {"status": "ok"}


@router.post("/logout", response_model=RespLogout)
def logout(response: Response):
    response.delete_cookie("token")
    return {"status": "ok"}
