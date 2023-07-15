import os.path

import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from app.api import api_router
from app.service.utils import UtilService

if __name__ == "__main__":
    load_dotenv(override=True)
    storage_path = UtilService.get_storage_path()
    try:
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)
    except:
        raise Exception(
            f"Make storage path failed: {storage_path}, please check the 'STORAGE_PATH' item in your .env file.")
    app = FastAPI()
    app.include_router(api_router)
    uvicorn.run(app, port=8080, host="0.0.0.0")
