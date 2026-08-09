import html
from pathlib import Path

from fastapi.responses import Response
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic_extra_types import Color

TEMPLATES_DIR = str(Path(__file__).resolve().parent.parent.parent / "templates" / "svg")


class SVGRenderer:
    BASE_TEMPLATE = "base"

    def __init__(self, templates_dir: str = TEMPLATES_DIR):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["svg", "html"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["escape"] = lambda x: html.escape(str(x))
        self.env.filters["color_hex"] = self._color_to_hex

    @staticmethod
    def _color_to_hex(color: Color) -> str:
        """Convert Color to HEX"""
        return color.as_hex()

    def render(self, template_name: str, **context) -> str:
        widget = self.env.get_template(f"{template_name}.svg").render(**context)
        base = self.env.get_template(f"{self.BASE_TEMPLATE}.svg")
        return base.render(widget_content=widget, **context)

    def response(self, template_name: str, **context) -> Response:
        element = self.render(template_name, **context)
        return Response(
            content=element,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"},
        )


renderer = SVGRenderer()
