from typing import Annotated

from fastapi import Depends, Query

from schemas.widgets import (
    DEFAULT_BG_COLOR,
    DEFAULT_BORDER_COLOR,
    DEFAULT_PRIMARY_COLOR,
    DEFAULT_WIDTH,
    WidgetStyleParams,
)


def widget_style_params(
    width: int = Query(DEFAULT_WIDTH, ge=300, le=1600),
    primary_color: str = Query(DEFAULT_PRIMARY_COLOR, alias="primary-color"),
    bg_color: str = Query(DEFAULT_BG_COLOR, alias="bg-color"),
    border_color: str = Query(DEFAULT_BORDER_COLOR, alias="border-color"),
) -> WidgetStyleParams:
    return WidgetStyleParams.model_validate(
        {
            "width": width,
            "primary-color": primary_color,
            "bg-color": bg_color,
            "border-color": border_color,
        }
    )


WidgetStyle = Annotated[WidgetStyleParams, Depends(widget_style_params)]
