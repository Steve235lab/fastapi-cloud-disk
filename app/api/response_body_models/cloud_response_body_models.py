from pydantic import BaseModel


class RespUpload(BaseModel):
    fileID: int


class RespExists(BaseModel):
    exists: bool


class RespShare(BaseModel):
    shareLink: str
