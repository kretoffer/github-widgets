import html
from pathlib import Path

from fastapi.responses import HTMLResponse
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic_extra_types import Color

TEMPLATES_DIR = str(Path(__file__).resolve().parent.parent.parent / "templates" / "html")


class HTMLRenderer:
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
        template = self.env.get_template(f"{template_name}.html")
        return template.render(**context)

    def response(self, template_name: str, **context) -> HTMLResponse:
        element = self.render(template_name, **context)
        return HTMLResponse(content=element, headers={"Cache-Control": "public, max-age=3600"})


renderer = HTMLRenderer()
