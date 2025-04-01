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
Version: 2.0.0
"""

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import API_V1_STR, API_V2_STR, PROJECT_NAME
from app.controllers.v1 import api_router as api_v1_router
from app.controllers.v2 import api_router as api_v2_router
from app.db.base import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict
from app.schemas.common import ErrorResponseModel, BaseResponseModel, ResponseStatus

description = """
🚀 Tài Liệu API

## Tính Năng
* Quản Lý Người Dùng
* Quản Lý Mục
* Các Phép Toán
"""

app = FastAPI(
    title=PROJECT_NAME,
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """
    Xử lý các tác vụ khởi động ứng dụng

    Chức năng:
    - Khởi tạo kết nối cơ sở dữ liệu
    - Thiết lập bộ nhớ đệm nếu cần
    - Khởi tạo các dịch vụ bên ngoài

    Raises:
        Exception: Ghi log các lỗi xảy ra trong quá trình khởi động
    """
    try:
        # Bạn có thể khởi tạo tài nguyên ở đây
        pass
    except Exception as e:
        print(f"Lỗi khởi động: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Xử lý các tác vụ khi tắt ứng dụng

    Chức năng:
    - Đóng kết nối cơ sở dữ liệu
    - Giải phóng tài nguyên
    - Lưu trạng thái nếu cần

    Raises:
        Exception: Ghi log các lỗi xảy ra trong quá trình tắt
    """
    try:
        # Bạn có thể dọn dẹp tài nguyên ở đây
        pass
    except Exception as e:
        print(f"Lỗi khi tắt: {e}")


@app.get("/health", response_model=BaseResponseModel[Dict[str, str]])
async def health_check():
    """
    Kiểm tra trạng thái hoạt động của API

    Returns:
        Dict[str, str]: Từ điển chứa trạng thái và phiên bản API
            - status: Trạng thái hoạt động hiện tại
            - version: Số phiên bản API

    Example:
        Response: {"status": "hoạt động", "version": "2.0.0"}
    """
    return {
        "status": ResponseStatus.SUCCESS,
        "message": "Health check completed successfully",
        "data": {
            "status": "hoạt động",
            "version": "2.0.0"
        }
    }


@app.get("/test-db", response_model=BaseResponseModel[Dict[str, str]])
async def test_db(db: Session = Depends(get_db)):
    """
    Kiểm tra kết nối đến cơ sở dữ liệu

    Args:
        db (Session): Phiên làm việc với cơ sở dữ liệu, được inject tự động

    Returns:
        dict: Kết quả kiểm tra kết nối
            - status: Trạng thái kết nối
            - message: Thông báo chi tiết
            - result: Kết quả truy vấn test

    Raises:
        HTTPException: Khi không thể kết nối đến cơ sở dữ liệu
    """
    try:
        result = db.execute(text("SELECT 1 as test"))
        return {
            "status": ResponseStatus.SUCCESS,
            "message": "Database connection test completed successfully",
            "data": {
                "status": "thành công",
                "message": "Kết nối cơ sở dữ liệu thành công",
                "result": result.first()[0]
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Kết nối cơ sở dữ liệu thất bại: {str(e)}"
        )


# Xử lý ngoại lệ
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Xử lý các ngoại lệ HTTP

    Args:
        request: Request gây ra ngoại lệ
        exc: Đối tượng ngoại lệ HTTP

    Returns:
        JSONResponse: Phản hồi JSON chứa thông tin lỗi
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponseModel(
            status=ResponseStatus.ERROR,
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail
        ).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Xử lý các ngoại lệ chung

    Args:
        request: Request gây ra ngoại lệ
        exc: Đối tượng ngoại lệ

    Returns:
        JSONResponse: Phản hồi JSON chứa thông báo lỗi chung
    """
    return JSONResponse(
        status_code=500,
        content=ErrorResponseModel(
            status=ResponseStatus.ERROR,
            error_code="INTERNAL_SERVER_ERROR",
            message="Lỗi máy chủ nội bộ"
        ).dict()
    )


# Bao gồm các controller routers
app.include_router(
    api_v1_router,
    prefix=API_V1_STR,
    tags=["API v1"]
)
app.include_router(
    api_v2_router,
    prefix=API_V2_STR,
    tags=["API v2"]
)
