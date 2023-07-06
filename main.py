import uvicorn
from fastapi import FastAPI

from app.api import api_router

if __name__ == "__main__":
    app = FastAPI()
    app.include_router(api_router)
    uvicorn.run(app, port=8080, host="0.0.0.0")
