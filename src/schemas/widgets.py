from pydantic import BaseModel, Field, PositiveInt
from pydantic_extra_types import Color

DEFAULT_WIDTH = 700
_WIDGET_SIDE_PADDING = 20


class WidgetColors(BaseModel):
    primary: Color
    secondary: Color
    background: Color
    surface: Color
    text: Color
    border: Color
    success: Color
    warning: Color
    header: Color
    widget_border: Color


class WidgetFontSizes(BaseModel):
    large: PositiveInt = Field(default=28)
    big: PositiveInt = Field(default=16)
    medium: PositiveInt = Field(default=15)
    small: PositiveInt = Field(default=12)
    tiny: PositiveInt = Field(default=11)


DEFAULT_FONT_SIZES = WidgetFontSizes()


class WidgetStyleParams(BaseModel):
    width: int = Field(default=DEFAULT_WIDTH, ge=300, le=1600)
    colors: WidgetColors
    font_sizes: WidgetFontSizes = Field(default_factory=lambda: WidgetFontSizes())

    @property
    def content_width(self):
        return self.width - _WIDGET_SIDE_PADDING

    def to_template_context(self) -> dict:
        return {
            "width": self.width,
            "content_width": self.content_width,
            "colors": {name: color.as_hex() for name, color in self.colors.model_dump().items()},
            "fonts": self.font_sizes.model_dump(),
        }
