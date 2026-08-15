from fastapi import APIRouter

from api.issues import issues_router
from api.repo import repo_router
from api.tech_stack import tech_stack_router
from api.users import users_router

api_router = APIRouter(prefix="/api", tags=["API"])

api_router.include_router(issues_router)
api_router.include_router(repo_router)
api_router.include_router(tech_stack_router)
api_router.include_router(users_router)
