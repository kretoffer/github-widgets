from fastapi.responses import HTMLResponse

from schemas.external.gh import Issue
from tools.svg_tools import renderer


def generate_issues_roadmap_resp(
    issues: list[Issue], template_name: str = "issues_roadmap", header_text: str = "Roadmap"
) -> HTMLResponse:
    issues_data = [issue.model_dump() for issue in issues]

    return renderer.response(template_name, issues=issues_data, header_text=header_text)
