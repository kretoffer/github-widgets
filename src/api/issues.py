from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.api_tools.issues import get_gh_issues_list
from tools.svg_tools.issues_roadmap import generate_issues_roadmap_resp

issues_router = APIRouter(tags=["Issues"])


@issues_router.get("/issues-list/{username}/{repo}")
async def get_issues_list(
    username: str,
    repo: str,
    style: WidgetStyle,
    count: int = 20,
    header_text: str = Query("Roadmap", alias="header-text"),
    labels: bool = Query(True),
) -> Response:
    issueses = await get_gh_issues_list(username, repo, count, labels)
    return generate_issues_roadmap_resp(issueses, header_text=header_text, style=style)
