from fastapi import APIRouter, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.api_tools.streak import get_gh_contribution_streak
from tools.svg_tools.streak import generate_streak_resp

streak_router = APIRouter(tags=["Streak"])


@streak_router.get("/contribution-streak/{username}")
async def get_contribution_streak(
    username: str,
    style: WidgetStyle,
    header_text: str = Query(None, alias="header-text"),
    animation_duration: float = Query(0.6, ge=0, le=10, alias="animation-duration"),
) -> Response:
    stats = await get_gh_contribution_streak(username)
    return generate_streak_resp(
        stats,
        style=style,
        header_text=header_text,
        animation_duration=animation_duration,
    )
