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


class Metric(BaseModel):
    key: str
    label: str
    value: str
    icon: str


class LanguageShare(BaseModel):
    name: str
    share: float = 0.0
    count: int = 0


class UserStats(BaseModel):
    name: str
    handle: str
    metrics: list[Metric]


class StreakStats(BaseModel):
    total_contributions: int
    total_range: str
    current_streak: int
    current_streak_range: str
    longest_streak: int
    longest_streak_range: str
    current_progress: float
