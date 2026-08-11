from schemas.widgets import WidgetColors, WidgetFontSizes, WidgetStyleParams

DEFAULT_THEME = "default"

_DEFAULT_COLORS = WidgetColors.model_validate(
    {
        "primary": "#4493f8",
        "secondary": "#ffffff",
        "background": "#0d1117",
        "surface": "#161b22",
        "text": "#e6edf3",
        "border": "#30363d",
        "success": "#3fb950",
        "warning": "#a371f7",
        "header": "#d0d0d0",
    }
)

THEMES: dict[str, WidgetColors] = {
    DEFAULT_THEME: _DEFAULT_COLORS,
}


def build_style(theme: str = DEFAULT_THEME, **overrides) -> WidgetStyleParams:
    if theme not in THEMES:
        raise ValueError(f"Unknown theme {theme!r}. Available: {sorted(THEMES)}")
    colors = THEMES[theme]
    font_sizes = WidgetFontSizes()
    return WidgetStyleParams(colors=colors, font_sizes=font_sizes, **overrides)
