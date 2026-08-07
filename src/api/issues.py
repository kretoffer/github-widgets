from fastapi import APIRouter, Query
from fastapi.responses import HTMLResponse

from tools.api_tools.issues import get_gh_issues_list
from tools.svg_tools.issues_roadmap import generate_issues_roadmap_resp

issues_router = APIRouter(tags=["Issues"])


@issues_router.get("/issues-list/{username}/{repo}")
async def get_issues_list(
    username: str, repo: str, count: int = 20, header_text: str = Query("Roadmap", alias="header-text")
) -> HTMLResponse:
    issueses = await get_gh_issues_list(username, repo, count)
    return generate_issues_roadmap_resp(issueses, header_text=header_text)
