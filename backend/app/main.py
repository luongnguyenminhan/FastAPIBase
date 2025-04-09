"""
FastAPI Main Application Entry Point

This file serves as the main entry point for the FastAPI application.
It contains:
- Application initialization and configuration
- CORS middleware setup
- Global exception handlers
- Health check endpoints
- Database connection test endpoints
- API router inclusion for different versions

Dependencies:
- FastAPI framework
- SQLAlchemy for database operations
- Various internal modules from app package

Author: Minh An
Last Modified: 23 Jun 2024
Version: 2.0.1
"""

from app.controllers.v1 import router as api_v1_router
#from app.controllers.v2 import api_router as api_v2_router
from app.core.config import settings
from app.db.base import get_db
from app.schemas.business_model.response_base import ErrorResponseModel, BaseResponseModel, ResponseStatus, \
    SuccessResponseModel
from app.services.utils.exceptions.exceptions import (
    register_exception_handlers,
    APIException,
    BadRequestException,
    UnauthorizedException,
    ForbiddenException,
    NotFoundException,
    ConflictException,
    InternalServerException
)
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

description = """
🚀 Tài Liệu API

## Tính Năng
* Quản Lý Người Dùng
* Quản Lý Mục
* Các Phép Toán
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Hỗ Trợ API",
        "url": "http://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[" *"],
    allow_credentials=True,
    allow_methods=[" *"],
    allow_headers=[" *"],
)

# Đăng ký các exception handlers từ app.services.utils.exceptions.exceptions
register_exception_handlers(app)


# Health check endpoints
@app.get("/health", tags=["Health"], summary="Get application health status")
async def health_check() -> SuccessResponseModel:
    """
    Health check endpoint to verify the application is running
    
    Returns:
        SuccessResponseModel: Health status information
    """
    return SuccessResponseModel(
        message="API is running",
        data={"status": "healthy"},
        metadata={"version": "2.0.0"}
    )


@app.get("/test-db", tags=["Health"], summary="Test database connection")
async def test_db_connection(db: Session = Depends(get_db)) -> SuccessResponseModel:
    """
    Test the database connection
    
    Args:
        db (Session): The database session
    
    Returns:
        SuccessResponseModel: Database connection status
        
    Raises:
        InternalServerException: If the database connection fails
    """
    try:
        result = db.execute(text("SELECT 1")).scalar()
        return SuccessResponseModel(
            message="Database connection successful",
            data={"database_test": result == 1},
            metadata={"database_uri": settings.SQLALCHEMY_DATABASE_URI.replace(settings.DB_PASSWORD, " ****")}
        )
    except Exception as e:
        raise InternalServerException(
            error_code="DATABASE_CONNECTION_ERROR",
            message=f"Database connection failed: {str(e)}"
        )


# Error test endpoints (for testing exception handling)
@app.get("/test-error/{error_type}", tags=["Testing"], summary="Test error responses")
async def test_error(error_type: str) -> SuccessResponseModel:
    """
    Test endpoint to verify error handling
    
    Args:
        error_type (str): Type of error to simulate
    
    Returns:
        SuccessResponseModel: Never returned as this always raises an exception
        
    Raises:
        Various exceptions based on the error_type parameter
    """
    if error_type == "bad_request":
        raise BadRequestException(message="Bad request error test")
    elif error_type == "unauthorized":
        raise UnauthorizedException(message="Unauthorized error test")
    elif error_type == "forbidden":
        raise ForbiddenException(message="Forbidden error test")
    elif error_type == "not_found":
        raise NotFoundException(message="Not found error test")
    elif error_type == "conflict":
        raise ConflictException(message="Conflict error test")
    elif error_type == "server_error":
        raise InternalServerException(message="Internal server error test")
    elif error_type == "unhandled":
        # Test unhandled exception
        raise ValueError("Unhandled error test")
    else:
        return SuccessResponseModel(
            message="No error triggered",
            data={"error_type": error_type}
        )


# Bao gồm các controller routers
app.include_router(
    api_v1_router,
    prefix=settings.API_V1_STR,
    tags=["API v1"]
)
