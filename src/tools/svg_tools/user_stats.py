import math

from fastapi.responses import Response

from schemas.external.gh import UserStats
from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_HEADER_HEIGHT = 50
_USER_HEADER_HEIGHT = 72
_METRIC_HEIGHT = 34
_METRIC_GAP = 6
_WIDGET_BORDER = 4
_BOTTOM_PADDING = 10
_SAFETY_FACTOR = 1.12
_COLUMN_GAP = 18


def _auto_columns(count: int, width: int) -> int:
    if count <= 0:
        return 1
    columns = math.ceil(math.sqrt(count))
    while columns > 1 and (width - _COLUMN_GAP * (columns - 1)) / columns < 160:
        columns -= 1
    return max(1, min(columns, 4))


def _split_columns(metrics: list, columns: int | None, width: int) -> list[list]:
    if not metrics:
        return []
    count = len(metrics)
    if columns is None:
        columns = _auto_columns(count, width)
    columns = max(1, min(columns or 1, count))
    base, extra = divmod(count, columns)
    result: list[list] = []
    idx = 0
    for col in range(columns):
        size = base + (1 if col < extra else 0)
        result.append(metrics[idx : idx + size])
        idx += size
    return result


def estimate_height(metrics_count: int, columns: int | None, width: int, header: str | None = None) -> int:
    count = columns if columns is not None else _auto_columns(metrics_count, width)
    columns_count = max(1, min(count, max(1, metrics_count)))
    rows = math.ceil(metrics_count / columns_count) if metrics_count else 0
    header_height = _HEADER_HEIGHT if header else 0
    metric_height = rows * _METRIC_HEIGHT + (rows - 1) * _METRIC_GAP if rows else 0
    raw = _WIDGET_BORDER + header_height + _USER_HEADER_HEIGHT + metric_height + _BOTTOM_PADDING
    return math.floor(raw * _SAFETY_FACTOR)


def generate_user_stats_resp(
    stats: UserStats,
    template_name: str = "user_stats",
    style: WidgetStyleParams | None = None,
    columns: int | None = None,
    header_text: str | None = None,
    animation_duration: float = 0,
) -> Response:
    style = style or build_style()
    metrics = [metric.model_dump() for metric in stats.metrics]
    column_groups = _split_columns([m for m in metrics], columns, style.width)
    height = estimate_height(len(metrics), columns, style.width, header=header_text)

    return renderer.response(
        template_name,
        user_name=stats.name,
        user_handle=stats.handle,
        column_groups=column_groups,
        height=height,
        animation_duration=animation_duration,
        header_text=header_text,
        **style.to_template_context(),
    )
