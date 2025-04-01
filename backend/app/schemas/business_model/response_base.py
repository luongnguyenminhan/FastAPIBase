"""
Base Response Model

This file defines the base response model for all API endpoints.
It provides a standardized structure for API responses with status,
error code, message, data, and metadata fields.

Dependencies:
- Pydantic for data validation and serialization
- TypeVar for generic typing

Author: Minh An
Last Modified: 21 Jan 2024
Version: 1.0.0
"""

from enum import Enum
from typing import TypeVar, Generic, Optional, Dict, Any

from pydantic import BaseModel, Field

# Generic type variable for response data
T = TypeVar('T')


class ResponseStatus(str, Enum):
    """
    Enum representing possible response statuses
    """
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class BaseResponseModel(BaseModel, Generic[T]):
    """
    Base response model for all API endpoints
    
    Attributes:
        status (ResponseStatus): The status of the response (success, error, etc.)
        error_code (Optional[str]): Error code for error responses, null for successful responses
        message (str): A human-readable message describing the result
        data (Optional[T]): The actual response data, can be any type
        metadata (Optional[Dict[str, Any]]): Additional metadata about the response
    """
    status: ResponseStatus = Field(
        default=ResponseStatus.SUCCESS,
        description="Response status indicating success or failure"
    )
    error_code: Optional[str] = Field(
        default=None,
        description="Error code for error responses, null for successful responses"
    )
    message: str = Field(
        default="Operation completed successfully",
        description="Human-readable message describing the result"
    )
    data: Optional[T] = Field(
        default=None,
        description="The actual response data"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional metadata about the response"
    )

    class Config:
        """
        Pydantic model configuration
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "status": "success",
                "error_code": None,
                "message": "Data retrieved successfully",
                "data": {},
                "metadata": {
                    "total_count": 100,
                    "page": 1,
                    "page_size": 10
                }
            }
        }


class SuccessResponseModel(BaseResponseModel[T]):
    """
    Success response model for successful API operations
    
    Pre-configures the status to success and error_code to None
    """
    status: ResponseStatus = ResponseStatus.SUCCESS
    error_code: None = None
    message: str = "Operation completed successfully"


class ErrorResponseModel(BaseResponseModel[None]):
    """
    Error response model for failed API operations
    
    Pre-configures the status to error and data to None
    """
    status: ResponseStatus = ResponseStatus.ERROR
    error_code: str
    message: str
    data: None = None
