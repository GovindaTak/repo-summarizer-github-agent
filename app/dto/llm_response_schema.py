from pydantic import BaseModel, Field
from typing import List


class RepoAnalysisResponse(BaseModel):
    summary: str = Field(
        description="Concise summary of the repository"
    )

    technologies: List[str] = Field(
        description="Main technologies used in the project"
    )

    structure: str = Field(
        description="Overall project structure description"
    )