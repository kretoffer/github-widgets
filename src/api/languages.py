from typing import Literal

from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.api_tools.languages import get_gh_most_used_languages
from tools.svg_tools.languages import generate_languages_resp

languages_router = APIRouter(tags=["Languages"])


@languages_router.get("/most-used-languages/{username}")
async def get_most_used_languages(
    username: str,
    style: WidgetStyle,
    count: int = Query(5, ge=1, le=15),
    header_text: str = Query("Most used languages", alias="header-text"),
    exclude_forks: bool = Query(True, alias="exclude-forks"),
    layout: Literal["bars", "inline", "pie", "donut", "compact"] = Query("inline"),
    columns: int = Query(2, ge=1, le=4),
    center_percent: bool = Query(False, alias="center-percent"),
    show_percent: bool = Query(True, alias="show-percent"),
    animation_duration: float = Query(0.7, ge=0, le=10, alias="animation-duration"),
) -> Response:
    languages = await get_gh_most_used_languages(username, count, exclude_forks)
    return generate_languages_resp(
        languages,
        style=style,
        header_text=header_text,
        show_percent=show_percent,
        layout=layout,
        columns=columns,
        show_donut_center=center_percent,
        animation_duration=animation_duration,
    )
