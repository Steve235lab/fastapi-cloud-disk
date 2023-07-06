from pydantic import BaseModel


class RespLogin(BaseModel):
    status: str


class RespSignUp(RespLogin):
    pass
