from fastapi import APIRouter

from tools.api_tools.issues import get_gh_issues_list


issues_router = APIRouter(tags=["Issues"])


@issues_router.get("/issues-list/{username}/{repo}")
async def get_issues_list(username: str, repo: str, count: int = 20):
    return await get_gh_issues_list(username, repo, count)
