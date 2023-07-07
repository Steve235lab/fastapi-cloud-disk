from fastapi import APIRouter, UploadFile

from app.api.response_body_models.cloud_response_body_models import RespUpload

router = APIRouter()


@router.post("/upload", response_model=RespUpload)
def upload(file: UploadFile, user_auth):
    pass
