import re

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from api.deps import WidgetStyle
from tools.svg_tools.tech_stack import generate_tech_stack_resp, parse_skills

tech_stack_router = APIRouter(tags=["Tech Stack"])

_ICON_COLOR_RE = re.compile(r"^#[0-9a-fA-F]{6}$")


@tech_stack_router.get("/tech-stack")
async def get_tech_stack(
    skills: str,
    style: WidgetStyle,
    header_text: str | None = Query("Tech stack", alias="header-text"),
    columns: int = Query(4, ge=1, le=10),
    show_titles: bool = Query(True, alias="show-titles"),
    icon_size: int = Query(48, ge=16, le=128, alias="icon-size"),
    use_original_colors: bool = Query(True, alias="use-original-colors"),
    icon_color: str | None = Query(None, alias="icon-color"),
    gap: int = Query(16, ge=0, le=64),
    animation_duration: float = Query(0.6, ge=0, le=10, alias="animation-duration"),
) -> Response:
    if icon_color is not None and not _ICON_COLOR_RE.match(icon_color):
        raise HTTPException(status_code=422, detail="icon-color must be a hex color in #rrggbb format")
    if not parse_skills(skills):
        raise HTTPException(status_code=400, detail="No valid skills provided")
    return generate_tech_stack_resp(
        skills,
        style=style,
        header_text=header_text,
        columns=columns,
        show_titles=show_titles,
        icon_size=icon_size,
        use_original_colors=use_original_colors,
        icon_color=icon_color,
        gap=gap,
        animation_duration=animation_duration,
    )
