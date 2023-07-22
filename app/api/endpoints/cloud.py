import os.path

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form, File as FastAPIFile
from fastapi.responses import Response

from app.DAO.database import Session
from app.DAO.models.file import File
from app.DAO.models.user import User
from app.api.response_body_models.cloud_response_body_models import RespUpload, RespExists, RespShare
from app.service.auth import Authentication
from app.service.storage import get_folder_size
from app.service.utils import UtilService

router = APIRouter()


@Authentication.refresh_token_in_cookie
@router.get("/exists/{filename}", response_model=RespExists)
def exists(
    response: Response,
    filename: str,
    user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token),
):
    """Call this API before uploading files to avoid unexpected overwriting"""
    with Session() as session:
        file = (
            session.query(File).filter(File.filename == filename, File.user_id == user_id_token_tuple[0]).one_or_none()
        )
        if file:
            return {"exists": True}
        return {"exists": False}


@Authentication.refresh_token_in_cookie
@router.post("/upload", response_model=RespUpload)
def upload(
    response: Response,
    file: UploadFile = FastAPIFile(),
    file_name_to_replace: str = Form(default=""),
    user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token),
):
    """Upload a file to user's storage path
    * This will overwrite the file if there's already a file having the same name in the user's folder.
    :param response:
    :param user_id_token_tuple:
    :param file:
    :param file_name_to_replace: Override the original file name
    """
    filename = file_name_to_replace if file_name_to_replace else file.filename
    file_for_db = File(user_id=user_id_token_tuple[0], filename=filename)
    file_for_db.add_to_db()
    file_path = UtilService.get_storage_path() + user_id_token_tuple[0]
    # Create user storage folder if it doesn't exist
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    # Check if there's enough space for this upload
    used_space = get_folder_size(file_path)
    user = User.get_by_id(user_id_token_tuple[0])
    if user.storage_size - used_space < file.size:
        raise HTTPException(status_code=400, detail=f"No enough space to upload the file {file.filename}!")
    # Write file
    try:
        with open(file_path + f"/{filename}", "wb") as file_to_disk:
            file_to_disk.write(await file.read())
    except:
        file_for_db.delete_from_db()
        raise HTTPException(status_code=500, detail="Write file failed!")
    return {"fileID": file_for_db.id}


@Authentication.refresh_token_in_cookie
@router.post("/download/{filename}", response_class=Response)
def download_own_file(
    response: Response,
    filename: str,
    user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token),
):
    """Download the file uploaded by themselves"""
    file_path = UtilService.get_storage_path() + user_id_token_tuple[0] + f"/{filename}"
    with Session() as session:
        file = (
            session.query(File).filter(File.filename == filename, File.user_id == user_id_token_tuple[0]).one_or_none()
        )
        if file is None:
            if os.path.exists(file_path):
                os.remove(file_path)
            raise HTTPException(status_code=404, detail=f"No file named {filename}")
        try:
            file_on_disk = open(file_path, "rb")
            file_bytes = file_on_disk.read()
        except:
            raise HTTPException(status_code=400, detail=f"Failed to read file {filename}")
        headers = {"Content-Disposition": f'attachment; filename="{file.filename}"'}
        return Response(file_bytes, headers=headers)


@Authentication.refresh_token_in_cookie
@router.get("/share/{filename}", response_model=RespShare)
def share(
    response: Response,
    filename: str,
    user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token),
):
    """Generate a link to share the file"""
    pass


@router.post("/download_shared/{file_id_hash}", response_class=Response)
def download_shared_file(file_id_hash: str):
    """Download the file shared by others, no need to login"""
    pass
