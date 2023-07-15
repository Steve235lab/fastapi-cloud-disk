import os.path

from fastapi import APIRouter, UploadFile, Depends, HTTPException, Form, File as FastAPIFile
from fastapi.responses import Response

from app.api.response_body_models.cloud_response_body_models import RespUpload, RespExists
from app.service.auth import Authentication
from app.service.utils import UtilService
from app.DAO.models.file import File
from app.DAO.database import Session

router = APIRouter()


@Authentication.refresh_token_in_cookie
@router.get("/exists/{filename}", response_model=RespExists)
def exists(response: Response, filename: str,
           user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token)):
    """Call this API before uploading files to avoid unexpected overwriting"""
    with Session() as session:
        file = session.query(File).filter(File.filename == filename,
                                          File.user_id == user_id_token_tuple[0]).one_or_none()
        if file:
            return {"exists": True}
        return {"exists": False}


@Authentication.refresh_token_in_cookie
@router.post("/upload", response_model=RespUpload)
def upload(response: Response, file: UploadFile = FastAPIFile(), file_name_to_replace: str = Form(default=""),
           user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token)):
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
    if not os.path.exists(file_path):  # Create user storage folder if it doesn't exist
        os.mkdir(file_path)
    # Write file
    try:
        with open(file_path + f"/{filename}", "wb") as file_to_disk:
            file_to_disk.write(await file.read())
    except:
        file_for_db.delete_from_db()
        raise HTTPException(status_code=400, detail="Write file failed!")
    return {"fileID": file_for_db.id}


@Authentication.refresh_token_in_cookie
@router.post("/download/{filename}", response_class=Response)
def download(response: Response, filename: str,
             user_id_token_tuple: tuple[str, str] = Depends(Authentication.get_authed_user_id_and_token)):
    file_path = UtilService.get_storage_path() + user_id_token_tuple[0] + f"/{filename}"
    with Session() as session:
        file = session.query(File).filter(File.filename == filename,
                                          File.user_id == user_id_token_tuple[0]).one_or_none()
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
