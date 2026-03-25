from pydantic import BaseModel
from typing import List


class RepoSummarizeResponse(BaseModel):
    summary: str
    technologies: List[str]
    structure: str


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str