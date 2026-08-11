from typing import Annotated

from fastapi import Depends, HTTPException, Query

from schemas.themes import DEFAULT_THEME, THEMES, build_style
from schemas.widgets import WidgetStyleParams


def widget_style_params(
    theme: str = Query(DEFAULT_THEME, description="Predefined widget theme"),
    width: int | None = Query(None, ge=300, le=1600),
) -> WidgetStyleParams:
    if theme not in THEMES:
        available = ", ".join(sorted(THEMES))
        raise HTTPException(status_code=400, detail=f"Unknown theme {theme!r}. Available: {available}")
    return build_style(theme=theme, width=width) if width is not None else build_style(theme=theme)


WidgetStyle = Annotated[WidgetStyleParams, Depends(widget_style_params)]
