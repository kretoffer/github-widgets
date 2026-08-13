from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.api_tools.now_working_on import get_gh_now_working_on_repo
from tools.api_tools.repo import get_gh_repo_info
from tools.svg_tools.repo_card import generate_repo_info_resp

repo_router = APIRouter(tags=["Repositories"])


@repo_router.get("/repo-info/{username}/{repo}")
async def get_repo_info(
    username: str,
    repo: str,
    style: WidgetStyle,
    header_text: str = Query(None, alias="header-text"),
    description_lines: int = Query(2, ge=1, le=6, alias="lines"),
    show_license: bool = Query(True, alias="show-license"),
    show_language: bool = Query(True, alias="show-language"),
    show_forks: bool = Query(True, alias="show-forks"),
    show_stars: bool = Query(True, alias="show-stars"),
) -> Response:
    info = await get_gh_repo_info(username, repo, show_license, show_language)
    return generate_repo_info_resp(
        info,
        style=style,
        description_lines=description_lines,
        show_forks=show_forks,
        show_stars=show_stars,
        header_text=header_text,
    )


@repo_router.get("/now-working-on/{username}")
async def get_now_working_on(
    username: str,
    style: WidgetStyle,
    header_text: str = Query(None, alias="header-text"),
    description_lines: int = Query(2, ge=1, le=6, alias="lines"),
    show_license: bool = Query(True, alias="show-license"),
    show_language: bool = Query(True, alias="show-language"),
    show_forks: bool = Query(True, alias="show-forks"),
    show_stars: bool = Query(True, alias="show-stars"),
) -> Response:
    username, repo = await get_gh_now_working_on_repo(username)
    return await get_repo_info(
        username, repo, style, header_text, description_lines, show_license, show_language, show_forks, show_stars
    )
