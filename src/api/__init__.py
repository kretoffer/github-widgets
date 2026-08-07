from fastapi import APIRouter

from api.issues import issues_router

api_roter = APIRouter(prefix="/api", tags=["API"])

api_roter.include_router(issues_router)
