import math

from fastapi.responses import Response

from schemas.external.gh import LanguageShare
from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_HEADER_HEIGHT = 50
_ROW_HEIGHT = 28
_ROW_GAP = 10
_TOP_PADDING = 8
_BOTTOM_PADDING = 10
_WIDGET_BORDER = 4
_SAFETY_FACTOR = 1.15

_CHIP_HEIGHT = 22
_CHIP_GAP = 6
_CHIP_CHAR_WIDTH = 7.5
_CHIP_BASE_WIDTH = 72
_BAR_HEIGHT = 10
_CAPTION_GAP = 6

_PIE_SIZE = 180
_PIE_RAD_OUT = 78
_PIE_RAD_IN = 46
_SLICE_GAP = 1.0

_COMPACT_ROW_HEIGHT = 24
_COMPACT_GAP = 14


def _estimate_bars(count: int, header: bool) -> int:
    rows = count * _ROW_HEIGHT + (count - 1) * _ROW_GAP if count else 0
    raw = _WIDGET_BORDER + (_HEADER_HEIGHT if header else 0) + _TOP_PADDING + rows + _BOTTOM_PADDING
    return math.floor(raw * _SAFETY_FACTOR)


def _chips_lines(items: list[dict], content_width: int) -> int:
    if not items:
        return 1
    width = sum(len(item["name"]) * _CHIP_CHAR_WIDTH + _CHIP_BASE_WIDTH for item in items)
    width += (len(items) - 1) * _CHIP_GAP
    return max(1, math.ceil(width / max(1, content_width)))


def _estimate_inline(items: list[dict], content_width: int, header: bool) -> int:
    lines = _chips_lines(items, content_width)
    raw = (
        _WIDGET_BORDER
        + (_HEADER_HEIGHT if header else 0)
        + _TOP_PADDING
        + _BAR_HEIGHT
        + _CAPTION_GAP
        + lines * _CHIP_HEIGHT
        + (lines - 1) * _CHIP_GAP
        + _BOTTOM_PADDING
    )
    return math.floor(raw * _SAFETY_FACTOR)


def _estimate_pie(items: list[dict], content_width: int, header: bool) -> int:
    lines = _chips_lines(items, content_width)
    raw = (
        _WIDGET_BORDER
        + (_HEADER_HEIGHT if header else 0)
        + _TOP_PADDING
        + _PIE_SIZE
        + _CAPTION_GAP
        + lines * _CHIP_HEIGHT
        + (lines - 1) * _CHIP_GAP
        + _BOTTOM_PADDING
    )
    return math.floor(raw * _SAFETY_FACTOR)


def _estimate_compact(count: int, header: bool, columns: int = 2) -> int:
    rows = math.ceil(count / columns) if count else 0
    body = rows * _COMPACT_ROW_HEIGHT + (rows - 1) * _COMPACT_GAP if rows else 0
    raw = _WIDGET_BORDER + (_HEADER_HEIGHT if header else 0) + _TOP_PADDING + body + _BOTTOM_PADDING
    return math.floor(raw * _SAFETY_FACTOR)


def _split_columns(items: list[dict], columns: int) -> list[list[dict]]:
    result: list[list[dict]] = []
    base, extra = divmod(len(items), columns)
    idx = 0
    for col in range(columns):
        size = base + (1 if col < extra else 0)
        result.append(items[idx : idx + size])
        idx += size
    return result


def _colored(items: list[dict]) -> list[dict]:
    return [{**item, "color": renderer.text_to_color(item["name"])} for item in items]


def _arc_points(cx: float, cy: float, rad: float, a0: float, a1: float) -> tuple[float, float, float, float]:
    x0 = cx + rad * math.cos(math.radians(a0 - 90))
    y0 = cy + rad * math.sin(math.radians(a0 - 90))
    x1 = cx + rad * math.cos(math.radians(a1 - 90))
    y1 = cy + rad * math.sin(math.radians(a1 - 90))
    return x0, y0, x1, y1


def _pie_path(cx: float, cy: float, rad: float, a0: float, a1: float) -> str:
    x0, y0, x1, y1 = _arc_points(cx, cy, rad, a0, a1)
    large = 1 if a1 - a0 > 180 else 0
    return f"M {cx:.1f} {cy:.1f} L {x0:.1f} {y0:.1f} A {rad} {rad} 0 {large} 1 {x1:.1f} {y1:.1f} Z"


def _donut_path(cx: float, cy: float, rad_in: float, rad_out: float, a0: float, a1: float) -> str:
    x0o, y0o, x1o, y1o = _arc_points(cx, cy, rad_out, a0, a1)
    x0i, y0i, x1i, y1i = _arc_points(cx, cy, rad_in, a0, a1)
    large = 1 if a1 - a0 > 180 else 0
    return (
        f"M {x0o:.1f} {y0o:.1f} A {rad_out} {rad_out} 0 {large} 1 {x1o:.1f} {y1o:.1f} "
        f"L {x1i:.1f} {y1i:.1f} A {rad_in} {rad_in} 0 {large} 0 {x0i:.1f} {y0i:.1f} Z"
    )


def _chart_slices(items: list[dict], donut: bool) -> list[dict]:
    total = sum(item["share"] for item in items) or 1
    cx = cy = _PIE_SIZE / 2
    start = 0.0
    slices: list[dict] = []
    for item in items:
        span = item["share"] / total * 360
        a0 = start + _SLICE_GAP
        a1 = start + span - _SLICE_GAP
        path = (
            _donut_path(cx, cy, _PIE_RAD_IN, _PIE_RAD_OUT, a0, a1) if donut else _pie_path(cx, cy, _PIE_RAD_OUT, a0, a1)
        )
        slices.append({**item, "d": path})
        start += span
    return slices


def _bar_segments(items: list[dict]) -> list[dict]:
    total = sum(item["share"] for item in items) or 1
    return [{**item, "width": item["share"] / total * 100} for item in items]


def generate_languages_resp(
    languages: list[LanguageShare],
    style: WidgetStyleParams | None = None,
    header_text: str | None = None,
    animation_duration: float = 0.7,
    show_percent: bool = True,
    layout: str = "bars",
    columns: int = 2,
    show_donut_center: bool = True,
) -> Response:
    style = style or build_style()
    items = _colored([lang.model_dump() for lang in languages])
    header = bool(header_text)
    context = {
        "height": 0,
        "header_text": header_text,
        "animation_duration": animation_duration,
        "show_percent": show_percent,
        **style.to_template_context(),
    }

    if layout == "inline":
        context.update(
            {
                "template": "languages_inline",
                "segments": _bar_segments(items),
                "chips": items,
                "height": _estimate_inline(items, style.content_width, header),
            }
        )
    elif layout == "pie":
        context.update(
            {
                "template": "languages_pie",
                "slices": _chart_slices(items, donut=False),
                "pie_size": _PIE_SIZE,
                "pie_center": _PIE_SIZE / 2,
                "height": _estimate_pie(items, style.content_width, header),
            }
        )
    elif layout == "donut":
        context.update(
            {
                "template": "languages_donut",
                "slices": _chart_slices(items, donut=True),
                "pie_size": _PIE_SIZE,
                "pie_center": _PIE_SIZE / 2,
                "donut_center": f"{items[0]['share']}%" if items and show_percent and show_donut_center else None,
                "height": _estimate_pie(items, style.content_width, header),
            }
        )
    elif layout == "compact":
        context.update(
            {
                "template": "languages_compact",
                "column_groups": _split_columns(items, columns),
                "height": _estimate_compact(len(items), header, columns),
            }
        )
    else:
        context.update({"template": "languages", "languages": items, "height": _estimate_bars(len(items), header)})

    template = context.pop("template")
    return renderer.response(template, **context)
