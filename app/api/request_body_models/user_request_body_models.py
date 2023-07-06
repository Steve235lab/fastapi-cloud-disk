from pydantic import BaseModel


class ReqLogin(BaseModel):
    username: str
    hashed_password: str


class ReqSignUp(ReqLogin):
    email: str
    invitation_code: str | None = None
