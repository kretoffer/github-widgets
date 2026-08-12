from typing import Literal

from pydantic import BaseModel, PositiveInt
from pydantic_extra_types import Color


class IssueLabel(BaseModel):
    name: str
    color: Color


class Issue(BaseModel):
    number: PositiveInt
    state: Literal["open", "closed", "all"]
    title: str
    labels: list[IssueLabel]


class RepoInfo(BaseModel):
    full_name: str
    description: str | None
    stars: int = 0
    forks: int = 0
    language: str | None
    license: str | None
