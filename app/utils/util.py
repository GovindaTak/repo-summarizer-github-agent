import asyncio
from typing import Optional, Dict, List

import aiohttp

from app.exceptions.app_exception import AppException
from app.core.logger import get_logger
from app.core.config import settings  

logger = get_logger(__name__)


class AIRAGUtils:
    """
    Centralized async HTTP utility for external API calls.
    Automatically injects GitHub token when calling GitHub API.
    """

    @staticmethod
    async def send_request(
        endpoint: str,
        method: str = "GET",
        json_data: Optional[Dict] = None,
        query_params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        valid_statuses: Optional[List[int]] = None,
        timeout: int = 15,
    ) -> Dict:

        if valid_statuses is None:
            valid_statuses = [200, 201, 204]

        default_headers = {
            "Accept": "application/json",
            "User-Agent": "repo-summarizer",
        }

        
        if "api.github.com" in endpoint and settings.GITHUB_TOKEN:
            default_headers["Authorization"] = (
                f"Bearer {settings.GITHUB_TOKEN}"
            )

      
        if headers:
            default_headers.update(headers)

        try:
            timeout_cfg = aiohttp.ClientTimeout(total=timeout)

            async with aiohttp.ClientSession(timeout=timeout_cfg) as session:

                request_method = getattr(session, method.lower(), None)
                if not request_method:
                    raise AppException("Unsupported HTTP method", 400)

                async with request_method(
                    endpoint,
                    json=json_data,
                    params=query_params,
                    headers=default_headers,
                ) as response:

                  
                    if response.status not in valid_statuses:
                        error_text = await response.text()

                        logger.error(
                            f"External API failed: {endpoint} | "
                            f"Status: {response.status} | {error_text}"
                        )

                        raise AppException(
                            message="External service failure",
                            status_code=response.status,
                        )

                   
                    if response.status == 204:
                        return {}

                    try:
                        result = await response.json()
                    except Exception:
                        result = {}

                    if not result:
                        raise AppException(
                            message="Empty response from external service",
                            status_code=502,
                        )

                    return result

        except asyncio.TimeoutError:
            logger.error(f"Timeout calling external API: {endpoint}")
            raise AppException(
                message="External service timeout",
                status_code=504,
            )

        except aiohttp.ClientError:
            logger.error(f"Connection error calling external API: {endpoint}")
            raise AppException(
                message="External service unavailable",
                status_code=503,
            )

        except AppException:
            raise

        except Exception:
            logger.exception("Unexpected error in external request")
            raise AppException(
                message="Unexpected error in external request",
                status_code=500,
            )