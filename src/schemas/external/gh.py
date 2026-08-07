from typing import Literal

from pydantic import BaseModel, HttpUrl, PositiveInt
from pydantic_extra_types import Color


class IssueLabel(BaseModel):
    name: str
    color: Color


class Issue(BaseModel):
    number: PositiveInt
    state: Literal["open", "closed", "all"]
    title: str
    labels: list[IssueLabel]
    url: HttpUrl
