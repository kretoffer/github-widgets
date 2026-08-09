from pydantic import BaseModel, ConfigDict, Field

DEFAULT_WIDTH = 700
DEFAULT_PRIMARY_COLOR = "#A0A0A0"
DEFAULT_BG_COLOR = "transparent"
DEFAULT_BORDER_COLOR = "transparent"
_WIDGET_SIDE_PADDING = 20


class WidgetStyleParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    width: int = Field(default=DEFAULT_WIDTH, ge=300, le=1600)
    primary_color: str = Field(default=DEFAULT_PRIMARY_COLOR, alias="primary-color")
    bg_color: str = Field(default=DEFAULT_BG_COLOR, alias="bg-color")
    border_color: str = Field(default=DEFAULT_BORDER_COLOR, alias="border-color")

    @property
    def content_width(self):
        return self.width - _WIDGET_SIDE_PADDING
