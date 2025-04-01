"""
Custom Exception Classes and Handlers

This file defines custom exception classes and handlers for the FastAPI application.
It provides a standardized way to raise and handle exceptions across the application,
ensuring consistent error responses in the API.

Dependencies:
- FastAPI for request and exception handling
- Pydantic for data models
- App schemas for response models

Author: Minh An
Last Modified: 23 Jun 2024
Version: 1.0.0
"""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, Type
from app.schemas.business_model.response_base import ErrorResponseModel, ResponseStatus


class APIException(HTTPException):
    """
    Base API Exception class that extends FastAPI's HTTPException
    with additional fields for standardized error responses
    """
    def __init__(
        self,
        status_code: int = 500,
        error_code: str = "INTERNAL_SERVER_ERROR",
        message: str = "Internal server error",
        headers: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize APIException

        Args:
            status_code: HTTP status code
            error_code: Application-specific error code
            message: Human-readable error message
            headers: Optional HTTP headers
        """
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=message, headers=headers)


# Common exception classes
class BadRequestException(APIException):
    """Exception for invalid request data"""
    def __init__(
        self, 
        error_code: str = "BAD_REQUEST", 
        message: str = "Invalid request data",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=400, error_code=error_code, message=message, headers=headers)


class UnauthorizedException(APIException):
    """Exception for authentication failures"""
    def __init__(
        self, 
        error_code: str = "UNAUTHORIZED", 
        message: str = "Authentication required",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=401, error_code=error_code, message=message, headers=headers)


class ForbiddenException(APIException):
    """Exception for authorization failures"""
    def __init__(
        self, 
        error_code: str = "FORBIDDEN", 
        message: str = "Access forbidden",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=403, error_code=error_code, message=message, headers=headers)


class NotFoundException(APIException):
    """Exception for resource not found"""
    def __init__(
        self, 
        error_code: str = "NOT_FOUND", 
        message: str = "Resource not found",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=404, error_code=error_code, message=message, headers=headers)


class ConflictException(APIException):
    """Exception for resource conflicts"""
    def __init__(
        self, 
        error_code: str = "CONFLICT", 
        message: str = "Resource conflict",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=409, error_code=error_code, message=message, headers=headers)


class InternalServerException(APIException):
    """Exception for internal server errors"""
    def __init__(
        self, 
        error_code: str = "INTERNAL_SERVER_ERROR", 
        message: str = "Internal server error",
        headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=500, error_code=error_code, message=message, headers=headers)


# Exception handlers
async def api_exception_handler(request: Request, exc: APIException):
    """
    Handler for APIException and its subclasses.
    Formats the exception into a standardized ErrorResponseModel.

    Args:
        request: FastAPI Request object
        exc: APIException instance

    Returns:
        JSONResponse with formatted error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status=ResponseStatus.ERROR,
            error_code=exc.error_code,
            message=exc.detail
        ).dict()
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler for standard FastAPI HTTPException.
    Formats the exception into a standardized ErrorResponseModel.

    Args:
        request: FastAPI Request object
        exc: HTTPException instance

    Returns:
        JSONResponse with formatted error details
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status=ResponseStatus.ERROR,
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail
        ).dict()
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Handler for general Python exceptions.
    Formats the exception into a standardized ErrorResponseModel.

    Args:
        request: FastAPI Request object
        exc: Exception instance

    Returns:
        JSONResponse with formatted error details
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponseModel(
            status=ResponseStatus.ERROR,
            error_code="INTERNAL_SERVER_ERROR",
            message="Lỗi máy chủ nội bộ"
        ).dict()
    )


# Function to register exception handlers with a FastAPI app
def register_exception_handlers(app):
    """
    Register all exception handlers with a FastAPI application

    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(APIException, api_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)