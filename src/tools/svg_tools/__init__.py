from jinja2 import Environment, FileSystemLoader, select_autoescape
from fastapi.responses import Response
import html


class SVGRenderer:
    def __init__(self, templates_dir: str = "templates/svg"):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['svg', 'html']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters['escape'] = lambda x: html.escape(str(x))


    def render(self, template_name: str, **context) -> str:
        """Render svg template"""
        template = self.env.get_template(f"{template_name}.svg")
        return template.render(**context)


    def response(self, template_name: str, **context) -> Response:
        """Return rendered SVG into Response"""
        svg = self.render(template_name, **context)
        return Response(
            content=svg,
            media_type="image/svg+xml",
            headers={"Cache-Control": "public, max-age=3600"}
        )


renderer = SVGRenderer()
