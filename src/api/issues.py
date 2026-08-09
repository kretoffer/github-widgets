from fastapi import APIRouter, Query
from fastapi.responses import Response

from tools.api_tools.issues import get_gh_issues_list
from tools.svg_tools.issues_roadmap import DEFAULT_WIDTH, generate_issues_roadmap_resp

issues_router = APIRouter(tags=["Issues"])


@issues_router.get("/issues-list/{username}/{repo}")
async def get_issues_list(
    username: str,
    repo: str,
    count: int = 20,
    header_text: str = Query("Roadmap", alias="header-text"),
    width: int = Query(DEFAULT_WIDTH, ge=300, le=1600),
    primary_color=Query("#A0A0A0", alias="primary-color"),
    bg_color=Query("transparent", alias="bg-color"),
) -> Response:
    issueses = await get_gh_issues_list(username, repo, count)
    return generate_issues_roadmap_resp(
        issueses, header_text=header_text, width=width, primary_color=primary_color, bg_color=bg_color
    )
