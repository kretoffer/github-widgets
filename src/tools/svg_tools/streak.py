import math

from fastapi.responses import Response

from schemas.external.gh import StreakStats
from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_HEADER_HEIGHT = 50
_BOX_HEIGHT = 150
_BOX_GAP = 10
_TOP_PADDING = 8
_BOTTOM_PADDING = 10
_WIDGET_BORDER = 4
_SAFETY_FACTOR = 1.1

_RING_RADIUS = 28
_FLAME_SIZE = 40
_FLAME_TOP = 26
_RING_NUMBER_Y = 85


def _format_big_number(value: int) -> str:
    return f"{value:,}"


def _estimate_height(has_header: bool) -> int:
    raw = _WIDGET_BORDER + (_HEADER_HEIGHT if has_header else 0) + _TOP_PADDING + _BOX_HEIGHT + _BOTTOM_PADDING
    return math.floor(raw * _SAFETY_FACTOR)


def _ring_context(stats: StreakStats) -> dict:
    circumference = 2 * math.pi * _RING_RADIUS
    return {
        "ring_radius": _RING_RADIUS,
        "ring_circumference": circumference,
        "ring_dashoffset": circumference * (1 - min(1.0, stats.current_progress)),
        "flame_top": _FLAME_TOP,
        "ring_number_y": _RING_NUMBER_Y,
    }


def generate_streak_resp(
    stats: StreakStats,
    style: WidgetStyleParams | None = None,
    header_text: str | None = None,
    animation_duration: float = 0.6,
) -> Response:
    style = style or build_style()
    has_header = bool(header_text)
    height = _estimate_height(has_header)

    context = {
        "total_contributions": _format_big_number(stats.total_contributions),
        "total_range": stats.total_range,
        "current_streak": str(stats.current_streak),
        "current_streak_range": stats.current_streak_range,
        "longest_streak": _format_big_number(stats.longest_streak),
        "longest_streak_range": stats.longest_streak_range,
        "height": height,
        "header_text": header_text,
        "animation_duration": animation_duration,
        **style.to_template_context(),
        **_ring_context(stats),
    }

    return renderer.response("streak", **context)
