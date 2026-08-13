import math

from fastapi.responses import Response

from schemas.external.gh import RepoInfo
from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_CHAR_WIDTH = 8
_HEADER_HEIGHT = 40
_NAME_LINE_HEIGHT = 28
_DESC_LINE_HEIGHT = 20
_METRICS_HEIGHT = 24
_TOP_PADDING = 24
_BOTTOM_PADDING = 10


def _available_chars(width: int) -> int:
    return max(10, int((width - 60) / _CHAR_WIDTH))


def _count_wrapped_lines(description: str | None, available_chars: int) -> int:
    if not description:
        return 0
    lines = 0
    current = 0
    for word in description.split():
        if current == 0:
            current = len(word)
        elif current + 1 + len(word) <= available_chars:
            current += 1 + len(word)
        else:
            lines += 1
            current = len(word)
    return lines + 1


def estimate_height(desc_height: int, width: int, has_header: bool = False) -> int:
    header_height = _HEADER_HEIGHT if has_header else 0
    raw_height = _TOP_PADDING + header_height + _NAME_LINE_HEIGHT + desc_height + _METRICS_HEIGHT + _BOTTOM_PADDING
    return math.floor(raw_height * 1.15)


def generate_repo_info_resp(
    repo: RepoInfo,
    template_name: str = "repo_info",
    style: WidgetStyleParams | None = None,
    description_lines: int = 2,
    **kwargs,
) -> Response:
    style = style or build_style()
    available = _available_chars(style.width)
    shown_lines = min(description_lines, _count_wrapped_lines(repo.description, available))
    desc_height = shown_lines * _DESC_LINE_HEIGHT
    has_header = bool(kwargs.get("header_text"))
    height = estimate_height(desc_height, style.width, has_header)

    return renderer.response(
        template_name,
        **repo.model_dump(),
        description_lines=description_lines,
        height=height,
        **style.to_template_context(),
        **kwargs,
    )
