from pydantic import BaseModel


class RespUpload(BaseModel):
    fileID: int
