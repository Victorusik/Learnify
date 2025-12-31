from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import logging
from typing import Union

logger = logging.getLogger(__name__)

class GlobalErrorHandler(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            return await self.handle_exception(e)

    async def handle_exception(self, exc: Exception) -> JSONResponse:
        error_content = {"message": "Internal Server Error", "detail": str(exc)}
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        if isinstance(exc, integrity_error_handler):
             # Handled separately if needed, but below covers generic SQLAlchemy
             pass

        if isinstance(exc, OperationalError):
            logger.error(f"Database Operational Error: {exc}")
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE
            error_content["message"] = "Service Unavailable"
            error_content["detail"] = "Database connection failed temporarily."
        
        elif isinstance(exc, IntegrityError):
            logger.error(f"Database Integrity Error: {exc}")
            status_code = status.HTTP_409_CONFLICT
            error_content["message"] = "Conflict"
            error_content["detail"] = "Data integrity violation."

        elif isinstance(exc, SQLAlchemyError):
            logger.error(f"Database Error: {exc}")
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            error_content["message"] = "Database Error"

        elif isinstance(exc, RequestValidationError):
            # This is usually handled by FastAPI default internal handler, but catching here just in case
            # or if we override exception_handlers in main.py
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
            error_content["message"] = "Validation Error"
            error_content["detail"] = str(exc.errors())

        else:
            logger.exception(f"Unhandled Exception: {exc}")
        
        return JSONResponse(
            status_code=status_code,
            content=error_content
        )

# Helper function if we want to use exception_handlers instead of middleware for some specific types
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation Error", "detail": exc.errors()},
    )
