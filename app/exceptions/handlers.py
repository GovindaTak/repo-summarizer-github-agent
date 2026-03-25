from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.dto.response_schema import ErrorResponse

from app.exceptions.app_exception import AppException
from app.core.logger import get_logger

logger = get_logger(__name__)


async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"AppException: {exc.message}")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message).model_dump(),
    )

async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.warning(f"Validation error: {exc.errors()}")

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(message="Invalid request data").model_dump(),
    )

async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
):
    logger.warning(f"HTTP error: {exc.detail}")

    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=str(exc.detail)).model_dump(),
    )

async def generic_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(message="Internal Server Error").model_dump(),
    )