from fastapi import APIRouter, HTTPException

from app.api.response_body_models.user_response_body_models import RespLogin, RespSignUp
from app.api.request_body_models.user_request_body_models import ReqLogin, ReqSignUp
from app.DAO.models.user import User
from app.service.auth import unpack_invitation_code

router = APIRouter()


@router.post("/login", response_model=RespLogin)
def login(request: ReqLogin):
    user_in_db = User.get_by_name(request.username)
    if user_in_db:
        if user_in_db.hashed_password == request.hashed_password:
            user_in_db.touch()
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
