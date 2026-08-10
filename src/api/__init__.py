from fastapi import APIRouter

from api.issues import issues_router

api_router = APIRouter(prefix="/api", tags=["API"])

api_router.include_router(issues_router)
