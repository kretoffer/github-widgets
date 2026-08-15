import math
from functools import lru_cache

from fastapi.responses import Response
from simpleicons.all import icons
from simpleicons.icon import Icon

from schemas.themes import build_style
from schemas.widgets import WidgetStyleParams
from tools.svg_tools import renderer

_PAD = 10
_WIDGET_H_PADDING = 10
_WIDGET_BORDER_SIDE = 2
_HEADER_HEIGHT = 70
_SECTION_HEIGHT = 30
_TILE_PADDING = 12
_TILE_H_PADDING = 8
_TILE_BORDER = 4
_ICON_CAPTION_GAP = 6
_CAPTION_HEIGHT = 16
_BOTTOM_PADDING = 10
_WIDGET_BORDER = 4
_SAFETY_FACTOR = 1.12


def _pretty_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").strip().title()


def parse_skills(skills: str) -> list[dict]:
    raw: list[dict] = []
    for token in skills.split("|"):
        token = token.strip()
        if not token:
            continue
        if token.startswith("--") and token.endswith("--"):
            title = token[2:-2].strip()
            if title:
                raw.append({"type": "section", "title": title})
            continue
        if len(token) < 5 and "-" in token:
            continue
        if ":" in token:
            title, slug = token.split(":", 1)
            title = title.strip()
            slug = slug.strip()
            explicit_title = True
        else:
            slug = token.strip()
            title = _pretty_title(slug)
            explicit_title = False
        if not slug:
            continue
        raw.append({"type": "skill", "title": title, "slug": slug, "explicit_title": explicit_title})
    elements: list[dict] = []
    pending_section: dict | None = None
    for item in raw:
        if item["type"] == "section":
            if pending_section is not None:
                elements.append(pending_section)
            pending_section = item
        else:
            if pending_section is not None:
                elements.append(pending_section)
                pending_section = None
            elements.append(item)
    if pending_section is not None:
        elements.append(pending_section)
    return elements


@lru_cache(maxsize=512)
def _resolve_icon(slug: str) -> Icon | None:
    icon = icons.get(slug)
    if icon is not None:
        return icon
    return icons.get(slug.replace("-", ""))


def _build_elements(
    skills_str: str,
    use_original_colors: bool,
    icon_color: str | None,
    text_color: str,
) -> list[dict]:
    elements: list[dict] = []
    for item in parse_skills(skills_str):
        if item["type"] == "section":
            elements.append(item)
            continue
        icon = _resolve_icon(item["slug"])
        if icon is None and item["explicit_title"]:
            icon = _resolve_icon(item["title"].lower())
        if icon is None:
            elements.append(
                {
                    "type": "skill",
                    "title": item["title"],
                    "path": None,
                    "hex": None,
                    "missing": True,
                    "icon_color": icon_color or text_color,
                }
            )
        else:
            elements.append(
                {
                    "type": "skill",
                    "title": item["title"],
                    "path": icon.path,
                    "hex": f"#{icon.hex}",
                    "missing": False,
                    "icon_color": icon_color or (f"#{icon.hex}" if use_original_colors else text_color),
                }
            )
    return elements


def _cell_height(icon_size: int, show_titles: bool) -> int:
    height = icon_size + _TILE_PADDING * 2 + _TILE_BORDER
    if show_titles:
        height += _ICON_CAPTION_GAP + _CAPTION_HEIGHT
    return height


def _inner_width(width: int) -> int:
    return width - 2 * _PAD - 2 * _WIDGET_H_PADDING - 2 * _WIDGET_BORDER_SIDE


def _compute_layout(width: int, columns: int, gap: int, icon_size: int) -> tuple[int, int]:
    inner = _inner_width(width)
    min_cell = icon_size + _TILE_H_PADDING * 2 + _TILE_BORDER
    while columns > 1:
        cell = (inner - (columns - 1) * gap) // columns
        if cell >= min_cell:
            return columns, cell
        columns -= 1
    return 1, max(1, inner)


def estimate_height(
    elements: list[dict],
    columns: int,
    gap: int,
    show_titles: bool,
    icon_size: int = 48,
    header: bool = False,
) -> int:
    cell_height = _cell_height(icon_size, show_titles)
    rows: list[int] = []
    current_row = 0
    skills_in_row = 0
    for element in elements:
        if element["type"] == "section":
            if skills_in_row > 0:
                rows.append(current_row)
                current_row = 0
                skills_in_row = 0
            rows.append(_SECTION_HEIGHT)
        else:
            if skills_in_row == 0:
                current_row = cell_height
            skills_in_row += 1
            if skills_in_row == columns:
                rows.append(current_row)
                current_row = 0
                skills_in_row = 0
    if skills_in_row > 0:
        rows.append(current_row)
    header_height = _HEADER_HEIGHT if header else 0
    rows_height = sum(rows) + (len(rows) - 1) * gap if rows else 0
    raw = _WIDGET_BORDER + header_height + rows_height + _BOTTOM_PADDING
    return math.floor(raw * _SAFETY_FACTOR)


def generate_tech_stack_resp(
    skills_str: str,
    style: WidgetStyleParams | None = None,
    header_text: str | None = None,
    columns: int = 4,
    show_titles: bool = True,
    icon_size: int = 48,
    use_original_colors: bool = True,
    icon_color: str | None = None,
    gap: int = 16,
    animation_duration: float = 1.0,
) -> Response:
    style = style or build_style()
    elements = _build_elements(skills_str, use_original_colors, icon_color, style.colors.text.as_hex())
    columns, cell_size = _compute_layout(style.width, columns, gap, icon_size)
    height = estimate_height(
        elements,
        columns,
        gap,
        show_titles,
        icon_size=icon_size,
        header=bool(header_text),
    )
    return renderer.response(
        "tech_stack",
        elements=elements,
        columns=columns,
        cell=cell_size,
        gap=gap,
        icon_size=icon_size,
        show_titles=show_titles,
        header_text=header_text,
        height=height,
        animation_duration=animation_duration,
        **style.to_template_context(),
    )
