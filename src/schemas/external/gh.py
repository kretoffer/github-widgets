from pydantic import BaseModel, PositiveInt
from typing import List, Literal


class IssueLabel(BaseModel):
    name: str
    color: str

class Issue(BaseModel):
    number: PositiveInt
    state: Literal["open", "closed", "all"]
    title: str
    labels: List[IssueLabel]
    
