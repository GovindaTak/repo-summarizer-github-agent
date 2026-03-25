from fastapi import APIRouter, status

from app.dto.request_schema import RepoSummarizeRequest
from app.dto.response_schema import RepoSummarizeResponse
from app.service.repo_service import RepoService


router = APIRouter(
    tags=["Repository Analysis"],
)


@router.post(
    "/summarize",
    response_model=RepoSummarizeResponse,
    status_code=status.HTTP_200_OK,
)
async def summarize_repository(request: RepoSummarizeRequest):
    """
    Analyze a GitHub repository and return summary,
    technologies, and structure.
    """

    return await RepoService.summarize_repository(request)