from fastapi import APIRouter

from app.api.endpoints import user, cloud

api_router = APIRouter()
api_router.include_router(user.router, prefix="/api/user", tags=["user"])
api_router.include_router(cloud.router, prefix="/api/cloud", tags=["cloud"])
