from app.dto.request_schema import RepoSummarizeRequest
from app.dto.response_schema import RepoSummarizeResponse
from app.exceptions.app_exception import AppException
from app.graph.graph import repo_graph
from app.core.logger import get_logger


logger = get_logger(__name__)


class RepoService:
    """
    Business logic for repository summarization.
    """

    @staticmethod
    async def summarize_repository(
        request: RepoSummarizeRequest,
    ) -> RepoSummarizeResponse:

        github_url = str(request.github_url)

        logger.info(f"Processing repository: {github_url}")

   
        initial_state = {
            "github_url": github_url
        }

        try:
      
            final_state = await repo_graph.ainvoke(initial_state)

        except AppException:
            raise

        except Exception as e:
            logger.exception("Graph execution failed")
            raise AppException(
                message=str(e),
                status_code=500
            )

   
        summary = final_state.get("summary")
        technologies = final_state.get("technologies")
        structure = final_state.get("structure")

        if not summary:
            raise AppException(
                "Unable to generate repository summary",
                500,
            )

   
        return RepoSummarizeResponse(
            summary=summary,
            technologies=technologies or [],
            structure=structure or "",
        )