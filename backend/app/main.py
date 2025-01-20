from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import API_V1_STR, API_V2_STR, PROJECT_NAME
from app.api.api_v1.api import api_router as api_v1_router
from app.api.api_v2.api import api_router as api_v2_router
from app.db.base import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict

description = """
🚀 API Documentation

## Features
* User Management
* Item Management
* Math Operations
"""

app = FastAPI(
    title=PROJECT_NAME,
    description=description,
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

# CORS configuration
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
    Actions to run on application startup
    """
    try:
        # You could initialize resources here
        pass
    except Exception as e:
        print(f"Startup error: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Actions to run on application shutdown
    """
    try:
        # You could cleanup resources here
        pass
    except Exception as e:
        print(f"Shutdown error: {e}")

@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "version": "2.0.0"
    }

@app.get("/test-db")
async def test_db(db: Session = Depends(get_db)):
    """
    Test database connection
    """
    try:
        result = db.execute(text("SELECT 1 as test"))
        return {
            "status": "success",
            "message": "Database connection successful",
            "result": result.first()[0]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database connection failed: {str(e)}"
        )

# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )

# Include routers
app.include_router(
    api_v1_router,
    prefix=API_V1_STR,
)
app.include_router(
    api_v2_router,
    prefix=API_V2_STR,
)
