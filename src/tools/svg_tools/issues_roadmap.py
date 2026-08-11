import math

from fastapi.responses import Response

from schemas.external.gh import Issue
from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_CHAR_WIDTH = 8
_TITLE_LINE_HEIGHT = 22
_STATUS_BUFFER_HEIGHT = 26
_LABEL_ROW_HEIGHT = 24
_HEADER_HEIGHT = 40
_ISSUE_PADDING = 8
_ISSUE_MARGIN = 4
_BOTTOM_PADDING = 14


def _estimate_title_lines(title: str, available_chars: int) -> int:
    if not title:
        return 1
    words = title.split()
    lines = 1
    current = 0
    for word in words:
        word_len = len(word)
        if current == 0:
            current = word_len
        elif current + 1 + word_len > available_chars:
            lines += 1
            current = word_len
        else:
            current += 1 + word_len
    return lines


def estimate_height(issues: list[dict], width: int) -> int:
    reserved_chars = max(10, int((width - 140) / _CHAR_WIDTH))

    issues_height = 0
    for issue in issues:
        title_lines = _estimate_title_lines(issue["title"], reserved_chars)
        title_height = max(title_lines, 1) * _TITLE_LINE_HEIGHT
        labels_height = _LABEL_ROW_HEIGHT if len(issue["labels"]) > 0 else 0
        issues_height += max(title_height, _STATUS_BUFFER_HEIGHT) + labels_height + _ISSUE_PADDING * 2 + _ISSUE_MARGIN

    raw_height = _HEADER_HEIGHT + issues_height + _BOTTOM_PADDING
    return math.floor(raw_height * 1.15)


def generate_issues_roadmap_resp(
    issues: list[Issue],
    template_name: str = "issues_roadmap",
    header_text: str = "Roadmap",
    style: WidgetStyleParams | None = None,
) -> Response:
    style = style or build_style()
    issues_data = [issue.model_dump() for issue in issues]
    height = estimate_height(issues_data, style.width)

    return renderer.response(
        template_name,
        issues=issues_data,
        header_text=header_text,
        height=height,
        **style.to_template_context(),
    )
